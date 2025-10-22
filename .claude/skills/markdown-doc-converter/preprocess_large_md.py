#!/usr/bin/env python3
"""
대용량 마크다운 파일 전처리 도구
Base64 이미지로 인해 크기가 커진 마크다운 파일을 처리 가능한 크기로 분할합니다.
Usage: uv run preprocess_large_md.py <file_path> [--max-size MB]
"""

import os
import re
import sys
import argparse
from pathlib import Path

def split_large_markdown(file_path, max_size_mb=50):
    """대용량 마크다운 파일을 처리 가능한 크기로 분할"""

    if not os.path.exists(file_path):
        print(f"오류: {file_path} 파일을 찾을 수 없습니다.")
        return []

    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"파일 크기: {file_size_mb:.2f}MB")

    if file_size_mb <= max_size_mb:
        print(f"파일 크기가 {max_size_mb}MB 이하입니다. 분할이 필요하지 않습니다.")
        return [file_path]

    print(f"파일이 {max_size_mb}MB보다 큽니다. 분할을 시작합니다...")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Base64 이미지 추출 및 임시 제거
    base64_pattern = r'(\[image\d+\]:\s*<data:image/[^>]+>)'
    images = re.findall(base64_pattern, content)
    print(f"발견된 Base64 이미지: {len(images)}개")

    # 이미지를 플레이스홀더로 교체
    for idx, img in enumerate(images):
        content = content.replace(img, f'[IMAGE_PLACEHOLDER_{idx}]')

    # 섹션별로 분할 (# 헤더 기준)
    sections = re.split(r'(^#+ .+$)', content, flags=re.MULTILINE)

    # 청크 생성
    chunks = []
    current_chunk = ""
    current_size = 0
    max_chunk_size = max_size_mb * 1024 * 1024

    for i, section in enumerate(sections):
        section_size = len(section.encode('utf-8'))

        # 섹션이 최대 크기보다 큰 경우 강제 분할
        if section_size > max_chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
                current_size = 0

            # 큰 섹션을 줄 단위로 분할
            lines = section.split('\n')
            temp_chunk = ""
            temp_size = 0

            for line in lines:
                line_size = len((line + '\n').encode('utf-8'))
                if temp_size + line_size > max_chunk_size:
                    if temp_chunk:
                        chunks.append(temp_chunk)
                    temp_chunk = line + '\n'
                    temp_size = line_size
                else:
                    temp_chunk += line + '\n'
                    temp_size += line_size

            if temp_chunk:
                current_chunk = temp_chunk
                current_size = temp_size
        elif current_size + section_size > max_chunk_size:
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
    base_path = Path(file_path)
    base_name = base_path.stem
    base_dir = base_path.parent

    for idx, chunk in enumerate(chunks):
        output_file = base_dir / f"{base_name}_part{idx+1}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
        output_files.append(str(output_file))
        chunk_size_mb = len(chunk.encode('utf-8')) / (1024 * 1024)
        print(f"생성됨: {output_file} ({chunk_size_mb:.2f}MB)")

    # 이미지 매핑 파일 생성
    if images:
        mapping_file = base_dir / f"{base_name}_images.txt"
        with open(mapping_file, 'w', encoding='utf-8') as f:
            f.write("# Base64 이미지 매핑 파일\n")
            f.write(f"# 원본 파일: {file_path}\n")
            f.write(f"# 총 이미지 수: {len(images)}\n\n")

            for idx, img in enumerate(images):
                f.write(f"=== IMAGE_PLACEHOLDER_{idx} ===\n")
                # 이미지 타입 추출
                img_type_match = re.search(r'data:image/([\w+]+);', img)
                if img_type_match:
                    f.write(f"Type: {img_type_match.group(1)}\n")
                f.write(f"Size: {len(img)} characters\n")
                f.write("Original:\n")
                f.write(img[:200] + "...[truncated]" if len(img) > 200 else img)
                f.write("\n\n")

        print(f"이미지 매핑 파일 생성: {mapping_file}")

    print(f"\n분할 완료: {len(chunks)}개 파일 생성")
    return output_files

def reassemble_markdown(base_file_path):
    """분할된 마크다운 파일을 다시 합치기"""
    base_path = Path(base_file_path)
    base_name = base_path.stem.replace('_part1', '')
    base_dir = base_path.parent

    # 모든 파트 파일 찾기
    part_files = sorted(base_dir.glob(f"{base_name}_part*.md"))

    if not part_files:
        print(f"분할된 파일을 찾을 수 없습니다: {base_name}_part*.md")
        return None

    print(f"발견된 파트 파일: {len(part_files)}개")

    # 이미지 매핑 파일 읽기
    mapping_file = base_dir / f"{base_name}_images.txt"
    image_mapping = {}

    if mapping_file.exists():
        with open(mapping_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 간단한 파싱 (실제 구현시 더 정교하게)
            placeholders = re.findall(r'=== (IMAGE_PLACEHOLDER_\d+) ===', content)
            print(f"이미지 플레이스홀더 발견: {len(placeholders)}개")

    # 파트 파일들 합치기
    combined_content = ""
    for part_file in part_files:
        with open(part_file, 'r', encoding='utf-8') as f:
            combined_content += f.read()

    # 출력 파일 저장
    output_file = base_dir / f"{base_name}_reassembled.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(combined_content)

    print(f"재조립 완료: {output_file}")
    return str(output_file)

def main():
    parser = argparse.ArgumentParser(
        description='대용량 마크다운 파일 전처리 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  # 파일 분할 (기본 50MB)
  uv run preprocess_large_md.py large_file.md

  # 파일 분할 (사용자 지정 크기)
  uv run preprocess_large_md.py large_file.md --max-size 30

  # 파일 재조립
  uv run preprocess_large_md.py large_file_part1.md --reassemble
        """
    )

    parser.add_argument('file_path', help='처리할 마크다운 파일 경로')
    parser.add_argument('--max-size', type=int, default=50,
                       help='최대 파일 크기 (MB, 기본값: 50)')
    parser.add_argument('--reassemble', action='store_true',
                       help='분할된 파일을 다시 합치기')

    args = parser.parse_args()

    if args.reassemble:
        result = reassemble_markdown(args.file_path)
        if result:
            print(f"✅ 재조립 성공: {result}")
        else:
            print("❌ 재조립 실패")
            sys.exit(1)
    else:
        result = split_large_markdown(args.file_path, args.max_size)
        if result:
            print(f"✅ 처리 완료")
            print(f"결과 파일: {', '.join(result)}")
        else:
            print("❌ 처리 실패")
            sys.exit(1)

if __name__ == "__main__":
    main()