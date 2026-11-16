function createPdfPanel(lang) {
  const byId = id => document.getElementById(id);
  const view = byId("pdf-view");
  const body = byId("source-body");
  const tools = byId("pdf-tools");
  const status = byId("pdf-status");
  const previous = byId("pdf-previous");
  const next = byId("pdf-next");
  const zoom = byId("pdf-zoom");
  const words = lang.startsWith("zh") ? {
    previous: "上一页", next: "下一页", zoom: "放大", fit: "适合宽度",
    loading: "正在定位 PDF 原文…", noMatch: "这一处未能在 PDF 上唯一定位。下方保留已核对的摘录。",
    error: "PDF 原页加载失败。", page: number => "PDF 第 " + number + " 页",
    noAnchor: "此节点暂无对应的原文。"
  } : {
    previous: "Previous", next: "Next", zoom: "Zoom", fit: "Fit width",
    loading: "Locating the passage in the PDF…",
    noMatch: "This passage could not be uniquely located in the PDF. The verified excerpt is below.",
    error: "Could not open the PDF page.", page: number => "PDF page " + number,
    noAnchor: "There is no source passage for this node."
  };
  const matches = new WeakMap();
  let reader;
  let doc;
  let textLayerClass;
  let originalUrl;
  let currentPage;
  let currentSource;
  let target;
  let generation = 0;
  let zoomed = false;
  let widthAtDraw;
  let observer;

  previous.textContent = words.previous;
  next.textContent = words.next;
  zoom.textContent = words.zoom;

  function setStatus(message) {
    status.textContent = message || "";
    status.hidden = !message;
  }

  function bytes(id) {
    const encoded = byId(id).textContent.trim();
    if (Uint8Array.fromBase64) return Uint8Array.fromBase64(encoded);
    const content = atob(encoded);
    const result = new Uint8Array(content.length);
    for (let index = 0; index < content.length; index++) result[index] = content.charCodeAt(index);
    return result;
  }

  async function open() {
    if (!reader) {
      reader = (async () => {
        const main = URL.createObjectURL(new Blob([bytes("pdfjs-main-data")], {type: "text/javascript"}));
        const worker = URL.createObjectURL(new Blob([bytes("pdfjs-worker-data")], {type: "text/javascript"}));
        try {
          const library = await import(main);
          library.GlobalWorkerOptions.workerSrc = worker;
          textLayerClass = library.TextLayer;
          const data = bytes("pdf-original-data");
          originalUrl = URL.createObjectURL(new Blob([data], {type: "application/pdf"}));
          doc = await library.getDocument({
            data, useWasm: false, useSystemFonts: true,
            isEvalSupported: false, disableFontFace: false
          }).promise;
          return doc;
        } catch (error) {
          URL.revokeObjectURL(worker);
          if (originalUrl) URL.revokeObjectURL(originalUrl);
          throw error;
        } finally {
          URL.revokeObjectURL(main);
        }
      })();
    }
    return reader;
  }

  function drawHighlights(sheet, layer, spans) {
    const overlay = sheet.querySelector(".pdf-highlight-layer");
    const origin = sheet.getBoundingClientRect();
    const rectangles = [];
    for (const span of spans) {
      const text = layer.textDivs[span.index]?.firstChild;
      if (text?.nodeType !== Node.TEXT_NODE) continue;
      const range = document.createRange();
      range.setStart(text, span.start);
      range.setEnd(text, span.end);
      for (const rect of range.getClientRects()) {
        if (rect.width > 0 && rect.height > 0) {
          rectangles.push({left: rect.left - origin.left, top: rect.top - origin.top,
            width: rect.width, height: rect.height});
        }
      }
    }
    for (const rect of rectangles) {
      const marker = document.createElement("span");
      marker.className = "pdf-highlight";
      for (const [key, value] of Object.entries(rect)) marker.style[key] = value + "px";
      overlay.append(marker);
    }
    if (rectangles.length === 0) return null;
    return {
      left: Math.min(...rectangles.map(rect => rect.left)),
      top: Math.min(...rectangles.map(rect => rect.top))
    };
  }

  async function draw(pageNumber, match, token) {
    const page = await doc.getPage(pageNumber);
    if (token !== generation) return;
    const base = page.getViewport({scale: 1});
    const style = getComputedStyle(body);
    const width = body.clientWidth;
    const padding = parseFloat(style.paddingLeft) + parseFloat(style.paddingRight);
    const scale = Math.max(.2, (width - padding - 2) / base.width) * (zoomed ? 1.65 : 1);
    const viewport = page.getViewport({scale});
    const sheet = document.createElement("div");
    sheet.className = "pdf-sheet";
    sheet.setAttribute("aria-label", words.page(pageNumber));
    sheet.style.width = viewport.width + "px";
    sheet.style.height = viewport.height + "px";
    sheet.style.setProperty("--total-scale-factor", scale * page.userUnit);

    const canvas = document.createElement("canvas");
    canvas.setAttribute("aria-hidden", "true");
    const pixels = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.ceil(viewport.width * pixels);
    canvas.height = Math.ceil(viewport.height * pixels);
    const overlay = document.createElement("div");
    overlay.className = "pdf-highlight-layer";
    overlay.setAttribute("aria-hidden", "true");
    const text = document.createElement("div");
    text.className = "textLayer";
    sheet.append(canvas, overlay, text);

    const task = page.render({canvas, viewport, transform: [pixels, 0, 0, pixels, 0, 0]});
    const layer = new textLayerClass({
      textContentSource: match?.textContent || page.streamTextContent(), container: text, viewport
    });
    await Promise.all([task.promise, layer.render()]);
    if (token !== generation) return;

    view.replaceChildren(sheet);
    view.hidden = false;
    tools.hidden = false;
    const showExcerpt = !target && !!currentSource;
    byId("locator").hidden = !showExcerpt || !currentSource?.locator;
    byId("excerpt").hidden = !showExcerpt;
    byId("no-source").hidden = true;
    currentPage = pageNumber;
    widthAtDraw = width;
    byId("pdf-page").textContent = pageNumber + " / " + doc.numPages;
    previous.disabled = pageNumber === 1;
    next.disabled = pageNumber === doc.numPages;
    zoom.textContent = zoomed ? words.fit : words.zoom;
    zoom.setAttribute("aria-pressed", String(zoomed));
    byId("original").href = originalUrl + "#page=" + pageNumber;
    byId("original").hidden = false;
    const first = match && drawHighlights(sheet, layer, match.spans);
    if (match && !first) throw new Error("PDF match has no visible text rectangles.");
    setStatus(target ? "" : currentSource ? words.noMatch : words.noAnchor);
    body.scrollTop = first ? Math.max(0, first.top - body.clientHeight * .34) : 0;
    body.scrollLeft = first && zoomed ? Math.max(0, first.left - body.clientWidth * .22) : 0;

    if (!observer && typeof ResizeObserver === "function") {
      observer = new ResizeObserver(() => {
        if (currentPage && Math.abs(widthAtDraw - body.clientWidth) > 3) {
          widthAtDraw = body.clientWidth;
          showPage(currentPage);
        }
      });
      observer.observe(body);
    }
  }

  function fallback(source, message) {
    view.hidden = true;
    tools.hidden = true;
    byId("locator").hidden = !source?.locator;
    byId("excerpt").hidden = !source;
    byId("no-source").hidden = Boolean(source) || !message;
    setStatus(message);
  }

  async function showPage(pageNumber) {
    if (!doc || pageNumber < 1 || pageNumber > doc.numPages) return;
    const token = ++generation;
    try {
      await draw(pageNumber, target?.pageNumber === pageNumber ? target : null, token);
    } catch (error) {
      if (token === generation) fallback(currentSource, words.error);
    }
  }

  async function select(source) {
    const token = ++generation;
    currentPage = null;
    currentSource = source;
    target = null;
    fallback(source, words.loading);
    try {
      const pdf = await open();
      if (token !== generation) return;
      if (source?.highlight && !matches.has(source)) {
        const lookup = findPdfText(pdf, source.highlight, source.page).then(match =>
          match || (source.pdfAnchor ? findPdfText(pdf, source.pdfAnchor, source.page) : null)
        );
        matches.set(source, lookup);
      }
      const match = source?.highlight ? await matches.get(source) : null;
      if (token !== generation) return;
      target = match;
      const page = match?.pageNumber || source?.page;
      const validPage = Number.isInteger(page) && page >= 1 && page <= pdf.numPages;
      await draw(validPage ? page : 1, match, token);
    } catch (error) {
      if (token === generation) fallback(source, words.error);
    }
  }

  previous.addEventListener("click", () => showPage(currentPage - 1));
  next.addEventListener("click", () => showPage(currentPage + 1));
  zoom.addEventListener("click", () => {
    zoomed = !zoomed;
    showPage(currentPage);
  });
  return {select};
}
