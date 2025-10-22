# 마크다운 문서 변환 도구

대용량 마크다운 파일을 처리하고 GitHub 호환 형식으로 변환하는 통합 도구입니다.

## 주요 기능

- 🔄 **대용량 파일 자동 분할**: 100MB 이상 파일 자동 처리
- 🖼️ **Base64 이미지 추출**: 임베디드 이미지를 실제 파일로 변환
- 🔧 **포맷 자동 정리**: 코드 블록, 이미지 링크 자동 수정
- 🌏 **다국어 지원**: 한국어 번역 가이드라인 포함
- ✅ **결과 검증**: 처리 결과 자동 검증

## 설치

```bash
# uv가 설치되어 있어야 합니다
pip install uv
```

## 사용법

### 통합 CLI 도구 (권장)

```bash
# 단일 파일 처리
uv run md_converter_cli.py process --file Chapter-1.md

# 디렉토리 전체 처리
uv run md_converter_cli.py process --dir original/

# 대용량 파일 처리 (30MB로 분할)
uv run md_converter_cli.py process --file large.md --max-size 30

# 처리 결과 검증
uv run md_converter_cli.py validate

# 임시 파일 정리
uv run md_converter_cli.py clean
```

### 개별 도구 사용

#### 1. 대용량 파일 전처리

```bash
# 파일 분할 (기본 50MB)
uv run preprocess_large_md.py large_file.md

# 사용자 정의 크기로 분할
uv run preprocess_large_md.py large_file.md --max-size 30

# 분할된 파일 재조립
uv run preprocess_large_md.py large_file_part1.md --reassemble
```

#### 2. 이미지 추출

```bash
# 단일 파일에서 이미지 추출
uv run extract_images_enhanced.py --file Chapter-1.md

# 디렉토리 내 모든 파일 처리
uv run extract_images_enhanced.py --dir original/

# 상세 출력
uv run extract_images_enhanced.py --verbose
```

## 파일 구조

```
markdown-doc-converter/
├── SKILL.md                    # Claude 스킬 정의 (한글)
├── README.md                   # 이 파일
├── md_converter_cli.py         # 통합 CLI 도구
├── preprocess_large_md.py      # 대용량 파일 분할 도구
└── extract_images_enhanced.py  # 이미지 추출 도구
```

## 처리 흐름

1. **파일 크기 확인**: 100MB 이상인 경우 자동 분할
2. **이미지 추출**: Base64 인코딩된 이미지를 PNG/SVG 파일로 변환
3. **포맷 정리**: 불필요한 Base64 참조 제거, 이미지 링크 수정
4. **검증**: 처리 결과 자동 확인

## 지원 형식

### 이미지 패턴
- `[image1]: <data:image/png;base64,DATA>`
- `![alt](data:image/png;base64,DATA)`
- `<img src="data:image/png;base64,DATA">`

### 이미지 형식
- PNG, SVG, JPEG, GIF, WebP

## 문제 해결

### 메모리 오류
→ `--max-size` 옵션으로 더 작은 크기로 분할

### 이미지를 찾을 수 없음
→ `--verbose` 옵션으로 상세 로그 확인

### Python 실행 오류
→ `python` 대신 `uv run` 사용

## 라이선스

이 도구는 Claude 스킬로 제공되며, 프로젝트 내에서 자유롭게 사용 가능합니다.