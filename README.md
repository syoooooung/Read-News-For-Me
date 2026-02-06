# 뉴스 요약 및 관점 정리 에이전트 (read-news-for-me)

CrewAI를 활용한 AI 뉴스 분석 시스템입니다. 주어진 주제에 대한 최신 뉴스를 자동으로 수집하고, 핵심 내용을 요약하며, 다양한 관점을 분석합니다.

## 특징

### 🤖 3개의 전문 AI 에이전트

1. **Researcher (뉴스 수집가)**: 주제와 관련된 최신 뉴스 기사를 검색하고 수집
2. **Summarizer (요약 전문가)**: 수집된 기사를 분석하여 핵심 내용을 5줄로 요약
3. **Analyst (심층 분석가)**: 주요 쟁점 3가지와 서로 다른 관점 2가지를 도출

### 📊 출력 결과

- **핵심 요약** (5줄)
- **주요 쟁점 3가지**
- **서로 다른 관점 2가지**

결과는 `news_analysis.md` 파일로 저장됩니다.

## 설치 방법

### 1. 필수 요구사항

- Python 3.10 이상 3.14 미만
- uv (패키지 관리자)

### 2. 프로젝트 설정

```bash
# 저장소 클론 또는 프로젝트 디렉토리로 이동
cd read-news-for-me

# 의존성 설치
uv sync
```

### 3. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 만들고, API 키를 입력합니다:

```bash
cp .env.example .env
```

`.env` 파일을 편집하여 OpenAI API 키를 설정합니다:

```env
# OpenAI API 키 (필수)
OPENAI_API_KEY=sk-your-actual-key-here
```

**참고**: 뉴스 검색은 DuckDuckGo Search를 사용하므로 별도의 API 키가 필요하지 않습니다.

#### API 키 발급 방법

- **OpenAI API**: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

## 사용 방법

### 기본 실행

```bash
# 가상환경 활성화 (자동)
uv run python src/news_analyzer/main.py
```

대화형으로 주제를 입력하라는 메시지가 나타납니다.

### 주제를 인자로 전달

```bash
uv run python src/news_analyzer/main.py "AI 기술 발전"
```

### 실행 예시

```bash
$ uv run python src/news_analyzer/main.py "기후 변화"

============================================================
뉴스 요약 및 관점 정리 에이전트
============================================================

주제: 기후 변화
분석을 시작합니다...

[에이전트들이 작업을 수행합니다...]

============================================================
분석이 완료되었습니다!
============================================================

결과가 'news_analysis.md' 파일에 저장되었습니다.
```

## 프로젝트 구조

```
read-news-for-me/
├── .env                          # 환경 변수 (생성 필요)
├── .env.example                  # 환경 변수 예시
├── .gitignore                    # Git 제외 파일
├── pyproject.toml                # 프로젝트 설정
├── README.md                     # 이 파일
├── Claude.md                     # CrewAI 가이드
├── news_analysis.md              # 출력 결과 (생성됨)
└── src/
    └── news_analyzer/
        ├── __init__.py
        ├── main.py               # 진입점
        ├── crew.py               # Crew 정의
        ├── config/
        │   ├── agents.yaml       # 에이전트 설정
        │   └── tasks.yaml        # 태스크 설정
        └── tools/
            └── __init__.py
```

## 커스터마이징

### 에이전트 수정

`src/news_analyzer/config/agents.yaml` 파일을 수정하여 에이전트의 역할, 목표, 배경 스토리를 변경할 수 있습니다.

### 태스크 수정

`src/news_analyzer/config/tasks.yaml` 파일을 수정하여 각 태스크의 설명과 기대 출력을 조정할 수 있습니다.

### 도구 추가

`src/news_analyzer/tools/` 디렉토리에 커스텀 도구를 추가하고, `crew.py`에서 에이전트에 할당할 수 있습니다.

## 문제 해결

### API 키 관련 오류

환경 변수가 제대로 설정되었는지 확인하세요:

```bash
# .env 파일 확인
cat .env
```

### 의존성 오류

의존성을 다시 설치해보세요:

```bash
uv sync --reinstall
```

## 기술 스택

- **CrewAI**: Multi-agent orchestration framework
- **OpenAI GPT**: LLM (기본 모델)
- **DuckDuckGo Search**: 무료 웹 검색 (API 키 불필요)
- **uv**: 빠른 Python 패키지 관리자

## 라이선스

MIT License

## 참고 자료

- [CrewAI 공식 문서](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [CrewAI 예제](https://github.com/crewAIInc/crewAI-examples)
