---
name: 마크다운 문서 변환하기
description: Base64 이미지 추출, 코드 블록 포맷팅, 다국어 번역을 지원하는 GitHub 호환 마크다운 문서 변환 도구입니다. 임베디드 Base64 이미지가 포함된 문서 변환, 코드 블록 포맷 수정, 번역 버전 생성 시 사용합니다. 대용량 파일은 자동으로 분할 처리합니다.
---

# 마크다운 문서 변환하기

## 목적
적절한 이미지 처리, 코드 포맷팅, 다국어 지원을 통해 기술 마크다운 문서를 GitHub 호환 형식으로 변환합니다.

## 사용 시기
- Base64 인코딩된 이미지를 PNG/SVG 파일로 변환할 때
- 테이블 형식의 코드 블록을 적절한 코드 블록으로 수정할 때
- 기술 문서의 한국어 번역본을 생성할 때
- GitHub 렌더링을 위한 마크다운 포맷 표준화할 때
- `original/` 폴더의 문서를 프로덕션 준비 형식으로 처리할 때
- 대용량 마크다운 파일(100MB 이상)을 처리할 때

## 작업 지침

### 1단계: 초기 설정
1. `original/` 폴더에 소스 마크다운 파일이 있는지 확인
2. 작업 브랜치 생성 (예: `docs-restructure`)
3. 정규화된 이름으로 원본 파일을 루트 디렉토리에 복사:
   - `Chapter 1 Original.md` → `Chapter-1-Topic-Name.md`
4. 이미지 폴더 구조 생성: `images/chapter1/`, `images/chapter2/` 등

### 2단계: 대용량 파일 전처리
대용량 마크다운 파일의 경우 먼저 분할 처리를 수행합니다:

```python
# preprocess_large_md.py
import os
import re
from pathlib import Path

def split_large_markdown(file_path, max_size_mb=50):
    """대용량 마크다운 파일을 처리 가능한 크기로 분할"""
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

    if file_size_mb <= max_size_mb:
        return [file_path]  # 분할 불필요

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Base64 이미지 추출 및 임시 제거
    base64_pattern = r'(\[image\d+\]:\s*<data:image/[^>]+>)'
    images = re.findall(base64_pattern, content)

    # 이미지를 플레이스홀더로 교체
    for idx, img in enumerate(images):
        content = content.replace(img, f'[IMAGE_PLACEHOLDER_{idx}]')

    # 섹션별로 분할 (# 헤더 기준)
    sections = re.split(r'(^#+ .+$)', content, flags=re.MULTILINE)

    # 청크 생성
    chunks = []
    current_chunk = ""
    current_size = 0

    for section in sections:
        section_size = len(section.encode('utf-8'))
        if current_size + section_size > max_size_mb * 1024 * 1024:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = section
            current_size = section_size
        else:
            current_chunk += section
            current_size += section_size

    if current_chunk:
        chunks.append(current_chunk)

    # 분할된 파일 저장
    output_files = []
    base_name = Path(file_path).stem
    for idx, chunk in enumerate(chunks):
        output_file = f"{base_name}_part{idx+1}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
        output_files.append(output_file)

    # 이미지 매핑 파일 생성
    with open(f"{base_name}_images.txt", 'w') as f:
        for idx, img in enumerate(images):
            f.write(f"IMAGE_PLACEHOLDER_{idx}\n{img}\n\n")

    return output_files
```

### 3단계: Base64 이미지 추출
1. 원본 파일에서 Base64 이미지 검색:
   ```bash
   grep -r '\[image[0-9]*\]:' original/
   ```

