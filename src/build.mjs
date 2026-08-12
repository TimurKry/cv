#!/usr/bin/env node
//
// Сборка CV: index.html, три PDF и og.png — всё из src/cv.data.json.
// Зависимостей нет, нужен только Node ≥18 и Chromium.
//
//   node src/build.mjs
//
// Путь к Chromium берётся из CHROME_PATH, иначе перебираются типичные места.

import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

import { renderSite } from './site.template.mjs';
import { renderPrint } from './print.template.mjs';
import { renderOg } from './og.template.mjs';

const SRC = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(SRC, '..');
const BUILD = join(ROOT, 'build');

const MIN_PDF_BYTES = 20 * 1024;

const CHROME_CANDIDATES = [
  process.env.CHROME_PATH,
  '/opt/pw-browsers/chromium',
  '/usr/bin/chromium',
  '/usr/bin/chromium-browser',
  '/usr/bin/google-chrome',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
].filter(Boolean);

function findChrome() {
  const found = CHROME_CANDIDATES.find((p) => existsSync(p));
  if (!found) {
    throw new Error(
      'Chromium не найден. Укажите путь явно: CHROME_PATH=/путь/к/chrome node src/build.mjs\n' +
        `Проверены: ${CHROME_CANDIDATES.join(', ')}`
    );
  }
  return found;
}

// {{token}} → facts[token]. Неизвестный токен = ошибка сборки, а не пустая строка.
function interpolate(value, facts) {
  if (typeof value === 'string') {
    return value.replace(/\{\{(\w+)\}\}/g, (_, key) => {
      if (!(key in facts)) throw new Error(`Неизвестный токен {{${key}}} в cv.data.json`);
      return facts[key];
    });
  }
  if (Array.isArray(value)) return value.map((v) => interpolate(v, facts));
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, interpolate(v, facts)]));
  }
  return value;
}

function runChrome(chrome, args) {
  execFileSync(
    chrome,
    ['--headless=new', '--disable-gpu', '--no-sandbox', '--hide-scrollbars', ...args],
    { stdio: ['ignore', 'ignore', 'pipe'] }
  );
}

function assertProduced(path, minBytes) {
  if (!existsSync(path)) throw new Error(`Файл не создан: ${path}`);
  const { size } = statSync(path);
  if (size < minBytes) {
    throw new Error(`Подозрительно маленький файл ${path}: ${size} байт (< ${minBytes})`);
  }
  return size;
}

const kb = (bytes) => `${(bytes / 1024).toFixed(0)} КБ`;

function main() {
  const chrome = findChrome();
  const raw = JSON.parse(readFileSync(join(SRC, 'cv.data.json'), 'utf8'));
  const data = interpolate({ site: raw.site, variants: raw.variants }, raw.facts);
  data.facts = raw.facts;

  const buildDate = new Date().toISOString().slice(0, 10);

  rmSync(BUILD, { recursive: true, force: true });
  mkdirSync(BUILD, { recursive: true });

  // 1. index.html
  const siteCss = readFileSync(join(SRC, 'site.css'), 'utf8').trimEnd();
  const indexPath = join(ROOT, 'index.html');
  writeFileSync(indexPath, renderSite({ data, css: siteCss, buildDate }));
  console.log(`✓ index.html            ${kb(statSync(indexPath).size)}`);

  // 2. PDF из печатных шаблонов
  const printCss = readFileSync(join(SRC, 'print.css'), 'utf8').trimEnd();
  for (const variant of data.variants) {
    const htmlPath = join(BUILD, `${variant.id}.html`);
    writeFileSync(htmlPath, renderPrint({ variant, facts: data.facts, css: printCss }));

    const pdfPath = join(ROOT, variant.output);
    runChrome(chrome, [
      '--no-pdf-header-footer',
      `--print-to-pdf=${pdfPath}`,
      pathToFileURL(htmlPath).href,
    ]);
    console.log(`✓ ${variant.output.padEnd(22)} ${kb(assertProduced(pdfPath, MIN_PDF_BYTES))}`);
  }

  // 3. og.png — карточка превью для мессенджеров и соцсетей
  const ogHtml = join(BUILD, 'og.html');
  writeFileSync(ogHtml, renderOg({ data }));
  const ogPath = join(ROOT, 'og.png');
  runChrome(chrome, [
    '--window-size=1200,630',
    `--screenshot=${ogPath}`,
    pathToFileURL(ogHtml).href,
  ]);
  console.log(`✓ og.png                ${kb(assertProduced(ogPath, 5 * 1024))}`);

  console.log(`\nГотово. Дата сборки в футере: ${buildDate}`);
}

main();
