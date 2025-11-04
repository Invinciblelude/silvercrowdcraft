"""
WallModel DXF Generator

Generates a single DXF file per wall using ezdxf, enforcing:
- Framing (plates, studs @ 16" O.C., openings: kings, jacks, header, sill, cripples)
- Electrical 6 ft / 12 ft outlet spacing rule with Z-CLASH error markers
- Plumbing boring rule per IRC with Z-CLASH warning markers

Units: inches
Layers:
- S-FRAMING (studs, plates, headers, sills, cripples)
- E-RECEPT (electrical outlets)
- Z-CLASH (errors/warnings)

Output: A01_Framing_Model.dxf
"""

from __future__ import annotations

from typing import Dict, List, Tuple, Any

import math
import json
import argparse
import csv
from ezdxf.tools.standards import setup_dimstyle

try:
    import ezdxf
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: ezdxf. Install with `pip install ezdxf` and re-run."
    ) from exc


def clamp(value: float, min_value: float, max_value: float) -> float:
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def create_layer(doc: "ezdxf.EzDxfDocument", name: str, color: int) -> None:
    if name in doc.layers:
        return
    doc.layers.new(name, dxfattribs={"color": color})


def draw_rect(msp: "ezdxf.layouts.Layout", x0: float, y0: float, x1: float, y1: float, layer: str) -> None:
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})


def draw_line(msp: "ezdxf.layouts.Layout", x0: float, y0: float, x1: float, y1: float, layer: str) -> None:
    msp.add_line((x0, y0), (x1, y1), dxfattribs={"layer": layer})


def draw_circle(msp: "ezdxf.layouts.Layout", x: float, y: float, r: float, layer: str, color: int | None = None) -> None:
    attribs = {"layer": layer}
    if color is not None:
        attribs["color"] = color
    msp.add_circle((x, y), r, dxfattribs=attribs)


def draw_cross(msp: "ezdxf.layouts.Layout", x: float, y: float, size: float, layer: str, color: int | None = None) -> None:
    half = size / 2.0
    attribs = {"layer": layer}
    if color is not None:
        attribs["color"] = color
    msp.add_line((x - half, y - half), (x + half, y + half), dxfattribs=attribs)
    msp.add_line((x - half, y + half), (x + half, y - half), dxfattribs=attribs)


def draw_circle3d(msp: "ezdxf.layouts.Layout", x: float, y: float, z: float, r: float, layer: str, color: int | None = None) -> None:
    attribs = {"layer": layer}
    if color is not None:
        attribs["color"] = color
    msp.add_circle((x, y, z), r, dxfattribs=attribs)


def draw_cross3d(msp: "ezdxf.layouts.Layout", x: float, y: float, z: float, size: float, layer: str, color: int | None = None) -> None:
    half = size / 2.0
    attribs = {"layer": layer}
    if color is not None:
        attribs["color"] = color
    msp.add_line((x - half, y - half, z), (x + half, y + half, z), dxfattribs=attribs)
    msp.add_line((x - half, y + half, z), (x + half, y - half, z), dxfattribs=attribs)


