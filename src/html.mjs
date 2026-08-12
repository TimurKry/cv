// Общие помощники для шаблонов.
//
// Соглашение по данным cv.data.json:
//   - поля about / intro / bullets / note / focus могут содержать инлайновый HTML
//     (<strong>) и вставляются как есть;
//   - всё остальное (имена, ссылки, метки, теги) прогоняется через esc().

export function esc(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export const list = (items, render) => items.map(render).join('\n');
