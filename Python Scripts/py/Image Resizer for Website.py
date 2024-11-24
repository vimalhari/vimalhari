from PIL import Image
import os
import io
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Define input and output folders
input_folder = r'D:\Webp'
output_folder = r'D:\Webp\Output'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Target sizes in KB
TARGET_SIZE_KB = 20  # For PNG images
WEBP_TARGET_SIZE_KB = 50  # Target size for WebP conversion (if different from PNG)

# Function to optimize PNG image size
def reduce_image_to_target_size(input_image_path, output_image_path, target_size_kb):
    with Image.open(input_image_path) as img:
        img_format = 'PNG' if img.mode in ('RGBA', 'LA', 'P') else 'WEBP'

        # Check if the original image is under target size
        with io.BytesIO() as output:
            img.save(output, format=img_format, optimize=True)
            size_kb = output.tell() / 1024
            if size_kb <= target_size_kb:
                # Save the original image
                with open(output_image_path, 'wb') as f:
                    f.write(output.getvalue())
                logging.info(f"{os.path.basename(input_image_path)}: Already under target size. Kept the original.")
                return

        # Binary search for optimal quality to fit within target size
        quality_min, quality_max = 10, 90
        best_output = None

        while quality_min <= quality_max:
            quality = (quality_min + quality_max) // 2
            with io.BytesIO() as output:
                img.save(output, format=img_format, quality=quality, optimize=True)
                size_kb = output.tell() / 1024

            if size_kb <= target_size_kb:
                best_output = output.getvalue()
                quality_min = quality + 1
            else:
                quality_max = quality - 1

        # Save the best output if binary search was successful
        if best_output:
            with open(output_image_path, 'wb') as f:
                f.write(best_output)
            logging.info(f"{os.path.basename(input_image_path)}: Compressed to {size_kb:.2f} KB at quality {quality}.")
            return

        # If resizing is required due to large image size
        resize_factor_min, resize_factor_max = 0.1, 1.0
        best_resize_factor, best_output = resize_factor_min, None

        while resize_factor_max - resize_factor_min > 0.01:
            resize_factor = (resize_factor_min + resize_factor_max) / 2
            new_size = (int(img.width * resize_factor), int(img.height * resize_factor))
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS)

            with io.BytesIO() as output:
                img_resized.save(output, format=img_format, quality=quality_min, optimize=True)
                size_kb = output.tell() / 1024

            if size_kb <= target_size_kb:
                best_resize_factor = resize_factor
                best_output = output.getvalue()
                resize_factor_min = resize_factor
            else:
                resize_factor_max = resize_factor

        # Save the resized output
        if best_output:
            with open(output_image_path, 'wb') as f:
                f.write(best_output)
            logging.info(f"{os.path.basename(input_image_path)}: Resized and compressed to {size_kb:.2f} KB.")
        else:
            # If all attempts fail, save the smallest possible image
            logging.warning(f"{os.path.basename(input_image_path)}: Could not meet target size. Saved at minimal quality.")
            img_resized.save(output_image_path, format=img_format, quality=10, optimize=True)

# Function to convert JPG to WebP for website optimization
def convert_jpg_to_webp(input_image_path, output_image_path, quality=80, max_dimensions=(1920, 1080)):
    with Image.open(input_image_path) as img:
        # Resize if larger than max dimensions, keeping aspect ratio
        img.thumbnail(max_dimensions, Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary and save as WebP
        img.convert('RGB').save(output_image_path, 'WEBP', quality=quality, optimize=True)
        size_kb = os.path.getsize(output_image_path) / 1024
        logging.info(f"Converted {os.path.basename(input_image_path)} to WebP ({size_kb:.2f} KB) at quality {quality}.")

# Process each file in the input folder
for filename in os.listdir(input_folder):
    input_image_path = os.path.join(input_folder, filename)
    output_image_path = os.path.join(output_folder, filename)

    try:
        if filename.lower().endswith('.png'):
            # Compress PNG image to target size
            reduce_image_to_target_size(input_image_path, output_image_path, TARGET_SIZE_KB)
        elif filename.lower().endswith(('.jpg', '.jpeg')):
            # Convert JPG to WebP and save to output folder
            webp_output_path = os.path.splitext(output_image_path)[0] + '.webp'
            convert_jpg_to_webp(input_image_path, webp_output_path)
    except Exception as e:
        logging.error(f"Failed to process {filename}: {e}")

logging.info("Image processing completed.")
