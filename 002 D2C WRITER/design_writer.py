import os

def generate_svgs(orders, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    # Example: Write one SVG file per order (replace with your real SVG logic)
    for order in orders:
        svg_path = os.path.join(output_dir, f"{order['order-item-id']}.svg")
        with open(svg_path, 'w', encoding='utf-8') as f:
            f.write(f"<svg><!-- SVG for {order['order-item-id']} --></svg>")
    print("SVG generation complete.")
