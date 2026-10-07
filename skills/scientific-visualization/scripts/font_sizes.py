#!/usr/bin/env python3
"""Proportional font-size hierarchy for figures of varying physical size.

Anchors the font-size hierarchy (plot title, subplot title, axis title,
legend, tick labels) to a figure's rendered width/height so the ratios
between tiers, and the font-size-to-figure-size ratio itself, stay constant
as output dimensions change. See references/publication_guidelines.md's
"Font-size hierarchy" and "Keep font size proportional to output size"
sections for the underlying rule of thumb this implements.
"""

from __future__ import annotations

import argparse
import json
import math
import sys

from _common import CliError

SCHEMA_VERSION = "1.0"

# Calibrated against a PowerPoint-exported reference figure at 96 dpi
# (1 pt = 96/72 px): a 1280x720 px standalone figure uses a 24 px (18 pt)
# axis title.
DEFAULT_REF_WIDTH = 1280.0
DEFAULT_REF_HEIGHT = 720.0
DEFAULT_REF_AXIS_TITLE_PX = 24.0
DEFAULT_TITLE_RATIO = 1.3
DEFAULT_SUBPLOT_TITLE_RATIO = 1.15
DEFAULT_LEGEND_RATIO = 0.85
DEFAULT_TICK_RATIO = 0.85
DEFAULT_MIN_PT = 8.0
_PX_PER_INCH = 96.0


def compute_font_sizes(
    width: float,
    height: float,
    *,
    ref_width: float = DEFAULT_REF_WIDTH,
    ref_height: float = DEFAULT_REF_HEIGHT,
    ref_axis_title_px: float = DEFAULT_REF_AXIS_TITLE_PX,
    title_ratio: float = DEFAULT_TITLE_RATIO,
    subplot_title_ratio: float = DEFAULT_SUBPLOT_TITLE_RATIO,
    legend_ratio: float = DEFAULT_LEGEND_RATIO,
    tick_ratio: float = DEFAULT_TICK_RATIO,
    min_pt: float = DEFAULT_MIN_PT,
) -> dict[str, float]:
    """Scale the whole font-size hierarchy to a given figure width/height.

    Axis title is the 100% baseline; the other tiers are set relative to it
    per the typography rule of thumb (plot title 120-140%, subplot title
    ~115%, legend/tick labels 80-90%), and every tier is floored at `min_pt`
    so nothing renders unreadably small.

    `width`/`height` are the rendered figure size, in the same unit as
    `ref_width`/`ref_height` (pixels by default); the scale factor is the
    geometric mean of the width and height ratios to the reference, so a
    non-uniform aspect-ratio change is handled gracefully. All five sizes
    are returned in points, ready to pass directly as a Matplotlib
    `fontsize=` value.
    """
    if width <= 0 or height <= 0:
        raise CliError("width and height must be positive")
    if ref_width <= 0 or ref_height <= 0:
        raise CliError("ref_width and ref_height must be positive")
    if ref_axis_title_px <= 0:
        raise CliError("ref_axis_title_px must be positive")
    if min_pt <= 0:
        raise CliError("min_pt must be positive")

    scale = math.sqrt((width / ref_width) * (height / ref_height))
    axis_title_px = ref_axis_title_px * scale
    axis_title_pt = axis_title_px * 72.0 / _PX_PER_INCH

    sizes = {
        "plot_title": axis_title_pt * title_ratio,
        "subplot_title": axis_title_pt * subplot_title_ratio,
        "axis_title": axis_title_pt,
        "legend": axis_title_pt * legend_ratio,
        "tick_labels": axis_title_pt * tick_ratio,
    }
    return {name: round(max(size, min_pt), 1) for name, size in sizes.items()}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Compute a proportional font-size hierarchy (plot title, "
            "subplot title, axis title, legend, tick labels) for a given "
            "figure width/height, anchored to a 1280x720 px / 18 pt "
            "axis-title reference."
        )
    )
    parser.add_argument("width", type=float, help="figure width, in pixels by default")
    parser.add_argument("height", type=float, help="figure height, in pixels by default")
    parser.add_argument(
        "--ref-width", type=float, default=DEFAULT_REF_WIDTH, help="reference width"
    )
    parser.add_argument(
        "--ref-height", type=float, default=DEFAULT_REF_HEIGHT, help="reference height"
    )
    parser.add_argument(
        "--ref-axis-title-px",
        type=float,
        default=DEFAULT_REF_AXIS_TITLE_PX,
        help="axis-title size (px) at the reference width/height",
    )
    parser.add_argument("--title-ratio", type=float, default=DEFAULT_TITLE_RATIO)
    parser.add_argument(
        "--subplot-title-ratio", type=float, default=DEFAULT_SUBPLOT_TITLE_RATIO
    )
    parser.add_argument("--legend-ratio", type=float, default=DEFAULT_LEGEND_RATIO)
    parser.add_argument("--tick-ratio", type=float, default=DEFAULT_TICK_RATIO)
    parser.add_argument(
        "--min-pt", type=float, default=DEFAULT_MIN_PT, help="floor applied to every tier"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        sizes = compute_font_sizes(
            args.width,
            args.height,
            ref_width=args.ref_width,
            ref_height=args.ref_height,
            ref_axis_title_px=args.ref_axis_title_px,
            title_ratio=args.title_ratio,
            subplot_title_ratio=args.subplot_title_ratio,
            legend_ratio=args.legend_ratio,
            tick_ratio=args.tick_ratio,
            min_pt=args.min_pt,
        )
        print(
            json.dumps(
                {
                    "schema_version": SCHEMA_VERSION,
                    "width": args.width,
                    "height": args.height,
                    "font_sizes_pt": sizes,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    except CliError as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
