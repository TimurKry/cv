import { esc, list } from './html.mjs';

const linkText = (url) => url.replace(/^https?:\/\//, '').replace(/\/$/, '');

export function renderPrint({ variant, facts, css }) {
  const s = variant.sections;

  const experience = list(
    variant.experience,
    (job) => `
    <div class="job">
      <div class="job-head">
        <h3 class="job-title">${esc(job.title)}</h3>
        <div class="job-meta">${job.meta.map(esc).join(' · ')}</div>
      </div>
${job.intro ? `      <p class="job-intro">${job.intro}</p>` : ''}
      <ul>
${list(job.bullets, (b) => `        <li>${b}</li>`)}
      </ul>
      <p class="tech">${esc(job.tech)}</p>
    </div>`
  );

  const projects = list(
    variant.projects,
    (project, i) => `
    <div class="project">
      <div class="project-head">
        <span class="project-index">${i + 1}</span>
        <h3 class="project-name">${esc(project.name)}</h3>
      </div>
      <p class="project-intro">${project.intro}</p>
      <ul>
${list(project.bullets, (b) => `        <li>${b}</li>`)}
      </ul>
      <p class="tech">${esc(project.tech)}</p>
      <a class="project-link" href="${esc(project.link)}">${esc(project.link)}</a>
    </div>`
  );

  return `<!doctype html>
<html lang="${esc(variant.lang)}">
<head>
<meta charset="UTF-8" />
<title>${esc(facts.name)} — ${esc(variant.role)}</title>
<style>
${css}
</style>
</head>
<body>

  <p class="doc-title">${esc(variant.documentTitle)}</p>
  <h1 class="name">${esc(facts.name)}</h1>
  <p class="role">${esc(variant.role)}</p>
  <div class="header-rule"></div>

  <div class="contact-grid">
    <div class="wide">${esc(variant.locationLine)}</div>
    <div>${esc(facts.phone)}</div>
    <div>${esc(facts.email)}</div>
${list(variant.availability, (a) => `    <div>${esc(a)}</div>`)}
    <div><a href="${esc(facts.linkedin)}">${esc(linkText(facts.linkedin))}</a></div>
    <div><a href="${esc(facts.github)}">${esc(linkText(facts.github))}</a></div>
    <div class="wide"><a href="${esc(facts.portfolio)}">${esc(linkText(facts.portfolio))}</a></div>
  </div>

  <div class="section about">
    <h2 class="section-title">${esc(s.about)}</h2>
${list(variant.about, (p) => `    <p>${p}</p>`)}
  </div>

  <div class="section">
    <h2 class="section-title">${esc(s.experience)}</h2>
${experience}
  </div>

  <div class="section">
    <h2 class="section-title">${esc(s.skills)}</h2>
${list(
  variant.skills,
  (skill) => `    <div class="skill-row">
      <div class="skill-label">${esc(skill.title)}</div>
      <div class="skill-items">${esc(skill.items)}</div>
    </div>`
)}
  </div>

  <div class="section">
    <h2 class="section-title">${esc(s.education)}</h2>
    <p class="edu-title">${esc(variant.education.title)}</p>
    <p class="edu-note">${variant.education.note}</p>
    <p class="edu-focus">${variant.education.focus}</p>
  </div>

  <div class="section">
    <h2 class="section-title">${esc(s.projects)}</h2>
${projects}
  </div>

  <div class="footer-grid">
    <div class="section">
      <h2 class="section-title">${esc(s.languages)}</h2>
${list(
  variant.languages,
  (l) => `      <div class="lang-item"><strong>${esc(l.name)}</strong> — ${esc(l.level)}</div>`
)}
    </div>
    <div class="section">
      <h2 class="section-title">${esc(s.preferences)}</h2>
      <ul class="pref-list">
${list(variant.preferences, (p) => `        <li>${esc(p)}</li>`)}
      </ul>
    </div>
  </div>

</body>
</html>
`;
}