class WallModel:
    def __init__(self, data: Dict, doc: "ezdxf.EzDxfDocument" | None = None, msp: "ezdxf.layouts.Layout" | None = None):
        self.data = data
        self.id = data.get("ID", "WALL")
        self.start_x, self.start_y = data.get("START_PT", (0.0, 0.0))
        self.end_x, self.end_y = data.get("END_PT", (0.0, 0.0))
        dx = float(self.end_x - self.start_x)
        dy = float(self.end_y - self.start_y)
        # Orientation & along-axis length
        self.is_horizontal = abs(dx) >= abs(dy)
        self.wall_length = float(abs(dx) if self.is_horizontal else abs(dy))
        self.wall_height = float(data.get("HEIGHT", 96.0))
        self.stud_size = str(data.get("STUD_SIZE", "2x4"))
        self.stud_spacing = float(data.get("STUD_SPACING", 16.0))
        self.is_load_bearing = bool(data.get("IS_LOAD_BEARING", False))
        # Vector math (unit direction along wall in world XY)
        length = math.hypot(dx, dy)
        self.ux = (dx / length) if length > 0 else 1.0
        self.uy = (dy / length) if length > 0 else 0.0
        self.ro_openings: List[Dict] = list(data.get("RO_OPENINGS", []))
        self.utilities: List[Dict] = list(data.get("UTILITIES", []))
        header_map = data.get("HEADER_DEPTH_MAP") or data.get("header_depth_map")
        if isinstance(header_map, dict):
            self.header_depth_map = header_map
        else:
            self.header_depth_map = {"2x4": 3.0, "2x6": 4.5}

        # Corner adjustments
        self.trim_start: float = float(data.get("TRIM_START", 0.0))
        self.trim_end: float = float(data.get("TRIM_END", 0.0))
        self.suppress_start_stud: bool = bool(data.get("SUPPRESS_START_STUD", False))
        self.suppress_end_stud: bool = bool(data.get("SUPPRESS_END_STUD", False))
        self.corner_studs: List[float] = list(data.get("CORNER_STUDS", []))  # positions along axis from start
        self.tee_warnings: List[float] = list(data.get("TEE_WARNINGS", []))  # positions along axis for warnings
        self.top_plate_lap_count: int = int(data.get("TOP_PLATE_LAP_COUNT", 0))
        self.stock_plate_length_in: float = float(data.get("STOCK_PLATE_LENGTH_IN", 144.0))

        # Document/modelspace (external for multi-wall runs)
        if doc is None or msp is None:
            self.doc = ezdxf.new("R2018")
            self.doc.header["$INSUNITS"] = 1
            self.msp = self.doc.modelspace()
            # Layers: S-FRAMING (white=7), E-RECEPTACLE (blue=5), P-DRAIN (green=3), Z-CLASH (red=1)
            create_layer(self.doc, "S-FRAMING", 7)
            create_layer(self.doc, "E-RECEPTACLE", 5)
            create_layer(self.doc, "P-DRAIN", 3)
            create_layer(self.doc, "Z-CLASH", 1)
            create_layer(self.doc, "A-DIMS", 6)
            setup_dimstyle(self.doc)
            self._owns_doc = True
        else:
            self.doc = doc
            self.msp = msp
            self._owns_doc = False

        # Lumber actual sizes (in)
        self.stud_thickness = 1.5
        self.stud_width = 3.5 if self.stud_size == "2x4" else 5.5

        # Plate heights
        self.bottom_plate_height = self.stud_thickness
        self.top_plates_height_total = self.stud_thickness * 2.0

        # BOM counters
        self.bom: Dict[str, float] = {
            "studs_common": 0,
            "studs_end": 0,
            "studs_king": 0,
            "studs_jack": 0,
            "studs_cripple": 0,
            "plates_bottom_linear_in": 0.0,
            "plates_top_linear_in": 0.0,  # includes both plates
            "headers_linear_in": 0.0,
            "sills_linear_in": 0.0,
        }

        # Cut list accumulator: key = f"{stud_size}|{component}", value = {length_in: qty}
        self.cut_list: Dict[str, Dict[float, int]] = {}

    def get_bom(self) -> Dict[str, Any]:
        return {"id": self.id, **self.bom}

    def get_cut_list_rows(self) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for key, length_map in self.cut_list.items():
            try:
                size, component = key.split("|", 1)
            except ValueError:
                size, component = self.stud_size, key
            for length_in, qty in length_map.items():
                rows.append({
                    "wall_id": self.id,
                    "size": size,
                    "component": component,
                    "length_in": round(float(length_in), 2),
                    "qty": int(qty),
                })
        return rows

    def _add_cut(self, component: str, length_in: float) -> None:
        key = f"{self.stud_size}|{component}"
        length_key = round(float(length_in), 2)
        bucket = self.cut_list.setdefault(key, {})
        bucket[length_key] = bucket.get(length_key, 0) + 1

    def save(self, filepath: str) -> None:
        if self._owns_doc:
            self.doc.saveas(filepath)

    # ------------------------ Framing ------------------------
    def generate_framing_geometry(self) -> None:
        # Effective along-axis extents with corner trims
        eff_len = max(0.0, self.wall_length - self.trim_start - self.trim_end)
        # Bottom plate
        if self.is_horizontal:
            x0 = self.start_x + (self.trim_start if (self.end_x >= self.start_x) else -self.trim_start)
            x1 = self.start_x + ((self.wall_length - self.trim_end) if (self.end_x >= self.start_x) else -(self.wall_length - self.trim_end))
            draw_rect(self.msp, min(x0, x1), 0.0, max(x0, x1), self.bottom_plate_height, layer="S-FRAMING")
        else:
            y0 = self.start_y + (self.trim_start if (self.end_y >= self.start_y) else -self.trim_start)
            y1 = self.start_y + ((self.wall_length - self.trim_end) if (self.end_y >= self.start_y) else -(self.wall_length - self.trim_end))
            # vertical plate as rectangle at constant x
            x = self.start_x
            draw_rect(self.msp, x - self.stud_thickness / 2, min(y0, y1), x + self.stud_thickness / 2, max(y0, y1), layer="S-FRAMING")
        self.bom["plates_bottom_linear_in"] += eff_len
        # Cut list: bottom plate segmented into stock lengths
        if eff_len > 0:
            self._add_plate_segments(eff_len, component="Plate")

        # Double top plates at very top
        top_plate_y0 = self.wall_height - self.top_plates_height_total
        top_plate_y1 = top_plate_y0 + self.stud_thickness
        top_plate_y2 = top_plate_y1 + self.stud_thickness
        if self.is_horizontal:
            x0 = self.start_x + (self.trim_start if (self.end_x >= self.start_x) else -self.trim_start)
            x1 = self.start_x + ((self.wall_length - self.trim_end) if (self.end_x >= self.start_x) else -(self.wall_length - self.trim_end))
            draw_rect(self.msp, min(x0, x1), top_plate_y0, max(x0, x1), top_plate_y1, layer="S-FRAMING")
            draw_rect(self.msp, min(x0, x1), top_plate_y1, max(x0, x1), top_plate_y2, layer="S-FRAMING")
        else:
            y0 = self.start_y + (self.trim_start if (self.end_y >= self.start_y) else -self.trim_start)
            y1 = self.start_y + ((self.wall_length - self.trim_end) if (self.end_y >= self.start_y) else -(self.wall_length - self.trim_end))
            x = self.start_x
            draw_rect(self.msp, x - self.stud_thickness / 2, min(y0, y1), x + self.stud_thickness / 2, max(y0, y1), layer="S-FRAMING")
            draw_rect(self.msp, x - self.stud_thickness / 2 - self.stud_thickness, min(y0, y1), x + self.stud_thickness / 2 - self.stud_thickness, max(y0, y1), layer="S-FRAMING")
        self.bom["plates_top_linear_in"] += self.wall_length * 2.0
        # Cut list: two top plates segmented into stock lengths
        if eff_len > 0:
            self._add_plate_segments(eff_len, component="Plate")
            self._add_plate_segments(eff_len, component="Plate")
        # Plate lap pieces (24") for corners/tees
        if self.top_plate_lap_count > 0:
            self.bom["plates_top_linear_in"] += 24.0 * self.top_plate_lap_count
            for _ in range(self.top_plate_lap_count):
                self._add_cut("Plate_Lap", 24.0)

        # Stud bay vertical clear span between plates
        stud_y0 = self.bottom_plate_height
        stud_y1 = self.wall_height - self.top_plates_height_total

        # Place common studs @ 16" O.C., skipping RO spans
        opening_spans = [(ro["START_X"], ro["START_X"] + ro["WIDTH"]) for ro in self.ro_openings]

        def is_within_opening(x: float) -> bool:
            for (ox0, ox1) in opening_spans:
                # Buffer slightly to avoid edge overlaps when drawing jacks/kings
                if (ox0 - 0.75) <= x <= (ox1 + 0.75):
                    return True
            return False

        # End studs at both ends (unless suppressed by corner logic)
        if not self.suppress_start_stud:
            self._draw_end_stud(position_along=0.0, y0=stud_y0, y1=stud_y1, category="studs_end")
        if not self.suppress_end_stud:
            self._draw_end_stud(position_along=self.wall_length, y0=stud_y0, y1=stud_y1, category="studs_end")

        oc = self.stud_spacing
        pos = oc
        while pos < (self.wall_length - 0.01):
            if not is_within_opening(pos):
                self._draw_stud_along(pos, stud_y0, stud_y1, category="studs_common")
            pos += oc

        # Corner studs (explicit positions along axis)
        for cpos in self.corner_studs:
            self._draw_stud_along(cpos, stud_y0, stud_y1, category="studs_king")

        # Openings (windows/doors)
        for ro in self.ro_openings:
            self._draw_opening(ro, stud_y0, stud_y1)

        # Auto-dimensioning
        self._add_dimensions()

        # Tee firestop/insulation warnings
        for pos in self.tee_warnings:
            if self.is_horizontal:
                sign = 1.0 if (self.end_x >= self.start_x) else -1.0
                wx = self.start_x + sign * pos
            else:
                wx = self.start_x
            draw_circle3d(self.msp, wx, 0.0, 0.0, 2.0, layer="Z-CLASH", color=2)
            draw_cross3d(self.msp, wx, 0.0, 0.0, 3.0, layer="Z-CLASH", color=2)
            try:
                self.msp.add_text("TEE FIRESTOP/INSUL CHECK", dxfattribs={"layer": "Z-CLASH", "height": 3.0}).set_pos((wx, -14.0, -30.0))
            except Exception:
                pass

    def _add_plate_segments(self, length_in: float, component: str = "Plate") -> None:
        # Segment plate run into stock-length pieces
        remaining = max(0.0, float(length_in))
        stock = max(24.0, float(self.stock_plate_length_in))
        while remaining > 0.0:
            piece = stock if remaining >= stock else remaining
            self._add_cut(component, piece)
            remaining -= piece

    def _add_dimensions(self) -> None:
        try:
            # Overall length dimension
            if self.is_horizontal:
                p1 = (self.start_x, 0.0)
                p2 = (self.end_x, 0.0)
                base = (self.start_x, -8.0)
                dim = self.msp.add_linear_dim(base=base, p1=p1, p2=p2, angle=0, dxfattribs={"layer": "A-DIMS"})
                dim.render()
                # RO centerline dims stacked below overall
                offset = 14.0
                for idx, ro in enumerate(self.ro_openings):
                    start_along = float(ro.get("START_X", 0.0))
                    width = float(ro.get("WIDTH", 0.0))
                    sign = 1.0 if (self.end_x >= self.start_x) else -1.0
                    cx = self.start_x + sign * (start_along + width / 2.0)
                    base = (self.start_x, -(offset + idx * 6.0))
                    dim = self.msp.add_linear_dim(base=base, p1=(self.start_x, 0.0), p2=(cx, 0.0), angle=0, dxfattribs={"layer": "A-DIMS"})
                    dim.render()
            else:
                p1 = (self.start_x, self.start_y)
                p2 = (self.end_x, self.end_y)
                base = (self.start_x - 8.0, self.start_y)
                dim = self.msp.add_linear_dim(base=base, p1=p1, p2=p2, angle=90, dxfattribs={"layer": "A-DIMS"})
                dim.render()
                # RO centerline dims stacked left of overall
                offset = 14.0
                for idx, ro in enumerate(self.ro_openings):
                    start_along = float(ro.get("START_X", 0.0))
                    width = float(ro.get("WIDTH", 0.0))
                    sign = 1.0 if (self.end_y >= self.start_y) else -1.0
                    cy = self.start_y + sign * (start_along + width / 2.0)
                    base = (self.start_x - (offset + idx * 6.0), self.start_y)
                    dim = self.msp.add_linear_dim(base=base, p1=(self.start_x, self.start_y), p2=(self.start_x, cy), angle=90, dxfattribs={"layer": "A-DIMS"})
                    dim.render()
        except Exception:
            pass

    def _draw_stud(self, center_x: float, y0: float, y1: float, category: str = "studs_common") -> None:
        half = self.stud_thickness / 2.0
        draw_rect(self.msp, center_x - half, y0, center_x + half, y1, layer="S-FRAMING")
        if category in self.bom:
            self.bom[category] += 1
        # Cut list entry by category
        comp_map = {
            "studs_common": "Stud",
            "studs_end": "Stud",
            "studs_king": "KingStud",
            "studs_jack": "JackStud",
            "studs_cripple": "CrippleStud",
        }
        comp = comp_map.get(category, "Stud")
        length_in = max(0.0, y1 - y0)
        if length_in > 0:
            self._add_cut(comp, length_in)

    def _draw_stud_along(self, pos_along: float, y0: float, y1: float, category: str = "studs_common") -> None:
        if self.is_horizontal:
            center_x = self.start_x + (pos_along if (self.end_x >= self.start_x) else -pos_along)
            self._draw_stud(center_x, y0, y1, category)
        else:
            center_y = self.start_y + (pos_along if (self.end_y >= self.start_y) else -pos_along)
            # For vertical walls, draw stud as rectangle centered on x, spanning y0..y1, thickness along x
            half = self.stud_thickness / 2.0
            draw_rect(self.msp, self.start_x - half, center_y - (y1 - y0) / 2.0, self.start_x + half, center_y + (y1 - y0) / 2.0, layer="S-FRAMING")
            if category in self.bom:
                self.bom[category] += 1

    def _draw_end_stud(self, position_along: float, y0: float, y1: float, category: str = "studs_end") -> None:
        self._draw_stud_along(position_along, y0, y1, category)

    def _draw_opening(self, ro: Dict, stud_y0: float, stud_y1: float) -> None:
        start_along = float(ro.get("START_X", 0.0))
        if self.is_horizontal:
            start_x = self.start_x + (start_along if (self.end_x >= self.start_x) else -start_along)
        else:
            start_x = self.start_x
        width = float(ro.get("WIDTH", 0.0))
        height = float(ro.get("HEIGHT", 0.0))
        sill_hgt = float(ro.get("SILL_HGT", 0.0))
        end_x = start_x + (width if self.is_horizontal else 0.0)

        # King studs: full height at opening edges
        self._draw_stud(start_x, stud_y0, stud_y1, category="studs_king")
        self._draw_stud(end_x, stud_y0, stud_y1, category="studs_king")

        # Jack studs: offset inside the opening by 1.5"
        jack_inset = self.stud_thickness
        self._draw_stud(start_x + jack_inset, stud_y0, sill_hgt + height, category="studs_jack")  # up to header bottom
        self._draw_stud(end_x - jack_inset, stud_y0, sill_hgt + height, category="studs_jack")

        # Sill (1.5" thick)
        sill_y0 = sill_hgt
        sill_y1 = sill_hgt + self.stud_thickness
        draw_rect(self.msp, start_x + jack_inset, sill_y0, end_x - jack_inset, sill_y1, layer="S-FRAMING")
        self.bom["sills_linear_in"] += max(0.0, (end_x - jack_inset) - (start_x + jack_inset))
        sill_len = max(0.0, (end_x - jack_inset) - (start_x + jack_inset))
        if sill_len > 0:
            self._add_cut("Sill", sill_len)

        # Header: use per-opening override if present, else map by stud size
        header_depth = (
            float(ro.get("HEADER_DEPTH"))
            if ro.get("HEADER_DEPTH") is not None
            else (
                float(ro.get("header_depth"))
                if ro.get("header_depth") is not None
                else float(self.header_depth_map.get(self.stud_size, 3.0 if self.stud_width <= 3.5 else 4.5))
            )
        )
        header_y0 = sill_hgt + height
        header_y1 = header_y0 + header_depth
        draw_rect(self.msp, start_x + jack_inset, header_y0, end_x - jack_inset, header_y1, layer="S-FRAMING")
        self.bom["headers_linear_in"] += max(0.0, (end_x - jack_inset) - (start_x + jack_inset))
        header_len = max(0.0, (end_x - jack_inset) - (start_x + jack_inset))
        if header_len > 0:
            self._add_cut("Header", header_len)

        # Cripples below sill: between bottom plate top and sill
        self._draw_cripples(start_x + jack_inset, end_x - jack_inset, stud_y0, sill_y0)

        # Cripples above header: between header top and bottom of top plates
        self._draw_cripples(start_x + jack_inset, end_x - jack_inset, header_y1, stud_y1)

    def _draw_cripples(self, x0: float, x1: float, y0: float, y1: float) -> None:
        if (x1 - x0) < 6.0 or (y1 - y0) < 6.0:
            return
        oc = self.stud_spacing
        # Start at first 16" from x0 and stop 16" before x1 for edge clearance
        x = x0 + oc
        while x < (x1 - 0.01):
            self._draw_stud(x, y0, y1, category="studs_cripple")
            x += oc

    # ------------------------ Electrical ------------------------
    def check_electrical_code(self) -> None:
        # Place outlets (3D symbol at z=16) and validate 6/12 rule
        outlet_z = 16.0
        outlet_r = 1.5

        outlet_positions: List[float] = []
        for util in self.utilities:
            if util.get("TYPE") == "OUTLET":
                along = float(util.get("X_LOC", 0.0))
                outlet_positions.append(along)
                # place symbol in elevation at world x based on orientation
                if self.is_horizontal:
                    sign = 1.0 if (self.end_x >= self.start_x) else -1.0
                    wx = self.start_x + sign * along
                    draw_circle3d(self.msp, wx, 0.0, outlet_z, outlet_r, layer="E-RECEPTACLE")
                else:
                    # vertical wall: keep symbol at wall x, elevation still uses z
                    draw_circle3d(self.msp, self.start_x, 0.0, outlet_z, outlet_r, layer="E-RECEPTACLE")
                # label (STD/GFCI) at same z
                outlet_type = util.get("OUTLET_TYPE") or ("GFCI" if util.get("GFCI") else "STANDARD")
                try:
                    label_x = wx if self.is_horizontal else self.start_x
                    self.msp.add_text(outlet_type, dxfattribs={"layer": "E-RECEPTACLE", "height": 2.0}).set_pos((label_x + 2.0, 2.0, outlet_z))
                except Exception:
                    pass

        # 6/12 rule: no point along wall is more than 6' from a receptacle →
        # spacing between outlets and between ends <= 12'
        outlet_positions = sorted(outlet_positions)
        checkpoints = [0.0] + sorted(outlet_positions) + [self.wall_length]

        for i in range(len(checkpoints) - 1):
            span = checkpoints[i + 1] - checkpoints[i]
            if span > 144.0:
                mid = checkpoints[i] + span / 2.0
                # Red clash marker at floor z=0 and text at z=-30
                # place marker at world x if horizontal, else at wall x
                if self.is_horizontal:
                    sign = 1.0 if (self.end_x >= self.start_x) else -1.0
                    wx = self.start_x + sign * mid
                else:
                    wx = self.start_x
                draw_circle3d(self.msp, wx, 0.0, 0.0, 2.0, layer="Z-CLASH", color=1)
                draw_cross3d(self.msp, wx, 0.0, 0.0, 3.0, layer="Z-CLASH", color=1)
                try:
                    self.msp.add_text("ELEC GAP > 12FT", dxfattribs={"layer": "Z-CLASH", "height": 3.0}).set_pos((wx, -10.0, -30.0))
                except Exception:
                    pass
                print(
                    f"[E-RECEPT] 6/12 rule violation on {self.id}: span {span:.1f} in (>144 in) between s={checkpoints[i]:.1f} and s={checkpoints[i+1]:.1f}."
                )

    # ------------------------ Plumbing ------------------------
    def check_plumbing_code(self) -> None:
        # IRC boring rule: load-bearing studs: max hole dia = 40% of stud width
        # Non-bearing typically 60%, we apply only the strict rule if load-bearing
        bearing_limit_ratio = 0.40
        non_bearing_limit_ratio = 0.60
        limit_ratio = bearing_limit_ratio if self.is_load_bearing else non_bearing_limit_ratio
        max_hole = self.stud_width * limit_ratio

        for util in self.utilities:
            if util.get("TYPE") == "PLUMBING_DRAIN":
                x = float(util.get("X_LOC", 0.0)) + self.start_x
                diameter = float(util.get("DIAMETER", 0.0))
                # Always draw the pipe on P-DRAIN at z=18
                draw_circle3d(self.msp, x, 0.0, 18.0, diameter / 2.0, layer="P-DRAIN")
                if diameter > max_hole and self.is_load_bearing:
                    # Yellow warning marker at floor and text below
                    draw_circle3d(self.msp, x, 0.0, 0.0, 2.0, layer="Z-CLASH", color=2)
                    draw_cross3d(self.msp, x, 0.0, 0.0, 3.0, layer="Z-CLASH", color=2)
                    try:
                        self.msp.add_text(
                            f"PLUMBING HOLE > {max_hole:.2f}\"",
                            dxfattribs={"layer": "Z-CLASH", "height": 3.0},
                        ).set_pos((x, -20.0, -30.0))
                    except Exception:
                        pass
                    print(
                        f"[PLUMBING] Boring violation on {self.id}: diameter {diameter:.2f} in > {max_hole:.2f} in (40% of {self.stud_width:.1f}\" for load-bearing)."
                    )


