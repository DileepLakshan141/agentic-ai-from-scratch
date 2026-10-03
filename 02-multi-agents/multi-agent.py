from typing import Literal, Annotated, Sequence
import operator
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langchain_huggingface import HuggingFaceEndpoint
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_node: str

class RouteResponse(BaseModel):
    next_agent: Literal["search_agent", "coder_agent", "FINISH"] = Field(
        description="The name of the next Agent to route to, or 'FINISH' if the task is complete"
    )
    reasoning: str = Field(description="The reasoning behind the decision of which agent to route to next.")


llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text-generation",
    max_new_tokens=200,
    temperature=0.1
)

# 4. Structured Output with Supervisor LLM
structured_supervisor_llm = llm.with_structured_output(RouteResponse)