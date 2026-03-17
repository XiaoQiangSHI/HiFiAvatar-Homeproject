# HiFiAvatar Project Page Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a polished academic project page for HiFiAvatar using the existing static template, filling it with paper-derived content, local videos, and method figures while keeping author identities as placeholders.

**Architecture:** Keep the existing single-page HTML structure and Bulma-based assets, but replace generic template sections with a cleaner editorial layout tailored to this paper. Source textual content from the LaTeX paper, copy paper PDFs into `static/pdfs/`, and surface local video assets through curated video grids/carousels.

**Tech Stack:** Static HTML, Bulma CSS, existing local CSS/JS, local PDF/video assets.

---

### Task 1: Extract paper content and map sections

**Files:**
- Read: `../FateAvatar-exp/单目人头重建paper/TMM-latex-template/HiFiAvatar_TMM/main.tex`
- Read: `../FateAvatar-exp/单目人头重建paper/TMM-latex-template/HiFiAvatar_TMM/src/00_abstract.tex`
- Read: `../FateAvatar-exp/单目人头重建paper/TMM-latex-template/HiFiAvatar_TMM/highlights_tmm.txt`
- Modify: `index.html`

**Step 1:** Extract title, abstract, highlights, and venue metadata.

**Step 2:** Map the content into hero, abstract, contributions, method, results, paper, and BibTeX sections.

**Step 3:** Keep author names as explicit placeholders while wiring all other content to real paper metadata.

### Task 2: Prepare local assets

**Files:**
- Read: `videos/`
- Read: `figures/`
- Create: `static/pdfs/paper.pdf`
- Create: `static/pdfs/supplementary.pdf`
- Optionally create: `static/images/method_figure.png`

**Step 1:** Copy `main.pdf` and `supplementary.pdf` into `static/pdfs/`.

**Step 2:** Reuse local video files directly from `videos/` where possible.

**Step 3:** Surface `figures/method.pdf` in a website-friendly way.

### Task 3: Redesign the page content

**Files:**
- Modify: `index.html`
- Modify: `static/css/index.css`
- Modify: `static/js/index.js`

**Step 1:** Replace generic metadata and hero content with HiFiAvatar content.

**Step 2:** Remove irrelevant placeholder sections (lab works, YouTube embed) and add concise contributions and method sections.

**Step 3:** Build result showcases for self reenactment, cross reenactment, and multiview videos.

**Step 4:** Add direct links to paper, supplementary, and GitHub placeholder.

### Task 4: Verify asset references and page integrity

**Files:**
- Verify: `index.html`
- Verify: `static/css/index.css`
- Verify: `static/js/index.js`

**Step 1:** Run `git diff --check` to ensure clean formatting.

**Step 2:** Verify all referenced local assets exist.

**Step 3:** Review final Git status and summarize remaining placeholders for the user.
