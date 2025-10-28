---
name: Converting Markdown Documents
description: Converts technical markdown files to GitHub-compatible format. Use when base64 images need extraction, code blocks need formatting fixes, or Korean translations are required. Handles large files automatically.
---

# Converting Markdown Documents

## Purpose
Transform technical markdown documents to GitHub-compatible format with proper image handling, code formatting, and multilingual support.

## When to Use
Use this Skill when working with markdown files that contain:
- Embedded base64 images requiring extraction
- Improperly formatted code blocks in table syntax
- Content needing Korean translation
- Large files (>100MB) requiring split processing
- Documents in `original/` folder needing production formatting

## Workflow

**CRITICAL: Complete All Phases in One Session**
- You MUST complete all 6 phases from start to finish in a single workflow
- Do NOT stop after completing only image extraction or intermediate steps
- Each chapter conversion requires the full workflow: setup → preprocessing (if needed) → image extraction → formatting → translation → cleanup
- Partial completion is considered incomplete work

### Phase 1: Setup and Validation
**Checklist:**
- [ ] Verify source files exist in `original/` folder
- [ ] Create working branch (e.g., `docs-restructure`)
- [ ] Check file sizes - if >100MB, preprocessing required
- [ ] Set up image output structure: `images/chapter1/`, `images/chapter2/`, etc.

### Phase 2: Large File Preprocessing (if needed)
**When:** File size exceeds 100MB

**Actions:**
- [ ] Run `uv run preprocess_large_md.py --file <large_file>`
- [ ] Verify split files created successfully
- [ ] Note image placeholder mappings
- [ ] Proceed with split files individually

See `preprocess_large_md.py` for implementation details.

### Phase 3: Image Extraction
**Checklist:**
- [ ] Scan for base64 images: `grep -r '\[image[0-9]*\]:' original/`
- [ ] Run extraction: `uv run extract_images_enhanced.py --dir original/`
- [ ] Verify extracted image count matches expected
- [ ] Confirm image formats (PNG/SVG) are correct

**Validation:**
```bash
find images -name "*.png" -o -name "*.svg" | wc -l
```

See `extract_images_enhanced.py` for supported patterns and error handling.

### Phase 4: Markdown Formatting
**Checklist:**
- [ ] Identify malformed code blocks: `grep -r '^\| .*`' Chapter-*.md`
- [ ] Convert table-style code to proper code blocks with language tags
- [ ] Remove base64 references: `sed -i '' '/^\[image[0-9]*\]:.*/d' Chapter-*.md`
- [ ] Update image links from `.md` to actual extensions (`.png`, `.svg`)
- [ ] Verify code indentation and line breaks

**Special Case: Single-Column Table Code Blocks**

Some documents use single-column tables to wrap code blocks:
```markdown
| `code content` |
| :---- |
```

These should be converted to standard fenced code blocks:
````markdown
```python
code content
```
````

**Pattern Detection:**
```bash
# Find single-column tables with code content
grep -E '^\| `.*` \|$' Chapter-*.md
# Find table separators (usually follows code tables)
grep -E '^\| :-+ \|$' Chapter-*.md
```

**Conversion Steps:**
1. Identify consecutive lines matching the pattern: `| `code` |` followed by `| :---- |`
2. Extract the code content (remove `| ` prefix, ` |` suffix, and backticks)
3. Determine language (python, bash, json, etc.) from context or content
4. Replace with proper fenced code block using triple backticks
5. Preserve indentation and formatting within code

**Example Transformation:**
Before:
```markdown
| `import os` |
| :---- |
```

After:
````markdown
```python
import os
```
````

**Validation:**
```bash
grep -Hn '^\| .*`' Chapter-*.md | wc -l  # Should return 0
grep -r '^\[image[0-9]*\]:' Chapter-*.md  # Should return nothing
# Verify no orphaned table separators
grep -E '^\| :-+ \|$' Chapter-*.md | wc -l  # Should return 0
```

### Phase 5: Translation (if required)
**Checklist:**
- [ ] Create Korean version with `.ko.md` suffix
- [ ] Follow translation guidelines (preserve technical terms, code blocks, links)
- [ ] Update image references in translated files
- [ ] Maintain identical markdown structure

**Translation Guidelines:**
- Keep technical terms in English (LLM, Agent, API, JSON)
- Never modify code blocks or image URLs
- Preserve markdown formatting exactly
- Use consistent technical documentation tone

**Validation:**
```bash
ls -1 Chapter-*.ko.md | wc -l  # Should match number of English files
```

### Phase 6: Documentation and Cleanup
**Checklist:**
- [ ] Update `README.md` with language selection section
- [ ] Add links to both English and Korean versions
- [ ] Remove obsolete Mermaid `.md` files: `find images -name "*.md" -type f -delete`
- [ ] Test rendering on GitHub
- [ ] Prepare commit messages

## Expected Output Structure
```
project/
├── original/                      # Source files (never modify)
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
├── preprocess_large_md.py         # Large file preprocessing
└── extract_images_enhanced.py     # Enhanced image extraction
```

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Base64 images not found | Check pattern formats in original files: `<data:image/` or `data:image/` |
| Python script failures | Use `uv run script.py` instead of `python script.py` |
| Memory errors on large files | Run `preprocess_large_md.py` to split files before processing |
| Image links not updating | Verify chapter numbers match folder names (chapter1, chapter2, etc.) |
| Code blocks still malformed | Manually review with Edit tool, ensure proper language tags |
| Single-column table code blocks | Pattern: `\| \`code\` \|` followed by `\| :---- \|`. Convert to fenced code blocks with triple backticks |
| Table separators remain after conversion | Search for orphaned `\| :---- \|` lines and remove them after converting table-style code blocks |

## Important Notes
- **Never modify** files in `original/` folder - always preserve source
- **ALWAYS complete all 6 phases** - partial work is incomplete work
- Do NOT stop after only extracting images - continue through all phases including translation
- Use ISO 639-1 language codes (`.ko.md`, `.ja.md`)
- Verify image extensions match actual formats (PNG vs SVG)
- Test markdown rendering on GitHub after changes
- Files >100MB should be split before processing
- Each chapter requires BOTH English and Korean versions