# Chapter 20: Prioritization

복잡하고 동적인 환경에서 Agent는 수많은 잠재적 행동, 상충되는 목표, 제한된 리소스에 직면함. 다음 행동을 결정하는 명확한 프로세스가 없으면 효율성 저하, 운영 지연 또는 핵심 목표 달성 실패가 발생할 수 있음. Prioritization 패턴은 Agent가 중요도, 긴급성, 종속성 및 정의된 기준에 따라 작업, 목표 또는 행동을 평가하고 순위를 매길 수 있도록 하여 이 문제를 해결함. 이를 통해 Agent가 가장 중요한 작업에 집중하여 효과성과 목표 정렬이 향상됨.

# Prioritization Pattern Overview

Agent는 prioritization을 사용하여 작업, 목표 및 하위 목표를 효과적으로 관리하고 후속 행동을 안내함. 이 프로세스는 여러 요구 사항을 처리할 때 정보에 입각한 의사 결정을 용이하게 하며, 덜 중요한 활동보다 중요하거나 긴급한 활동을 우선시함. 이는 리소스가 제약되고 시간이 제한되며 목표가 충돌할 수 있는 실제 시나리오에서 특히 관련성이 높음.

Agent prioritization의 기본 측면은 일반적으로 여러 요소를 포함함. 첫째, 기준 정의는 작업 평가를 위한 규칙이나 메트릭을 설정함. 여기에는 긴급성(작업의 시간 민감도), 중요도(주요 목표에 미치는 영향), 종속성(작업이 다른 작업의 전제 조건인지 여부), 리소스 가용성(필요한 도구나 정보의 준비 상태), 비용/편익 분석(노력 대 예상 결과), 개인화된 Agent를 위한 사용자 선호도가 포함될 수 있음. 둘째, 작업 평가는 정의된 기준에 따라 각 잠재적 작업을 평가하는 것으로, 단순한 규칙부터 LLM의 복잡한 점수 매기기나 추론까지 다양한 방법을 활용함. 셋째, 스케줄링 또는 선택 논리는 평가를 기반으로 최적의 다음 행동이나 작업 순서를 선택하는 알고리즘을 의미하며, 큐나 고급 계획 구성 요소를 잠재적으로 활용함. 마지막으로 동적 재우선순위 지정은 Agent가 새로운 중요 이벤트 발생이나 마감일 임박과 같은 상황 변화에 따라 우선순위를 수정할 수 있게 하여 Agent의 적응성과 응답성을 보장함.

Prioritization은 다양한 수준에서 발생할 수 있음: 전반적인 목표 선택(high-level goal prioritization), 계획 내 단계 순서 지정(sub-task prioritization), 사용 가능한 옵션에서 다음 즉각적인 행동 선택(action selection). 효과적인 prioritization을 통해 Agent는 특히 복잡한 다목표 환경에서 더 지능적이고 효율적이며 견고한 동작을 보임. 이는 관리자가 모든 구성원의 의견을 고려하여 작업의 우선순위를 지정하는 인간 팀 조직을 반영함.

# Practical Applications & Use Cases

다양한 실제 애플리케이션에서 AI Agent는 시기적절하고 효과적인 결정을 내리기 위해 정교한 prioritization을 사용함.

* **자동화된 고객 지원**: Agent는 비밀번호 재설정과 같은 일상적인 문제보다 시스템 장애 보고서와 같은 긴급 요청을 우선시함. 또한 고가치 고객에게 우선 처리를 제공할 수 있음.
* **Cloud Computing**: AI는 피크 수요 시 중요한 애플리케이션에 대한 할당을 우선시하고 덜 긴급한 배치 작업을 비피크 시간으로 미루어 리소스를 관리하고 스케줄링하여 비용을 최적화함.
* **자율 주행 시스템**: 안전과 효율성을 보장하기 위해 지속적으로 행동의 우선순위를 지정함. 예를 들어, 충돌을 피하기 위한 제동은 차선 유지나 연료 효율 최적화보다 우선함.
* **금융 거래**: Bot은 시장 상황, 위험 허용도, 이익률, 실시간 뉴스와 같은 요인을 분석하여 거래의 우선순위를 지정하여 우선순위가 높은 거래의 신속한 실행을 가능하게 함.
* **프로젝트 관리**: AI Agent는 마감일, 종속성, 팀 가용성 및 전략적 중요성을 기반으로 프로젝트 보드의 작업 우선순위를 지정함.
* **사이버 보안**: 네트워크 트래픽을 모니터링하는 Agent는 위협 심각도, 잠재적 영향 및 자산 중요도를 평가하여 경고의 우선순위를 지정하여 가장 위험한 위협에 즉각적으로 대응함.
* **개인 비서 AI**: Prioritization을 활용하여 일상 생활을 관리하고 사용자 정의 중요도, 다가오는 마감일 및 현재 컨텍스트에 따라 캘린더 이벤트, 알림 및 통지를 구성함.

