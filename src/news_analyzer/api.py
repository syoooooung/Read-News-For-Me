from fastapi import FastAPI, Request, HTTPException
from news_analyzer.crew import NewsAnalyzerCrew
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="기술 뉴스 분석 봇")


@app.get("/")
async def root():
    """헬스 체크 엔드포인트"""
    return {
        "status": "ok",
        "message": "기술 뉴스 분석 봇 API 서버",
        "endpoint": "/basic"
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

        # Crew 실행
        inputs = {'topic': utterance}
        result = NewsAnalyzerCrew().crew().kickoff(inputs=inputs)

        # 결과 텍스트 변환 및 길이 제한 (카카오톡 제한: 1000자)
        result_text = str(result)
        if len(result_text) > 1000:
            result_text = result_text[:997] + "..."

        logger.info(f"Analysis completed for: {utterance}")

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
