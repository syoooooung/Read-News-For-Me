# 기술 뉴스 요약 및 관점 정리 에이전트 (read-news-for-me)

CrewAI를 활용한 AI 기술 뉴스 분석 API 서버입니다. GeekNews, Hacker News, PyTorch 블로그 등 주요 기술 커뮤니티에서 주어진 주제에 대한 최신 글을 자동으로 수집하고, 핵심 내용을 요약하며, 다양한 관점을 분석합니다.

**카카오톡 챗봇 연동 가능**

## 특징

### 🤖 3개의 전문 AI 에이전트

1. **Researcher (기술 뉴스 수집가)**: GeekNews, Hacker News, PyTorch 블로그에서 주제 관련 최신 글 수집
2. **Summarizer (요약 전문가)**: 수집된 글들을 분석하여 핵심 내용을 5줄로 요약
3. **Analyst (심층 분석가)**: 주요 쟁점 3가지와 서로 다른 관점 2가지를 도출

### 🌐 자동 웹 스크래핑

- **GeekNews** (https://news.hada.io/)
- **Hacker News** (https://news.ycombinator.com/)
- **PyTorch Blog** (https://pytorch.org/blog/)

### 📊 출력 결과

- **핵심 요약** (5줄)
- **주요 쟁점 3가지**
- **서로 다른 관점 2가지**

결과는 API 응답으로 반환됩니다.

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

**참고**: 기술 뉴스 수집은 웹 스크래핑을 사용하므로 별도의 검색 API 키가 필요하지 않습니다.

#### API 키 발급 방법

- **OpenAI API**: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

## 사용 방법

### API 서버 실행

```bash
# 서버 시작
uv run uvicorn news_analyzer.api:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면 http://localhost:8000 에서 접근 가능합니다.

### API 테스트

```bash
# curl로 테스트
curl -X POST http://localhost:8000/basic \
  -H "Content-Type: application/json" \
  -d '{
    "userRequest": {
      "utterance": "AI 기술"
    }
  }'
```

### 카카오톡 챗봇 연동

1. [카카오 i 오픈빌더](https://i.kakao.com/)에서 챗봇 생성
2. 스킬 서버 URL에 `http://your-server:8000/basic` 입력
3. 챗봇에 주제 입력 시 자동으로 뉴스 분석 실행

자세한 연동 방법은 [카카오톡 챗봇 가이드](https://wikidocs.net/280514) 참고

## 프로젝트 구조

```
read-news-for-me/
├── .env                          # 환경 변수 (생성 필요)
├── .env.example                  # 환경 변수 예시
├── .gitignore                    # Git 제외 파일
├── pyproject.toml                # 프로젝트 설정
├── README.md                     # 이 파일
├── Claude.md                     # CrewAI 가이드
└── src/
    └── news_analyzer/
        ├── __init__.py
        ├── api.py                # FastAPI 서버 (카카오톡 챗봇 연동)
        ├── main.py               # CLI 실행 (옵션)
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

### API 응답 형식 수정

`src/news_analyzer/api.py` 파일을 수정하여 응답 형식을 변경할 수 있습니다. 현재는 카카오톡 챗봇 형식으로 설정되어 있습니다.

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
- **FastAPI**: 고성능 웹 API 프레임워크
- **Uvicorn**: ASGI 서버
- **ScrapeWebsiteTool**: 웹 스크래핑 (API 키 불필요)
- **uv**: 빠른 Python 패키지 관리자

## 수집 대상 사이트

이 프로젝트는 다음 기술 커뮤니티에서 뉴스를 수집합니다:
- GeekNews (https://news.hada.io/)
- Hacker News (https://news.ycombinator.com/)
- PyTorch Blog (https://pytorch.org/blog/)

더 많은 사이트를 추가하려면 `src/news_analyzer/crew.py`의 `TECH_NEWS_SITES` 리스트를 수정하세요.

## 라이선스

MIT License

## 참고 자료

- [CrewAI 공식 문서](https://docs.crewai.com)
- [CrewAI GitHub](https://github.com/crewAIInc/crewAI)
- [CrewAI 예제](https://github.com/crewAIInc/crewAI-examples)
- [카카오톡 챗봇 연동 가이드](https://wikidocs.net/280514)
