from PIL import Image
import os
import io

# Define input and output folders
input_folder = r'D:\Webp'
output_folder = r'D:\Webp\Output'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Define target size in KB
TARGET_SIZE_KB = 20

# Function to optimize image for web with a specific file size target
def reduce_image_to_target_size(input_image_path, output_image_path, target_size_kb=TARGET_SIZE_KB):
    with Image.open(input_image_path) as img:
        img_format = 'PNG' if img.mode in ('RGBA', 'LA', 'P') else 'WEBP'

        # Check if original image is under target size
        with io.BytesIO() as output:
            img.save(output, format=img_format, optimize=True)
            size_kb = output.tell() / 1024
            if size_kb <= target_size_kb:
                # Save the original image
                with open(output_image_path, 'wb') as f:
                    f.write(output.getvalue())
                print(f"{os.path.basename(input_image_path)}: Already under target size. Kept the original.")
                return

        # Binary search for optimal quality
        quality_min = 10
        quality_max = 90
        best_quality = quality_min
        best_output = None

        while quality_min <= quality_max:
            quality = (quality_min + quality_max) // 2

            with io.BytesIO() as output:
                img.save(output, format=img_format, quality=quality, optimize=True)
                size_kb = output.tell() / 1024

            if size_kb <= target_size_kb:
                best_quality = quality
                best_output = output.getvalue()
                quality_min = quality + 1
            else:
                quality_max = quality - 1

        if best_output:
            # Save the best quality image under target size
            with open(output_image_path, 'wb') as f:
                f.write(best_output)
            print(f"{os.path.basename(input_image_path)}: Compressed to {size_kb:.2f} KB at quality {best_quality}.")
            return

        # If quality adjustment isn't enough, adjust resize factor
        resize_factor_min = 0.1
        resize_factor_max = 1.0
        best_resize_factor = resize_factor_min
        best_output = None

        while resize_factor_max - resize_factor_min > 0.01:
            resize_factor = (resize_factor_min + resize_factor_max) / 2
            new_size = (int(img.width * resize_factor), int(img.height * resize_factor))
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS)

            with io.BytesIO() as output:
                img_resized.save(output, format=img_format, quality=best_quality, optimize=True)
                size_kb = output.tell() / 1024

            if size_kb <= target_size_kb:
                best_resize_factor = resize_factor
                best_output = output.getvalue()
                resize_factor_min = resize_factor
            else:
                resize_factor_max = resize_factor

        if best_output:
            # Save the resized image under target size
            with open(output_image_path, 'wb') as f:
                f.write(best_output)
            print(f"{os.path.basename(input_image_path)}: Resized and compressed to {size_kb:.2f} KB.")
        else:
            # Save with lowest quality and smallest size if all else fails
            new_size = (int(img.width * resize_factor_min), int(img.height * resize_factor_min))
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
            with io.BytesIO() as output:
                img_resized.save(output, format=img_format, quality=10, optimize=True)
                size_kb = output.tell() / 1024
                with open(output_image_path, 'wb') as f:
                    f.write(output.getvalue())
            print(f"{os.path.basename(input_image_path)}: Could not meet target size. Saved at lowest quality and size ({size_kb:.2f} KB).")

# Function to convert JPG to WebP for website optimization
def convert_jpg_to_webp(input_image_path, output_image_path, quality=80, max_dimensions=(1920, 1080)):
    with Image.open(input_image_path) as img:
        # Resize image if it's larger than the max dimensions while keeping aspect ratio
        img.thumbnail(max_dimensions, Image.Resampling.LANCZOS)

        # Convert to RGB (if not already) and save as WebP
        img.convert('RGB').save(output_image_path, 'WEBP', quality=quality, optimize=True)
        print(f"Converted {os.path.basename(input_image_path)} to WebP and saved as {output_image_path}.")

# Iterate over all files in the input folder
for filename in os.listdir(input_folder):
    input_image_path = os.path.join(input_folder, filename)
    output_image_path = os.path.join(output_folder, filename)

    if filename.lower().endswith('.png'):
        # Reduce PNG image to target size and save to output folder
        reduce_image_to_target_size(input_image_path, output_image_path)
    elif filename.lower().endswith(('.jpg', '.jpeg')):
        # Convert JPG to WebP and save to output folder
        webp_output_path = os.path.splitext(output_image_path)[0] + '.webp'
        convert_jpg_to_webp(input_image_path, webp_output_path)

print("Image processing completed.")