2. 향상된 이미지 추출 스크립트 실행:
   ```python
   # extract_images_enhanced.py
   import re
   import base64
   import os
   from pathlib import Path
   import argparse

   def extract_base64_images_from_file(markdown_file, output_dir):
       """파일에서 Base64 이미지를 추출하여 실제 이미지 파일로 저장"""

       # 대용량 파일 체크
       file_size_mb = os.path.getsize(markdown_file) / (1024 * 1024)
       if file_size_mb > 100:
           print(f"경고: {markdown_file}은 {file_size_mb:.1f}MB로 큽니다. 분할 처리를 권장합니다.")

       with open(markdown_file, 'r', encoding='utf-8') as f:
           content = f.read()

       # 다양한 패턴 지원
       patterns = [
           r'\[image(\d+)\]:\s*<data:image/(png|svg\+xml|jpeg|jpg);base64,([^>]+)>',
           r'\[image(\d+)\]:\s*data:image/(png|svg\+xml|jpeg|jpg);base64,([^>\s]+)',
           r'!\[.*?\]\(data:image/(png|svg\+xml|jpeg|jpg);base64,([^)]+)\)'
       ]

       all_matches = []
       for pattern in patterns:
           matches = re.findall(pattern, content, re.MULTILINE)
           all_matches.extend(matches)

       if not all_matches:
           print(f"{markdown_file}에서 Base64 이미지를 찾을 수 없습니다")
           return []

       Path(output_dir).mkdir(parents=True, exist_ok=True)
       extracted_images = []

       for match in all_matches:
           if len(match) == 3:
               image_num, image_type, base64_data = match
           else:
               image_type, base64_data = match
               image_num = len(extracted_images) + 1

           ext = 'svg' if 'svg' in image_type else image_type.replace('jpeg', 'jpg')
           filename = f"diagram-{image_num}.{ext}"
           filepath = os.path.join(output_dir, filename)

           try:
               # Base64 데이터 정리
               base64_data = base64_data.strip()
               image_data = base64.b64decode(base64_data)

               with open(filepath, 'wb') as f:
                   f.write(image_data)

               print(f"추출됨: {filepath} ({len(image_data)/1024:.1f}KB)")
               extracted_images.append((f"image{image_num}", filename))
           except Exception as e:
               print(f"image{image_num} 추출 오류: {e}")

       return extracted_images

   def main():
       parser = argparse.ArgumentParser(description='마크다운에서 Base64 이미지 추출')
       parser.add_argument('--file', help='처리할 마크다운 파일')
       parser.add_argument('--dir', help='처리할 디렉토리', default='original/')
       parser.add_argument('--output', help='출력 디렉토리', default='images/')
       args = parser.parse_args()

       if args.file:
           # 단일 파일 처리
           chapter_num = re.search(r'Chapter[\s-]?(\d+)', args.file)
           if chapter_num:
               output_dir = f"{args.output}/chapter{chapter_num.group(1)}"
           else:
               output_dir = args.output

           extract_base64_images_from_file(args.file, output_dir)
       else:
           # 디렉토리 내 모든 파일 처리
           for md_file in Path(args.dir).glob('*.md'):
               chapter_num = re.search(r'Chapter[\s-]?(\d+)', str(md_file))
               if chapter_num:
                   output_dir = f"{args.output}/chapter{chapter_num.group(1)}"
                   print(f"\n처리 중: {md_file}...")
                   images = extract_base64_images_from_file(str(md_file), output_dir)
                   print(f"{output_dir}에 {len(images)}개 이미지 추출됨")

   if __name__ == "__main__":
       main()
   ```

3. `uv run extract_images_enhanced.py --dir original/` 실행
4. 추출된 이미지 개수 확인