def _normalize_wall_from_json(raw: Dict[str, Any], defaults: Dict[str, Any] | None) -> Dict[str, Any]:
    d: Dict[str, Any] = {}
    # Defaults
    defaults = defaults or {}
    def getd(key: str, alt: str | None = None, fallback: Any | None = None):
        if key in raw: return raw[key]
        if alt and alt in raw: return raw[alt]
        return defaults.get(key.lower()) if isinstance(defaults, dict) else fallback

    d["ID"] = raw.get("id") or raw.get("ID") or "WALL"
    start_pt = raw.get("start_pt") or raw.get("START_PT") or [0, 0]
    end_pt = raw.get("end_pt") or raw.get("END_PT") or [0, 0]
    d["START_PT"] = (float(start_pt[0]), float(start_pt[1]))
    d["END_PT"] = (float(end_pt[0]), float(end_pt[1]))
    d["HEIGHT"] = float(raw.get("wall_height") or raw.get("HEIGHT") or defaults.get("wall_height", 96))
    d["STUD_SIZE"] = (raw.get("stud_size") or raw.get("STUD_SIZE") or defaults.get("stud_size", "2x4")).upper()
    d["STUD_SPACING"] = float(raw.get("stud_spacing") or raw.get("STUD_SPACING") or defaults.get("stud_spacing", 16))
    d["IS_LOAD_BEARING"] = bool(raw.get("is_load_bearing") if "is_load_bearing" in raw else raw.get("IS_LOAD_BEARING", defaults.get("is_load_bearing", True)))
    # Stock plate length for segmentation (defaults level)
    if isinstance(defaults, dict) and "stock_plate_length_in" in defaults:
        d["STOCK_PLATE_LENGTH_IN"] = float(defaults.get("stock_plate_length_in", 144))
    # Header map
    header_map = raw.get("header_depth_map") or raw.get("HEADER_DEPTH_MAP") or defaults.get("header_depth_map")
    if isinstance(header_map, dict):
        d["HEADER_DEPTH_MAP"] = header_map

    # Openings
    openings = []
    for ro in raw.get("ro_openings") or raw.get("RO_OPENINGS") or []:
        openings.append({
            "TYPE": ro.get("TYPE") or ro.get("type", "Window"),
            "START_X": float(ro.get("START_X") or ro.get("start_x", 0)),
            "WIDTH": float(ro.get("WIDTH") or ro.get("width", 0)),
            "HEIGHT": float(ro.get("HEIGHT") or ro.get("height", 0)),
            "SILL_HGT": float(ro.get("SILL_HGT") or ro.get("sill_hgt", 0)),
            "HEADER_DEPTH": ro.get("HEADER_DEPTH") or ro.get("header_depth"),
        })
    d["RO_OPENINGS"] = openings

    # Utilities
    utils = []
    for u in raw.get("utilities") or raw.get("UTILITIES") or []:
        t = (u.get("TYPE") or u.get("type", "")).upper()
        if t == "OUTLET":
            utils.append({
                "TYPE": "OUTLET",
                "X_LOC": float(u.get("X_LOC") or u.get("x_loc", 0)),
                "OUTLET_TYPE": u.get("OUTLET_TYPE") or ("GFCI" if u.get("GFCI") else "STANDARD"),
                "GFCI": bool(u.get("GFCI", (str(u.get("OUTLET_TYPE")).upper() == "GFCI"))),
            })
        elif t == "PLUMBING_DRAIN":
            utils.append({
                "TYPE": "PLUMBING_DRAIN",
                "X_LOC": float(u.get("X_LOC") or u.get("x_loc", 0)),
                "DIAMETER": float(u.get("DIAMETER") or u.get("diameter", 0)),
            })
    d["UTILITIES"] = utils
    return d


