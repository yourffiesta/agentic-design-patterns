# Chapter 3: Parallelization

# Parallelization Pattern 개요

이전 챕터에서는 순차적 워크플로우를 위한 Prompt Chaining과 동적 의사결정 및 다양한 경로 간 전환을 위한 Routing을 탐구함. 이러한 pattern은 필수적이지만, 많은 복잡한 agentic 작업에는 하나씩이 아니라 *동시에* 실행할 수 있는 여러 sub-task가 포함됨. 여기서 **Parallelization** pattern이 중요해짐.

Parallelization은 LLM 호출, tool 사용 또는 전체 sub-agent와 같은 여러 구성요소를 동시에 실행하는 것을 포함함 (Fig.1 참조). 한 단계가 완료될 때까지 기다린 후 다음 단계를 시작하는 대신, parallel 실행은 독립적인 작업이 동시에 실행되도록 하여 독립적인 부분으로 분해될 수 있는 작업의 전체 실행 시간을 크게 줄임.

주제를 연구하고 결과를 요약하도록 설계된 agent를 고려해보면, 순차적 접근 방식은 다음과 같을 수 있음:

1. Source A를 검색함.
2. Source A를 요약함.
3. Source B를 검색함.
4. Source B를 요약함.
5. 요약 A와 B에서 최종 답변을 합성함.

parallel 접근 방식은 대신 다음과 같을 수 있음:

1. Source A 검색 *및* Source B 검색을 동시에 수행함.
2. 두 검색이 모두 완료되면, Source A 요약 *및* Source B 요약을 동시에 수행함.
3. 요약 A와 B에서 최종 답변을 합성함 (이 단계는 일반적으로 순차적이며 parallel 단계가 완료될 때까지 기다림).

핵심 아이디어는 다른 부분의 출력에 의존하지 않는 워크플로우의 부분을 식별하고 parallel로 실행하는 것임. 이는 대기 시간이 있는 외부 서비스(API 또는 데이터베이스)를 다룰 때 특히 효과적이며, 여러 요청을 동시에 발행할 수 있음.

Parallelization을 구현하려면 비동기 실행 또는 multi-threading/multi-processing을 지원하는 프레임워크가 필요한 경우가 많음. 최신 agentic 프레임워크는 비동기 작업을 염두에 두고 설계되어 parallel로 실행할 수 있는 단계를 쉽게 정의할 수 있도록 함.

![Parallelization Flow](./images/chapter3/diagram-1.png)

Fig.1. Sub-agent를 사용한 parallelization 예제

LangChain, LangGraph, Google ADK와 같은 프레임워크는 parallel 실행을 위한 메커니즘을 제공함. LangChain Expression Language (LCEL)에서는 | (순차용)와 같은 연산자를 사용하여 runnable 객체를 결합하고 동시에 실행되는 branch를 갖도록 chain 또는 그래프를 구조화하여 parallel 실행을 달성할 수 있음. 그래프 구조를 가진 LangGraph는 단일 상태 전환에서 실행할 수 있는 여러 노드를 정의할 수 있도록 하여 워크플로우에서 parallel branch를 효과적으로 활성화함. Google ADK는 복잡한 multi-agent 시스템의 효율성과 확장성을 크게 향상시키는 agent의 parallel 실행을 촉진하고 관리하는 강력하고 기본적인 메커니즘을 제공함. ADK 프레임워크 내의 이러한 고유 기능을 통해 개발자는 여러 agent가 순차적이 아닌 동시에 작동할 수 있는 솔루션을 설계하고 구현할 수 있음.

Parallelization pattern은 특히 여러 독립적인 조회, 계산 또는 외부 서비스와의 상호작용을 포함하는 작업을 처리할 때 agentic 시스템의 효율성과 응답성을 개선하는 데 필수적임. 복잡한 agent 워크플로우의 성능을 최적화하는 핵심 기법임.

# 실용적 응용 사례

