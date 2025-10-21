"""
Template script for extracting base64 images from markdown files
Usage: uv run extract_base64_template.py
"""

import re
import base64
import os
from pathlib import Path

def extract_base64_images(markdown_file, output_dir):
    """Extract base64 images from markdown and save as actual image files."""

    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match: [image1]: <data:image/png;base64,DATA>
    pattern = r'\[image(\d+)\]:\s*<data:image/(png|svg\+xml);base64,([^>]+)>'
    matches = re.findall(pattern, content, re.MULTILINE)

    if not matches:
        print(f"No base64 images found in {markdown_file}")
        return []

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    extracted_images = []

    for image_num, image_type, base64_data in matches:
        # Determine file extension
        if image_type == 'svg+xml':
            ext = 'svg'
        else:
            ext = image_type

        # Generate filename
        filename = f"diagram-{image_num}.{ext}"
        filepath = os.path.join(output_dir, filename)

        try:
            # Decode base64 and save to file
            image_data = base64.b64decode(base64_data)
            with open(filepath, 'wb') as f:
                f.write(image_data)

            print(f"Extracted: {filepath}")
            extracted_images.append((f"image{image_num}", filename))
        except Exception as e:
            print(f"Error extracting image{image_num}: {e}")

    return extracted_images

def main():
    """Process chapters - modify this section for your project"""
    chapters = [
        ("original/Chapter 1 Prompt Chaining.md", "images/chapter1"),
        ("original/Chapter 2 Routing.md", "images/chapter2"),
        # Add more chapters as needed
    ]

    all_results = {}
    for markdown_file, output_dir in chapters:
        if os.path.exists(markdown_file):
            print(f"\nProcessing {markdown_file}...")
            images = extract_base64_images(markdown_file, output_dir)
            all_results[markdown_file] = images
            print(f"Extracted {len(images)} images to {output_dir}")

    # Print summary
    print("\n=== Summary ===")
    total_images = 0
    for file, images in all_results.items():
        if images:
            print(f"\n{file}:")
            for img_ref, filename in images:
                print(f"  {img_ref} -> {filename}")
            total_images += len(images)

    print(f"\nTotal images extracted: {total_images}")

if __name__ == "__main__":
    main()
