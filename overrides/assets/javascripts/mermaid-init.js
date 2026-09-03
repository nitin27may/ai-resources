/*
 * Mermaid rendering.
 *
 * Material for MkDocs ships its own Mermaid integration: it finds `pre.mermaid`,
 * replaces it with a `div.mermaid`, pulls mermaid@11 from unpkg and renders into
 * it. On this site that pipeline produced an empty div on every page -- no SVG,
 * no console error, 49 diagrams rendering as nothing in production. It
 * reproduces on a stock Material site with no overrides and no custom CSS, so it
 * is upstream rather than anything in this repo.
 *
 * So we opt out of it instead. `fence_div_format` in mkdocs.yml emits
 * `div.mermaid` directly, which means Material's handler finds no `pre.mermaid`
 * to touch, and this file owns rendering end to end against a pinned version.
 *
 * The source text is stashed on the element before the first render, because
 * rendering replaces the element's contents -- without it, re-rendering on a
 * light/dark toggle would have nothing left to render.
 */
(function () {
  var SRC_ATTR = "data-mermaid-source";

  function currentTheme() {
    return document.body.getAttribute("data-md-color-scheme") === "slate"
      ? "dark"
      : "default";
  }

  function renderAll() {
    if (!window.mermaid) return;
    var nodes = document.querySelectorAll("div.mermaid");
    if (!nodes.length) return;

    window.mermaid.initialize({
      startOnLoad: false,
      theme: currentTheme(),
      securityLevel: "strict",
      flowchart: { htmlLabels: true, useMaxWidth: true },
      sequence: { useMaxWidth: true }
    });

    Array.prototype.forEach.call(nodes, function (el, i) {
      if (!el.hasAttribute(SRC_ATTR)) {
        el.setAttribute(SRC_ATTR, el.textContent);
      }
      var source = el.getAttribute(SRC_ATTR);
      if (!source || !source.trim()) return;
      var id = "mermaid-" + i + "-" + Math.random().toString(36).slice(2, 8);
      try {
        window.mermaid
          .render(id, source)
          .then(function (result) { el.innerHTML = result.svg; })
          .catch(function (err) { showError(el, err); });
      } catch (err) {
        showError(el, err);
      }
    });
  }

  function showError(el, err) {
    // Fail visibly. A silent empty box is what this file exists to prevent.
    el.innerHTML =
      '<pre style="white-space:pre-wrap;color:#dc2626">Diagram failed to render: ' +
      String((err && err.message) || err).replace(/[<>&]/g, "") +
      "</pre>";
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderAll);
  } else {
    renderAll();
  }

  // Re-render on the palette toggle so diagrams follow light/dark.
  var scheme = document.body.getAttribute("data-md-color-scheme");
  new MutationObserver(function () {
    var next = document.body.getAttribute("data-md-color-scheme");
    if (next !== scheme) { scheme = next; renderAll(); }
  }).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
})();
