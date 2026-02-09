from fastapi import FastAPI, Request, HTTPException
from news_analyzer.crew import NewsAnalyzerCrew
import logging
import threading
import requests as http_requests
from bs4 import BeautifulSoup
from openai import OpenAI

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="기술 뉴스 분석 봇")


def scrape_geeknews_top():
    """GeekNews 상위 1개 기사 스크래핑"""
    resp = http_requests.get(
        "https://news.hada.io/",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=5,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    first_row = soup.select_one(".topic_row")
    if not first_row:
        return None

    title_tag = first_row.select_one(".topictitle h1")
    link_tag = first_row.select_one(".topictitle a")
    desc_tag = first_row.select_one(".topicdesc a")
    points_tag = first_row.select_one(".topicinfo span[id^=tp]")

    # topic?id=XXXXX 에서 id 추출
    topic_href = desc_tag.get("href", "") if desc_tag else ""
    topic_id = topic_href.split("id=")[-1] if "id=" in topic_href else ""

    return {
        "title": title_tag.get_text(strip=True) if title_tag else "",
        "link": link_tag.get("href", "") if link_tag else "",
        "description": desc_tag.get_text(strip=True) if desc_tag else "",
        "points": points_tag.get_text(strip=True) if points_tag else "0",
        "topic_id": topic_id,
    }


def scrape_geeknews_detail(topic_id: str) -> str:
    """GeekNews 상세 페이지에서 본문 내용 스크래핑"""
    resp = http_requests.get(
        f"https://news.hada.io/topic?id={topic_id}",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=5,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    contents = soup.select_one("#topic_contents")
    if not contents:
        return ""
    return contents.get_text(separator="\n", strip=True)


def analyze_with_llm(article: dict, detail_text: str) -> str:
    """OpenAI API로 기사 분석"""
    client = OpenAI()

    prompt = f"""다음은 GeekNews(긱뉴스) 오늘의 상위 기사입니다. 이 기사를 한국어로 분석해주세요.

제목: {article['title']}
출처: {article['link']}
포인트: {article['points']}

본문 요약:
{detail_text[:3000]}

다음 형식으로 작성해주세요 (총 800자 이내):

[제목]
(제목 그대로)

[요약] (3줄)
- 핵심 내용 1
- 핵심 내용 2
- 핵심 내용 3

[시사점] (2줄)
- 시사점 1
- 시사점 2

[원문 링크]
{article['link']}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 기술 뉴스를 분석하는 전문가입니다. 간결하고 명확하게 한국어로 답변하세요."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=800,
        temperature=0.3,
    )

    return response.choices[0].message.content


def process_and_callback(callback_url: str):
    """백그라운드에서 분석 후 콜백 URL로 결과 전송"""
    try:
        article = scrape_geeknews_top()
        if not article:
            result_text = "긱뉴스에서 기사를 가져올 수 없습니다."
        else:
            detail_text = ""
            if article["topic_id"]:
                detail_text = scrape_geeknews_detail(article["topic_id"])

            result_text = analyze_with_llm(article, detail_text)
            if len(result_text) > 1000:
                result_text = result_text[:997] + "..."

        # 콜백 URL로 결과 전송
        callback_response = {
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": result_text
                    }
                }]
            }
        }

        http_requests.post(callback_url, json=callback_response, timeout=5)
        logger.info("Callback sent successfully")

    except Exception as e:
        logger.error(f"Callback processing error: {e}", exc_info=True)
        try:
            error_response = {
                "version": "2.0",
                "template": {
                    "outputs": [{
                        "simpleText": {
                            "text": f"분석 중 오류가 발생했습니다: {str(e)}"
                        }
                    }]
                }
            }
            http_requests.post(callback_url, json=error_response, timeout=5)
        except Exception:
            logger.error("Failed to send error callback", exc_info=True)


@app.get("/")
async def root():
    """헬스 체크 엔드포인트"""
    return {
        "status": "ok",
        "message": "기술 뉴스 분석 봇 API 서버",
        "endpoints": {
            "/basic": "일반 뉴스 분석 (주제 입력)",
            "/geeknews": "오늘의 긱뉴스 TOP 1 분석",
        }
    }


@app.post("/basic")
async def basic(request: Request):
    """카카오톡 챗봇 스킬 엔드포인트"""
    try:
        # 요청 데이터 파싱
        req_data = await request.json()
        logger.info(f"Request received: {req_data}")

        # utterance 추출
        utterance = req_data.get('userRequest', {}).get('utterance', '')

        if not utterance:
            return {
                "version": "2.0",
                "template": {
                    "outputs": [{
                        "simpleText": {
                            "text": "주제를 입력해주세요.\n예: AI 기술, 파이토치, 딥러닝"
                        }
                    }]
                }
            }

        logger.info(f"Processing topic: {utterance}")

        # TODO: 실제 분석은 시간이 너무 오래 걸림 (1-3분)
        # 카카오톡 타임아웃: 5초

        # 임시: 빠른 응답 (연동 테스트용)
        result_text = f"'{utterance}' 주제로 뉴스 분석을 요청하셨습니다.\n\n분석에는 1-3분 정도 소요됩니다.\n현재는 테스트 모드입니다."

        # 실제 분석 (주석 처리)
        # inputs = {'topic': utterance}
        # result = NewsAnalyzerCrew().crew().kickoff(inputs=inputs)
        # result_text = str(result)
        # if len(result_text) > 1000:
        #     result_text = result_text[:997] + "..."

        logger.info(f"Response prepared for: {utterance}")

        # 카카오톡 응답 형식
        response = {
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": result_text
                    }
                }]
            }
        }

        return response

    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return {
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": "잘못된 요청 형식입니다."
                    }
                }]
            }
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return {
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": f"오류가 발생했습니다: {str(e)}\n잠시 후 다시 시도해주세요."
                    }
                }]
            }
        }


@app.post("/geeknews")
async def geeknews(request: Request):
    """오늘의 긱뉴스 분석 엔드포인트"""
    try:
        req_data = await request.json()
        logger.info(f"GeekNews request received: {req_data}")

        # 콜백 URL 확인 (AI 챗봇 콜백 기능이 활성화된 경우)
        callback_url = req_data.get("userRequest", {}).get("callbackUrl")

        if callback_url:
            # 콜백 모드: 즉시 응답 후 백그라운드에서 처리
            logger.info(f"Using callback mode: {callback_url}")
            thread = threading.Thread(
                target=process_and_callback,
                args=(callback_url,),
                daemon=True,
            )
            thread.start()

            return {
                "version": "2.0",
                "useCallback": True,
                "data": {
                    "text": "긱뉴스 분석 중... 잠시만 기다려주세요."
                }
            }

        # 일반 모드: 5초 내 빠른 응답 (스크래핑만, LLM 분석 없음)
        logger.info("Using quick response mode (no callback)")
        article = scrape_geeknews_top()

        if not article:
            result_text = "긱뉴스에서 기사를 가져올 수 없습니다.\n잠시 후 다시 시도해주세요."
        else:
            result_text = (
                f"오늘의 긱뉴스 TOP 1\n\n"
                f"제목: {article['title']}\n\n"
                f"{article['description']}\n\n"
                f"원문: {article['link']}"
            )
            if len(result_text) > 1000:
                result_text = result_text[:997] + "..."

        return {
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": result_text
                    }
                }]
            }
        }

    except Exception as e:
        logger.error(f"GeekNews error: {str(e)}", exc_info=True)
        return {
            "version": "2.0",
            "template": {
                "outputs": [{
                    "simpleText": {
                        "text": f"오류가 발생했습니다: {str(e)}\n잠시 후 다시 시도해주세요."
                    }
                }]
            }
        }
