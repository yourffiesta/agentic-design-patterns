# Chapter 4: Reflection

# Reflection 패턴 개요

앞선 챕터에서 순차 실행을 위한 Chaining, 동적 경로 선택을 위한 Routing, 동시 작업 실행을 위한 Parallelization 등 기본적인 agentic 패턴들을 살펴봄. 이러한 패턴들은 agent가 복잡한 작업을 더 효율적이고 유연하게 수행할 수 있게 함. 하지만 정교한 워크플로우를 갖추고 있어도 agent의 초기 출력이나 계획이 최적이거나 정확하거나 완전하지 않을 수 있음. 여기서 **Reflection** 패턴이 필요함.

Reflection 패턴은 agent가 자신의 작업, 출력 또는 내부 상태를 평가하고 그 평가를 사용하여 성능을 개선하거나 응답을 정제하는 것을 의미함. 일종의 자기 수정 또는 자기 개선 형태로, agent가 피드백, 내부 비평 또는 원하는 기준과의 비교를 기반으로 출력을 반복적으로 개선하거나 접근 방식을 조정할 수 있게 함. Reflection은 때때로 초기 agent의 출력을 분석하는 특정 역할을 가진 별도의 agent에 의해 촉진될 수 있음.

출력이 다음 단계로 직접 전달되는 단순한 순차 체인이나 경로를 선택하는 라우팅과 달리, reflection은 피드백 루프를 도입함. Agent는 단순히 출력을 생성하는 것이 아니라 그 출력(또는 그것을 생성한 프로세스)을 검토하고, 잠재적인 문제나 개선 영역을 식별하며, 그 인사이트를 사용하여 더 나은 버전을 생성하거나 향후 작업을 수정함.

프로세스는 일반적으로 다음을 포함함:

1. **실행:** Agent가 작업을 수행하거나 초기 출력을 생성함.
2. **평가/비평:** Agent가 (다른 LLM 호출이나 규칙 세트를 사용하여) 이전 단계의 결과를 분석함. 이 평가는 사실 정확성, 일관성, 스타일, 완전성, 지시사항 준수 또는 기타 관련 기준을 확인할 수 있음.
3. **Reflection/정제:** 비평을 기반으로 agent가 개선 방법을 결정함. 이는 정제된 출력 생성, 후속 단계의 매개변수 조정 또는 전체 계획 수정을 포함할 수 있음.
4. **반복 (선택적이지만 일반적):** 정제된 출력이나 조정된 접근 방식이 실행되고, 만족스러운 결과가 달성되거나 중단 조건이 충족될 때까지 reflection 프로세스가 반복될 수 있음.

Reflection 패턴의 핵심적이고 매우 효과적인 구현은 프로세스를 Producer와 Critic이라는 두 가지 별개의 논리적 역할로 분리함. 이는 종종 "Generator-Critic" 또는 "Producer-Reviewer" 모델이라고 불림. 단일 agent가 자기 reflection을 수행할 수 있지만, 두 개의 특화된 agent(또는 서로 다른 시스템 프롬프트를 가진 두 개의 별도 LLM 호출)를 사용하면 더 견고하고 편향되지 않은 결과를 얻을 수 있음.

1. Producer Agent: 이 agent의 주요 책임은 작업의 초기 실행을 수행하는 것임. 코드 작성, 블로그 포스트 초안 작성 또는 계획 생성 등 콘텐츠 생성에만 집중함. 초기 프롬프트를 받아 출력의 첫 번째 버전을 생성함.

2. Critic Agent: 이 agent의 유일한 목적은 Producer가 생성한 출력을 평가하는 것임. 다른 지시사항 세트, 종종 별개의 페르소나(예: "당신은 시니어 소프트웨어 엔지니어입니다", "당신은 세심한 팩트체커입니다")가 주어짐. Critic의 지시사항은 사실 정확성, 코드 품질, 스타일 요구사항 또는 완전성과 같은 특정 기준에 대해 Producer의 작업을 분석하도록 안내함. 결함을 찾고, 개선사항을 제안하며, 구조화된 피드백을 제공하도록 설계됨.

