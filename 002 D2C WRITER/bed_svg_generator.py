import svgwrite
import xml.etree.ElementTree as ET
import os

def create_bed_svg(
    output_path,
    bed_width_mm,
    bed_height_mm,
    grid_cols,
    grid_rows,
    part_svg_path,
    part_width_mm,
    part_height_mm,
    spacing_x_mm=0,
    spacing_y_mm=0,
    x_offset_mm=0,
    y_offset_mm=0
):
    """
    Generate a tiled SVG bed using the specified part SVG.
    Each part is inlined (not referenced), for maximum compatibility.
    """
    dwg = svgwrite.Drawing(
        output_path,
        size=(f"{bed_width_mm}mm", f"{bed_height_mm}mm"),
        viewBox=f"0 0 {bed_width_mm} {bed_height_mm}"
    )
    # Parse the part SVG as XML
    part_tree = ET.parse(part_svg_path)
    part_root = part_tree.getroot()
    # Remove width/height/viewBox from the part to avoid scaling issues
    for attr in ["width", "height", "viewBox", "x", "y"]:
        if attr in part_root.attrib:
            del part_root.attrib[attr]
    # Convert part SVG to string (without outer <svg> tag)
    part_xml = ET.tostring(part_root, encoding="unicode", method="xml")
    # Remove the outer <svg ...>...</svg> wrapper
    if part_xml.startswith("<svg"):
        part_xml = part_xml[part_xml.find('>')+1:part_xml.rfind('</svg>')]
    # Tile the part SVG
    for row in range(grid_rows):
        for col in range(grid_cols):
            x = x_offset_mm + col * (part_width_mm + spacing_x_mm)
            y = y_offset_mm + row * (part_height_mm + spacing_y_mm)
            # Embed the part SVG at (x, y) using svgwrite's raw XML capability
            dwg.add(svgwrite.container.Group())  # placeholder for grouping
            dwg.add(svgwrite.raw(part_xml, insert=(x, y)))
    dwg.save()
    print(f"Bed SVG saved to: {output_path}")
