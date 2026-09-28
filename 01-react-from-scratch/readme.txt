React  Pattern - Reasoning + Acting

* How the process works
---------------------------------------

this whole process is a loop

step 1 -> first you will write a prompt to do some task

step 2 -> then the LLM will think how to achieve that (chain of though, what to do next)

step 3 -> based on the though made on step 2, LLM will use one or more tools mentioned in the 
thought and select necessary params for that tool

step 4 -> execution engine will run that tool and add the results into the context to run it 
again. this will call the step 2 and act as a loop until given task is complete or reach max iteration 
count

* How tools are called (function calling)

prompts cant directly call the functions. so we will use an API schema or prompt
to tell the LLM what kind of tools we have 

{
  "name": "read_file",
  "description": "Reads the content of a file",
  "parameters": {
    "type": "object",
    "properties": {
      "file_path": {"type": "string"}
    },
    "required": ["file_path"]
  }
}


so LLM will generate json output instead of text output for the above scenario

our python script (execution loop) will parse that json output and call the necessary python function.

so the output (code content) will be shown into the system

GOAL of the Lesson
--------------------------------------------------

understand the skeleton of the ReAct loop with pure python without external libs.

1. how to setup the virtual env

- python -m venv venv (create virtual env)

- ./venv/Scripts/activate (activate the venv)

- pip install google-genai