이러한 예시들은 prioritization 능력이 다양한 상황에서 AI Agent의 향상된 성능과 의사 결정 능력에 얼마나 근본적인지 보여줌.

# Hands-On Code Example

다음은 LangChain을 사용하여 Project Manager AI Agent를 개발하는 방법을 보여줌. 이 Agent는 작업 생성, 우선순위 지정 및 팀 구성원에게 할당을 용이하게 하며, 자동화된 프로젝트 관리를 위한 맞춤형 도구와 함께 대형 언어 모델의 적용을 보여줌.

```python
import os
import asyncio
from typing import List, Optional, Dict, Type
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory

# --- 0. Configuration and Setup ---
# Loads the OPENAI_API_KEY from the .env file.
load_dotenv()

# The ChatOpenAI client automatically picks up the API key from the environment.
llm = ChatOpenAI(temperature=0.5, model="gpt-4o-mini")

# --- 1. Task Management System ---
class Task(BaseModel):
    """Represents a single task in the system."""
    id: str
    description: str
    priority: Optional[str] = None  # P0, P1, P2
    assigned_to: Optional[str] = None # Name of the worker

class SuperSimpleTaskManager:
    """An efficient and robust in-memory task manager."""
    def __init__(self):
        # Use a dictionary for O(1) lookups, updates, and deletions.
        self.tasks: Dict[str, Task] = {}
        self.next_task_id = 1

    def create_task(self, description: str) -> Task:
        """Creates and stores a new task."""
        task_id = f"TASK-{self.next_task_id:03d}"
        new_task = Task(id=task_id, description=description)
        self.tasks[task_id] = new_task
        self.next_task_id += 1
        print(f"DEBUG: Task created - {task_id}: {description}")
        return new_task

    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """Safely updates a task using Pydantic's model_copy."""
        task = self.tasks.get(task_id)
        if task:
            # Use model_copy for type-safe updates.
            update_data = {k: v for k, v in kwargs.items() if v is not None}
            updated_task = task.model_copy(update=update_data)
            self.tasks[task_id] = updated_task
            print(f"DEBUG: Task {task_id} updated with {update_data}")
            return updated_task

        print(f"DEBUG: Task {task_id} not found for update.")
        return None

    def list_all_tasks(self) -> str:
        """Lists all tasks currently in the system."""
        if not self.tasks:
            return "No tasks in the system."

        task_strings = []
        for task in self.tasks.values():
            task_strings.append(
                f"ID: {task.id}, Desc: '{task.description}', "
                f"Priority: {task.priority or 'N/A'}, "
                f"Assigned To: {task.assigned_to or 'N/A'}"
            )
        return "Current Tasks:\n" + "\n".join(task_strings)

task_manager = SuperSimpleTaskManager()

# --- 2. Tools for the Project Manager Agent ---
# Use Pydantic models for tool arguments for better validation and clarity.
class CreateTaskArgs(BaseModel):
    description: str = Field(description="A detailed description of the task.")

class PriorityArgs(BaseModel):
    task_id: str = Field(description="The ID of the task to update, e.g., 'TASK-001'.")
    priority: str = Field(description="The priority to set. Must be one of: 'P0', 'P1', 'P2'.")

class AssignWorkerArgs(BaseModel):
    task_id: str = Field(description="The ID of the task to update, e.g., 'TASK-001'.")
    worker_name: str = Field(description="The name of the worker to assign the task to.")

def create_new_task_tool(description: str) -> str:
    """Creates a new project task with the given description."""
    task = task_manager.create_task(description)
    return f"Created task {task.id}: '{task.description}'."

def assign_priority_to_task_tool(task_id: str, priority: str) -> str:
    """Assigns a priority (P0, P1, P2) to a given task ID."""
    if priority not in ["P0", "P1", "P2"]:
        return "Invalid priority. Must be P0, P1, or P2."
    task = task_manager.update_task(task_id, priority=priority)
    return f"Assigned priority {priority} to task {task.id}." if task else f"Task {task_id} not found."

def assign_task_to_worker_tool(task_id: str, worker_name: str) -> str:
    """Assigns a task to a specific worker."""
    task = task_manager.update_task(task_id, assigned_to=worker_name)
    return f"Assigned task {task.id} to {worker_name}." if task else f"Task {task_id} not found."

# All tools the PM agent can use
pm_tools = [
    Tool(
        name="create_new_task",
        func=create_new_task_tool,
        description="Use this first to create a new task and get its ID.",
        args_schema=CreateTaskArgs
    ),
    Tool(
        name="assign_priority_to_task",
        func=assign_priority_to_task_tool,
        description="Use this to assign a priority to a task after it has been created.",
        args_schema=PriorityArgs
    ),
    Tool(
        name="assign_task_to_worker",
        func=assign_task_to_worker_tool,
        description="Use this to assign a task to a specific worker after it has been created.",
        args_schema=AssignWorkerArgs
    ),
    Tool(
        name="list_all_tasks",
        func=task_manager.list_all_tasks,
        description="Use this to list all current tasks and their status."
    ),
]

# --- 3. Project Manager Agent Definition ---
pm_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are a focused Project Manager LLM agent. Your goal is to manage project tasks efficiently.

When you receive a new task request, follow these steps:
    1.  First, create the task with the given description using the `create_new_task` tool. You must do this first to get a `task_id`.
    2.  Next, analyze the user's request to see if a priority or an assignee is mentioned.
        - If a priority is mentioned (e.g., "urgent", "ASAP", "critical"), map it to P0. Use `assign_priority_to_task`.
        - If a worker is mentioned, use `assign_task_to_worker`.
    3.  If any information (priority, assignee) is missing, you must make a reasonable default assignment (e.g., assign P1 priority and assign to 'Worker A').
    4.  Once the task is fully processed, use `list_all_tasks` to show the final state.

Available workers: 'Worker A', 'Worker B', 'Review Team'
    Priority levels: P0 (highest), P1 (medium), P2 (lowest)
    """),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# Create the agent executor
pm_agent = create_react_agent(llm, pm_tools, pm_prompt_template)
pm_agent_executor = AgentExecutor(
    agent=pm_agent,
    tools=pm_tools,
    verbose=True,
    handle_parsing_errors=True,
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
)

# --- 4. Simple Interaction Flow ---
async def run_simulation():
    print("--- Project Manager Simulation ---")
    # Scenario 1: Handle a new, urgent feature request
    print("\n[User Request] I need a new login system implemented ASAP. It should be assigned to Worker B.")
    await pm_agent_executor.ainvoke({"input": "Create a task to implement a new login system. It's urgent and should be assigned to Worker B."})
    print("\n" + "-"*60 + "\n")
    # Scenario 2: Handle a less urgent content update with fewer details
    print("[User Request] We need to review the marketing website content.")
    await pm_agent_executor.ainvoke({"input": "Manage a new task: Review marketing website content."})
    print("\n--- Simulation Complete ---")

# Run the simulation
if __name__ == "__main__":
    asyncio.run(run_simulation())
```

