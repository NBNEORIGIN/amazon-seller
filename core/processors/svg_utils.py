"""
SVG Drawing Utilities for Stake Processors
-----------------------------------------
Helpers for drawing SVG elements, unit conversions, and text.
"""
import base64
import os
# import svgwrite # Not needed at top-level if only used type hinted or within functions

def draw_rounded_rect(dwg, insert, size, rx, ry, fill, stroke, stroke_width):
    """Draw a rounded rectangle on the SVG drawing."""
    return dwg.rect(insert=insert, size=size, rx=rx, ry=ry, fill=fill, stroke=stroke, stroke_width=stroke_width)

def add_multiline_text(dwg, lines, insert, font_size, font_family, anchor, fill, line_spacing_factor=1.2):
    """
    Add multi-line text to SVG using tspans for each line.
    The `insert` tuple is the (x,y) for the first line's baseline.
    `font_size` should be a string with units (e.g., "12pt", "5mm").
    `line_spacing_factor` is applied to the font_size for `dy` of subsequent lines.
    """
    text_elem = dwg.text("", insert=insert, font_size=font_size, font_family=font_family, text_anchor=anchor, fill=fill)
    for idx, line in enumerate(lines):
        # dy_val = "0" if idx == 0 else f"{line_spacing_factor}em" # 'em' is relative to current font size
        # For svgwrite, it's often easier to manage absolute dy if font_size is consistent,
        # or use a fixed offset based on font_size if known in pixels/mm.
        # Using 'em' is generally good for relative spacing.
        if idx == 0:
            dy_val = "0"
        else:
            # This attempts to use a relative spacing based on the font size.
            # If font_size is "12pt", 1.2em would be 1.2 * 12pt.
            # svgwrite might need explicit pixel/mm values for dy if 'em' is not well-supported for tspans.
            # For simplicity and common use, "1.2em" is standard.
            dy_val = f"{line_spacing_factor}em"

        tspan = dwg.tspan(line.strip(), x=[insert[0]], dy=[dy_val])
        text_elem.add(tspan)
    dwg.add(text_elem) # Ensure the parent text element is added to the drawing
    return text_elem

def mm_to_px(mm, px_per_mm=3.7795275591): # Added default px_per_mm
    """Convert millimeters to pixels."""
    return mm * px_per_mm

def pt_to_mm(pt):
    """Convert points to millimeters."""
    return pt * 0.352778 # Standard conversion factor