def _save_wall_to_dxf(wall_data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    model = WallModel(wall_data)
    model.generate_framing_geometry()
    model.check_electrical_code()
    model.check_plumbing_code()
    safe_id = str(model.id).replace("/", "-").replace(" ", "_")
    outfile = f"{safe_id}_Framing_Model.dxf"
    model.save(outfile)
    return outfile, model.get_bom()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate DXF for wall framing from JSON or built-in sample")
    parser.add_argument("--json", dest="json_path", help="Path to JSON input file", required=False)
    args = parser.parse_args()

    if args.json_path:
        with open(args.json_path, "r") as f:
            data = json.load(f)
        # Support both single-wall schema and project schema with defaults
        if isinstance(data, dict) and "walls" in data:
            defaults = data.get("defaults") or {}
            # Shared DXF document for multi-wall run
            doc = ezdxf.new("R2018")
            doc.header["$INSUNITS"] = 1
            msp = doc.modelspace()
            create_layer(doc, "S-FRAMING", 7)
            create_layer(doc, "E-RECEPTACLE", 5)
            create_layer(doc, "P-DRAIN", 3)
            create_layer(doc, "Z-CLASH", 1)
            create_layer(doc, "A-DIMS", 6)
            setup_dimstyle(doc)

            # Normalize walls
            walls_norm: List[Dict[str, Any]] = []
            for wall in data.get("walls", []):
                norm = _normalize_wall_from_json(wall, defaults)
                if "header_depth_map" in data.get("defaults", {}):
                    norm["HEADER_DEPTH_MAP"] = data["defaults"]["header_depth_map"]
                walls_norm.append(norm)

            # Corner detection and adjustment (3-stud California corner)
            def wall_endpoints(w: Dict[str, Any]) -> Tuple[Tuple[float, float], Tuple[float, float]]:
                sx, sy = w["START_PT"]
                ex, ey = w["END_PT"]
                return (sx, sy), (ex, ey)

            def stud_width_for(w: Dict[str, Any]) -> float:
                size = (w.get("STUD_SIZE") or "2x4").upper()
                return 3.5 if size == "2X4" else 5.5

            eps: Dict[Tuple[float, float], List[int]] = {}
            for idx, w in enumerate(walls_norm):
                a, b = wall_endpoints(w)
                eps.setdefault(a, []).append(idx)
                eps.setdefault(b, []).append(idx)

            for pt, idxs in eps.items():
                if len(idxs) < 2:
                    continue
                owner = min(idxs)
                others = [i for i in idxs if i != owner]
                for i in idxs:
                    w = walls_norm[i]
                    sx, sy = w["START_PT"]
                    ex, ey = w["END_PT"]
                    is_start = (pt == (sx, sy))
                    key = "SUPPRESS_START_STUD" if is_start else "SUPPRESS_END_STUD"
                    w[key] = True
                if others:
                    owner_w = walls_norm[owner]
                    owner_sw = stud_width_for(owner_w)
                    for i in others:
                        w = walls_norm[i]
                        sx, sy = w["START_PT"]
                        is_start = (pt == (sx, sy))
                        trim_key = "TRIM_START" if is_start else "TRIM_END"
                        w[trim_key] = float(w.get(trim_key, 0.0)) + owner_sw
                ow = walls_norm[owner]
                sx, sy = ow["START_PT"]
                ex, ey = ow["END_PT"]
                along_len = abs(ex - sx) if abs(ex - sx) >= abs(ey - sy) else abs(ey - sy)
                cluster = ow.get("CORNER_STUDS", [])
                cluster.extend([max(along_len - 1.5, 0.0), max(along_len - 3.0, 0.0), max(along_len - 5.5, 0.0)])
                ow["CORNER_STUDS"] = cluster
                # Add top-plate lap requirement at corner (24")
                ow["TOP_PLATE_LAP_COUNT"] = int(ow.get("TOP_PLATE_LAP_COUNT", 0)) + 1

            # Tee intersection detection (endpoint of one wall lies mid-span of another)
            def point_on_segment(pt_xy: Tuple[float, float], a_xy: Tuple[float, float], b_xy: Tuple[float, float], tol: float = 1e-3) -> bool:
                (px, py), (ax, ay), (bx, by) = pt_xy, a_xy, b_xy
                vx, vy = bx - ax, by - ay
                wx, wy = px - ax, py - ay
                seg_len2 = vx * vx + vy * vy
                if seg_len2 == 0:
                    return False
                # Projection parameter t in [0,1]
                t = (wx * vx + wy * vy) / seg_len2
                if t <= 0.0 or t >= 1.0:
                    return False
                projx, projy = ax + t * vx, ay + t * vy
                dx, dy = px - projx, py - projy
                return (dx * dx + dy * dy) <= (tol * tol)

            for i, wi in enumerate(walls_norm):
                a_i, b_i = wall_endpoints(wi)
                for endpoint in (a_i, b_i):
                    for j, wj in enumerate(walls_norm):
                        if j == i:
                            continue
                        a_j, b_j = wall_endpoints(wj)
                        # skip if endpoint coincides with j endpoints (already handled as corner)
                        if endpoint == a_j or endpoint == b_j:
                            continue
                        if point_on_segment(endpoint, a_j, b_j):
                            # wi is branch, wj is through wall at tee point
                            # Suppress branch end stud and trim branch plates by through stud width
                            is_start_branch = (endpoint == a_i)
                            key_sup = "SUPPRESS_START_STUD" if is_start_branch else "SUPPRESS_END_STUD"
                            key_trim = "TRIM_START" if is_start_branch else "TRIM_END"
                            wi[key_sup] = True
                            wi[key_trim] = float(wi.get(key_trim, 0.0)) + stud_width_for(wj)

                            # Add tee studs to through wall near the tee position
                            sx, sy = wj["START_PT"]
                            ex, ey = wj["END_PT"]
                            if abs(ex - sx) >= abs(ey - sy):
                                pos = abs(endpoint[0] - sx)
                            else:
                                pos = abs(endpoint[1] - sy)
                            cluster = wj.get("CORNER_STUDS", [])
                            # two studs at tee: centered and offset by 1.5"
                            cluster.extend([max(pos - 0.75, 0.0), min(pos + 0.75, abs(ex - sx) if abs(ex - sx) >= abs(ey - sy) else abs(ey - sy))])
                            wj["CORNER_STUDS"] = cluster
                            # Firestop/Insulation warning marker and top-plate lap at tee on through wall
                            tw = wj.get("TEE_WARNINGS", [])
                            tw.append(pos)
                            wj["TEE_WARNINGS"] = tw
                            wj["TOP_PLATE_LAP_COUNT"] = int(wj.get("TOP_PLATE_LAP_COUNT", 0)) + 1

            # Render all walls into shared doc
            per_wall_bom: List[Dict[str, Any]] = []
            agg: Dict[str, float] = {}
            cut_rows_all: List[Dict[str, Any]] = []
            for w in walls_norm:
                model = WallModel(w, doc=doc, msp=msp)
                model.generate_framing_geometry()
                model.check_electrical_code()
                model.check_plumbing_code()
                bom = model.get_bom()
                per_wall_bom.append(bom)
                for k, v in bom.items():
                    if k == "id":
                        continue
                    agg[k] = agg.get(k, 0.0) + float(v)
                # Collect cut list rows per wall
                cut_rows_all.extend(model.get_cut_list_rows())

            project_name = str(data.get("project", "project")).replace(" ", "_")
            dxf_name = f"{project_name}_Framing_Model.dxf"
            doc.saveas(dxf_name)
            print("DXF saved:", dxf_name)

            # write CSV aggregate
            csv_path = f"{project_name}_bom.csv"
            with open(csv_path, "w", newline="") as fcsv:
                writer = csv.writer(fcsv)
                writer.writerow(["component", "quantity_or_linear_in"])
                for k, v in sorted(agg.items()):
                    writer.writerow([k, f"{v:.2f}"])
            # write per-wall JSON
            json_path = f"{project_name}_bom_per_wall.json"
            with open(json_path, "w") as fj:
                json.dump(per_wall_bom, fj, indent=2)
            print("BOM written:", csv_path, json_path)

            # write aggregated Cut List CSV and per-wall Cut List JSON
            # Aggregate by (size, component, length_in)
            cut_agg: Dict[Tuple[str, str, float], int] = {}
            for row in cut_rows_all:
                key = (str(row.get("size")), str(row.get("component")), float(row.get("length_in", 0.0)))
                cut_agg[key] = cut_agg.get(key, 0) + int(row.get("qty", 0))

            cut_csv = f"{project_name}_cut_list.csv"
            with open(cut_csv, "w", newline="") as fcsv:
                writer = csv.writer(fcsv)
                writer.writerow(["size", "component", "length_in", "qty"])
                for (size, comp, length_in), qty in sorted(cut_agg.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
                    writer.writerow([size, comp, f"{length_in:.2f}", qty])

            cut_json = f"{project_name}_cut_list_per_wall.json"
            with open(cut_json, "w") as fj:
                json.dump(cut_rows_all, fj, indent=2)
            print("Cut List written:", cut_csv, cut_json)
        else:
            norm = _normalize_wall_from_json(data, data.get("defaults") if isinstance(data, dict) else None)
            out, bom = _save_wall_to_dxf(norm)
            print("DXF saved:", out)
            # also write single-wall BOM JSON
            bom_json = f"{bom['id']}_bom.json" if isinstance(bom, dict) and 'id' in bom else "wall_bom.json"
            with open(bom_json, "w") as fj:
                json.dump(bom, fj, indent=2)
            print("BOM written:", bom_json)
            # also write single-wall Cut List CSV/JSON
            single_model = WallModel(norm)
            single_model.generate_framing_geometry()
            single_model.check_electrical_code()
            single_model.check_plumbing_code()
            cut_rows = single_model.get_cut_list_rows()
            # aggregate
            cut_agg: Dict[Tuple[str, str, float], int] = {}
            for row in cut_rows:
                key = (str(row.get("size")), str(row.get("component")), float(row.get("length_in", 0.0)))
                cut_agg[key] = cut_agg.get(key, 0) + int(row.get("qty", 0))
            wall_prefix = str(bom.get('id', 'wall')).replace(' ', '_')
            cut_csv = f"{wall_prefix}_cut_list.csv"
            with open(cut_csv, "w", newline="") as fcsv:
                writer = csv.writer(fcsv)
                writer.writerow(["size", "component", "length_in", "qty"])
                for (size, comp, length_in), qty in sorted(cut_agg.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
                    writer.writerow([size, comp, f"{length_in:.2f}", qty])
            cut_json = f"{wall_prefix}_cut_list.json"
            with open(cut_json, "w") as fj:
                json.dump(cut_rows, fj, indent=2)
            print("Cut List written:", cut_csv, cut_json)
    else:
        # Built-in sample
        wall_sample: Dict = {
            "ID": "A-01_Exterior",
            "START_PT": (0, 0),
            "END_PT": (168, 0),
            "HEIGHT": 96,
            "STUD_SIZE": "2x4",
            "STUD_SPACING": 16,
            "IS_LOAD_BEARING": True,
            "RO_OPENINGS": [
                {"TYPE": "Window", "START_X": 48, "WIDTH": 36, "HEIGHT": 48, "SILL_HGT": 44}
            ],
            "UTILITIES": [
                {"TYPE": "PLUMBING_DRAIN", "X_LOC": 100, "DIAMETER": 2.0},
                {"TYPE": "OUTLET", "X_LOC": 18, "OUTLET_TYPE": "STANDARD"},
                {"TYPE": "OUTLET", "X_LOC": 150, "OUTLET_TYPE": "GFCI"},
            ],
        }
        out, bom = _save_wall_to_dxf(wall_sample)
        print("DXF saved:", out)
        bom_json = f"{bom['id']}_bom.json"
        with open(bom_json, "w") as fj:
            json.dump(bom, fj, indent=2)
        print("BOM written:", bom_json)
        # Generate and write sample cut list
        sample_model = WallModel(wall_sample)
        sample_model.generate_framing_geometry()
        sample_model.check_electrical_code()
        sample_model.check_plumbing_code()
        cut_rows = sample_model.get_cut_list_rows()
        # aggregate
        cut_agg: Dict[Tuple[str, str, float], int] = {}
        for row in cut_rows:
            key = (str(row.get("size")), str(row.get("component")), float(row.get("length_in", 0.0)))
            cut_agg[key] = cut_agg.get(key, 0) + int(row.get("qty", 0))
        cut_csv = f"{bom['id']}_cut_list.csv"
        with open(cut_csv, "w", newline="") as fcsv:
            writer = csv.writer(fcsv)
            writer.writerow(["size", "component", "length_in", "qty"])
            for (size, comp, length_in), qty in sorted(cut_agg.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
                writer.writerow([size, comp, f"{length_in:.2f}", qty])
        cut_json = f"{bom['id']}_cut_list.json"
        with open(cut_json, "w") as fj:
            json.dump(cut_rows, fj, indent=2)
        print("Cut List written:", cut_csv, cut_json)


if __name__ == "__main__":
    main()


