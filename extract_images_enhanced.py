#!/usr/bin/env python3
"""
Enhanced image extraction script for markdown files with base64 encoded images.
Supports both individual files and directory scanning.
"""
import re
import base64
import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


def extract_images_from_file(file_path: Path, output_dir: Path) -> List[Tuple[str, str]]:
    """
    Extract base64 images from a markdown file.

    Args:
        file_path: Path to the markdown file
        output_dir: Directory to save extracted images

    Returns:
        List of tuples (image_placeholder, output_filename)
    """
    content = file_path.read_text(encoding='utf-8')

    # Pattern to match: [imageN]: <data:image/png;base64,<base64data>>
    # Also supports: [imageN]: data:image/png;base64,<base64data> (without angle brackets)
    pattern = r'\[(image\d+)\]:\s*<?data:image/(png|svg\+xml);base64,([A-Za-z0-9+/=\n\r]+)>?'
    matches = re.finditer(pattern, content, re.MULTILINE)

    extracted = []
    output_dir.mkdir(parents=True, exist_ok=True)

    for idx, match in enumerate(matches, 1):
        placeholder = match.group(1)  # imageN
        img_format = match.group(2)   # png or svg+xml
        b64_data = match.group(3).replace('\n', '').replace('\r', '')

        # Determine file extension
        ext = 'svg' if img_format == 'svg+xml' else 'png'
        output_filename = f"diagram-{idx}.{ext}"
        output_path = output_dir / output_filename

        try:
            # Decode and save
            img_data = base64.b64decode(b64_data)
            output_path.write_bytes(img_data)
            extracted.append((placeholder, output_filename))
            print(f"✓ Extracted {placeholder} → {output_path}")
        except Exception as e:
            print(f"✗ Failed to extract {placeholder}: {e}")

    return extracted


def main():
    parser = argparse.ArgumentParser(description='Extract base64 images from markdown files')
    parser.add_argument('path', help='File or directory to process')
    parser.add_argument('--output-dir', default='images', help='Output directory for images')
    args = parser.parse_args()

    input_path = Path(args.path)

    if not input_path.exists():
        print(f"Error: {input_path} does not exist")
        return 1

    report = {
        "stats": {
            "total_files": 0,
            "total_images": 0,
            "failed_images": 0,
            "total_size_kb": 0
        },
        "files": {}
    }

    # Process files
    if input_path.is_file():
        files = [input_path]
    else:
        files = list(input_path.glob('**/*.md'))

    for file_path in files:
        if file_path.name.startswith('.'):
            continue

        # Determine output directory
        if input_path.is_file():
            output_dir = Path(args.output_dir)
        else:
            rel_path = file_path.relative_to(input_path)
            output_dir = Path(args.output_dir) / rel_path.parent

        extracted = extract_images_from_file(file_path, output_dir)

        if extracted:
            report["files"][str(file_path)] = extracted
            report["stats"]["total_files"] += 1
            report["stats"]["total_images"] += len(extracted)

            # Calculate total size
            for _, filename in extracted:
                img_path = output_dir / filename
                if img_path.exists():
                    report["stats"]["total_size_kb"] += img_path.stat().st_size / 1024

    # Save report
    report_path = Path('image_extraction_report.json')
    report_path.write_text(json.dumps(report, indent=2))

    print(f"\n{'='*60}")
    print(f"Extraction complete!")
    print(f"Total files: {report['stats']['total_files']}")
    print(f"Total images: {report['stats']['total_images']}")
    print(f"Total size: {report['stats']['total_size_kb']:.2f} KB")
    print(f"Report saved to: {report_path}")
    print(f"{'='*60}")

    return 0


if __name__ == '__main__':
    exit(main())