이 코드는 Python과 LangChain을 사용하여 대형 언어 모델로 구동되는 프로젝트 관리자 Agent를 시뮬레이션하도록 설계된 간단한 작업 관리 시스템을 구현함.

시스템은 SuperSimpleTaskManager 클래스를 사용하여 메모리 내에서 작업을 효율적으로 관리하며, 빠른 데이터 검색을 위해 딕셔너리 구조를 활용함. 각 작업은 고유 식별자, 설명 텍스트, 선택적 우선순위 수준(P0, P1, P2) 및 선택적 담당자 지정을 포함하는 Task Pydantic 모델로 표현됨. 메모리 사용량은 작업 유형, 작업자 수 및 기타 기여 요인에 따라 달라짐. Task manager는 작업 생성, 작업 수정 및 모든 작업 검색을 위한 메서드를 제공함.

Agent는 정의된 Tool 세트를 통해 task manager와 상호 작용함. 이러한 도구는 새 작업 생성, 작업에 우선순위 할당, 인력에게 작업 할당 및 모든 작업 나열을 용이하게 함. 각 도구는 SuperSimpleTaskManager 인스턴스와의 상호 작용을 가능하게 하도록 캡슐화됨. Pydantic 모델은 도구의 필수 인수를 설명하여 데이터 검증을 보장하는 데 활용됨.

AgentExecutor는 언어 모델, 도구 세트 및 컨텍스트 연속성을 유지하기 위한 대화 메모리 구성 요소로 구성됨. 특정 ChatPromptTemplate이 프로젝트 관리 역할에서 Agent의 동작을 지시하도록 정의됨. 프롬프트는 Agent에게 작업 생성으로 시작하고, 그 후 지정된 대로 우선순위와 인력을 할당하고, 포괄적인 작업 목록으로 마무리하도록 지시함. P1 우선순위와 'Worker A'와 같은 기본 할당은 정보가 없는 경우를 위해 프롬프트 내에 규정됨.