def embed_image(dwg, image_path, insert, size, clip_path_id=None, defs=None):
    """
    Embeds a raster image (PNG, JPG) into the SVG using svgwrite.

    Args:
        dwg: The svgwrite drawing object.
        image_path (str): Path to the image file.
        insert (tuple): (x, y) coordinates for the top-left of the image.
        size (tuple): (width, height) for displaying the image.
        clip_path_id (str, optional): ID of an existing clipPath to apply.
        defs (svgwrite.container.Defs, optional): Pass dwg.defs if you want to ensure
                                                 CSS for image rendering is defined.
                                                 (e.g., image-rendering: pixelated)
    """
    if not os.path.exists(image_path):
        print(f"Warning: Image not found at {image_path}")
        # Optionally, draw a placeholder
        dwg.add(dwg.rect(insert=insert, size=size, fill='#cccccc', stroke='red', stroke_width=1))
        dwg.add(dwg.text("Image Missing", insert=(insert[0] + size[0]/2, insert[1] + size[1]/2),
                       text_anchor="middle", alignment_baseline="middle", fill="red", font_size="10px"))
        return None

    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        mime_type = ''
        if image_path.lower().endswith('.png'):
            mime_type = 'image/png'
        elif image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
            mime_type = 'image/jpeg'
        else:
            print(f"Warning: Unsupported image type for {image_path}")
            # Draw placeholder for unsupported type
            dwg.add(dwg.rect(insert=insert, size=size, fill='#e0e0e0', stroke='orange', stroke_width=1))
            dwg.add(dwg.text("Unsupported Img", insert=(insert[0] + size[0]/2, insert[1] + size[1]/2),
                           text_anchor="middle", alignment_baseline="middle", fill="orange", font_size="8px"))
            return None

        image_href = f"data:{mime_type};base64,{encoded_string}"

        img_obj = dwg.image(href=image_href, insert=insert, size=size)
        if clip_path_id:
            img_obj.update({'clip-path': f'url(#{clip_path_id})'})

        # Optional: Add style for pixelated rendering if needed for some images
        if defs is not None:
            # Check if style already exists to avoid duplicates
            style_id = "img-pixelated-style"
            # A more robust check would be to iterate through defs content if it's complex
            # For now, assuming simple addition or that duplicate styles are harmless / handled by SVG renderers.
            # if not defs.getElementById(style_id): # getElementById is not a standard svgwrite Defs method
            # A simple way to check is to query elements, but svgwrite doesn't offer easy query by id before save.
            # For now, we'll add it; browsers usually handle duplicate styles gracefully.
            defs.add(dwg.style(f".pixelated {{ image-rendering: optimizeSpeed; image-rendering: -moz-crisp-edges; image-rendering: -webkit-optimize-contrast; image-rendering: pixelated; -ms-interpolation-mode: nearest-neighbor; }}", id=style_id))
            img_obj.attribs['class'] = 'pixelated'

        dwg.add(img_obj)
        return img_obj
    except Exception as e:
        print(f"Error embedding image {image_path}: {e}")
        # Optionally, draw a placeholder on error
        dwg.add(dwg.rect(insert=insert, size=size, fill='#ffdddd', stroke='red', stroke_width=1))
        dwg.add(dwg.text("Img Error", insert=(insert[0] + size[0]/2, insert[1] + size[1]/2),
                       text_anchor="middle", alignment_baseline="middle", fill="red", font_size="10px"))
        return None

def add_reference_point(dwg, x_mm=None, y_mm=None, size_px=5, color='magenta', px_per_mm=3.7795275591):
    """
    Adds a small reference point (circle) to the SVG drawing.
    Useful for debugging alignment and positioning.
    Coordinates are given in mm and converted to px.

    Args:
        dwg: The svgwrite drawing object.
        x_mm (float, optional): X-coordinate in mm. Defaults to page center (approx A4).
        y_mm (float, optional): Y-coordinate in mm. Defaults to page center (approx A4).
        size_px (int): Radius of the circle in pixels.
        color (str): Color of the reference point.
        px_per_mm (float): Conversion factor from mm to pixels.
    """
    # Determine page dimensions from viewBox if available, otherwise use defaults
    page_width_px = None
    page_height_px = None
    if hasattr(dwg, 'attribs') and 'viewBox' in dwg.attribs:
        try:
            _, _, vb_w, vb_h = map(float, dwg.attribs['viewBox'].split())
            page_width_px = vb_w
            page_height_px = vb_h
        except ValueError:
            pass # Could not parse viewBox

    if x_mm is None:
        x_px = (page_width_px / 2) if page_width_px else (210 * px_per_mm / 2) # Default to center
    else:
        x_px = x_mm * px_per_mm

    if y_mm is None:
        y_px = (page_height_px / 2) if page_height_px else (297 * px_per_mm / 2) # Default to center
    else:
        y_px = y_mm * px_per_mm

    dwg.add(dwg.circle(center=(x_px, y_px), r=size_px, fill=color, stroke='black', stroke_width=0.5, opacity=0.7))

# It's good practice to have a class SVGUtils if these are meant to be methods of it.
# For now, they are standalone functions as per the original structure.
# class SVGUtils:
#     def __init__(self, px_per_mm_default=3.7795275591):
#         self.px_per_mm = px_per_mm_default
#         # Other common settings can be initialized here
#
#     def mm_to_px(self, mm):
#         return mm * self.px_per_mm
#
#     def pt_to_mm(self, pt):
#         return pt * 0.352778
#
#     # Then draw_rounded_rect, add_multiline_text, embed_image, add_reference_point would be methods.
#     # This would require processors to instantiate SVGUtils: self.svg_utils = SVGUtils()
#     # and call methods like self.svg_utils.embed_image(...)
#     # For now, keeping them as standalone functions as per current processor usage.
