"""Prepare attributed, openly licensed figures used by Chapter 4.

Run before the HTML build. Download only the specified published figures,
validate them with Pillow, and save web-sized JPEGs without cropping, changing
panels, or altering plotted data. Sources and licenses are recorded separately
in assets/SPATIAL-FIGURE-CREDITS.md. Failure is fatal, not a silent placeholder.
"""
from __future__ import annotations

import hashlib
import io
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "spatial-literature"


def elife(article: str, figure: str, version: int) -> list[str]:
    name = f"elife-{article}-{figure}-v{version}.tif"
    return [
        f"https://cdn.elifesciences.org/articles/{article}/{name}",
        f"https://iiif.elifesciences.org/lax:{article}%2F{name}/full/1500,/0/default.jpg",
        f"https://iiif.elifesciences.org/lax/{article}%2F{name}/full/1500,/0/default.jpg",
    ]


FIGURES = [
    ("hippocampal-circuit.jpg", [
        "https://raw.githubusercontent.com/compcogneuro/book/e0c697b4d4d134f29cb5c2bbde41b1b6b409b63d/figures/fig_hippo_mem_formation.png",
    ]),
    ("place-fields.jpg", [
        "https://www.frontiersin.org/files/Articles/618658/xml-images/fncel-15-618658-g0006.webp",
        "https://www.frontiersin.org/files/Articles/618658/fncel-15-618658-HTML/image_m/fncel-15-618658-g006.jpg",
    ]),
    ("grid-fields.jpg", elife("16937", "fig2", 2)),
    ("head-direction.jpg", elife("14592", "fig3", 2)),
    ("border-fields.jpg", elife("16937", "fig5", 2)),
    ("speed-cells.jpg", [
        "https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-022-29583-z/MediaObjects/41467_2022_29583_Fig2_HTML.png",
        "https://media.springernature.com/lw1200/springer-static/image/art%3A10.1038%2Fs41467-022-29583-z/MediaObjects/41467_2022_29583_Fig2_HTML.png",
    ]),
    ("time-distance-cells.jpg", elife("83930", "fig2", 1)),
]


def prepare() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    records = []
    for filename, urls in FIGURES:
        errors = []
        for url in urls:
            try:
                request = Request(url, headers={"User-Agent": "Mozilla/5.0 (textbook figure build; attribution in caption)"})
                with urlopen(request, timeout=40) as response:
                    data = response.read(25 * 1024 * 1024 + 1)
                if len(data) > 25 * 1024 * 1024:
                    raise ValueError("Figure exceeds 25 MiB download limit")
                with Image.open(io.BytesIO(data)) as original:
                    original.load()
                    image = ImageOps.exif_transpose(original).convert("RGB")
                    source_size = image.size
                    if min(source_size) < 180:
                        raise ValueError(f"Implausibly small figure: {source_size}")
                    image.thumbnail((1800, 2400), Image.Resampling.LANCZOS)
                    image.save(OUT / filename, format="JPEG", quality=93, optimize=True)
                record = {"file": filename, "url": url, "source_size": source_size,
                          "sha256": hashlib.sha256(data).hexdigest()}
                records.append(record)
                print(f"FIGURE OK: {filename} source={source_size} url={url}", flush=True)
                break
            except (HTTPError, URLError, OSError, ValueError) as exc:
                errors.append(f"{url}: {type(exc).__name__}: {exc}")
        else:
            raise RuntimeError("Could not retrieve a valid image for " + filename + "\n" + "\n".join(errors))
    (OUT / "source-downloads.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(f"Validated {len(records)} licensed spatial-cell figures.")


if __name__ == "__main__":
    prepare()
