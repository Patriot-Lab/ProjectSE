from PIL import Image
import numpy as np
import os

def generate_image(file_path, size_mb):
    num_pixels = size_mb * 1024 * 1024 // 3
    side_length = int(np.sqrt(num_pixels))
    while side_length * side_length * 3 < num_pixels:
        side_length += 1
    
    random_pixels = np.random.randint(0, 256, (side_length, side_length, 3), dtype=np.uint8)
    
    # Create and save the image
    img = Image.fromarray(random_pixels)
    img.save(file_path)

# Define sizes in MB
sizes_mb = [2, 4, 8, 16, 32, 64, 128, 256, 512]

# Directory to save images
output_dir = '../images'
os.makedirs(output_dir, exist_ok=True)

# Generate images
for size in sizes_mb:
    file_name = f'{size}MB_image.png'
    file_path = os.path.join(output_dir, file_name)
    generate_image(file_path, size)
    print(f'Generated {file_name}')