Parallelization은 다양한 애플리케이션에서 agent 성능을 최적화하는 강력한 pattern임:

1\. 정보 수집 및 연구:
여러 소스에서 동시에 정보를 수집하는 것은 고전적인 사용 사례임.

* **사용 사례:** 회사를 연구하는 agent.
  * **Parallel 작업:** 뉴스 기사 검색, 주식 데이터 가져오기, 소셜 미디어 언급 확인, 회사 데이터베이스 쿼리를 모두 동시에 수행함.
  * **이점:** 순차 조회보다 훨씬 빠르게 포괄적인 뷰를 수집함.

2\. 데이터 처리 및 분석:
다양한 분석 기법을 적용하거나 다양한 데이터 세그먼트를 동시에 처리함.

* **사용 사례:** 고객 피드백을 분석하는 agent.
  * **Parallel 작업:** 감정 분석 실행, 키워드 추출, 피드백 분류, 긴급 문제 식별을 피드백 항목 배치 전체에 걸쳐 동시에 수행함.
  * **이점:** 다각적인 분석을 빠르게 제공함.

3\. Multi-API 또는 Tool 상호작용:
여러 독립적인 API 또는 tool을 호출하여 다양한 유형의 정보를 수집하거나 다양한 작업을 수행함.

* **사용 사례:** 여행 계획 agent.
  * **Parallel 작업:** 항공편 가격 확인, 호텔 가용성 검색, 지역 이벤트 조회, 레스토랑 추천 찾기를 동시에 수행함.
  * **이점:** 완전한 여행 계획을 더 빠르게 제시함.

4\. 여러 구성요소를 사용한 콘텐츠 생성:
복잡한 콘텐츠의 다양한 부분을 parallel로 생성함.

* **사용 사례:** 마케팅 이메일을 만드는 agent.
  * **Parallel 작업:** 제목 생성, 이메일 본문 초안 작성, 관련 이미지 찾기, 행동 유도 버튼 텍스트 생성을 동시에 수행함.
  * **이점:** 최종 이메일을 더 효율적으로 조립함.

5\. 검증 및 확인:
여러 독립적인 확인 또는 검증을 동시에 수행함.

* **사용 사례:** 사용자 입력을 확인하는 agent.
  * **Parallel 작업:** 이메일 형식 확인, 전화번호 검증, 데이터베이스에 대해 주소 확인, 욕설 확인을 동시에 수행함.
  * **이점:** 입력 유효성에 대한 더 빠른 피드백을 제공함.

6\. Multi-Modal 처리:
동일한 입력의 다양한 modality (텍스트, 이미지, 오디오)를 동시에 처리함.

* **사용 사례:** 텍스트와 이미지가 있는 소셜 미디어 게시물을 분석하는 agent.
  * **Parallel 작업:** 감정 및 키워드에 대한 텍스트 분석 *및* 객체 및 장면 설명에 대한 이미지 분석을 동시에 수행함.
  * **이점:** 다양한 modality의 인사이트를 더 빠르게 통합함.

7\. A/B 테스팅 또는 여러 옵션 생성:
응답 또는 출력의 여러 변형을 parallel로 생성하여 최상의 옵션을 선택함.

* **사용 사례:** 다양한 창의적 텍스트 옵션을 생성하는 agent.
  * **Parallel 작업:** 약간 다른 prompt 또는 모델을 사용하여 기사의 세 가지 다른 헤드라인을 동시에 생성함.
  * **이점:** 빠른 비교 및 최상의 옵션 선택을 가능하게 함.

Parallelization은 agentic 설계의 기본 최적화 기법으로, 개발자가 독립적인 작업에 대한 동시 실행을 활용하여 더 성능이 뛰어나고 반응성이 높은 애플리케이션을 구축할 수 있도록 함.

# 실습 코드 예제 (LangChain)

