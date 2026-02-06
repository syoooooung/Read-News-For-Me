from fastapi import FastAPI, Request
from news_analyzer.crew import NewsAnalyzerCrew

app = FastAPI()

@app.post("/basic")
async def basic(request: Request):
    req_data = await request.json()
    utterance = req_data['userRequest']['utterance']

    # Crew 실행
    inputs = {'topic': utterance}
    result = NewsAnalyzerCrew().crew().kickoff(inputs=inputs)

    # 카카오톡 응답 형식
    return {
        "version": "2.0",
        "template": {
            "outputs": [{
                "simpleText": {
                    "text": str(result)
                }
            }]
        }
    }
