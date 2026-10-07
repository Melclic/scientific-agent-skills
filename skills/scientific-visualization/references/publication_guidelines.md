# Publication Figure Principles

Reviewed 2026-07-23. These are general scientific-communication principles, not publisher requirements. Date-sensitive rules belong in `journal_requirements.md`. Source IDs resolve in `sources.md`.

## Preserve evidence before styling

Keep three layers separate:

1. **Raw/source data**: immutable originals, acquisition metadata, exclusions, and missing-value codes.
2. **Transformation record**: executable code or a machine-readable log of filtering, normalization, aggregation, statistical estimation, image processing, and random seeds.
3. **Presentation output**: the figure and an export manifest recording dimensions, format, package versions, and source references.

Do not overwrite raw images or tabular data. Keep native-resolution images. Upsampling changes pixel count, not information; PLOS, Science, Nature, Cell Press, Elsevier, and IEEE explicitly warn against treating it as improved quality [PLOS-FIG] [SCIENCE-REVISED] [NATURE-FINAL] [CELL-FIG] [ELSEVIER-SIZE] [IEEE-SIZE].

For experimental/observational images:

- Apply necessary brightness, contrast, and color adjustments consistently to the whole image unless a disclosed scientific method requires otherwise.
- Never selectively erase, obscure, clone, or enhance features.
- Preserve background and nonspecific signal.
- Mark and explain splices, omitted lanes, composites, or stitched fields.
- Retain originals and the exact processing steps. Some publishers request originals during review or production [CELL-FIG] [PLOS-FIG].

The bundled exporter can write a provenance manifest, but it cannot confirm that supplied provenance is complete.

## Avoid visual deception

### Baselines and context

- **Bars and filled areas encode length/area from a baseline**: normally show the zero baseline. If a nonzero reference is scientifically meaningful, make that reference explicit and avoid implying absolute magnitude.
- **Points and lines encode position**: a nonzero axis limit can be valid, but show enough context, disclose breaks, and avoid choosing limits solely to magnify a small effect.
- Use common limits for panels intended for direct comparison. If limits differ, make the difference unmistakable.
- Do not extend axes far beyond observed data merely to suppress visible variation; Science explicitly advises that scales not extend beyond plotted data [SCIENCE-INITIAL].

### Uncertainty and raw observations

- Do not add error bars mechanically. Show uncertainty when an estimate is displayed, and show spread when the distribution is the question.
- Name the interval precisely: SD, SE, percentile interval, parametric CI, bootstrap CI, posterior interval, or another definition.
- State sample size, unit of replication, estimator, interval level, and dependence/repeated-measure handling.
- Use deterministic seeds for bootstrap displays. Seaborn 0.13.2 supports `errorbar="sd"`, `"se"`, `"pi"`, `"ci"`, tuples such as `("ci", 95)`, or a callable; bootstrap results vary unless `seed` is set [SEABORN-ERROR].
- Show raw observations when feasible. Do not jitter points so far that their category or value becomes ambiguous.
- Significance stars are not uncertainty. Add them only for a reported analysis, identify the test and multiplicity handling, and provide exact values where practical.

### Missing, excluded, and censored data

- Keep missing values distinct from zero, below-detection-limit values, and excluded observations.
- Do not silently connect across missing time points. Use a gap, explicit interpolation style, or a model curve whose status is stated.
- Give missing values a dedicated legend entry or neutral `bad` colormap color.
- Record exclusions and their rationale outside the plotting code as well as in the caption/methods.

### Area, volume, and 3D encodings

- Prefer position on a common scale.
- If area represents magnitude, scale **area**, not radius. If volume represents magnitude, scale volume, not diameter.
- Avoid perspective 3D bars, pies, and surfaces for simple comparisons; occlusion and perspective distort values.
- If a true 3D scientific structure is necessary, add orthogonal views, scale/orientation cues, and accessible alternatives.

### Logarithms and other transforms

- Label the transformed scale and base. Say whether values, axes, or model outputs were transformed.
- A logarithmic axis requires a declared policy for zero and negative values; never silently discard them.
- Interpret equal distances as ratios, not additive differences.
- For signed data around zero, consider `SymLogNorm`/a symmetric log axis with a disclosed linear region; for unequal ranges around a meaningful center, consider `TwoSlopeNorm` [MPL-NORM].
- Power-law or arbitrary transforms need strong justification and conspicuous disclosure. Matplotlib itself notes that viewers are less familiar with power normalization [MPL-NORM].

### Binning, smoothing, and aggregation

- Record bin edges, inclusion convention, bandwidth/window, smoothing method, and whether choices were made before seeing the result.
- Show sensitivity to reasonable bin or bandwidth choices when conclusions depend on them.
- Do not use interpolation or smoothing to imply observations between measured points.
- Preserve and, where practical, expose underlying observations.

### Normalization and color limits

