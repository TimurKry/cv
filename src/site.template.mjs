import { esc, list } from './html.mjs';

const FAVICON = encodeURIComponent(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">` +
    `<rect width="64" height="64" rx="14" fill="#4338ca"/>` +
    `<text x="32" y="43" font-family="Helvetica,Arial,sans-serif" font-size="30" ` +
    `font-weight="bold" fill="#ffffff" text-anchor="middle">TK</text>` +
    `</svg>`
);

function jsonLd(facts, site) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: facts.name,
    jobTitle: 'Full-Stack / Frontend Developer',
    email: `mailto:${facts.email}`,
    url: facts.siteUrl,
    address: {
      '@type': 'PostalAddress',
      addressLocality: facts.city,
      addressCountry: 'DE',
    },
    knowsLanguage: site.languages.map((l) => l.name),
    sameAs: [facts.linkedin, facts.github, facts.portfolio],
  };
}

export function renderSite({ data, css, buildDate }) {
  const { facts, site } = data;

  const experience = list(
    site.experience,
    (job) => `
      <div class="card">
        <div class="card-top">
          <h3 class="card-title">${esc(job.title)}</h3>
          <span class="card-period">${esc(job.period)}</span>
        </div>
        <p>${job.intro}</p>
        <ul>
${list(job.bullets, (b) => `          <li>${b}</li>`)}
        </ul>
        <div class="tags">${job.tags.map((t) => `<span class="tag">${esc(t)}</span>`).join('')}</div>
      </div>`
  );

  const projects = list(
    site.projects,
    (project) => `
      <div class="card">
        <div class="card-top"><h3 class="card-title">${esc(project.name)}</h3></div>
        <p>${project.intro}</p>
${
  project.bullets.length
    ? `        <ul>\n${list(project.bullets, (b) => `          <li>${b}</li>`)}\n        </ul>`
    : ''
}
        <div class="tags">${project.tags.map((t) => `<span class="tag">${esc(t)}</span>`).join('')}</div>
        <a class="proj-link" href="${esc(project.link)}" target="_blank" rel="noopener">${esc(project.linkLabel)}</a>
      </div>`
  );

  return `<!doctype html>
<html lang="${esc(site.lang)}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>${esc(site.title)}</title>
<meta name="description" content="${esc(site.description)}" />
<link rel="canonical" href="${esc(facts.siteUrl)}" />
<link rel="icon" href="data:image/svg+xml,${FAVICON}" />

<meta property="og:type" content="profile" />
<meta property="og:title" content="${esc(site.title)}" />
<meta property="og:description" content="${esc(site.description)}" />
<meta property="og:url" content="${esc(facts.siteUrl)}" />
<meta property="og:image" content="${esc(facts.siteUrl)}og.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:locale" content="en_US" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="${esc(site.title)}" />
<meta name="twitter:description" content="${esc(site.description)}" />
<meta name="twitter:image" content="${esc(facts.siteUrl)}og.png" />

<script type="application/ld+json">
${JSON.stringify(jsonLd(facts, site), null, 2)}
</script>

<style>
${css}
</style>
</head>
<body>
<div class="page">

  <header>
    <span class="badge">${esc(site.badge)}</span>
    <h1>${esc(facts.name)}</h1>
    <p class="headline">${esc(site.headline)}</p>
    <div class="contact">
${list(site.contact, (c) => `      <span>${esc(c)}</span>`)}
      <a href="mailto:${esc(facts.email)}">${esc(facts.email)}</a>
      <a href="${esc(facts.linkedin)}" target="_blank" rel="noopener">LinkedIn</a>
      <a href="${esc(facts.github)}" target="_blank" rel="noopener">GitHub</a>
      <a href="${esc(facts.portfolio)}" target="_blank" rel="noopener">Portfolio</a>
    </div>
    <div class="downloads">
${list(
  site.downloads,
  (d) => `      <a href="${esc(d.file)}" hreflang="${esc(d.hreflang)}">↓ ${esc(d.label)}</a>`
)}
    </div>
  </header>

  <section>
    <div class="section-head"><h2 class="section-title">About</h2></div>
${list(site.about, (p) => `    <p>${p}</p>`)}
  </section>

  <section>
    <div class="section-head"><h2 class="section-title">Experience</h2></div>
${experience}
  </section>

  <section>
    <div class="section-head"><h2 class="section-title">Skills</h2></div>
    <div class="skills-grid">
${list(
  site.skills,
  (s) => `      <div>
        <p class="skill-title">${esc(s.title)}</p>
        <p class="skill-items">${esc(s.items)}</p>
      </div>`
)}
    </div>
  </section>

  <section>
    <div class="section-head"><h2 class="section-title">Education</h2></div>
    <div class="card">
      <p class="card-title" style="font-size:15px;">${esc(site.education.title)}</p>
      <p style="margin-top:6px;">${site.education.note}</p>
    </div>
  </section>

  <section>
    <div class="section-head"><h2 class="section-title">Projects</h2></div>
${projects}
  </section>

  <div class="footer-meta">
    <div>
      <div class="section-head"><h2 class="section-title">Languages</h2></div>
${list(
  site.languages,
  (l) => `      <div class="lang-item"><strong>${esc(l.name)}</strong> — ${esc(l.level)}</div>`
)}
    </div>
    <div>
      <div class="section-head"><h2 class="section-title">Preferences</h2></div>
      <ul class="pref-list">
${list(site.preferences, (p) => `        <li>${esc(p)}</li>`)}
      </ul>
    </div>
  </div>

  <footer>Last updated ${esc(buildDate)} · ${esc(facts.email)}</footer>
</div>
</body>
</html>
`;
}
