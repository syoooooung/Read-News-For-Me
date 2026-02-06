#!/usr/bin/env python
# src/news_analyzer/main.py
import sys
from news_analyzer.crew import NewsAnalyzerCrew


def run():
    """
    뉴스 분석 Crew를 실행합니다.
    """
    # 사용자 입력 받기
    print("=" * 60)
    print("뉴스 요약 및 관점 정리 에이전트")
    print("=" * 60)

    if len(sys.argv) > 1:
        # 커맨드 라인 인자로 주제 전달
        topic = ' '.join(sys.argv[1:])
    else:
        # 대화형 입력
        topic = input("\n분석할 뉴스 주제나 키워드를 입력하세요: ").strip()

        if not topic:
            print("주제를 입력하지 않았습니다. 기본 주제 'AI 기술'을 사용합니다.")
            topic = "AI 기술"

    print(f"\n주제: {topic}")
    print("분석을 시작합니다...\n")

    # Crew 실행
    inputs = {
        'topic': topic
    }

    try:
        result = NewsAnalyzerCrew().crew().kickoff(inputs=inputs)

        print("\n" + "=" * 60)
        print("분석이 완료되었습니다!")
        print("=" * 60)
        print("\n결과가 'news_analysis.md' 파일에 저장되었습니다.")

        return result

    except Exception as e:
        print(f"\n오류가 발생했습니다: {str(e)}")
        print("\n환경 변수를 확인해주세요:")
        print("  - OPENAI_API_KEY: OpenAI API 키")
        sys.exit(1)


def train():
    """
    Crew를 훈련시킵니다 (선택적).
    """
    inputs = {
        'topic': 'AI 기술'
    }
    try:
        NewsAnalyzerCrew().crew().train(
            n_iterations=int(sys.argv[1]) if len(sys.argv) > 1 else 3,
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"훈련 중 오류 발생: {e}")


def replay():
    """
    특정 태스크를 다시 실행합니다 (선택적).
    """
    try:
        NewsAnalyzerCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"재실행 중 오류 발생: {e}")


def test():
    """
    Crew를 테스트합니다 (선택적).
    """
    inputs = {
        'topic': 'AI 기술'
    }
    try:
        NewsAnalyzerCrew().crew().test(
            n_iterations=int(sys.argv[1]) if len(sys.argv) > 1 else 3,
            openai_model_name=sys.argv[2] if len(sys.argv) > 2 else 'gpt-4o-mini',
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"테스트 중 오류 발생: {e}")


if __name__ == "__main__":
    run()
