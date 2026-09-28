import os
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()
if "GEMINI_API_KEY" not in os.environ:
    raise ValueError("The GEMINI API KEY variable is not found in .env file")

client = genai.Client(
    http_options=types.HttpOptions(
        timeout=30000  
    )
)

# tools that our agent can use
def get_system_time() -> str:
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate_math(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error while evaluating expression: {e}"


AVAILABLE_TOOLS = {
    "get_system_time": get_system_time,
    "calculate_math": calculate_math,
}

# decalre the prompt

SYSTEM_PROMPT = """

You are an AI Agent that follows the ReAct (Reasoning + Acting) pattern.
You can use the following Tools to solve the user's request:

Available Tools:

get_system_time(): Returns the current time and date. Requires no arguments.

calculate_math(expression): Evaluates a mathematical calculation given as a Python expression. Example: calculate_math("25 * 4")

You must strictly adhere to the following format:

Thought: Reason logically about what step to take next.
Action: ToolName(arguments)
Observation: The output returned by the Tool (this will be provided by the System).

You can go through as many Thought -> Action -> Observation steps as necessary.
Once you have obtained the complete answer to the user's request, provide it in the following format:

Final Answer: [Write your final answer here]

Let's begin!

"""


def run_react_agent(prompt: str, max_iterations_count=5):
    print(f"User query is : {prompt}")

    prompt_history = f"{SYSTEM_PROMPT}\nUser Query: {prompt}\n"

    for i in range(max_iterations_count):
        print(f"\n--- Iteration {i + 1} ---")
        
    
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt_history
        )
        model_output = response.text.strip()

        print(f"Model Output:\n{model_output}\n")
        
        prompt_history += f"{model_output}\n"
        
    
        if "Final Answer:" in model_output:
            final_answer = model_output.split("Final Answer:")[1].strip()
            print("==========================================")
            print(f"Final Answer Reached:\n{final_answer}")
            print("==========================================")
            return final_answer
        
        
        action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", model_output)
        
        if action_match:
            tool_name = action_match.group(1).strip()
            tool_arg = action_match.group(2).strip().strip('"\'')
            
            print(f"⚙️ Executing Tool: {tool_name} with Arg: '{tool_arg}'")
            
            # check for tool existnce
            if tool_name in AVAILABLE_TOOLS:
                tool_func = AVAILABLE_TOOLS[tool_name]
                if tool_arg:
                    observation = tool_func(tool_arg)
                else:
                    observation = tool_func()
            else:
                observation = f"Error: Tool '{tool_name}' is not recognized."
                
            print(f"👁️ Observation: {observation}")
            
            # meomry feedback
            prompt_history += f"Observation: {observation}\n"
        else:
            print("⚠️ Action format unrecognized or no action found. Continuing loop...")

if __name__ == "__main__":
    # Test Case 1: Simple ReAct requiring system time & math
    run_react_agent("What is the time now? Also, what is the value of 15 * 84?")