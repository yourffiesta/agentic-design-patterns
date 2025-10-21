---
name: Markdown Documentation Converter
description: Convert technical markdown documents to GitHub-compatible format with base64 image extraction, code block formatting, and multi-language translation support. Use this when converting documentation with embedded base64 images, fixing code block formatting issues, or creating translated versions.
---

# Markdown Documentation Converter

## Purpose
Convert technical markdown documentation to GitHub-compatible format with proper image handling, code formatting, and multi-language support.

## When to Use This Skill
- Converting documentation with base64-encoded images to PNG/SVG files
- Fixing table-formatted code blocks to proper code blocks
- Creating Korean translations of technical documentation
- Standardizing markdown formatting for GitHub rendering
- Processing documentation from `original/` folder to production-ready format

## Instructions

### Phase 1: Initial Setup
1. Verify `original/` folder contains source markdown files
2. Create working branch (e.g., `docs-restructure`)
3. Copy original files to root directory with normalized names:
   - `Chapter 1 Original.md` → `Chapter-1-Topic-Name.md`
4. Create image folder structure: `images/chapter1/`, `images/chapter2/`, etc.

### Phase 2: Base64 Image Extraction
1. Search for base64 images in original files:
   ```bash
   grep -r '\[image[0-9]*\]:' original/
   ```

2. Create Python script to extract images:
   ```python
   import re
   import base64
   from pathlib import Path

   def extract_base64_images(markdown_file, output_dir):
       with open(markdown_file, 'r', encoding='utf-8') as f:
           content = f.read()

       # Pattern: [image1]: <data:image/png;base64,DATA>
       pattern = r'\[image(\d+)\]:\s*<data:image/(png|svg\+xml);base64,([^>]+)>'
       matches = re.findall(pattern, content, re.MULTILINE)

       Path(output_dir).mkdir(parents=True, exist_ok=True)

       for image_num, image_type, base64_data in matches:
           ext = 'svg' if image_type == 'svg+xml' else image_type
           filename = f"diagram-{image_num}.{ext}"
           filepath = f"{output_dir}/{filename}"

           image_data = base64.b64decode(base64_data)
           with open(filepath, 'wb') as f:
               f.write(image_data)
   ```

3. Run script with `uv run extract_base64.py`
4. Verify extracted images count

### Phase 3: Markdown Formatting Fixes
1. Find table-formatted code blocks:
   ```bash
   grep -r '^\| .*`' Chapter-*.md
   ```

2. Convert to proper code blocks with language specification:
   - AS-IS: `| `backtick`code`backtick``
   - TO-BE: ` ```python` or ` ```bash`

3. Remove base64 image references:
   ```bash
   sed -i '' '/^\[image[0-9]*\]:.*/d' Chapter-*.md
   ```

4. Update image links from .md to .png:
   - AS-IS: `![Diagram](./images/chapter1/context-engineering.md)`
   - TO-BE: `![Diagram](./images/chapter1/diagram-1.png)`

5. Verify code indentation and line breaks

### Phase 4: Multi-Language Translation
1. Create Korean translation files with `.ko.md` extension:
   - `Chapter-1-Topic.md` → `Chapter-1-Topic.ko.md`

2. Translation guidelines:
   - Keep technical terms in English: LLM, Agent, API, JSON, etc.
   - Preserve all code blocks unchanged
   - Maintain image links and URLs unchanged
   - Keep markdown structure identical
   - Use consistent technical writing tone

3. Update image references in translated files to use .png

### Phase 5: Documentation and Cleanup
1. Update `README.md`:
   - Add language selection section
   - Link both English and Korean versions

2. Delete old Mermaid .md files:
   ```bash
   find images -name "*.md" -type f -delete
   ```

3. Update formatting guide with new procedures
4. Prepare commit message

## Validation Commands

### Check table-formatted code blocks
```bash
grep -Hn '^\| .*`' Chapter-*.md | wc -l
```

### Verify base64 removal
```bash
grep -r '^\[image[0-9]*\]:' Chapter-*.md
```

### Count extracted images
```bash
find images -name "*.png" | wc -l
```

### Check language files
```bash
ls -1 Chapter-*.ko.md | wc -l
```

## Expected Output Structure
```
project/
├── original/                      # Source files (DO NOT MODIFY)
│   ├── Chapter 1 Original.md
│   └── Chapter 2 Original.md
├── Chapter-1-Topic.md             # English (normalized filename)
├── Chapter-1-Topic.ko.md          # Korean translation
├── images/                        # Extracted images
│   ├── chapter1/
│   │   ├── diagram-1.png
│   │   └── diagram-2.png
│   └── chapter2/
│       └── diagram-1.png
├── README.md                      # With language selection
└── MARKDOWN_FORMATTING_GUIDE.md   # This guide
```

## Common Issues and Solutions

### Issue: Base64 images not found
**Solution**: Check pattern format in original files. May use `<data:image/` or `data:image/` format.

### Issue: Python script fails
**Solution**: Use `uv run script.py` instead of `python script.py`

### Issue: Image links not updating
**Solution**: Verify chapter number matches folder name (chapter1, chapter2, etc.)

### Issue: Code blocks still malformed
**Solution**: Manually review and fix using Edit tool, ensuring proper language tags

## Notes
- Always preserve `original/` folder contents - never modify source files
- Use ISO 639-1 language codes (`.ko.md`, `.ja.md`, etc.)
- Verify image file extensions match actual format (PNG vs SVG)
- Test markdown rendering on GitHub after changes
