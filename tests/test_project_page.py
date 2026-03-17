import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = (ROOT / "index.html").read_text(encoding="utf-8")
INDEX_JS = (ROOT / "static/js/index.js").read_text(encoding="utf-8")
INDEX_CSS = (ROOT / "static/css/index.css").read_text(encoding="utf-8")


class ProjectPageStructureTests(unittest.TestCase):
    def test_hero_uses_compact_review_focused_layout(self):
        self.assertIn('class="hero-frame"', INDEX_HTML)
        self.assertIn('class="hero-heading"', INDEX_HTML)
        self.assertIn('class="hero-meta-strip"', INDEX_HTML)
        self.assertNotIn('class="hero-facts"', INDEX_HTML)
        self.assertIn('<source src="videos/demo.mp4" type="video/mp4">', INDEX_HTML)
        self.assertNotIn('class="metric-ribbon"', INDEX_HTML)
        self.assertNotIn('class="teaser-card hero-teaser-card"', INDEX_HTML)

        hero_title_css = re.search(
            r"\.hero-title\s*\{(?P<body>.*?)\}",
            INDEX_CSS,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(hero_title_css)
        self.assertIn("max-width: 30ch;", hero_title_css.group("body"))

    def test_demo_video_avoids_bulma_hero_video_class_collision(self):
        self.assertNotIn('class="hero-video"', INDEX_HTML)
        self.assertIn('class="hero-demo-video"', INDEX_HTML)
        self.assertRegex(INDEX_CSS, r"\.hero-demo-video\s*\{")
        self.assertRegex(INDEX_CSS, r"\.featured-video\s*\{")

    def test_results_videos_preserve_full_frame_visibility(self):
        featured_css = re.search(
            r"\.featured-video\s*\{(?P<body>.*?)\}",
            INDEX_CSS,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(featured_css)
        self.assertIn("object-fit: contain;", featured_css.group("body"))
        self.assertIn("height: auto;", featured_css.group("body"))
        self.assertNotIn("aspect-ratio", featured_css.group("body"))

        gallery_css = re.search(
            r"\.video-card video\s*\{(?P<body>.*?)\}",
            INDEX_CSS,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(gallery_css)
        self.assertIn("object-fit: contain;", gallery_css.group("body"))
        self.assertIn("height: auto;", gallery_css.group("body"))
        self.assertNotIn("aspect-ratio", gallery_css.group("body"))

    def test_page_uses_neutral_svg_favicon_instead_of_avatar_ico(self):
        self.assertIn('href="static/images/favicon.svg"', INDEX_HTML)
        self.assertNotIn('href="static/images/favicon.ico"', INDEX_HTML)

    def test_demo_video_area_uses_only_minimal_labeling(self):
        self.assertIn(">Demo Video<", INDEX_HTML)
        for phrase in [
            "Qualitative overview across reconstruction, reenactment, and view consistency",
            "Monocular input, subject-specific prior regularization, and standard 3D Gaussian rendering.",
            "The primary demo summarizes reconstruction quality, cross-subject driving fidelity, and viewpoint stability under the evaluation settings described in the paper.",
            "Input",
            "Core Idea",
            "Evidence",
            "class=\"hero-fact\"",
        ]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, INDEX_HTML)

    def test_abstract_and_highlights_extra_headings_are_removed(self):
        banned_phrases = [
            "Regularizing the stage where monocular ambiguity causes over-smoothing",
            "Contribution Highlights",
            "Three design choices define the method",
            'href="#highlights"',
            'id="highlights"',
        ]

        for phrase in banned_phrases:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, INDEX_HTML)

    def test_resources_section_is_removed(self):
        banned_phrases = [
            "Paper and review materials",
            'href="#paper"',
            'id="paper"',
            'class="paper-layout"',
            'class="paper-copy"',
            'class="paper-viewer-card"',
            'class="resource-card"',
        ]

        for phrase in banned_phrases:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, INDEX_HTML)

    def test_page_hides_full_paper_and_supplementary_links(self):
        for phrase in [
            ">Paper PDF<",
            ">Supplementary<",
            'href="static/pdfs/paper.pdf"',
            'href="static/pdfs/supplementary.pdf"',
        ]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, INDEX_HTML)

    def test_hero_removes_review_metadata_and_method_figure_button(self):
        for phrase in [
            '>IEEE Transactions on Multimedia<',
            '>Anonymous Review Draft · 2026<',
            '>Anonymous Review Draft<',
            ">Method Figure<",
            'class="hero-kicker-row"',
            'class="action-group"',
        ]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, INDEX_HTML)

    def test_hero_includes_code_link(self):
        self.assertIn('class="hero-links"', INDEX_HTML)
        self.assertIn(">Code<", INDEX_HTML)
        self.assertIn(
            'href="https://github.com/XiaoQiangSHI/HiFiAvatar-"',
            INDEX_HTML,
        )
        self.assertIn('aria-label="Open code repository"', INDEX_HTML)

    def test_hero_shows_author_names_only(self):
        self.assertIn(
            "Xiaoqiang Shi · Zhenyu Yin · Guangjie Han · Feiqing Zhang · Chen Wang",
            INDEX_HTML,
        )
        for phrase in [
            "Author Placeholder",
            "Affiliation Placeholder",
            "Author names and affiliations remain anonymized in this review version.",
            'class="hero-affiliation-line"',
        ]:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, INDEX_HTML)

    def test_copy_avoids_casual_repository_wording(self):
        page_source = "\n".join([INDEX_HTML, INDEX_JS])
        banned_phrases = [
            "Local videos",
            "local result clips",
            "Repository asset",
            "Representative local clip",
            "Local demo clip",
            "first impression",
            "This page is structured for the way paper readers scan",
            "exact story you want a project page to tell",
            "The project page is self-contained",
            "Remaining placeholders",
            "keep updating the local result set",
        ]

        for phrase in banned_phrases:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, page_source)

    def test_mixed_height_grids_do_not_stretch_columns(self):
        expected_align_start = {
            ".hero-grid": "hero cards should size to content instead of filling the title column height",
            ".results-stage": "results description card should not stretch to the featured video height",
        }

        for selector, message in expected_align_start.items():
            with self.subTest(selector=selector):
                match = re.search(
                    rf"{re.escape(selector)}\s*\{{(?P<body>.*?)\}}",
                    INDEX_CSS,
                    flags=re.DOTALL,
                )
                self.assertIsNotNone(match, selector)
                self.assertIn("align-items: start;", match.group("body"), message)

    def test_pipeline_is_centered_single_column_layout(self):
        self.assertNotIn('id="benchmarks"', INDEX_HTML)
        self.assertIn('class="figure-card"', INDEX_HTML)
        self.assertNotIn("Open method figure PDF", INDEX_HTML)
        self.assertNotIn("Read method in paper", INDEX_HTML)
        pipeline_css = re.search(
            r"\.pipeline-layout\s*\{(?P<body>.*?)\}",
            INDEX_CSS,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(pipeline_css)
        self.assertNotIn("grid-template-columns", pipeline_css.group("body"))
        self.assertIn("justify-items: center;", pipeline_css.group("body"))
        figure_card_css = re.search(
            r"\.figure-card\s*\{(?P<body>.*?)\}",
            INDEX_CSS,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(figure_card_css)
        self.assertIn("box-shadow:", figure_card_css.group("body"))

    def test_research_sections_are_present(self):
        for section_id in [
            "abstract",
            "pipeline",
            "results",
            "bibtex",
        ]:
            with self.subTest(section_id=section_id):
                self.assertIn(f'id="{section_id}"', INDEX_HTML)

    def test_results_section_has_filter_bar_and_gallery_mount(self):
        self.assertIn('class="results-filter"', INDEX_HTML)
        for group_name in ["self", "cross", "multiview"]:
            with self.subTest(group_name=group_name):
                self.assertRegex(
                    INDEX_HTML,
                    rf'data-group="{group_name}"',
                )
        self.assertIn('id="results-gallery"', INDEX_HTML)

    def test_bibtex_block_is_present_but_empty(self):
        self.assertIn('id="bibtex-code"', INDEX_HTML)
        self.assertNotIn("@article{hifiavatar2026", INDEX_HTML)
        bibtex_code = re.search(
            r'<pre id="bibtex-code"><code>(?P<body>.*?)</code></pre>',
            INDEX_HTML,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(bibtex_code)
        self.assertEqual("", bibtex_code.group("body").strip())

    def test_gallery_script_tracks_active_group_and_descriptions(self):
        self.assertIn("let activeGroupKey", INDEX_JS)
        self.assertIn("description:", INDEX_JS)
        self.assertIn("results-gallery", INDEX_JS)
        cross_group = re.search(
            r"cross:\s*\{(?P<body>.*?)\n\s*\},\n\s*multiview:",
            INDEX_JS,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(cross_group)
        self.assertIn("Array.from({ length: 4 }", cross_group.group("body"))

    def test_local_resource_files_exist(self):
        for relative_path in [
            "static/pdfs/paper.pdf",
            "static/pdfs/supplementary.pdf",
            "static/images/teaser_figure.png",
            "static/images/method_figure.png",
            "static/images/favicon.svg",
            "videos/self_reeactment/1.mp4",
            "videos/cross_reacttment/1.mp4",
            "videos/multiview/1.mp4",
        ]:
            with self.subTest(relative_path=relative_path):
                self.assertTrue((ROOT / relative_path).exists(), relative_path)


if __name__ == "__main__":
    unittest.main()