코드는 비동기적 성격의 시뮬레이션 함수(run_simulation)를 통합하여 Agent의 운영 능력을 시연함. 시뮬레이션은 두 가지 시나리오를 실행함: 지정된 인력과 함께 긴급한 작업 관리, 최소한의 입력으로 덜 긴급한 작업 관리. Agent의 작업과 논리적 프로세스는 AgentExecutor 내에서 verbose=True 활성화로 인해 콘솔에 출력됨.

# At a Glance

**What:** 복잡한 환경에서 운영되는 AI Agent는 수많은 잠재적 행동, 상충되는 목표 및 유한한 리소스에 직면함. 다음 행동을 결정하는 명확한 방법이 없으면 이러한 Agent는 비효율적이고 비효과적이 될 위험이 있음. 이는 상당한 운영 지연이나 주요 목표 달성의 완전한 실패로 이어질 수 있음. 핵심 과제는 Agent가 목적 있고 논리적으로 행동할 수 있도록 압도적인 수의 선택을 관리하는 것임.

**Why:** Prioritization 패턴은 Agent가 작업과 목표의 순위를 매길 수 있도록 하여 이 문제에 대한 표준화된 솔루션을 제공함. 이는 긴급성, 중요도, 종속성 및 리소스 비용과 같은 명확한 기준을 설정함으로써 달성됨. Agent는 이러한 기준에 따라 각 잠재적 행동을 평가하여 가장 중요하고 시기적절한 행동 방침을 결정함. 이 Agentic 능력은 시스템이 변화하는 상황에 동적으로 적응하고 제약된 리소스를 효과적으로 관리할 수 있게 함. 우선순위가 가장 높은 항목에 집중함으로써 Agent의 동작은 더 지능적이고 견고하며 전략적 목표와 일치하게 됨.

**Rule of thumb:** Agentic 시스템이 리소스 제약 하에서 여러 개의 종종 상충되는 작업이나 목표를 자율적으로 관리하여 동적 환경에서 효과적으로 운영해야 할 때 Prioritization 패턴을 사용함.

**Visual summary:**

**![Diagram 1](images/chapter20/diagram-1.png)**

Fig.1: Prioritization Design pattern

# Key Takeaways

* Prioritization은 AI Agent가 복잡하고 다면적인 환경에서 효과적으로 기능할 수 있게 함.
* Agent는 긴급성, 중요도 및 종속성과 같은 확립된 기준을 활용하여 작업을 평가하고 순위를 매김.
* 동적 재우선순위 지정을 통해 Agent는 실시간 변화에 대응하여 운영 초점을 조정할 수 있음.
* Prioritization은 전반적인 전략적 목표와 즉각적인 전술적 결정을 포함하여 다양한 수준에서 발생함.
* 효과적인 prioritization은 AI Agent의 효율성 증가와 운영 견고성 향상을 가져옴.

# Conclusions

결론적으로 prioritization 패턴은 효과적인 agentic AI의 초석이며, 시스템이 목적과 지능으로 동적 환경의 복잡성을 탐색할 수 있게 함. 이는 Agent가 수많은 상충되는 작업과 목표를 자율적으로 평가하고 제한된 리소스를 집중할 위치에 대해 이성적인 결정을 내릴 수 있게 함. 이 agentic 능력은 단순한 작업 실행을 넘어 시스템이 능동적이고 전략적인 의사 결정자로 행동할 수 있게 함. 긴급성, 중요도 및 종속성과 같은 기준을 평가함으로써 Agent는 정교하고 인간과 유사한 추론 프로세스를 보여줌.

이 agentic 동작의 주요 특징은 동적 재우선순위 지정으로, Agent에게 조건이 변함에 따라 실시간으로 초점을 조정할 수 있는 자율성을 부여함. 코드 예제에서 보여주듯이 Agent는 모호한 요청을 해석하고, 적절한 도구를 자율적으로 선택 및 사용하며, 목표를 달성하기 위해 작업을 논리적으로 순서화함. 워크플로를 자체 관리하는 이 능력이 진정한 agentic 시스템을 단순한 자동화 스크립트와 구별함. 궁극적으로 prioritization을 마스터하는 것은 복잡한 실제 시나리오에서 효과적이고 안정적으로 작동할 수 있는 견고하고 지능적인 Agent를 만드는 데 근본적임.

# References

1. Examining the Security of Artificial Intelligence in Project Management: A Case Study of AI-driven Project Scheduling and Resource Allocation in Information Systems Projects ; [https://www.irejournals.com/paper-details/1706160](https://www.irejournals.com/paper-details/1706160)
2. AI-Driven Decision Support Systems in Agile Software Project Management: Enhancing Risk Mitigation and Resource Allocation; [https://www.mdpi.com/2079-8954/13/3/208](https://www.mdpi.com/2079-8954/13/3/208)