이러한 관심사의 분리는 agent가 자신의 작업을 검토할 때 발생하는 "인지 편향"을 방지하기 때문에 강력함. Critic agent는 전적으로 오류와 개선 영역을 찾는 데 전념하면서 새로운 관점으로 출력에 접근함. Critic의 피드백은 Producer agent에게 다시 전달되며, Producer는 이를 가이드로 사용하여 새롭고 정제된 버전의 출력을 생성함. 제공된 LangChain과 ADK 코드 예제는 모두 이 두 agent 모델을 구현함: LangChain 예제는 특정 "reflector_prompt"를 사용하여 critic 페르소나를 생성하고, ADK 예제는 producer와 reviewer agent를 명시적으로 정의함.

Reflection 구현은 종종 이러한 피드백 루프를 포함하도록 agent의 워크플로우를 구조화해야 함. 이는 코드의 반복 루프를 통해 또는 상태 관리와 평가 결과에 기반한 조건부 전환을 지원하는 프레임워크를 사용하여 달성할 수 있음. 단일 평가 및 정제 단계는 LangChain/LangGraph, ADK 또는 Crew.AI 체인 내에서 구현될 수 있지만, 진정한 반복적 reflection은 일반적으로 더 복잡한 오케스트레이션을 필요로 함.

Reflection 패턴은 고품질 출력을 생성하고, 미묘한 작업을 처리하며, 어느 정도의 자기 인식과 적응성을 나타낼 수 있는 agent를 구축하는 데 중요함. Agent를 단순히 지시사항을 실행하는 것을 넘어 더 정교한 형태의 문제 해결과 콘텐츠 생성으로 이동시킴.

Reflection과 목표 설정 및 모니터링(Chapter 11 참조)의 교차점은 주목할 가치가 있음. 목표는 agent의 자기 평가를 위한 궁극적인 벤치마크를 제공하고, 모니터링은 진행 상황을 추적함. 많은 실제 사례에서 Reflection은 모니터링된 피드백을 사용하여 편차를 분석하고 전략을 조정하는 교정 엔진 역할을 함. 이러한 시너지는 agent를 수동적인 실행자에서 목표를 달성하기 위해 적응적으로 작동하는 목적 지향적 시스템으로 전환함.

또한, Reflection 패턴의 효과는 LLM이 대화의 메모리를 유지할 때 크게 향상됨(Chapter 8 참조). 이 대화 히스토리는 평가 단계에 중요한 컨텍스트를 제공하여, agent가 출력을 단독으로 평가하는 것이 아니라 이전 상호작용, 사용자 피드백 및 발전하는 목표를 배경으로 평가할 수 있게 함. 이를 통해 agent가 과거 비평에서 배우고 오류 반복을 피할 수 있음. 메모리가 없으면 각 reflection은 독립적인 이벤트이지만, 메모리가 있으면 reflection은 각 사이클이 이전 사이클을 기반으로 구축되는 누적 프로세스가 되어 더 지능적이고 컨텍스트를 인식하는 정제로 이어짐.

# 실전 응용 사례 및 활용 예시

Reflection 패턴은 출력 품질, 정확성 또는 복잡한 제약조건 준수가 중요한 시나리오에서 가치가 있음:

1. 창작 글쓰기 및 콘텐츠 생성:
생성된 텍스트, 스토리, 시 또는 마케팅 카피 정제.

* **활용 사례:** 블로그 포스트를 작성하는 agent.
  * **Reflection:** 초안을 생성하고, 흐름, 톤, 명확성에 대해 비평한 다음, 비평을 기반으로 재작성함. 포스트가 품질 기준을 충족할 때까지 반복함.
  * **이점:** 더 세련되고 효과적인 콘텐츠 생성.

2. 코드 생성 및 디버깅:
코드 작성, 오류 식별 및 수정.

* **활용 사례:** Python 함수를 작성하는 agent.
  * **Reflection:** 초기 코드를 작성하고, 테스트나 정적 분석을 실행하며, 오류나 비효율성을 식별한 다음, 발견사항을 기반으로 코드를 수정함.
  * **이점:** 더 견고하고 기능적인 코드 생성.

3. 복잡한 문제 해결:
다단계 추론 작업에서 중간 단계나 제안된 솔루션 평가.

* **활용 사례:** 논리 퍼즐을 푸는 agent.
  * **Reflection:** 단계를 제안하고, 그것이 솔루션에 더 가까워지는지 또는 모순을 일으키는지 평가하며, 필요하면 백트래킹하거나 다른 단계를 선택함.
  * **이점:** 복잡한 문제 공간을 탐색하는 agent의 능력 향상.