LangChain 프레임워크 내의 parallel 실행은 LangChain Expression Language (LCEL)에 의해 촉진됨. 주요 방법은 dictionary 또는 list 구조 내에서 여러 runnable 구성요소를 구조화하는 것을 포함함. 이 컬렉션이 chain의 후속 구성요소에 입력으로 전달되면, LCEL 런타임은 포함된 runnable을 동시에 실행함.

LangGraph의 맥락에서 이 원칙은 그래프의 토폴로지에 적용됨. Parallel 워크플로우는 직접적인 순차적 의존성이 없는 여러 노드가 단일 공통 노드에서 시작될 수 있도록 그래프를 설계하여 정의됨. 이러한 parallel 경로는 독립적으로 실행되며, 결과가 그래프의 후속 수렴 지점에서 집계될 수 있음.

다음 구현은 LangChain 프레임워크로 구성된 parallel 처리 워크플로우를 시연함. 이 워크플로우는 단일 사용자 쿼리에 대한 응답으로 두 개의 독립적인 작업을 동시에 실행하도록 설계됨. 이러한 parallel 프로세스는 별개의 chain 또는 함수로 인스턴스화되며, 각각의 출력은 통합된 결과로 집계됨.

이 구현의 전제 조건에는 langchain, langchain-community 및 langchain-openai와 같은 모델 제공자 라이브러리와 같은 필수 Python 패키지 설치가 포함됨. 또한 인증을 위해 로컬 환경에서 선택한 언어 모델의 유효한 API key를 구성해야 함.

```python
import os
import asyncio
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable, RunnableParallel, RunnablePassthrough

# --- Configuration ---
# Ensure your API key environment variable is set (e.g., OPENAI_API_KEY)
try:
    llm: Optional[ChatOpenAI] = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
except Exception as e:
    print(f"Error initializing language model: {e}")
    llm = None

# --- Define Independent Chains ---
# These three chains represent distinct tasks that can be executed in parallel.
summarize_chain: Runnable = (
    ChatPromptTemplate.from_messages([
        ("system", "Summarize the following topic concisely:"),
        ("user", "{topic}")
    ])
    | llm
    | StrOutputParser()
)

questions_chain: Runnable = (
    ChatPromptTemplate.from_messages([
        ("system", "Generate three interesting questions about the following topic:"),
        ("user", "{topic}")
    ])
    | llm
    | StrOutputParser()
)

terms_chain: Runnable = (
    ChatPromptTemplate.from_messages([
        ("system", "Identify 5-10 key terms from the following topic, separated by commas:"),
        ("user", "{topic}")
    ])
    | llm
    | StrOutputParser()
)

# --- Build the Parallel + Synthesis Chain ---
# 1. Define the block of tasks to run in parallel. The results of these,
#    along with the original topic, will be fed into the next step.
map_chain = RunnableParallel(
    {
        "summary": summarize_chain,
        "questions": questions_chain,
        "key_terms": terms_chain,
        "topic": RunnablePassthrough(),  # Pass the original topic through
    }
)

# 2. Define the final synthesis prompt which will combine the parallel results.
synthesis_prompt = ChatPromptTemplate.from_messages([
    ("system", """Based on the following information:
    Summary: {summary}
    Related Questions: {questions}
    Key Terms: {key_terms}
    Synthesize a comprehensive answer."""),
    ("user", "Original topic: {topic}")
])

# 3. Construct the full chain by piping the parallel results directly
#    into the synthesis prompt, followed by the LLM and output parser.
full_parallel_chain = map_chain | synthesis_prompt | llm | StrOutputParser()

# --- Run the Chain ---
async def run_parallel_example(topic: str) -> None:
    """
    Asynchronously invokes the parallel processing chain with a specific topic
    and prints the synthesized result.
    Args:
        topic: The input topic to be processed by the LangChain chains.
    """
    if not llm:
        print("LLM not initialized. Cannot run example.")
        return

    print(f"\n--- Running Parallel LangChain Example for Topic: '{topic}' ---")
    try:
        # The input to `ainvoke` is the single 'topic' string,
        # then passed to each runnable in the `map_chain`.
        response = await full_parallel_chain.ainvoke(topic)
        print("\n--- Final Response ---")
        print(response)
    except Exception as e:
        print(f"\nAn error occurred during chain execution: {e}")

if __name__ == "__main__":
    test_topic = "The history of space exploration"
    # In Python 3.7+, asyncio.run is the standard way to run an async function.
    asyncio.run(run_parallel_example(test_topic))
```

