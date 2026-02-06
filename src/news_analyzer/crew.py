# src/news_analyzer/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from typing import List

# 주요 기술 뉴스 사이트 URL
TECH_NEWS_SITES = [
    "https://news.hada.io/",  # GeekNews
    "https://news.ycombinator.com/",  # Hacker News
    "https://pytorch.org/blog/",  # PyTorch Blog
]


@CrewBase
class NewsAnalyzerCrew:
    """뉴스 요약 및 관점 정리 Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        """뉴스 수집 에이전트"""
        # 각 사이트마다 스크래핑 도구 생성
        scrape_tools = [ScrapeWebsiteTool(website_url=url) for url in TECH_NEWS_SITES]

        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            tools=scrape_tools,  # 기술 뉴스 사이트 스크래핑 도구
            max_iter=5  # 도구 호출 최대 5번으로 제한
        )

    @agent
    def summarizer(self) -> Agent:
        """뉴스 요약 에이전트"""
        return Agent(
            config=self.agents_config['summarizer'],
            verbose=True
        )

    @agent
    def analyst(self) -> Agent:
        """관점 분석 에이전트"""
        return Agent(
            config=self.agents_config['analyst'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        """뉴스 수집 태스크"""
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher()
        )

    @task
    def summarize_task(self) -> Task:
        """뉴스 요약 태스크"""
        return Task(
            config=self.tasks_config['summarize_task'],
            agent=self.summarizer()
        )

    @task
    def analyze_task(self) -> Task:
        """관점 분석 태스크"""
        return Task(
            config=self.tasks_config['analyze_task'],
            agent=self.analyst()
        )

    @crew
    def crew(self) -> Crew:
        """뉴스 분석 Crew 생성"""
        return Crew(
            agents=self.agents,  # @agent 데코레이터로 자동 생성됨
            tasks=self.tasks,    # @task 데코레이터로 자동 생성됨
            process=Process.sequential,  # 순차적 실행
            verbose=True,
        )
