const pdfTextPageCache = new WeakMap();

function normalizePdfText(text) {
  return text.normalize("NFKD").toLowerCase().replace(/[^\p{L}\p{N}]/gu, "");
}

function readPdfTextPage(pdf, pageNumber) {
  let pages = pdfTextPageCache.get(pdf);
  if (!pages) {
    pages = new Map();
    pdfTextPageCache.set(pdf, pages);
  }
  if (!pages.has(pageNumber)) {
    const read = pdf.getPage(pageNumber).then(async page => {
      const textContent = await page.getTextContent();
      const runs = [];
      let normalizedEnd = 0;
      for (const item of textContent.items) {
        if (typeof item.str !== "string") continue;
        const normalized = normalizePdfText(item.str);
        runs.push({ text: item.str, normalized, start: normalizedEnd });
        normalizedEnd += normalized.length;
      }
      const text = runs.map(run => run.normalized).join("");
      return { pageNumber, textContent, runs, text };
    }).catch(error => {
      pages.delete(pageNumber);
      throw error;
    });
    pages.set(pageNumber, read);
  }
  return pages.get(pageNumber);
}

function rawPdfTextOffsets(run, start, end) {
  let rawIndex = 0;
  let normalizedIndex = run.start;
  let matchStart;
  let matchEnd;
  for (const character of run.text) {
    const nextRawIndex = rawIndex + character.length;
    const nextNormalizedIndex = normalizedIndex + normalizePdfText(character).length;
    if (nextNormalizedIndex > Math.max(start, normalizedIndex) && normalizedIndex < end) {
      matchStart ??= rawIndex;
      matchEnd = nextRawIndex;
    }
    if (nextNormalizedIndex >= end) break;
    rawIndex = nextRawIndex;
    normalizedIndex = nextNormalizedIndex;
  }
  return { start: matchStart, end: matchEnd };
}

function locatePdfTextMatch(page, offset, length) {
  const end = offset + length;
  const endOf = run => run.start + run.normalized.length;
  const first = page.runs.findIndex(run => endOf(run) > offset);
  const last = page.runs.findIndex(run => endOf(run) >= end);
  const spans = [];

  for (let index = first; index <= last; index++) {
    const run = page.runs[index];
    if (!run.text) continue;
    const boundary = index === first || index === last
      ? rawPdfTextOffsets(run, offset, end)
      : null;
    const start = index === first ? boundary.start : 0;
    const finish = index === last ? boundary.end : run.text.length;
    if (start < finish) spans.push({ index, start, end: finish });
  }

  return { pageNumber: page.pageNumber, textContent: page.textContent, spans };
}

async function findPdfText(pdf, query, preferredPage) {
  const needle = normalizePdfText(query || "");
  if (!needle) return null;

  const hasPreferred = Number.isInteger(preferredPage)
    && preferredPage >= 1 && preferredPage <= pdf.numPages;
  if (hasPreferred) {
    const page = await readPdfTextPage(pdf, preferredPage);
    const offset = page.text.indexOf(needle);
    if (offset !== -1) {
      return page.text.indexOf(needle, offset + 1) === -1
        ? locatePdfTextMatch(page, offset, needle.length)
        : null;
    }
  }

  let match = null;
  for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
    if (hasPreferred && pageNumber === preferredPage) continue;
    const page = await readPdfTextPage(pdf, pageNumber);
    const offset = page.text.indexOf(needle);
    if (offset === -1) continue;
    if (match || page.text.indexOf(needle, offset + 1) !== -1) return null;
    match = { page, offset };
  }
  return match ? locatePdfTextMatch(match.page, match.offset, needle.length) : null;
}