제공된 Python 코드는 parallel 실행을 활용하여 주어진 주제를 효율적으로 처리하도록 설계된 LangChain 애플리케이션을 구현함. asyncio는 parallelism이 아닌 concurrency를 제공한다는 점에 유의해야 함. 한 작업이 유휴 상태(예: 네트워크 요청 대기)일 때 작업 간 지능적으로 전환하는 이벤트 루프를 사용하여 단일 스레드에서 이를 달성함. 이렇게 하면 여러 작업이 동시에 진행되는 효과가 생기지만, 코드 자체는 여전히 하나의 스레드에서만 실행되며 Python의 Global Interpreter Lock (GIL)에 의해 제약됨.

코드는 언어 모델, prompt, 출력 구문 분석 및 runnable 구조를 위한 구성요소를 포함하여 langchain_openai 및 langchain_core에서 필수 모듈을 가져오는 것으로 시작함. 코드는 창의성을 제어하기 위해 지정된 temperature로 특히 "gpt-4o-mini" 모델을 사용하여 ChatOpenAI 인스턴스를 초기화하려고 시도함. 언어 모델 초기화 중 견고성을 위해 try-except 블록이 사용됨. 그런 다음 각각 입력 주제에 대한 별개의 작업을 수행하도록 설계된 세 개의 독립적인 LangChain "chain"이 정의됨. 첫 번째 chain은 시스템 메시지와 주제 자리 표시자가 포함된 사용자 메시지를 사용하여 주제를 간결하게 요약하기 위한 것임. 두 번째 chain은 주제와 관련된 세 가지 흥미로운 질문을 생성하도록 구성됨. 세 번째 chain은 입력 주제에서 5~10개의 핵심 용어를 식별하도록 설정되어 쉼표로 구분하도록 요청함. 이러한 각 독립적인 chain은 특정 작업에 맞춤화된 ChatPromptTemplate과 초기화된 언어 모델, 출력을 문자열로 포맷하는 StrOutputParser로 구성됨.

그런 다음 이러한 세 가지 chain을 번들로 묶어 동시에 실행할 수 있도록 RunnableParallel 블록이 구성됨. 이 parallel runnable에는 원래 입력 주제가 후속 단계에서 사용할 수 있도록 하는 RunnablePassthrough도 포함됨. 최종 합성 단계에 대해 요약, 질문, 핵심 용어 및 원래 주제를 입력으로 사용하여 포괄적인 답변을 생성하는 별도의 ChatPromptTemplate이 정의됨. full_parallel_chain이라는 전체 엔드투엔드 처리 chain은 map_chain (parallel 블록)을 합성 prompt로 시퀀싱하고 언어 모델과 출력 파서를 뒤따라 생성됨. 이 full_parallel_chain을 호출하는 방법을 시연하기 위해 비동기 함수 run_parallel_example이 제공됨. 이 함수는 주제를 입력으로 받아 invoke를 사용하여 비동기 chain을 실행함. 마지막으로 표준 Python if __name__ == "__main__": 블록은 asyncio.run을 사용하여 비동기 실행을 관리하는 샘플 주제(이 경우 "The history of space exploration")로 run_parallel_example을 실행하는 방법을 보여줌.

본질적으로 이 코드는 주어진 주제에 대해 여러 LLM 호출(요약, 질문, 용어)이 동시에 발생하는 워크플로우를 설정하고, 결과가 최종 LLM 호출로 결합됨. 이는 LangChain을 사용하는 agentic 워크플로우에서 parallelization의 핵심 아이디어를 보여줌.

