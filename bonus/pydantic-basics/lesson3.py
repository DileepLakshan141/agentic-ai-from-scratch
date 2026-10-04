import json
import os
import re
from typing import Callable, Dict, Literal, Optional
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from pydantic import BaseModel, Field

load_dotenv()


class ToolCall(BaseModel):
    tool_name: str = Field(description="The name of the tool to be used.")
    tool_input: str = Field(description="The input string required by the tool.")

class ReactStep(BaseModel):
    thought: str = Field(description="The AI's reasoning or thought process.")
    action: Literal["call_tool", "final_answer"] = Field(
        description="The action to be taken: either a tool call or providing the final answer."
    )
    tool_call: Optional[ToolCall] = Field(
        default=None, description="Details of the tool to be called, if action is 'call_tool'."
    )
    final_answer: Optional[str] = Field(
        default=None, description="The final answer to be provided, if action is 'final_answer'."
    )

def calculator(expression: str) -> str:
    try:
        allowed_chars = "0123456789+-*/(). "
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression."
        return str(eval(expression))
    except Exception as e:
        return f"Error: {str(e)}"

def reverse_string(input_string: str) -> str:
    return input_string[::-1]

TOOL_REGISTRY: Dict[str, Callable[[str], str]] = {
    "calculator": calculator,
    "reverse_string": reverse_string  
}


client = InferenceClient(
    model="mistralai/Ministral-3-14B-Reasoning-2512",
    token=os.getenv("HUGGINGFACE_API_KEY"),
    provider="hf-inference"
)

def call_llm(prompt: str) -> str:
    
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.1,
    )
    return response.choices[0].message.content

def get_pydantic_schema() -> str:
    return json.dumps(ReactStep.model_json_schema(), indent=2)

def build_prompt(user_input: str, history: str) -> str:
    schema = get_pydantic_schema()
    return f"""You are a ReAct AI Agent operating in a Thought -> Action -> Observation loop.

Available Tools:
1. calculator: Evaluates basic math expressions (e.g., "25 * 48").
2. reverse_string: Reverses a string (e.g., "hello").

For EVERY step, you MUST respond ONLY with a valid JSON object matching this schema:
{schema}

Execution History:
User: {user_input}
{history}
Next Step JSON:"""

def parse_step(raw_response: str) -> ReactStep:
    json_match = re.search(r"\{.*\}", raw_response, re.DOTALL)
    if not json_match:
        raise ValueError("No valid JSON found in the LLM output.")
    return ReactStep.model_validate_json(json_match.group(0))

def execute_tool(tool_name: str, tool_input: str) -> str:
    tool_fn = TOOL_REGISTRY.get(tool_name)
    if not tool_fn:
        return f"Error: Tool '{tool_name}' not found."
    return tool_fn(tool_input)


def run_react_agent(user_query: str, max_iterations: int = 5) -> str:
    print(f"\n🚀 User Query: {user_query}\n" + "=" * 50)
    history = ""

    for iteration in range(1, max_iterations + 1):
        print(f"\n🔄 --- Iteration {iteration} ---")
        prompt = build_prompt(user_query, history)
        raw_response = call_llm(prompt)

        try:
            step = parse_step(raw_response)
        except Exception as e:
            print(f"❌ JSON Parsing/Validation Error: {e}")
            history += f"\nSystem Error: Invalid JSON response ({e}). Please strictly output valid JSON.\n"
            continue

        print(f"💭 Thought: {step.thought}")

        if step.action == "final_answer":
            print(f"✅ Final Answer: {step.final_answer}")
            return step.final_answer or "No answer provided."

        elif step.action == "call_tool" and step.tool_call:
            tool_name = step.tool_call.tool_name
            tool_input = step.tool_call.tool_input

            print(f"🛠️ Action: Calling Tool '{tool_name}' with input: '{tool_input}'")
            observation = execute_tool(tool_name, tool_input)
            print(f"👁️ Observation: {observation}")

            history += (
                f"Thought: {step.thought}\n"
                f"Action: Call {tool_name}({tool_input})\n"
                f"Observation: {observation}\n"
            )

    return "Reached maximum iteration limit without a final answer."

if __name__ == "__main__":
    query = "Calculate (125 * 8) / 4 and then reverse the word 'Agentic'."
    result = run_react_agent(query, max_iterations=5)
    print(f"\nFinal Result: {result}")