### 4단계: 마크다운 포맷 수정
1. 테이블 형식 코드 블록 찾기:
   ```bash
   grep -r '^\| .*`' Chapter-*.md
   ```

2. 언어 지정과 함께 적절한 코드 블록으로 변환:
   - 변경 전: `| `backtick`code`backtick``
   - 변경 후: ` ```python` 또는 ` ```bash`

3. Base64 이미지 참조 제거:
   ```bash
   sed -i '' '/^\[image[0-9]*\]:.*/d' Chapter-*.md
   ```

4. 이미지 링크를 .md에서 .png로 업데이트:
   - 변경 전: `![Diagram](./images/chapter1/context-engineering.md)`
   - 변경 후: `![Diagram](./images/chapter1/diagram-1.png)`

5. 코드 들여쓰기 및 줄바꿈 확인

### 5단계: 다국어 번역
1. `.ko.md` 확장자로 한국어 번역 파일 생성:
   - `Chapter-1-Topic.md` → `Chapter-1-Topic.ko.md`

2. 번역 가이드라인:
   - 기술 용어는 영어 유지: LLM, Agent, API, JSON 등
   - 모든 코드 블록은 변경하지 않음
   - 이미지 링크와 URL은 변경하지 않음
   - 마크다운 구조는 동일하게 유지
   - 일관된 기술 문서 톤 사용

3. 번역된 파일에서 이미지 참조를 .png로 업데이트

### 6단계: 문서화 및 정리
1. `README.md` 업데이트:
   - 언어 선택 섹션 추가
   - 영어 및 한국어 버전 링크 연결

2. 오래된 Mermaid .md 파일 삭제:
   ```bash
   find images -name "*.md" -type f -delete
   ```

3. 새로운 절차로 포맷팅 가이드 업데이트
4. 커밋 메시지 준비

## 검증 명령어

### 테이블 형식 코드 블록 확인
```bash
grep -Hn '^\| .*`' Chapter-*.md | wc -l
```

### Base64 제거 확인
```bash
grep -r '^\[image[0-9]*\]:' Chapter-*.md
```

### 추출된 이미지 개수
```bash
find images -name "*.png" -o -name "*.svg" | wc -l
```

### 언어 파일 확인
```bash
ls -1 Chapter-*.ko.md | wc -l
```

### 파일 크기 확인
```bash
find . -name "*.md" -size +50M -ls
```

## 예상 출력 구조
```
project/
├── original/                      # 소스 파일 (수정 금지)
│   ├── Chapter 1 Original.md
│   └── Chapter 2 Original.md
├── Chapter-1-Topic.md             # 영어 (정규화된 파일명)
├── Chapter-1-Topic.ko.md          # 한국어 번역
├── images/                        # 추출된 이미지
│   ├── chapter1/
│   │   ├── diagram-1.png
│   │   └── diagram-2.png
│   └── chapter2/
│       └── diagram-1.png
├── README.md                      # 언어 선택 포함
├── preprocess_large_md.py         # 대용량 파일 전처리 스크립트
└── extract_images_enhanced.py     # 향상된 이미지 추출 스크립트
```

## 일반적인 문제 및 해결방법

### 문제: Base64 이미지를 찾을 수 없음
**해결**: 원본 파일의 패턴 형식 확인. `<data:image/` 또는 `data:image/` 형식 사용 가능

### 문제: Python 스크립트 실패
**해결**: `python script.py` 대신 `uv run script.py` 사용

### 문제: 대용량 파일로 인한 메모리 오류
**해결**: `preprocess_large_md.py`로 파일을 먼저 분할한 후 처리

### 문제: 이미지 링크가 업데이트되지 않음
**해결**: 챕터 번호가 폴더 이름과 일치하는지 확인 (chapter1, chapter2 등)

### 문제: 코드 블록이 여전히 잘못된 형식
**해결**: Edit 도구를 사용하여 수동으로 검토 및 수정, 적절한 언어 태그 확인

## 참고사항
- `original/` 폴더 내용은 항상 보존 - 소스 파일 수정 금지
- ISO 639-1 언어 코드 사용 (`.ko.md`, `.ja.md` 등)
- 이미지 파일 확장자가 실제 형식과 일치하는지 확인 (PNG vs SVG)
- 변경 후 GitHub에서 마크다운 렌더링 테스트
- 100MB 이상의 파일은 자동으로 분할 처리 권장