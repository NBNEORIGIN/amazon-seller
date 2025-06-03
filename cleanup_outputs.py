import os
import glob
import shutil

# Paths to clean
project_root = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(project_root, '001 AMAZON DATA DOWNLOAD')
svg_dir = os.path.join(project_root, 'SVG_OUTPUT')
images_dir = os.path.join(project_root, 'images')
old_images_dir = os.path.join(project_root, '004 IMAGES')

# 1. Delete all output.csv and output.txt in data_dir
for pattern in ['output.csv', 'output.txt']:
    for path in glob.glob(os.path.join(data_dir, pattern)):
        print(f"Deleting: {path}")
        os.remove(path)

# 2. Delete all CSVs in SVG_OUTPUT (batch files)
for csv_file in glob.glob(os.path.join(svg_dir, '*.csv')):
    print(f"Deleting: {csv_file}")
    os.remove(csv_file)

# 3. Delete all images in images_dir (but not the folder itself)
if os.path.isdir(images_dir):
    for img_file in glob.glob(os.path.join(images_dir, '*.jpg')):
        print(f"Deleting: {img_file}")
        os.remove(img_file)

# 4. Optionally, delete all images in old 004 IMAGES dir
if os.path.isdir(old_images_dir):
    for img_file in glob.glob(os.path.join(old_images_dir, '*.jpg')):
        print(f"Deleting old image: {img_file}")
        os.remove(img_file)

print("Cleanup complete. You can now re-run your pipeline to regenerate fresh outputs.")
