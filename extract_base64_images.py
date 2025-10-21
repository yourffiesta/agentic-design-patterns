import re
import base64
import os
from pathlib import Path

def extract_base64_images(markdown_file, output_dir):
    """Extract base64 images from markdown and save as actual image files."""
    
    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all base64 image references
    pattern = r'\[image(\d+)\]:\s*data:image/(png|svg\+xml);base64,([^\s]+)'
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

# Process each chapter
chapters = [
    ("original/Chapter 1 Prompt Chaining.md", "images/chapter1"),
    ("original/Chapter 2 Routing.md", "images/chapter2"),
    ("original/Chapter 3 Parallelization.md", "images/chapter3"),
    ("original/Chapter 4 Reflection.md", "images/chapter4"),
    ("original/Chapter 5 Tool Use.md", "images/chapter5"),
    ("original/Chapter 6 Planning.md", "images/chapter6"),
    ("original/Chapter 7 Multi-Agent Collaboration.md", "images/chapter7"),
]

for markdown_file, output_dir in chapters:
    if os.path.exists(markdown_file):
        print(f"\nProcessing {markdown_file}...")
        images = extract_base64_images(markdown_file, output_dir)
        print(f"Extracted {len(images)} images to {output_dir}")
