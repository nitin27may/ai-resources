/*
 * Click a diagram, get it full screen. Scroll to zoom, drag to pan.
 *
 * Portable across MkDocs Material sites on purpose: it does not know how the
 * diagram was rendered, only that an <svg> appeared inside a container matching
 * SELECTOR. That means it works with Material's built-in Mermaid integration,
 * with a hand-rolled renderer like this repo's mermaid-init.js, and with any
 * other SVG diagram, without either side importing the other.
 *
 * Drop-in for another site: copy this file and diagram-lightbox.css, add both
 * to extra_javascript / extra_css, and widen SELECTOR if that site emits a
 * different container class.
 */
(function () {
  "use strict";

  var SELECTOR = "div.mermaid, .mermaid-diagram, .diagram-zoomable";
  var P = "dlb";                     // class prefix
  var overlay = null;
  var wired = new WeakSet();

  /* ---------------------------------------------------------- attaching */

  function enhance(el) {
    if (!el.querySelector("svg")) return;

    // The button lives inside the container, so re-rendering the diagram (which
    // this repo does on every light/dark toggle) wipes it. The click listener is
    // on the container itself and survives that, so the two are tracked apart:
    // the listener once per element, the button whenever it has gone missing.
    if (!wired.has(el)) {
      wired.add(el);
      el.addEventListener("click", function (ev) {
        if (ev.target.closest("." + P + "__stage")) return;
        open(el.querySelector("svg"));
      });
    }

    if (!el.querySelector("." + P + "-expand")) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = P + "-expand";
      btn.setAttribute("aria-label", "View diagram full screen");
      btn.innerHTML = "&#x26F6;";
      el.appendChild(btn);
    }
    el.setAttribute("data-zoomable", "true");
    if (!el.getAttribute("title")) el.setAttribute("title", "Click to view full screen");
  }

  function scan() {
    Array.prototype.forEach.call(document.querySelectorAll(SELECTOR), enhance);
  }

  /* ---------------------------------------------------------- the overlay */

  function ensureOverlay() {
    if (overlay) return overlay;
    overlay = document.createElement("div");
    overlay.className = P;
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Diagram, full screen");
    overlay.innerHTML =
      '<div class="' + P + '__bar">' +
      '<span class="' + P + '__hint">Scroll to zoom &middot; drag to pan &middot; ' +
      "double-click to reset &middot; Esc to close</span>" +
      '<button type="button" class="' + P + '__close" aria-label="Close">&#x2715;</button>' +
      "</div>" +
      '<div class="' + P + '__stage"></div>';
    document.body.appendChild(overlay);

    overlay.querySelector("." + P + "__close").addEventListener("click", close);
    overlay.addEventListener("click", function (ev) {
      // Backdrop click closes; a click on the diagram itself must not.
      if (ev.target === overlay || ev.target.classList.contains(P + "__stage")) close();
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && overlay.classList.contains("is-open")) close();
    });
    return overlay;
  }

  var view = { scale: 1, x: 0, y: 0 };

  function apply(svg) {
    svg.style.transform =
      "translate(" + view.x + "px," + view.y + "px) scale(" + view.scale + ")";
  }

  function open(src) {
    if (!src) return;
    var ov = ensureOverlay();
    var stage = ov.querySelector("." + P + "__stage");
    stage.innerHTML = "";

    var svg = src.cloneNode(true);

    // Mermaid gives every SVG a unique id and scopes its embedded <style> to
    // that id (`#id .edgePath path { fill:none; stroke:... }`). Dropping the id
    // from the clone silently kills every rule and edges render as black filled
    // blobs. So give the clone a fresh id AND rewrite the stylesheet and any
    // url(#id-...) marker references to match, keeping it styled without
    // colliding with the original still on the page.
    var oldId = src.getAttribute("id");
    if (oldId) {
      var newId = oldId + "-" + P;
      svg.setAttribute("id", newId);
      var styles = svg.querySelectorAll("style");
      for (var i = 0; i < styles.length; i++) {
        styles[i].textContent = styles[i].textContent.split("#" + oldId).join("#" + newId);
      }
      var html = svg.innerHTML.split("url(#" + oldId).join("url(#" + newId);
      if (html !== svg.innerHTML) svg.innerHTML = html;
    }

    // Fit to the viewport using the viewBox, so aspect ratio is preserved and a
    // wide flowchart actually gets bigger rather than merely re-centred.
    var vb = (src.getAttribute("viewBox") || "0 0 800 600").split(/\s+/).map(Number);
    var vw = vb[2] || 800;
    var vh = vb[3] || 600;
    var pad = 48;
    var fit = Math.min(
      (window.innerWidth - pad * 2) / vw,
      (window.innerHeight - pad * 2 - 40) / vh
    );
    var w = Math.round(vw * fit);
    var h = Math.round(vh * fit);
    svg.style.maxWidth = "none";
    svg.setAttribute("width", w);
    svg.setAttribute("height", h);
    svg.style.width = w + "px";
    svg.style.height = h + "px";

    view = { scale: 1, x: 0, y: 0 };
    apply(svg);
    stage.appendChild(svg);

    stage.onwheel = function (ev) {
      ev.preventDefault();
      var rect = svg.getBoundingClientRect();
      var cx = ev.clientX - (rect.left + rect.width / 2);
      var cy = ev.clientY - (rect.top + rect.height / 2);
      var next = Math.min(8, Math.max(0.25, view.scale * (ev.deltaY < 0 ? 1.15 : 1 / 1.15)));
      var k = next / view.scale;
      view.x -= cx * (k - 1);          // zoom towards the cursor, not the centre
      view.y -= cy * (k - 1);
      view.scale = next;
      apply(svg);
    };

    var dragging = false, sx = 0, sy = 0, ox = 0, oy = 0;
    svg.onpointerdown = function (ev) {
      dragging = true;
      sx = ev.clientX; sy = ev.clientY; ox = view.x; oy = view.y;
      svg.setPointerCapture(ev.pointerId);
      svg.style.cursor = "grabbing";
    };
    svg.onpointermove = function (ev) {
      if (!dragging) return;
      view.x = ox + (ev.clientX - sx);
      view.y = oy + (ev.clientY - sy);
      apply(svg);
    };
    svg.onpointerup = svg.onpointercancel = function (ev) {
      dragging = false;
      svg.style.cursor = "grab";
      try { svg.releasePointerCapture(ev.pointerId); } catch (e) {}
    };
    svg.ondblclick = function () {
      view = { scale: 1, x: 0, y: 0 };
      apply(svg);
    };
    svg.style.cursor = "grab";

    ov.classList.add("is-open");
    document.documentElement.classList.add(P + "-open");
    ov.querySelector("." + P + "__close").focus();
  }

  function close() {
    if (!overlay) return;
    overlay.classList.remove("is-open");
    document.documentElement.classList.remove(P + "-open");
    overlay.querySelector("." + P + "__stage").innerHTML = "";
  }

  /* ---------------------------------------------------------- lifecycle */

  // Diagrams appear asynchronously (Mermaid renders after load) and are
  // replaced wholesale on a palette toggle, so watch rather than scan once.
  var pending = null;
  new MutationObserver(function () {
    clearTimeout(pending);
    pending = setTimeout(scan, 80);
  }).observe(document.body, { childList: true, subtree: true });

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(scan);          // Material instant navigation
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }
})();
