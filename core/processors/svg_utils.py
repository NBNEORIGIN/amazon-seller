"""
SVG Drawing Utilities for Stake Processors
-----------------------------------------
Helpers for drawing SVG elements, unit conversions, and text.
"""

def draw_rounded_rect(dwg, insert, size, rx, ry, fill, stroke, stroke_width):
    """Draw a rounded rectangle on the SVG drawing."""
    return dwg.rect(insert=insert, size=size, rx=rx, ry=ry, fill=fill, stroke=stroke, stroke_width=stroke_width)

def add_multiline_text(dwg, lines, insert, font_size, font_family, anchor, fill):
    """Add multi-line text to SVG using tspans for each line."""
    text_elem = dwg.text("", insert=insert, font_size=font_size, font_family=font_family, text_anchor=anchor, fill=fill)
    for idx, line in enumerate(lines):
        dy_val = "0" if idx == 0 else "1.2em"
        tspan = dwg.tspan(line.strip(), x=[insert[0]], dy=[dy_val])
        text_elem.add(tspan)
    return text_elem

def mm_to_px(mm, px_per_mm):
    """Convert millimeters to pixels."""
    return mm * px_per_mm

def pt_to_mm(pt):
    """Convert points to millimeters."""
    return pt * 0.352778
