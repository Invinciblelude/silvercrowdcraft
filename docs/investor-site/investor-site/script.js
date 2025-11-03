const pipeline = [
  {
    id: 'subject-a',
    title: 'Subject A — 5240 Rio Linda Blvd (Docs in hand)',
    location: 'Sacramento, CA 95838',
    zoning: 'C-1-R (Commercial / MF Residential)',
    size: '±1.38 acres',
    units: '43 apartments (planned)',
    price: '$1,285,000–$1,697,500 (verify ask)',
    landPerUnitNote: '≈ $30k–$40k/unit depending on final price',
    sourceUrl: 'https://sacramento.craigslist.org/reb/d/sacramento-land-with-plans-for-43/7887668400.html',
    sourceLabel: 'Craigslist listing',
  },
  {
    id: 'subject-b',
    title: 'Subject B — 2829 Rio Linda Blvd (Raw concept)',
    location: 'Sacramento, CA 95815',
    zoning: 'R2-B',
    size: 'TBD',
    units: '21 dwelling proposal (concept)',
    price: '$199,000',
    landPerUnitNote: '≈ $9.5k/unit (raw, entitlement risk)',
    sourceUrl: 'https://www.yogiandyoli.com/CA/Sacramento/30-225083866-2829-Rio_Linda-Boulevard-95815',
    sourceLabel: 'Listing page',
  },
];

function createPipelineCard(item) {
  const div = document.createElement('div');
  div.className = 'pipeline-card';
  div.innerHTML = `
    <h3>${item.title}</h3>
    <div class="pipeline-meta">
      <span class="tag">${item.location}</span>
      <span class="tag">${item.zoning}</span>
      <span class="tag">${item.size}</span>
      <span class="tag">${item.units}</span>
    </div>
    <div class="muted small">Ask: ${item.price}</div>
    <div class="muted small">Note: ${item.landPerUnitNote}</div>
    <div class="actions">
      <a class="btn" target="_blank" rel="noopener noreferrer" href="${item.sourceUrl}">Open ${item.sourceLabel}</a>
      <a class="btn" href="#invest">Request Access</a>
    </div>
  `;
  return div;
}

function renderPipeline() {
  const grid = document.getElementById('pipeline-grid');
  if (!grid) return;
  pipeline.forEach((p) => grid.appendChild(createPipelineCard(p)));
}

function setYear() {
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
}

document.addEventListener('DOMContentLoaded', () => {
  renderPipeline();
  setYear();
});


