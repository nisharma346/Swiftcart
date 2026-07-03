from PIL import Image
from pathlib import Path

# Banner directory
banners_dir = Path('static/images/banners')

# Get all banner images
banner_files = sorted(banners_dir.glob('banner*.png')) + sorted(banners_dir.glob('banner*.jpg'))

print(f"Found {len(banner_files)} banner(s)")

for banner_file in banner_files:
    # Open the image
    img = Image.open(banner_file)
    width, height = img.size
    print(f"\nProcessing {banner_file.name}: {width}x{height}")
    
    # Crop from top and bottom - remove 5% from each edge
    crop_top = int(height * 0.05)
    crop_bottom = int(height * 0.05)
    
    # Define crop box (left, top, right, bottom)
    crop_box = (0, crop_top, width, height - crop_bottom)
    
    # Crop the image
    cropped_img = img.crop(crop_box)
    
    # Save the cropped image (overwrite original)
    cropped_img.save(banner_file)
    print(f"✓ Cropped {banner_file.name} - Removed top {crop_top}px (5%) and bottom {crop_bottom}px (5%)")
    print(f"  New dimensions: {cropped_img.size}")

print("\n✓ All banners cropped successfully!")