# 실습 코드 예제 (Google ADK)

이제 Google ADK 프레임워크 내에서 이러한 개념을 설명하는 구체적인 예제를 살펴보겠음. ParallelAgent 및 SequentialAgent와 같은 ADK 기본 요소가 향상된 효율성을 위해 동시 실행을 활용하는 agent 흐름을 구축하는 데 어떻게 적용될 수 있는지 검토할 것임.

```python
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

GEMINI_MODEL="gemini-2.0-flash"

# --- 1. Define Researcher Sub-Agents (to run in parallel) ---

# Researcher 1: Renewable Energy
researcher_agent_1 = LlmAgent(
    name="RenewableEnergyResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in energy.
Research the latest advancements in 'renewable energy sources'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
""",
    description="Researches renewable energy sources.",
    tools=[google_search],
    # Store result in state for the merger agent
    output_key="renewable_energy_result"
)

# Researcher 2: Electric Vehicles
researcher_agent_2 = LlmAgent(
    name="EVResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in transportation.
Research the latest developments in 'electric vehicle technology'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
""",
    description="Researches electric vehicle technology.",
    tools=[google_search],
    # Store result in state for the merger agent
    output_key="ev_technology_result"
)

# Researcher 3: Carbon Capture
researcher_agent_3 = LlmAgent(
    name="CarbonCaptureResearcher",
    model=GEMINI_MODEL,
    instruction="""You are an AI Research Assistant specializing in climate solutions.
Research the current state of 'carbon capture methods'.
Use the Google Search tool provided.
Summarize your key findings concisely (1-2 sentences).
Output *only* the summary.
""",
    description="Researches carbon capture methods.",
    tools=[google_search],
    # Store result in state for the merger agent
    output_key="carbon_capture_result"
)

# --- 2. Create the ParallelAgent (Runs researchers concurrently) ---
# This agent orchestrates the concurrent execution of the researchers.
# It finishes once all researchers have completed and stored their results in state.
parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[researcher_agent_1, researcher_agent_2, researcher_agent_3],
    description="Runs multiple research agents in parallel to gather information."
)

# --- 3. Define the Merger Agent (Runs *after* the parallel agents) ---
# This agent takes the results stored in the session state by the parallel agents
# and synthesizes them into a single, structured response with attributions.
merger_agent = LlmAgent(
    name="SynthesisAgent",
    model=GEMINI_MODEL,  # Or potentially a more powerful model if needed for synthesis
    instruction="""You are an AI Assistant responsible for combining research findings into a structured report.
Your primary task is to synthesize the following research summaries, clearly attributing findings to their source areas.
Structure your response using headings for each topic. Ensure the report is coherent and integrates the key points smoothly.

**Crucially: Your entire response MUST be grounded *exclusively* on the information provided in the 'Input Summaries' below. Do NOT add any external knowledge, facts, or details not present in these specific summaries.**

**Input Summaries:**
*   **Renewable Energy:**
    {renewable_energy_result}
*   **Electric Vehicles:**
    {ev_technology_result}
*   **Carbon Capture:**
    {carbon_capture_result}

**Output Format:**

## Summary of Recent Sustainable Technology Advancements

### Renewable Energy Findings (Based on RenewableEnergyResearcher's findings)
[Synthesize and elaborate *only* on the renewable energy input summary provided above.]

### Electric Vehicle Findings (Based on EVResearcher's findings)
[Synthesize and elaborate *only* on the EV input summary provided above.]

### Carbon Capture Findings (Based on CarbonCaptureResearcher's findings)
[Synthesize and elaborate *only* on the carbon capture input summary provided above.]

### Overall Conclusion
[Provide a brief (1-2 sentence) concluding statement that connects *only* the findings presented above.]

Output *only* the structured report following this format. Do not include introductory or concluding phrases outside this structure, and strictly adhere to using only the provided input summary content.
""",
    description="Combines research findings from parallel agents into a structured, cited report, strictly grounded on provided inputs.",
    # No tools needed for merging
    # No output_key needed here, as its direct response is the final output of the sequence
)

# --- 4. Create the SequentialAgent (Orchestrates the overall flow) ---
# This is the main agent that will be run. It first executes the ParallelAgent
# to populate the state, and then executes the MergerAgent to produce the final output.
sequential_pipeline_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    # Run parallel research first, then merge
    sub_agents=[parallel_research_agent, merger_agent],
    description="Coordinates parallel research and synthesizes the results."
)

root_agent = sequential_pipeline_agent
```

