import { esc } from './html.mjs';

export function renderOg({ data }) {
  const { facts, site } = data;

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 1200px; height: 630px; }
  body {
    font-family: 'Liberation Sans', Arial, Helvetica, sans-serif;
    background: #101114;
    color: #f3f4f6;
    padding: 74px 80px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    -webkit-print-color-adjust: exact;
  }
  .badge {
    display: inline-block;
    align-self: flex-start;
    padding: 9px 20px;
    border-radius: 999px;
    background: #1e1b4b;
    color: #a5b4fc;
    font-size: 21px;
    font-weight: 700;
    letter-spacing: 0.02em;
  }
  h1 {
    font-size: 86px;
    line-height: 1.02;
    letter-spacing: -0.03em;
    font-weight: 700;
    margin-top: 40px;
  }
  .role {
    margin-top: 18px;
    font-size: 34px;
    font-weight: 600;
    color: #a5b4fc;
  }
  .stack {
    margin-top: 14px;
    font-size: 25px;
    color: #9ca3af;
  }
  .rule { height: 5px; width: 150px; background: #4f46e5; margin-top: 34px; }
  .foot {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    font-size: 23px;
    color: #9ca3af;
  }
  .foot .url { color: #f3f4f6; font-weight: 600; }
</style>
</head>
<body>
  <div>
    <span class="badge">${esc(site.badge)}</span>
    <h1>${esc(facts.name)}</h1>
    <p class="role">Full-Stack / Frontend Developer</p>
    <p class="stack">React · TypeScript · Next.js · Node.js · SQL — ${esc(facts.city)}, Germany</p>
    <div class="rule"></div>
  </div>
  <div class="foot">
    <span class="url">${esc(facts.siteUrl.replace(/^https?:\/\//, ''))}</span>
    <span>${esc(facts.email)}</span>
  </div>
</body>
</html>
`;
}
