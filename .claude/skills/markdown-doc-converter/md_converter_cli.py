#!/usr/bin/env python3
"""
마크다운 문서 변환 통합 CLI 도구
대용량 파일 처리, 이미지 추출, 포맷 변환 등을 한 번에 처리합니다.
Usage: uv run md_converter_cli.py [command] [options]
"""

import os
import sys
import re
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional

class MarkdownConverter:
    """마크다운 변환 통합 도구"""

    def __init__(self, verbose=False):
        self.verbose = verbose
        self.current_dir = Path.cwd()

    def check_file_size(self, file_path: str) -> float:
        """파일 크기를 MB 단위로 반환"""
        return os.path.getsize(file_path) / (1024 * 1024)

    def run_command(self, cmd: List[str]) -> bool:
        """명령 실행"""
        if self.verbose:
            print(f"실행: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                if self.verbose:
                    print(result.stdout)
                return True
            else:
                print(f"❌ 오류: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 명령 실행 실패: {e}")
            return False

    def process_file(self, file_path: str, max_size_mb: int = 50) -> List[str]:
        """단일 파일 처리"""
        file_path = Path(file_path).resolve()

        if not file_path.exists():
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return []

        print(f"\n📄 처리 중: {file_path.name}")
        file_size = self.check_file_size(file_path)
        print(f"   크기: {file_size:.2f}MB")

        # 1. 대용량 파일 체크 및 분할
        files_to_process = []
        if file_size > max_size_mb:
            print(f"   ⚠️  파일이 {max_size_mb}MB보다 큽니다. 분할 처리를 시작합니다...")

            script_dir = Path(__file__).parent
            preprocess_script = script_dir / "preprocess_large_md.py"

            if not preprocess_script.exists():
                print(f"❌ 전처리 스크립트를 찾을 수 없습니다: {preprocess_script}")
                return []

            cmd = ["uv", "run", str(preprocess_script), str(file_path), "--max-size", str(max_size_mb)]
            if self.run_command(cmd):
                # 분할된 파일 목록 찾기
                base_name = file_path.stem
                part_files = sorted(file_path.parent.glob(f"{base_name}_part*.md"))
                files_to_process = [str(f) for f in part_files]
                print(f"   ✅ {len(files_to_process)}개 파일로 분할됨")
            else:
                return []
        else:
            files_to_process = [str(file_path)]

        # 2. 각 파일에서 이미지 추출
        print("\n🖼️  이미지 추출 시작...")
        script_dir = Path(__file__).parent
        extract_script = script_dir / "extract_images_enhanced.py"

        if not extract_script.exists():
            print(f"❌ 이미지 추출 스크립트를 찾을 수 없습니다: {extract_script}")
            return files_to_process

        for file in files_to_process:
            cmd = ["uv", "run", str(extract_script), "--file", file]
            if self.verbose:
                cmd.append("--verbose")
            self.run_command(cmd)

        # 3. 마크다운 포맷 정리
        print("\n🔧 마크다운 포맷 정리...")
        for file in files_to_process:
            self.clean_markdown_format(file)

        return files_to_process

    def clean_markdown_format(self, file_path: str):
        """마크다운 포맷 정리"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_length = len(content)

            # Base64 이미지 참조 제거
            content = re.sub(r'^\[image\d+\]:\s*<data:image/[^>]+>$', '', content, flags=re.MULTILINE)
            content = re.sub(r'^\[image\d+\]:\s*data:image/[^>\s]+$', '', content, flags=re.MULTILINE)

            # 빈 줄 정리
            content = re.sub(r'\n{3,}', '\n\n', content)

            # 이미지 링크 업데이트 (.md -> .png)
            content = re.sub(r'(\!\[.*?\]\(.*?/.*?)\.md\)', r'\1.png)', content)

            if len(content) < original_length:
                # 백업 생성
                backup_path = f"{file_path}.backup"
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                size_reduction = (original_length - len(content)) / 1024
                print(f"   ✅ {Path(file_path).name} 정리 완료 (-{size_reduction:.1f}KB)")
        except Exception as e:
            print(f"   ❌ 포맷 정리 실패: {e}")

    def process_directory(self, directory: str, max_size_mb: int = 50):
        """디렉토리 내 모든 마크다운 파일 처리"""
        dir_path = Path(directory).resolve()

        if not dir_path.exists():
            print(f"❌ 디렉토리를 찾을 수 없습니다: {dir_path}")
            return

        md_files = list(dir_path.glob("*.md"))
        if not md_files:
            print(f"❌ {dir_path}에서 마크다운 파일을 찾을 수 없습니다")
            return

        print(f"📁 {dir_path} 디렉토리 처리")
        print(f"   발견된 파일: {len(md_files)}개\n")

        all_processed = []
        for md_file in md_files:
            processed = self.process_file(str(md_file), max_size_mb)
            all_processed.extend(processed)

        print("\n" + "=" * 60)
        print("✅ 처리 완료")
        print(f"   총 처리된 파일: {len(all_processed)}개")

    def validate_results(self, directory: str = "."):
        """처리 결과 검증"""
        print("\n🔍 검증 시작...")

        # 테이블 형식 코드 블록 확인
        result = subprocess.run(
            ["grep", "-Hn", r"^\| .*`", "Chapter-*.md"],
            capture_output=True, text=True, cwd=directory
        )
        table_blocks = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        print(f"   테이블 형식 코드 블록: {table_blocks}개")

        # Base64 이미지 잔재 확인
        result = subprocess.run(
            ["grep", "-r", r"^\[image[0-9]*\]:", "Chapter-*.md"],
            capture_output=True, text=True, cwd=directory
        )
        base64_remnants = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        print(f"   Base64 이미지 참조: {base64_remnants}개")

        # 추출된 이미지 개수
        image_count = 0
        images_dir = Path(directory) / "images"
        if images_dir.exists():
            for ext in ["*.png", "*.svg", "*.jpg", "*.gif"]:
                image_count += len(list(images_dir.rglob(ext)))
        print(f"   추출된 이미지: {image_count}개")

        # 한국어 번역 파일
        ko_files = list(Path(directory).glob("Chapter-*.ko.md"))
        print(f"   한국어 번역 파일: {len(ko_files)}개")

        return {
            'table_blocks': table_blocks,
            'base64_remnants': base64_remnants,
            'image_count': image_count,
            'ko_files': len(ko_files)
        }

def main():
    parser = argparse.ArgumentParser(
        description='마크다운 문서 변환 통합 CLI 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
명령어:
  process    마크다운 파일 또는 디렉토리 처리
  validate   처리 결과 검증
  clean      임시 파일 정리

예제:
  # 단일 파일 처리
  uv run md_converter_cli.py process --file Chapter-1.md

  # 디렉토리 처리
  uv run md_converter_cli.py process --dir original/

  # 대용량 파일 처리 (사용자 정의 크기)
  uv run md_converter_cli.py process --file large.md --max-size 30

  # 결과 검증
  uv run md_converter_cli.py validate

  # 상세 출력 모드
  uv run md_converter_cli.py process --dir original/ --verbose
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='명령어')

    # process 명령
    process_parser = subparsers.add_parser('process', help='파일 또는 디렉토리 처리')
    process_parser.add_argument('--file', help='처리할 단일 파일')
    process_parser.add_argument('--dir', help='처리할 디렉토리')
    process_parser.add_argument('--max-size', type=int, default=50,
                               help='최대 파일 크기 (MB, 기본값: 50)')
    process_parser.add_argument('--verbose', action='store_true', help='상세 출력')

    # validate 명령
    validate_parser = subparsers.add_parser('validate', help='처리 결과 검증')
    validate_parser.add_argument('--dir', default='.', help='검증할 디렉토리')

    # clean 명령
    clean_parser = subparsers.add_parser('clean', help='임시 파일 정리')
    clean_parser.add_argument('--dir', default='.', help='정리할 디렉토리')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    converter = MarkdownConverter(verbose=getattr(args, 'verbose', False))

    if args.command == 'process':
        if args.file:
            converter.process_file(args.file, args.max_size)
        elif args.dir:
            converter.process_directory(args.dir, args.max_size)
        else:
            print("❌ --file 또는 --dir 옵션을 지정해주세요")
            sys.exit(1)

    elif args.command == 'validate':
        results = converter.validate_results(args.dir)
        if results['base64_remnants'] > 0 or results['table_blocks'] > 0:
            print("\n⚠️  일부 정리가 필요한 항목이 있습니다")
        else:
            print("\n✅ 모든 검증 통과")

    elif args.command == 'clean':
        # 임시 파일 정리
        dir_path = Path(args.dir)
        temp_files = list(dir_path.glob("*_part*.md"))
        temp_files.extend(dir_path.glob("*_images.txt"))
        temp_files.extend(dir_path.glob("*.backup"))

        if temp_files:
            print(f"🗑️  {len(temp_files)}개 임시 파일 발견")
            for f in temp_files:
                print(f"   삭제: {f.name}")
                f.unlink()
            print("✅ 정리 완료")
        else:
            print("✅ 정리할 임시 파일이 없습니다")

if __name__ == "__main__":
    main()