이 코드는 지속 가능한 기술 발전에 대한 정보를 연구하고 합성하는 데 사용되는 multi-agent 시스템을 정의함. 세 개의 LlmAgent 인스턴스를 설정하여 특수화된 연구자 역할을 함. ResearcherAgent_1은 재생 에너지원에 초점을 맞추고, ResearcherAgent_2는 전기 자동차 기술을 연구하며, ResearcherAgent_3는 탄소 포집 방법을 조사함. 각 연구자 agent는 GEMINI_MODEL 및 google_search tool을 사용하도록 구성됨. 결과를 간결하게 요약(1-2문장)하고 output_key를 사용하여 세션 상태에 이러한 요약을 저장하도록 지시받음.

그런 다음 ParallelWebResearchAgent라는 ParallelAgent가 생성되어 이러한 세 연구자 agent를 동시에 실행함. 이를 통해 연구를 parallel로 수행하여 잠재적으로 시간을 절약할 수 있음. ParallelAgent는 모든 sub-agent(연구자)가 완료되고 상태를 채운 후 실행을 완료함.

다음으로 연구 결과를 합성하기 위해 MergerAgent (역시 LlmAgent)가 정의됨. 이 agent는 parallel 연구자가 세션 상태에 저장한 요약을 입력으로 받음. instruction은 출력이 제공된 입력 요약만을 엄격하게 기반으로 해야 하며 외부 지식 추가를 금지함을 강조함. MergerAgent는 결합된 결과를 각 주제에 대한 제목과 간략한 전체 결론이 있는 보고서로 구조화하도록 설계됨.

마지막으로 ResearchAndSynthesisPipeline이라는 SequentialAgent가 생성되어 전체 워크플로우를 조정함. 주요 컨트롤러로서 이 주 agent는 먼저 ParallelAgent를 실행하여 연구를 수행함. ParallelAgent가 완료되면 SequentialAgent는 MergerAgent를 실행하여 수집된 정보를 합성함. sequential_pipeline_agent가 root_agent로 설정되어 이 multi-agent 시스템을 실행하기 위한 진입점을 나타냄. 전체 프로세스는 여러 소스에서 정보를 parallel로 효율적으로 수집한 다음 단일 구조화된 보고서로 결합하도록 설계됨.

# 한눈에 보기

**무엇:** 많은 agentic 워크플로우에는 최종 목표를 달성하기 위해 완료해야 하는 여러 sub-task가 포함됨. 순수하게 순차적인 실행은 각 작업이 이전 작업이 완료될 때까지 기다리는 경우 비효율적이고 느림. 이러한 대기 시간은 다양한 API를 호출하거나 여러 데이터베이스를 쿼리하는 것과 같은 외부 I/O 작업에 의존하는 작업의 경우 중요한 병목 현상이 됨. 동시 실행을 위한 메커니즘이 없으면 총 처리 시간은 모든 개별 작업 기간의 합이 되어 시스템의 전체 성능과 응답성을 저해함.

