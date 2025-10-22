#!/usr/bin/env python3
"""
향상된 Base64 이미지 추출 도구
마크다운 파일에서 다양한 형식의 Base64 이미지를 추출하고 실제 이미지 파일로 저장합니다.
Usage: uv run extract_images_enhanced.py [--file FILE | --dir DIR] [--output OUTPUT]
"""

import re
import base64
import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

class ImageExtractor:
    """Base64 이미지 추출기"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.stats = {
            'total_files': 0,
            'total_images': 0,
            'failed_images': 0,
            'total_size_kb': 0
        }

    def extract_base64_images_from_file(self, markdown_file: str, output_dir: str) -> List[Tuple[str, str]]:
        """파일에서 Base64 이미지를 추출하여 실제 이미지 파일로 저장"""

        # 파일 크기 체크
        file_size_mb = os.path.getsize(markdown_file) / (1024 * 1024)
        if file_size_mb > 100:
            print(f"⚠️  경고: {markdown_file}은 {file_size_mb:.1f}MB로 큽니다.")
            print(f"   먼저 preprocess_large_md.py로 분할 처리를 권장합니다.")

        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 파일 읽기 오류: {e}")
            return []

        # 다양한 Base64 이미지 패턴
        patterns = [
            # [image1]: <data:image/png;base64,DATA> 형식
            (r'\[image(\d+)\]:\s*<data:image/([\w+]+);base64,([^>]+)>', 'reference'),
            # [image1]: data:image/png;base64,DATA 형식 (< > 없음)
            (r'\[image(\d+)\]:\s*data:image/([\w+]+);base64,([^>\s]+)', 'reference_no_brackets'),
            # ![alt](data:image/png;base64,DATA) 인라인 형식
            (r'!\[([^\]]*)\]\(data:image/([\w+]+);base64,([^)]+)\)', 'inline'),
            # <img src="data:image/png;base64,DATA"> HTML 형식
            (r'<img[^>]*src="data:image/([\w+]+);base64,([^"]+)"[^>]*>', 'html'),
            # 플레이스홀더 형식 (분할된 파일용)
            (r'\[IMAGE_PLACEHOLDER_(\d+)\]', 'placeholder')
        ]

        all_matches = []
        image_counter = 1

        for pattern, pattern_type in patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                if pattern_type == 'placeholder':
                    # 플레이스홀더는 나중에 처리
                    continue
                elif pattern_type == 'reference' or pattern_type == 'reference_no_brackets':
                    image_num = match.group(1)
                    image_type = match.group(2)
                    base64_data = match.group(3)
                elif pattern_type == 'inline':
                    alt_text = match.group(1)
                    image_type = match.group(2)
                    base64_data = match.group(3)
                    image_num = str(image_counter)
                    image_counter += 1
                elif pattern_type == 'html':
                    image_type = match.group(1)
                    base64_data = match.group(2)
                    image_num = str(image_counter)
                    image_counter += 1

                all_matches.append({
                    'num': image_num,
                    'type': image_type,
                    'data': base64_data,
                    'pattern_type': pattern_type,
                    'position': match.start()
                })

        if not all_matches:
            if self.verbose:
                print(f"  ℹ️  {markdown_file}에서 Base64 이미지를 찾을 수 없습니다")
            return []

        # 위치 순으로 정렬
        all_matches.sort(key=lambda x: x['position'])

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        extracted_images = []

        print(f"📄 {markdown_file}")
        print(f"   발견된 이미지: {len(all_matches)}개")

        for match in all_matches:
            image_num = match['num']
            image_type = match['type']
            base64_data = match['data']
            pattern_type = match['pattern_type']

            # 파일 확장자 결정
            if 'svg' in image_type:
                ext = 'svg'
            elif 'jpeg' in image_type or 'jpg' in image_type:
                ext = 'jpg'
            elif 'png' in image_type:
                ext = 'png'
            elif 'gif' in image_type:
                ext = 'gif'
            elif 'webp' in image_type:
                ext = 'webp'
            else:
                ext = image_type

            filename = f"diagram-{image_num}.{ext}"
            filepath = os.path.join(output_dir, filename)

            try:
                # Base64 데이터 정리
                base64_data = base64_data.strip()
                # 줄바꿈 제거
                base64_data = base64_data.replace('\n', '').replace('\r', '')

                # Base64 디코딩
                image_data = base64.b64decode(base64_data)

                # 파일 저장
                with open(filepath, 'wb') as f:
                    f.write(image_data)

                size_kb = len(image_data) / 1024
                self.stats['total_size_kb'] += size_kb

                print(f"   ✅ {filename} ({size_kb:.1f}KB) - {pattern_type}")
                extracted_images.append((f"image{image_num}", filename))
                self.stats['total_images'] += 1

            except Exception as e:
                print(f"   ❌ image{image_num} 추출 실패: {str(e)[:50]}")
                self.stats['failed_images'] += 1

        return extracted_images

    def process_directory(self, directory: str, output_base: str = 'images'):
        """디렉토리 내 모든 마크다운 파일 처리"""
        md_files = list(Path(directory).glob('*.md'))

        if not md_files:
            print(f"❌ {directory}에서 마크다운 파일을 찾을 수 없습니다")
            return

        print(f"📁 {directory} 디렉토리 처리")
        print(f"   발견된 마크다운 파일: {len(md_files)}개\n")

        all_results = {}

        for md_file in md_files:
            self.stats['total_files'] += 1

            # 챕터 번호 추출
            chapter_match = re.search(r'Chapter[\s-]?(\d+)', str(md_file))
            if chapter_match:
                chapter_num = chapter_match.group(1)
                output_dir = f"{output_base}/chapter{chapter_num}"
            else:
                # 챕터 번호가 없으면 파일명 기반 폴더
                file_stem = md_file.stem.lower().replace(' ', '-')
                output_dir = f"{output_base}/{file_stem}"

            images = self.extract_base64_images_from_file(str(md_file), output_dir)
            if images:
                all_results[str(md_file)] = images

        self.print_summary(all_results)

    def print_summary(self, results: dict):
        """처리 결과 요약 출력"""
        print("\n" + "=" * 60)
        print("📊 처리 결과 요약")
        print("=" * 60)

        print(f"✅ 처리된 파일: {self.stats['total_files']}개")
        print(f"🖼️  추출된 이미지: {self.stats['total_images']}개")
        print(f"❌ 실패한 이미지: {self.stats['failed_images']}개")
        print(f"💾 총 이미지 크기: {self.stats['total_size_kb']:.1f}KB "
              f"({self.stats['total_size_kb']/1024:.2f}MB)")

        if results and self.verbose:
            print("\n📝 상세 결과:")
            for file, images in results.items():
                if images:
                    print(f"\n{Path(file).name}:")
                    for img_ref, filename in images:
                        print(f"  • {img_ref} → {filename}")

        # 결과를 JSON 파일로 저장
        output_json = "image_extraction_report.json"
        report = {
            'stats': self.stats,
            'files': {file: images for file, images in results.items() if images}
        }

        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n📄 상세 보고서 저장: {output_json}")

def main():
    parser = argparse.ArgumentParser(
        description='향상된 Base64 이미지 추출 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  # 단일 파일 처리
  uv run extract_images_enhanced.py --file Chapter-1.md

  # 디렉토리 처리 (기본: original/)
  uv run extract_images_enhanced.py

  # 특정 디렉토리 처리
  uv run extract_images_enhanced.py --dir docs/

  # 출력 디렉토리 지정
  uv run extract_images_enhanced.py --output extracted_images/

  # 상세 출력 모드
  uv run extract_images_enhanced.py --verbose
        """
    )

    parser.add_argument('--file', help='처리할 단일 마크다운 파일')
    parser.add_argument('--dir', help='처리할 디렉토리', default='original/')
    parser.add_argument('--output', help='이미지를 저장할 기본 디렉토리', default='images/')
    parser.add_argument('--verbose', action='store_true', help='상세 출력 모드')

    args = parser.parse_args()

    extractor = ImageExtractor(verbose=args.verbose)

    if args.file:
        # 단일 파일 처리
        if not os.path.exists(args.file):
            print(f"❌ 파일을 찾을 수 없습니다: {args.file}")
            sys.exit(1)

        # 챕터 번호 추출
        chapter_match = re.search(r'Chapter[\s-]?(\d+)', args.file)
        if chapter_match:
            output_dir = f"{args.output}/chapter{chapter_match.group(1)}"
        else:
            output_dir = args.output

        images = extractor.extract_base64_images_from_file(args.file, output_dir)
        if images:
            extractor.print_summary({args.file: images})
        else:
            print("이미지를 찾을 수 없습니다.")
    else:
        # 디렉토리 처리
        if not os.path.exists(args.dir):
            print(f"❌ 디렉토리를 찾을 수 없습니다: {args.dir}")
            sys.exit(1)

        extractor.process_directory(args.dir, args.output)

if __name__ == "__main__":
    main()