- State the formula and reference: per-capita, percent of baseline, z-score axis, library-size factor, min-max range, or other transformation.
- Fit normalization parameters on the appropriate data partition; avoid information leakage.
- Use the same normalization and color limits across directly compared panels unless the difference is explicit.
- A diverging map needs a scientifically meaningful center. `Normalize`, `LogNorm`, `CenteredNorm`, `SymLogNorm`, `TwoSlopeNorm`, and `BoundaryNorm` encode different assumptions [MPL-NORM].
- Always label colorbars with units and transformed scale.

### Dual axes

Prefer aligned panels or normalized/common-unit displays. Dual y-axes can make unrelated series appear correlated because each range can be tuned independently. If unavoidable:

- justify the shared x-domain and distinct units;
- label each axis and series directly;
- avoid matching colors as the only association cue;
- choose limits independently of the desired visual relationship;
- provide the underlying data.

### Image contrast and channels

- Inspect histograms and clipped-pixel counts before and after adjustment.
- Apply comparable processing to images being compared.
- State channel assignment, lookup table, projection, denoising, deconvolution, thresholding, and contrast limits.
- Use scale bars based on calibration, not magnification text.
- Do not rely on red/green channel identity alone; use accessible channel combinations, outlines, labels, or separate grayscale panels.

## Encoding and color

Match the palette to data:

- **Qualitative** for unordered categories; do not imply order.
- **Sequential** for ordered magnitude.
- **Diverging** only when a meaningful midpoint exists.
- **Cyclic** for periodic variables such as direction or phase.

Use hue consistently across a manuscript. Avoid rainbow maps for ordered data unless there is a documented scientific reason and the map has been evaluated for perceptual artifacts. Paul Tol explains why ordinary rainbow schemes create false transitions and fail for some color-vision conditions [TOL].

Color is not a sufficient encoding:

- combine it with marker shape, line style, hatching, direct labels, or panel separation;
- audit contrast against the actual background;
- inspect grayscale, but do not treat grayscale conversion as a complete color-vision simulation;
- keep legends ordered like the data or direct-label series.

See `color_palettes.md` and run `scripts/palette_audit.py`.

## Accessibility

WCAG 2.2 is a web-content standard, not a journal-print specification. It provides useful targets for figures delivered on the web [WCAG22]:

- SC 1.4.1 (Level A): color is not the only visual means of conveying information.
- SC 1.4.3 (Level AA): normal text has at least 4.5:1 contrast; large text has at least 3:1, with stated exceptions.
- SC 1.4.11 (Level AA): graphical objects required to understand content have at least 3:1 contrast against adjacent colors, with an essential-presentation exception.
- SC 1.1.1 (Level A): non-text content has an equivalent text alternative.
- SC 1.4.5 (Level AA): use actual text rather than images of text when the technology can provide it, subject to exceptions.

For web/interactive figures also provide:

- a concise alt text naming chart type, variables, main pattern, and important exception;
- a long description or nearby narrative for complex figures;
- the underlying data in an accessible table/download;
- keyboard-operable interactions, visible focus, and non-hover access to values;
- a static fallback that preserves the scientific message.

Passing a palette ratio audit does not prove WCAG conformance; applicability depends on rendered context and alternatives.

## Layout, typography, and annotation

- Design at final physical size. Judge labels, symbols, and line weights at that size.
- Use one legible font family and a restrained size hierarchy (see below).
- Include units in axis/colorbar labels. Define abbreviations.
- Keep panel labels consistent and outside dense data regions.
- Use layout engines intentionally: `layout="constrained"` handles nested grids and colorbars; calling `tight_layout()` disables constrained layout [MPL-LAYOUT].
- Check all labels and legends after export. `bbox_inches="tight"` can alter physical page dimensions, so do not use it when exact page width is required [MPL-SAVE].
- Keep decorative ink subordinate to data, uncertainty, and annotations. Gridlines can help value lookup when light and sparse; removing them is not a universal rule.

### Font-size hierarchy

Anchor the hierarchy to the **axis title**, not the plot title: it is present on nearly every figure and is the steadiest reference point.

| Element | Relative to axis title | Typical absolute size |
|---|---:|---:|
| Plot/panel title | 120-140% | 14-16 pt |
| Axis titles (baseline) | 100% | 11-12 pt |
| Legend text | 80-90% | 9-10 pt |
| Tick labels | 80-90% | 9-10 pt |

A reliable default triplet is `title : axis title : legend/tick = 14 pt : 11 pt : 9 pt`. Keep adjacent levels roughly **2-3 pt apart**: collapsing title and axis-title to the same size, or closer than ~2 pt, flattens the hierarchy and makes it illegible once the figure is reduced to its final printed size.

These are design-time ratios, not a substitute for a target journal's final-reduced-size minimums (`journal_requirements.md`) — check both. Judge sizes at the figure's final printed/rendered dimensions, not at the on-screen editing size, and avoid text smaller than roughly **8 pt** after scaling.

