import os
import re
import datetime
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")
if not hf_token:
    raise ValueError("HF_TOKEN is missing in .env file")

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"

# Hugging Face Inference Client
client = InferenceClient(model=MODEL_ID, token=hf_token)

def get_system_time() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate_math(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

AVAILABLE_TOOLS = {
    "get_system_time": get_system_time,
    "calculate_math": calculate_math,
}

SYSTEM_PROMPT = """
You are an AI Agent that follows the ReAct (Reasoning + Acting) pattern.
You can use the following Tools to solve the user's request:

Available Tools:
- get_system_time(): Returns the current time and date. Requires no arguments.
- calculate_math(expression): Evaluates a mathematical calculation given as a Python expression. Example: calculate_math("25 * 4")

You must strictly adhere to the following format:

Thought: Reason logically about what step to take next.
Action: ToolName(arguments)
Observation: The output returned by the Tool.

You can go through as many Thought -> Action -> Observation steps as necessary.
Once you have obtained the complete answer, provide it in the following format:

Final Answer: [Write your final answer here]

Let's begin!
"""

def run_hf_react_agent(prompt: str, max_iterations=5):
    print(f"User query is: {prompt}")
    
    prompt_history = f"{SYSTEM_PROMPT}\nUser Query: {prompt}\n"

    for i in range(max_iterations):
        print(f"\n--- Iteration {i + 1} ---")

        # Hugging Face Chat / Text Generation Call
        try:
            response = client.text_generation(
                prompt=prompt_history,
                max_new_tokens=300,
                temperature=0.1,
                return_full_text=False
            )
            model_output = response.strip()
        except Exception as e:
            print(f"❌ HF API Error: {e}")
            break

        print(f"Model Output:\n{model_output}\n")
        prompt_history += f"{model_output}\n"

        if "Final Answer:" in model_output:
            final_answer = model_output.split("Final Answer:")[1].strip()
            print("==========================================")
            print(f"Final Answer Reached:\n{final_answer}")
            print("==========================================")
            return final_answer

        if "Observation:" in model_output:
            model_output = model_output.split("Observation:")[0].strip()
    
        # Action Extraction via Regex
        action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", model_output)

        if action_match:
            tool_name = action_match.group(1).strip()
            tool_arg = action_match.group(2).strip().strip('"\'')

            print(f"⚙️ Executing Tool: {tool_name} with Arg: '{tool_arg}'")

            if tool_name in AVAILABLE_TOOLS:
                tool_func = AVAILABLE_TOOLS[tool_name]
                if tool_arg:
                    observation = tool_func(tool_arg)
                else:
                    observation = tool_func()
            else:
                observation = f"Error: Tool '{tool_name}' is not recognized."

            print(f"👁️ Observation: {observation}")
            prompt_history += f"\nObservation: {observation}\n"
        else:
            print("⚠️ Action format not found or model didn't trigger a tool. Continuing...")

if __name__ == "__main__":
    run_hf_react_agent("What is the time now? Also, what is the value of 15 * 84?")