# Technical Analysis: LLM-Harness

**Repository:** https://github.com/picrew/LLM-Harness
**Version analyzed:** no release tag; paper published 2026-05-16
**Date:** 2026-05-28

---

## 1. Overview / What Problem It Solves

The LLM-Harness repository is the companion GitHub Pages site for the academic survey
paper *Agent Harness Engineering: A Survey* (Li et al., 2026). Its purpose is to give
the paper a persistent, indexable, citation-friendly URL and to bundle the assets that
cannot live inside a PDF: interactive navigation, structured data for academic crawlers,
one-click BibTeX copy, and figures that link directly to the paper PDF.

The paper itself argues that LLM agent reliability depends less on the underlying model
than on the infrastructure layer that wraps it — the *agent execution harness*. The site
introduces the **ETCLOVG** seven-layer taxonomy (Execution, Tooling, Context, Lifecycle,
Observability, Verification, Governance) and points to an actively maintained catalog of
open-source agent-harness projects at
[Awesome-Agent-Harness](https://github.com/Picrew/awesome-agent-harness) and a
HuggingFace dataset.

The primary user is an ML researcher or engineer discovering the survey via Google
Scholar, Semantic Scholar, or a shared link and wanting either to read the paper or to
cite it. A secondary user is an academic-web developer reproducing or extending the page
layout for a different paper.

---

## 2. High-Level Architecture

```
Browser
  │
  ▼
GitHub Pages CDN
  │
  ├─► docs/index.html          (single-page HTML; ~650 lines)
  │       │
  │       ├─► assets/css/style.css     (hand-rolled CSS; ~590 lines)
  │       ├─► assets/figs/*.png        (5 figures, 0.3–1.2 MB each)
  │       ├─► main.pdf                 (paper, 3.4 MB)
  │       └─► [inline <script>]        (copy-BibTeX button, ~30 lines)
  │
  ├─► docs/robots.txt          (crawl policy)
  ├─► docs/sitemap.xml         (single URL, canonical href)
  └─► docs/google*.html        (Search Console ownership verification)
```

Data flow from visitor to paper content:

1. Browser resolves `https://picrew.github.io/LLM-Harness/` via GitHub Pages CDN.
2. GitHub Pages serves `docs/index.html` and its linked CSS.
3. Browser fetches `assets/css/style.css` and the five figures from the same CDN.
4. Google Fonts CDN (`fonts.googleapis.com`) delivers Inter, Noto Serif, JetBrains Mono.
5. Reader clicks the "Paper" button; browser fetches `docs/main.pdf` (3.4 MB) directly
   from the same Pages CDN.
6. For citation: reader clicks "BibTeX"; the inline script copies
   `#bibtex-code`'s `innerText` to the clipboard via `navigator.clipboard.writeText`,
   with a `document.execCommand('copy')` fallback.

Persistent state: none. The site is fully static; no database, no server-side logic, no
cookies, no local storage.

---

## 3. The ETCLOVG Taxonomy

The central intellectual contribution is not a piece of software but a **taxonomic
framework** — the ETCLOVG model — which the site renders in HTML. It divides the agent
execution harness into seven layers:

| ID | Layer | Color token | Primary count |
|----|-------|-------------|---------------|
| E  | Execution environment & sandbox | `#7c5cff` | 20 projects |
| T  | Tool interface & protocol        | `#e07a3e` | 12 projects |
| C  | Context & memory management      | `#c79123` |  9 projects |
| L  | Lifecycle & orchestration        | `#3aa05c` | 47 projects |
| O  | Observability & operations       | `#1f9e8a` | 15 projects |
| V  | Verification & evaluation        | `#9b3b8c` | 21 projects |
| G  | Governance & security            | `#c54848` | 14 projects |

**Representation in HTML** (`docs/index.html`): each layer is a `<li>` element in the
`.layers` list with an inline `style="--lc:#rrggbb"` custom property that drives both
the left-border accent and the `.layers__id` badge background via `color-mix()`.
The same color tokens are reused in the counts table via `.dot` spans.

**Taxonomy tree**: a static PNG (`assets/figs/taxonomy_tree.png`) renders the full
subcategory hierarchy. No interactive or machine-readable encoding of the taxonomy is
present in this repo; the coded corpus lives at Awesome-Agent-Harness.

**Key design decisions encoded in markup:**
- Multi-label coding: a project gets a *primary* layer and optional *secondary* layers
  (described in prose; the table shows primary counts only).
- Layers E, T, L, V have the densest open-source coverage; C and G are thinner and more
  commercially concentrated (described in `#mapping` section prose).

---

## 4. LLM / External Service Integration

This repository does **not** call any LLM or external API. It is a static HTML document.
LLMs are the *subject* of the survey, not a runtime component. The only network
dependency at page-load time is the Google Fonts CDN:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700
            &family=Noto+Serif:wght@400;500;700
            &family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

`docs/index.html` (lines ~62–64). If this CDN is unavailable the page falls back to
`system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif` (CSS
`body` rule). All figures and the PDF are served from the same Pages CDN as the HTML.

---

## 5. The Page Delivery Pipeline

The "pipeline" here is the browser rendering path and the SEO indexing path.

**Rendering path:**

1. `<head>` metadata — SEO meta tags, OpenGraph, Twitter Card, `citation_*` tags for
   Google Scholar/Semantic Scholar, JSON-LD `ScholarlyArticle` structured data
   (`docs/index.html` lines ~1–105).
2. Font and stylesheet load — `Inter`, `Noto Serif`, `JetBrains Mono` from Google Fonts;
   `assets/css/style.css` linked in `<head>`.
3. Hero section renders — title, author list with affiliation superscripts, link buttons,
   teaser figure (`#hero`, lines ~108–200).
4. Content sections render in document order — Abstract, Claims, Phases, Timeline,
   Taxonomy (with two figures), Mapping (with figure + count table), Synthesis, Open
   Problems, Citation/BibTeX (`#abstract`–`#bibtex`, lines ~200–560).
5. Footer renders; inline `<script>` registers `click` handler on `#copy-bibtex` button
   (`docs/index.html` lines ~575–610).

**SEO / academic-indexing path:**

1. `docs/robots.txt` allows all crawlers.
2. `docs/sitemap.xml` exposes the canonical URL (`https://picrew.github.io/LLM-Harness/`).
3. `docs/google257dfa68b7720547.html` satisfies Google Search Console ownership.
4. `citation_*` meta tags (18 tags) drive Google Scholar and Semantic Scholar ingestion.
5. JSON-LD `ScholarlyArticle` block drives schema.org-aware indexers.

---

## 6. Key Files

| File | Approx lines | What It Does |
|------|-------------|--------------|
| `docs/index.html` | ~650 | Entire page — head metadata, all sections, inline BibTeX script |
| `docs/assets/css/style.css` | ~590 | All visual styling — design tokens, layout, component rules, responsive breakpoints, print styles |
| `docs/assets/figs/teaser.png` | — | Hero figure: prompt vs. context vs. harness engineering comparison (526 KB) |
| `docs/assets/figs/timeline.png` | — | Timeline of representative harness systems 2022–2026 (875 KB) |
| `docs/assets/figs/taxonomy.png` | — | ETCLOVG seven-layer taxonomy diagram (471 KB) |
| `docs/assets/figs/taxonomy_tree.png` | — | Detailed subcategory tree (311 KB) |
| `docs/assets/figs/construction_protocol.png` | — | Corpus construction protocol flowchart (1.2 MB) |
| `docs/main.pdf` | — | Full paper PDF (3.4 MB); served directly from Pages CDN |
| `docs/sitemap.xml` | ~12 | Single-URL sitemap; canonical + last-modified |
| `docs/robots.txt` | ~4 | `Allow: /` for all crawlers |
| `docs/google257dfa68b7720547.html` | 1 | Google Search Console ownership verification token |
| `README.md` | ~65 | Repo description, local preview instructions, Pages deploy steps, citation block |
| `LICENSE` | ~21 | MIT for code; docs/ content is CC BY-SA 4.0 (stated in footer, not in this file) |

---

## 7. Dependencies

No manifest file (`package.json`, `pyproject.toml`, etc.) exists. All runtime
dependencies are CDN-loaded or provided by the platform.

| Resource | Origin | Purpose |
|----------|--------|---------|
| Inter (400/500/600/700) | Google Fonts CDN | Body text, headings, UI labels |
| Noto Serif (400/500/700) | Google Fonts CDN | Pull-quote headlines (`.headline`) |
| JetBrains Mono (400/500) | Google Fonts CDN | Year tags, layer IDs, BibTeX block |
| GitHub Pages | GitHub infrastructure | Static file hosting, HTTPS, CDN delivery |

No npm packages, no Python packages, no build step, no bundler, no transpiler.

---

## 8. CLI / Usage Surface

**Local preview (from README):**

```bash
# Python built-in server
python3 -m http.server 8080 --directory docs

# or via npx (no global install required)
npx serve docs
```

Then open `http://localhost:8080`.

**GitHub Pages deploy:**

1. Push to `main` branch.
2. Repository Settings → Pages → Source: "Deploy from a branch", Branch: `main`,
   Folder: `/docs`.

No environment variables, no configuration files, no CLI flags.

---

## 9. Extensibility Points

- **Adding a new content section.** Insert a `<section class="section [section--alt]">`
  block inside `docs/index.html` at the desired position, following the existing
  `container--narrow` + `<h2>` pattern. Add a corresponding anchor and update
  `docs/sitemap.xml` if the section should be individually indexed.

- **Adding a new ETCLOVG layer card.** In the `<ul class="layers">` block
  (`docs/index.html`), add a `<li style="--lc:#hexcolor">` element with the
  `.layers__id` badge and prose. Add a corresponding row to the `.counts` table. Update
  the figure PNG (`assets/figs/taxonomy.png`) separately — there is no data-driven
  figure generation in this repo.

- **Replacing or adding figures.** Drop new PNGs into `docs/assets/figs/` and update
  the corresponding `<img src="...">` references in `docs/index.html`. There is no image
  build pipeline; filenames are hard-coded in HTML.

- **Extending the copy-button script.** The inline `<script>` at the bottom of
  `docs/index.html` is self-contained and scoped with an IIFE. Adding another copy
  target means duplicating the pattern with a new element ID.

- **Adding a second page.** The site is deliberately single-page. Adding a second
  HTML file under `docs/` would require manually linking the shared stylesheet and
  ensuring the Google Fonts link is included; there is no layout template or component
  system.

---

## 10. Limitations and Gotchas

- **`color-mix()` used without a fallback.** `docs/assets/css/style.css` uses
  `color-mix(in srgb, ...)` for the `.layers__id` badge background and the copy-button
  hover border. This function requires Chrome 111+, Firefox 113+, Safari 16.2+. No
  `@supports` fallback is provided; older browsers render transparent badges.

- **Google Fonts CDN hard dependency.** The page does not load Web fonts from
  `docs/assets/`. A network partition or Google Fonts outage degrades the visual
  rendering to system fonts, which shifts layout metrics (especially for Noto Serif
  headings). A self-hosted font subset would eliminate this.

- **3.4 MB PDF served from Pages CDN.** `docs/main.pdf` is committed directly to the
  repository and served via GitHub Pages. Git history will grow linearly with each
  re-upload of the PDF. No `git-lfs` is configured.

- **No navigation bar or section links.** The hero's "BibTeX" button is an anchor to
  `#bibtex`; there is no sticky nav or table of contents for the other nine sections.
  On mobile or on long displays, users must scroll to navigate.

- **No dark-mode support.** All CSS color variables are hardcoded light-mode values
  (`--bg: #ffffff`, `--bg-alt: #f7f7f3`, etc.). No `@media (prefers-color-scheme: dark)`
  block exists.

- **`text-wrap: balance` is a hint, not a guarantee.** Used on `.authors`, `.affil`,
  `.headline`, `.teaser figcaption`. Browsers that do not support it (pre-2023) silently
  ignore it; long author lists may break awkwardly.

- **Google Search Console file in-tree.** `docs/google257dfa68b7720547.html` is a
  one-line ownership token. It is version-controlled alongside content and will be served
  publicly forever. It is benign but technically unnecessary once Search Console is
  verified.

- **Catalog and paper are in separate repos.** The survey's coded corpus lives at
  `https://github.com/Picrew/awesome-agent-harness`; the project count table in
  `docs/index.html` is a static snapshot and will drift as the catalog grows.

---

## 11. How It Compares to Alternatives

**Nerfies / nerfies.github.io template.** The README explicitly cites Nerfies as the
stylistic inspiration. Nerfies uses Bulma CSS and includes a video carousel component;
LLM-Harness is dependency-free, using hand-rolled CSS instead. The tradeoff: LLM-Harness
loads faster and has no JavaScript framework, but any component reuse requires copy-paste.

**Distill.pub.** Distill is a web-native journal format with interactive figures,
equation rendering via MathJax/KaTeX, and a structured article schema. LLM-Harness is a
project landing page, not a publication format; it links out to a PDF rather than
attempting to render the paper in HTML. Distill requires a build pipeline and a more
complex authoring format; LLM-Harness requires only a text editor.

**academic-pages / al-folio.** These are Jekyll-based templates for full academic
personal sites or paper listings. They support multi-paper catalogs, blog posts, and
automatic BibTeX parsing. LLM-Harness is intentionally scoped to a single paper and has
no build step. The tradeoff: academic-pages scales better across many papers; LLM-Harness
is simpler to audit, fork, and deploy without Ruby or Node dependencies.

**HuggingFace Spaces (Gradio/Streamlit).**  HuggingFace Spaces are increasingly used as
ML paper companion pages, especially when the paper ships a demo. LLM-Harness is a
survey without an interactive demo; a static Pages site avoids the cold-start latency,
compute cost, and HF platform lock-in of a Spaces deployment.

LLM-Harness occupies the "minimal static project page" niche: single HTML file,
no build tooling, no framework, prioritizing simplicity and SEO completeness over
component reuse or interactive content.

---

## Appendix: Selected Code Snippets

**BibTeX copy button — clipboard write with execCommand fallback**
(`docs/index.html`, inline `<script>`, last ~30 lines of file)

```javascript
(function () {
  var btn = document.getElementById('copy-bibtex');
  var src = document.getElementById('bibtex-code');
  if (!btn || !src) return;
  btn.addEventListener('click', function () {
    var text = src.innerText.trim();
    var done = function () {
      var prev = btn.textContent;
      btn.textContent = 'Copied';
      btn.classList.add('is-copied');
      setTimeout(function () {
        btn.textContent = prev;
        btn.classList.remove('is-copied');
      }, 1400);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallback(); });
    } else {
      fallback();
    }
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', '');
      ta.style.position = 'absolute'; ta.style.left = '-9999px';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); done(); } catch (e) {}
      document.body.removeChild(ta);
    }
  });
})();
```

**CSS design token system — root custom properties**
(`docs/assets/css/style.css`, lines ~1–24)

```css
:root {
  --bg:        #ffffff;
  --bg-alt:    #f7f7f3;
  --ink:       #1f2328;
  --ink-soft:  #404953;
  --muted:     #6a727b;
  --line:      #e5e0d2;
  --line-soft: #edeae0;
  --link:      #0a59a4;
  --link-hov:  #08407a;
  --accent:    #114a6f;
  --code-bg:   #f6f8fa;
  --code-ink:  #1f2328;

  --maxw:        1080px;
  --maxw-narrow: 820px;

  --r:    6px;
  --t:    160ms ease-out;
}
```

**Per-layer color via CSS custom property inheritance**
(`docs/index.html`, `.layers` list; `docs/assets/css/style.css`, `.layers__id` rule)

```html
<!-- Each layer item sets --lc on itself; CSS reads it for border and badge -->
<li style="--lc:#7c5cff">
  <span class="layers__id">E</span>
  <div>
    <strong>Execution environment.</strong>
    ...
  </div>
</li>
```

```css
.layers__id {
  background: color-mix(in srgb, var(--lc) 14%, #fff);
  color: var(--lc);
  border: 1px solid color-mix(in srgb, var(--lc) 28%, transparent);
}
```

**JSON-LD ScholarlyArticle structured data for academic indexers**
(`docs/index.html`, lines ~67–104)

```json
{
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  "headline": "Agent Harness Engineering: A Survey",
  "datePublished": "2026",
  "dateModified": "2026-05-16",
  "url": "https://picrew.github.io/LLM-Harness/",
  "sameAs": [
    "https://openreview.net/forum?id=eONq7FdiHa",
    "https://github.com/Picrew/LLM-Harness",
    "https://github.com/Picrew/awesome-agent-harness",
    "https://huggingface.co/datasets/ChenLiu1996/Agent-Harness-Engineering"
  ],
  "encoding": {
    "@type": "MediaObject",
    "encodingFormat": "application/pdf",
    "contentUrl": "https://picrew.github.io/LLM-Harness/main.pdf"
  }
}
```