4. 요약 및 정보 합성:
정확성, 완전성, 간결성을 위한 요약 정제.

* **활용 사례:** 긴 문서를 요약하는 agent.
  * **Reflection:** 초기 요약을 생성하고, 원본 문서의 핵심 포인트와 비교하며, 누락된 정보를 포함하거나 정확성을 개선하도록 요약을 정제함.
  * **이점:** 더 정확하고 포괄적인 요약 생성.

5. 계획 및 전략:
제안된 계획을 평가하고 잠재적 결함이나 개선사항 식별.

* **활용 사례:** 목표를 달성하기 위한 일련의 작업을 계획하는 agent.
  * **Reflection:** 계획을 생성하고, 실행을 시뮬레이션하거나 제약조건에 대한 실행 가능성을 평가하며, 평가를 기반으로 계획을 수정함.
  * **이점:** 더 효과적이고 현실적인 계획 개발.

6. 대화형 Agent:
대화에서 이전 턴을 검토하여 컨텍스트를 유지하고, 오해를 수정하거나 응답 품질을 개선함.

* **활용 사례:** 고객 지원 챗봇.
  * **Reflection:** 사용자 응답 후, 대화 히스토리와 마지막 생성된 메시지를 검토하여 일관성을 보장하고 사용자의 최신 입력을 정확하게 처리함.
  * **이점:** 더 자연스럽고 효과적인 대화로 이어짐.

Reflection은 agentic 시스템에 메타 인지 레이어를 추가하여, 자신의 출력과 프로세스로부터 학습할 수 있게 하고, 더 지능적이고 신뢰할 수 있으며 고품질의 결과를 도출함.

# 실습 코드 예제 (LangChain)

완전한 반복적 reflection 프로세스 구현은 상태 관리와 순환 실행을 위한 메커니즘을 필요로 함. 이는 LangGraph와 같은 그래프 기반 프레임워크나 커스텀 절차적 코드를 통해 기본적으로 처리되지만, 단일 reflection 사이클의 기본 원리는 LCEL(LangChain Expression Language)의 조합 구문을 사용하여 효과적으로 시연될 수 있음.

이 예제는 Langchain 라이브러리와 OpenAI의 GPT-4o 모델을 사용하여 숫자의 계승을 계산하는 Python 함수를 반복적으로 생성하고 정제하는 reflection 루프를 구현함. 프로세스는 작업 프롬프트로 시작하여 초기 코드를 생성한 다음, 시뮬레이션된 시니어 소프트웨어 엔지니어 역할의 비평을 기반으로 코드를 반복적으로 reflection하고, 비평 단계가 코드가 완벽하다고 판단하거나 최대 반복 횟수에 도달할 때까지 각 반복에서 코드를 정제함. 마지막으로 결과적으로 정제된 코드를 출력함.

먼저, 필요한 라이브러리가 설치되어 있는지 확인:

```bash
pip install langchain langchain-community langchain-openai
```

선택한 언어 모델(예: OpenAI, Google Gemini, Anthropic)에 대한 API 키로 환경을 설정해야 함.

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# --- Configuration ---
# Load environment variables from .env file (for OPENAI_API_KEY)
load_dotenv()

# Check if the API key is set
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env file. Please add it.")

# Initialize the Chat LLM. We use gpt-4o for better reasoning.
# A lower temperature is used for more deterministic outputs.
llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