**왜:** Parallelization pattern은 독립적인 작업의 동시 실행을 가능하게 하여 표준화된 솔루션을 제공함. tool 사용 또는 LLM 호출과 같은 워크플로우의 구성요소를 식별하여 작동하며, 서로의 즉각적인 출력에 의존하지 않음. LangChain 및 Google ADK와 같은 agentic 프레임워크는 이러한 동시 작업을 정의하고 관리하기 위한 내장 구조를 제공함. 예를 들어, 주 프로세스는 parallel로 실행되는 여러 sub-task를 호출하고 다음 단계로 진행하기 전에 모두 완료될 때까지 기다릴 수 있음. 이러한 독립적인 작업을 하나씩이 아닌 동시에 실행함으로써 이 pattern은 총 실행 시간을 대폭 줄임.

**경험 법칙:** 워크플로우에 여러 API에서 데이터 가져오기, 다양한 데이터 청크 처리 또는 나중에 합성하기 위한 여러 콘텐츠 조각 생성과 같이 동시에 실행할 수 있는 여러 독립적인 작업이 포함된 경우 이 pattern을 사용함.

**시각적 요약**

![Parallelization with Agents](./images/chapter3/diagram-2.png)

Fig.2: Parallelization design pattern

# 주요 요점

주요 요점은 다음과 같음:

* Parallelization은 효율성을 개선하기 위해 독립적인 작업을 동시에 실행하는 pattern임.
* 특히 작업에 API 호출과 같은 외부 리소스 대기가 포함될 때 유용함.
* 동시 또는 parallel 아키텍처의 채택은 설계, 디버깅 및 시스템 로깅과 같은 주요 개발 단계에 영향을 미치는 상당한 복잡성과 비용을 도입함.
* LangChain 및 Google ADK와 같은 프레임워크는 parallel 실행을 정의하고 관리하기 위한 내장 지원을 제공함.
* LangChain Expression Language (LCEL)에서 RunnableParallel은 여러 runnable을 나란히 실행하기 위한 핵심 구조임.
* Google ADK는 Coordinator agent의 LLM이 독립적인 sub-task를 식별하고 특수화된 sub-agent에 의한 동시 처리를 트리거하는 LLM-Driven Delegation을 통해 parallel 실행을 촉진할 수 있음.
* Parallelization은 전체 대기 시간을 줄이고 복잡한 작업에 대해 agentic 시스템을 더 반응적으로 만드는 데 도움이 됨.

# 결론

Parallelization pattern은 독립적인 sub-task를 동시에 실행하여 계산 워크플로우를 최적화하는 방법임. 이 접근 방식은 여러 모델 추론 또는 외부 서비스 호출을 포함하는 복잡한 작업에서 특히 전체 대기 시간을 줄임.

프레임워크는 이 pattern을 구현하기 위한 별개의 메커니즘을 제공함. LangChain에서 RunnableParallel과 같은 구조는 여러 처리 chain을 동시에 명시적으로 정의하고 실행하는 데 사용됨. 반면 Google Agent Developer Kit (ADK)와 같은 프레임워크는 주 coordinator 모델이 다양한 sub-task를 동시에 작동할 수 있는 특수화된 agent에 할당하는 multi-agent 위임을 통해 parallelization을 달성할 수 있음.

parallel 처리를 순차(chaining) 및 조건부(routing) 제어 흐름과 통합함으로써 다양하고 복잡한 작업을 효율적으로 관리할 수 있는 정교하고 고성능의 계산 시스템을 구축하는 것이 가능해짐.

# 참고문헌

Parallelization pattern 및 관련 개념에 대한 추가 자료:

1. LangChain Expression Language (LCEL) Documentation (Parallelism): [https://python.langchain.com/docs/concepts/lcel/](https://python.langchain.com/docs/concepts/lcel/)
2. Google Agent Developer Kit (ADK) Documentation (Multi-Agent Systems): [https://google.github.io/adk-docs/agents/multi-agents/](https://google.github.io/adk-docs/agents/multi-agents/)
3. Python asyncio Documentation: [https://docs.python.org/3/library/asyncio.html](https://docs.python.org/3/library/asyncio.html)
