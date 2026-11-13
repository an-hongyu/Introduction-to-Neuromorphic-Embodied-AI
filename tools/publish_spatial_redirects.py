"""Preserve the former spatial-model URLs after merging their content into Chapter 4.

Run after the HTML build and before local-link validation. The source stub is
kept for old Markdown links, but the published legacy route redirects to the
matching section of the merged chapter. No external redirect targets are used.
"""
from html import escape
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_build" / "html"
BASE = os.environ.get("BASE_URL", "/Introduction-to-Neuromorphic-Embodied-AI").rstrip("/")
DEST = BASE + "/chapters/spatial-cells/"
ANCHORS = {
    "learning-objectives": "place-cell-models",
    "id-1-read-the-source-models-before-choosing-parameters": "grid-model-sources",
    "id-2-a-complete-hexagonal-grid-formula": "grid-cosine-model",
    "id-2-1-why-this-frequency-gives-the-requested-spacing": "grid-spacing-geometry",
    "id-2-2-phase-is-a-translation-not-a-change-in-grid-size": "grid-phase-model",
    "id-3-what-each-parameter-changes": "grid-model-parameters",
    "id-4-from-multiple-grid-inputs-to-a-place-like-output": "grid-place-readout",
    "id-4-1-the-exact-readout-in-the-interactive-experiment": "grid-place-readout",
    "id-4-2-why-diversity-and-threshold-matter": "grid-place-readout",
    "id-5-interactive-experiment": "grid-place-live-example",
    "grid-place-live-example": "grid-place-live-example",
    "grid-place-playground": "grid-place-playground",
    "id-6-editable-python-example": "place-model-notebooks",
    "id-7-from-a-fixed-readout-to-learned-mapping": "learned-place-models",
    "exercises": "spatial-exercises",
    "references": "references",
    "additional-reading-materials": "additional-reading-materials",
    "grid-ref-1": "spatial-ref-20",
    "grid-ref-2": "spatial-ref-21",
    "grid-ref-3": "spatial-ref-19",
}


def publish() -> None:
    chapter = SITE / "chapters" / "spatial-cells" / "index.html"
    if not chapter.is_file():
        raise FileNotFoundError("Build Chapter 4 before generating its legacy route")
    html = chapter.read_text(encoding="utf-8")
    for target in ANCHORS.values():
        if f'id="{target}"' not in html and f"id='{target}'" not in html:
            raise ValueError(f"Missing redirect target in Chapter 4: {target}")
    fallback = DEST + "#grid-place-readout"
    old_ids = "\n".join(f'<span id="{escape(key)}"></span>' for key in ANCHORS)
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Grid Cells and Grid-to-Place Mapping - Chapter 4</title>
<link rel="canonical" href="{escape(fallback)}">
<script>
(() => {{
  const targets = {json.dumps(ANCHORS, ensure_ascii=True)};
  let old = window.location.hash.slice(1);
  try {{ old = decodeURIComponent(old); }} catch (error) {{ old = ""; }}
  const next = Object.prototype.hasOwnProperty.call(targets, old)
    ? targets[old] : "grid-place-readout";
  window.location.replace({json.dumps(DEST)} + "#" + next);
}})();
</script>
<meta http-equiv="refresh" content="1;url={escape(fallback)}">
</head><body>
<h1>Spatial Cells and Their Models</h1>
<p>The former Grid Cells and Grid-to-Place Mapping section is now in
<a href="{escape(fallback)}">Chapter 4</a>.</p>
{old_ids}
</body></html>'''
    route = SITE / "chapters" / "grid-to-place" / "index.html"
    route.parent.mkdir(parents=True, exist_ok=True)
    route.write_text(page, encoding="utf-8")
    print(f"Published legacy grid-to-place redirect with {len(ANCHORS)} checked targets.")


if __name__ == "__main__":
    publish()