def run_reflection_loop():
    """
    Demonstrates a multi-step AI reflection loop to progressively improve a Python function.
    """
    # --- The Core Task ---
    task_prompt = """
    Your task is to create a Python function named `calculate_factorial`.
    This function should do the following:
    1.  Accept a single integer `n` as input.
    2.  Calculate its factorial (n!).
    3.  Include a clear docstring explaining what the function does.
    4.  Handle edge cases: The factorial of 0 is 1.
    5.  Handle invalid input: Raise a ValueError if the input is a negative number.
    """

    # --- The Reflection Loop ---
    max_iterations = 3
    current_code = ""

    # We will build a conversation history to provide context in each step.
    message_history = [HumanMessage(content=task_prompt)]

    for i in range(max_iterations):
        print("\n" + "="*25 + f" REFLECTION LOOP: ITERATION {i + 1} " + "="*25)

        # --- 1. GENERATE / REFINE STAGE ---
        # In the first iteration, it generates. In subsequent iterations, it refines.
        if i == 0:
            print("\n>>> STAGE 1: GENERATING initial code...")
            # The first message is just the task prompt.
            response = llm.invoke(message_history)
            current_code = response.content
        else:
            print("\n>>> STAGE 1: REFINING code based on previous critique...")
            # The message history now contains the task,
            # the last code, and the last critique.
            # We instruct the model to apply the critiques.
            message_history.append(HumanMessage(content="Please refine the code using the critiques provided."))
            response = llm.invoke(message_history)
            current_code = response.content

        print("\n--- Generated Code (v" + str(i + 1) + ") ---\n" + current_code)
        message_history.append(response) # Add the generated code to history

        # --- 2. REFLECT STAGE ---
        print("\n>>> STAGE 2: REFLECTING on the generated code...")
        # Create a specific prompt for the reflector agent.
        # This asks the model to act as a senior code reviewer.
        reflector_prompt = [
            SystemMessage(content="""
                You are a senior software engineer and an expert in Python.
                Your role is to perform a meticulous code review.
                Critically evaluate the provided Python code based on the original task requirements.
                Look for bugs, style issues, missing edge cases, and areas for improvement.
                If the code is perfect and meets all requirements,
                respond with the single phrase 'CODE_IS_PERFECT'.
                Otherwise, provide a bulleted list of your critiques.
            """),
            HumanMessage(content=f"Original Task:\n{task_prompt}\n\nCode to Review:\n{current_code}")
        ]
        critique_response = llm.invoke(reflector_prompt)
        critique = critique_response.content

        # --- 3. STOPPING CONDITION ---
        if "CODE_IS_PERFECT" in critique:
            print("\n--- Critique ---\nNo further critiques found. The code is satisfactory.")
            break
        print("\n--- Critique ---\n" + critique)

        # Add the critique to the history for the next refinement loop.
        message_history.append(HumanMessage(content=f"Critique of the previous code:\n{critique}"))

    print("\n" + "="*30 + " FINAL RESULT " + "="*30)
    print("\nFinal refined code after the reflection process:\n")
    print(current_code)

if __name__ == "__main__":
    run_reflection_loop()
```

코드는 환경 설정, API 키 로드, 집중된 출력을 위해 낮은 temperature로 GPT-4o와 같은 강력한 언어 모델을 초기화하는 것으로 시작함. 핵심 작업은 숫자의 계승을 계산하는 Python 함수를 요청하는 프롬프트로 정의되며, docstring, 엣지 케이스(0의 계승), 음수 입력에 대한 오류 처리에 대한 특정 요구사항을 포함함. run_reflection_loop 함수는 반복적 정제 프로세스를 오케스트레이션함. 루프 내에서 첫 번째 반복에서는 언어 모델이 작업 프롬프트를 기반으로 초기 코드를 생성함. 후속 반복에서는 이전 단계의 비평을 기반으로 코드를 정제함. 별도의 "reflector" 역할은 언어 모델이 담당하지만 다른 시스템 프롬프트로, 시니어 소프트웨어 엔지니어로서 생성된 코드를 원래 작업 요구사항에 대해 비평함. 이 비평은 문제 목록이나 문제가 발견되지 않으면 'CODE_IS_PERFECT'라는 문구로 제공됨. 루프는 비평이 코드가 완벽하다고 나타내거나 최대 반복 횟수에 도달할 때까지 계속됨. 대화 히스토리는 유지되고 각 단계에서 언어 모델에 전달되어 생성/정제 및 reflection 단계 모두에 컨텍스트를 제공함. 마지막으로 스크립트는 루프가 종료된 후 마지막으로 생성된 코드 버전을 출력함.

# 실습 코드 예제 (ADK)

이제 Google ADK를 사용하여 구현된 개념적 코드 예제를 살펴봄. 구체적으로, 코드는 Generator-Critic 구조를 사용하여 이를 보여줌. 하나의 컴포넌트(Generator)가 초기 결과나 계획을 생성하고, 다른 컴포넌트(Critic)가 비판적 피드백이나 비평을 제공하여 Generator를 더 정제되거나 정확한 최종 출력으로 안내함.

```python
from google.adk.agents import SequentialAgent, LlmAgent

