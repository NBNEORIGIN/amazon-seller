"""
SVG Generator Module
-------------------
Handles SVG creation by delegating to stake processors.
This module is independent of the GUI and can be tested separately.
"""

from core.processors.coloured_large_stakes import ColouredLargeStakesProcessor
from core.processors.regular_stakes import RegularStakesProcessor
# Import other processors as needed

class SVGGenerator:
    def __init__(self, graphics_path, output_dir):
        self.graphics_path = graphics_path
        self.output_dir = output_dir
        # Instantiate processors
        self.coloured_large = ColouredLargeStakesProcessor(graphics_path, output_dir)
        self.regular = RegularStakesProcessor(graphics_path, output_dir)
        # Add other processors as attributes

    def generate_svg(self, stake_type: str, orders, **kwargs):
        """Generate SVG for a given stake type and order data."""
        if stake_type == 'coloured_large':
            return self.coloured_large.process_orders(orders, **kwargs)
        elif stake_type == 'regular':
            return self.regular.process_orders(orders, **kwargs)
        # Add more stake types as needed
        else:
            raise ValueError(f"Unknown stake type: {stake_type}")

# Example usage (for testing, not run by GUI):
if __name__ == "__main__":
    svg_gen = SVGGenerator("graphics/", "SVG_OUTPUT/")
    # svg_gen.generate_svg('coloured_large', some_orders_df)
    # svg_gen.generate_svg('regular', some_orders_df)