`scripts/font_sizes.py` implements this hierarchy as `compute_font_sizes(width, height)`, so the ratios and the 8 pt floor are computed instead of hand-tuned per figure. Call it for every panel of a multi-panel figure too, passing that panel's own rendered width/height (the figure size divided by its grid geometry), not the whole figure's.

### Keep font size proportional to output size

The same absolute point size reads as a different *relative* size depending on how large the figure is rendered: a 10 pt title on a 50x50 cm poster panel looks tiny next to the same 10 pt title on a 5x5 cm thumbnail. When the same figure role (e.g. "panel title") is exported at different physical output dimensions across a project, scale every level of the hierarchy with the output dimension so the font-size-to-figure-size ratio — and the 2-3 pt gaps between levels — stays constant. For example, doubling a figure's physical width/height should double its point sizes at every tier (10 pt -> 20 pt title), not leave them fixed. Parameterize sizes from one reference figure size (e.g. a scale factor relative to a baseline width in inches) rather than hardcoding the same pt values across figures of differing output sizes, and scale all tiers together so the hierarchy itself does not distort.

Use `scripts/font_sizes.py` instead of hand-tuning sizes per figure:

```python
from font_sizes import compute_font_sizes

# Standalone figure: compute from its own rendered pixel size.
fig, ax = plt.subplots(figsize=(7, 5.8))
fig_w, fig_h = fig.get_size_inches()
sizes = compute_font_sizes(fig_w * 96, fig_h * 96)
ax.set_xlabel("Time (hours)", fontsize=sizes["axis_title"])
ax.tick_params(labelsize=sizes["tick_labels"])
ax.legend(fontsize=sizes["legend"])

# Multi-panel figure: call compute_font_sizes() per panel, passing that
# panel's own rendered size (the figure size divided by its grid geometry),
# so panels in a 2x3 grid get smaller fonts than the same figure drawn as a
# single panel.
n_rows, n_cols = 2, 3
fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 7))
fig_w, fig_h = fig.get_size_inches()
panel_sizes = compute_font_sizes((fig_w / n_cols) * 96, (fig_h / n_rows) * 96)
for ax in axes.flat:
    ax.set_title("Panel title", fontsize=panel_sizes["subplot_title"])
```

## Static, vector, raster, and interactive output

### Vector

PDF/SVG/EPS are useful for text and line art, but a vector container may include rasterized artists. DPI still controls those raster elements [MPL-SAVE]. Dense scatter plots can be selectively rasterized to control file size while preserving vector text/axes.

For Matplotlib:

```python
import matplotlib as mpl

mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["svg.fonttype"] = "none"
```

PDF/PS Type 42 embeds TrueType fonts. `svg.fonttype="none"` leaves text as text and therefore depends on font availability; `svg.fonttype="path"` trades editability/searchability for appearance portability [MPL-STYLE]. Inspect the delivered file rather than assuming font behavior.

### Raster

Required pixel width is:

```text
pixels = final width (inches) × target pixels per inch
```

Embedded DPI metadata alone does not add detail. TIFF/PNG are lossless choices; JPEG can be accepted by some publishers for photographs but is a poor choice for line art or text because it is lossy. Preserve original bit depth and color profile when scientifically important.

Transparency can reveal an unintended background or change apparent contrast. Matplotlib's `transparent=True` makes axes patches transparent and, unless explicitly overridden, the figure patch too [MPL-SAVE]. Prefer an explicit opaque background for submission unless the destination requires transparency.

### Plotly

- `write_html()` preserves interaction and is self-contained by default; that embeds Plotly.js and creates a large file. `include_plotlyjs` and `full_html=False` change portability and embedding behavior [PLOTLY-HTML].
- Static `write_image()` uses Kaleido and supports PNG, JPEG, WebP, SVG, and PDF. Width/height are logical pixels; `scale` changes physical output pixel count, not a journal DPI declaration [PLOTLY-STATIC].
- WebGL traces are partly rasterized inside SVG/PDF output [PLOTLY-STATIC].
- Export a static, captioned fallback and accessible data alongside interactive output.

## Final scientific review

- [ ] Raw data and native images are preserved.
- [ ] Transformations, exclusions, normalization, bins, and random seeds are recorded.
- [ ] Missing/censored values are explicit.
- [ ] Baselines, limits, log scales, and breaks are scientifically justified.
- [ ] Uncertainty and sample size are defined.
- [ ] Area/volume and color normalization encode magnitude correctly.
- [ ] Color is redundant; foreground/background contrast was reviewed.
- [ ] Alt text/long description and underlying data are available for web delivery.
- [ ] Physical size, raster pixels, fonts, transparency, and file format were inspected after export.
- [ ] The current target-journal instructions were checked for the correct submission phase.