# The first agent generates the initial draft.
generator = LlmAgent(
   name="DraftWriter",
   description="Generates initial draft content on a given subject.",
   instruction="Write a short, informative paragraph about the user's subject.",
   output_key="draft_text" # The output is saved to this state key.
)

# The second agent critiques the draft from the first agent.
reviewer = LlmAgent(
   name="FactChecker",
   description="Reviews a given text for factual accuracy and provides a structured critique.",
   instruction="""
   You are a meticulous fact-checker.
   1. Read the text provided in the state key 'draft_text'.
   2. Carefully verify the factual accuracy of all claims.
   3. Your final output must be a dictionary containing two keys:
      - "status": A string, either "ACCURATE" or "INACCURATE".
      - "reasoning": A string providing a clear explanation for your status, citing specific issues if any are found.
   """,
   output_key="review_output" # The structured dictionary is saved here.
)

# The SequentialAgent ensures the generator runs before the reviewer.
review_pipeline = SequentialAgent(
   name="WriteAndReview_Pipeline",
   sub_agents=[generator, reviewer]
)

# Execution Flow:
# 1. generator runs -> saves its paragraph to state['draft_text'].
# 2. reviewer runs -> reads state['draft_text'] and saves its dictionary output to state['review_output'].
```

이 코드는 텍스트를 생성하고 검토하기 위한 Google ADK의 순차 agent 파이프라인 사용을 보여줌. 두 개의 LlmAgent 인스턴스를 정의함: generator와 reviewer. generator agent는 주어진 주제에 대한 초기 초안 문단을 작성하도록 설계됨. 짧고 유익한 내용을 작성하도록 지시받고 출력을 상태 키 draft_text에 저장함. reviewer agent는 generator가 생성한 텍스트의 팩트체커 역할을 함. draft_text에서 텍스트를 읽고 사실 정확성을 확인하도록 지시받음. reviewer의 출력은 두 개의 키를 가진 구조화된 딕셔너리임: status와 reasoning. status는 텍스트가 "ACCURATE"인지 "INACCURATE"인지를 나타내고, reasoning은 status에 대한 설명을 제공함. 이 딕셔너리는 상태 키 review_output에 저장됨. review_pipeline이라는 SequentialAgent가 두 agent의 실행 순서를 관리하기 위해 생성됨. generator가 먼저 실행된 다음 reviewer가 실행되도록 보장함. 전체 실행 흐름은 generator가 텍스트를 생성하고 상태에 저장함. 이후 reviewer가 상태에서 이 텍스트를 읽고, 팩트체킹을 수행하고, 발견사항(status와 reasoning)을 다시 상태에 저장함. 이 파이프라인은 별도의 agent를 사용한 콘텐츠 생성 및 검토의 구조화된 프로세스를 가능하게 함. **참고:** ADK의 LoopAgent를 활용한 대체 구현도 관심 있는 사람들을 위해 제공됨.

결론을 내리기 전에, Reflection 패턴이 출력 품질을 크게 향상시키지만 중요한 트레이드오프가 있다는 점을 고려해야 함. 반복 프로세스는 강력하지만 더 높은 비용과 지연시간을 초래할 수 있음. 모든 정제 루프가 새로운 LLM 호출을 필요로 할 수 있어 시간에 민감한 애플리케이션에는 최적이 아님. 또한, 패턴은 메모리 집약적임. 각 반복마다 초기 출력, 비평, 후속 정제를 포함하여 대화 히스토리가 확장됨.

# 한눈에 보기

**무엇:** Agent의 초기 출력은 종종 최적이 아니며, 부정확성, 불완전성 또는 복잡한 요구사항을 충족하지 못하는 문제를 겪음. 기본 agentic 워크플로우는 agent가 자신의 오류를 인식하고 수정하는 내장 프로세스가 부족함. 이는 agent가 자신의 작업을 평가하거나, 더 견고하게는 별도의 논리적 agent를 critic 역할로 도입하여 해결되며, 품질에 관계없이 초기 응답이 최종 응답이 되는 것을 방지함.

**왜:** Reflection 패턴은 자기 수정 및 정제 메커니즘을 도입하여 솔루션을 제공함. "producer" agent가 출력을 생성한 다음 "critic" agent(또는 producer 자체)가 미리 정의된 기준에 대해 평가하는 피드백 루프를 설정함. 이 비평은 개선된 버전을 생성하는 데 사용됨. 생성, 평가, 정제의 반복적 프로세스는 최종 결과의 품질을 점진적으로 향상시켜 더 정확하고 일관되며 신뢰할 수 있는 결과로 이어짐.

**경험칙:** 최종 출력의 품질, 정확성, 세부사항이 속도 및 비용보다 중요할 때 Reflection 패턴을 사용함. 세련된 장문의 콘텐츠 생성, 코드 작성 및 디버깅, 상세한 계획 생성과 같은 작업에 특히 효과적임. 작업이 높은 객관성이나 일반적인 producer agent가 놓칠 수 있는 전문적인 평가를 필요로 할 때 별도의 critic agent를 사용함.

**시각적 요약**

![Reflection Pattern](./images/chapter4/diagram-1.png)

Fig. 1: Reflection 디자인 패턴, self-reflection

![Self-Reflection Loop](./images/chapter4/diagram-2.png)

Fig.2: Reflection 디자인 패턴, producer와 critique agent

# 핵심 요약

* Reflection 패턴의 주요 이점은 출력을 반복적으로 자기 수정하고 정제하는 능력으로, 훨씬 더 높은 품질, 정확성 및 복잡한 지시사항 준수로 이어짐.
* 실행, 평가/비평, 정제의 피드백 루프를 포함함. Reflection은 고품질, 정확하거나 미묘한 출력을 요구하는 작업에 필수적임.
* 강력한 구현은 Producer-Critic 모델로, 별도의 agent(또는 프롬프트된 역할)가 초기 출력을 평가함. 이러한 관심사의 분리는 객관성을 향상시키고 더 전문화되고 구조화된 피드백을 가능하게 함.
* 그러나 이러한 이점은 증가된 지연시간과 계산 비용, 그리고 모델의 컨텍스트 윈도우를 초과하거나 API 서비스에 의해 throttle될 위험이 높아지는 대가로 옴.
* 완전한 반복적 reflection은 종종 상태를 가진 워크플로우(LangGraph와 같은)를 필요로 하지만, 단일 reflection 단계는 LangChain에서 LCEL을 사용하여 비평 및 후속 정제를 위해 출력을 전달하는 방식으로 구현될 수 있음.
* Google ADK는 한 agent의 출력이 다른 agent에 의해 비평되는 순차적 워크플로우를 통해 reflection을 촉진할 수 있으며, 후속 정제 단계를 가능하게 함.
* 이 패턴은 agent가 자기 수정을 수행하고 시간이 지남에 따라 성능을 향상시킬 수 있게 함.

# 결론

Reflection 패턴은 agent의 워크플로우 내에서 자기 수정을 위한 중요한 메커니즘을 제공하여, 단일 패스 실행을 넘어 반복적 개선을 가능하게 함. 이는 시스템이 출력을 생성하고, 특정 기준에 대해 평가한 다음, 그 평가를 사용하여 정제된 결과를 생성하는 루프를 만들어 달성됨. 이 평가는 agent 자체(self-reflection)에 의해 수행되거나, 종종 더 효과적으로는 별개의 critic agent에 의해 수행될 수 있으며, 이는 패턴 내의 핵심 아키텍처 선택을 나타냄.

완전히 자율적인 다단계 reflection 프로세스는 상태 관리를 위한 견고한 아키텍처를 필요로 하지만, 그 핵심 원리는 단일 생성-비평-정제 사이클에서 효과적으로 시연됨. 제어 구조로서 reflection은 다른 기본 패턴과 통합되어 더 견고하고 기능적으로 복잡한 agentic 시스템을 구축할 수 있음.

# 참고자료

Reflection 패턴 및 관련 개념에 대한 추가 자료:

1. Training Language Models to Self-Correct via Reinforcement Learning, [https://arxiv.org/abs/2409.12917](https://arxiv.org/abs/2409.12917)
2. LangChain Expression Language (LCEL) Documentation: [https://python.langchain.com/docs/introduction/](https://python.langchain.com/docs/introduction/)
3. LangGraph Documentation:[https://www.langchain.com/langgraph](https://www.langchain.com/langgraph)
4. Google Agent Developer Kit (ADK) Documentation (Multi-Agent Systems): [https://google.github.io/adk-docs/agents/multi-agents/](https://google.github.io/adk-docs/agents/multi-agents/)
