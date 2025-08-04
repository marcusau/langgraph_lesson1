import os
from typing import TypedDict
from dotenv import load_dotenv

from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt
from langgraph.types import Command


load_dotenv(override=True)
os.environ["DEEPSEEK_API_KEY"]=os.getenv("DEEPSEEK_API_KEY")

class CodeAssistantState(TypedDict):
    task:str
    code:str
    tests:str
    
model=ChatDeepSeek(model="deepseek-chat",temperature=0)


code_prompt=ChatPromptTemplate.from_template(  """ Generate a python code for: {task}.  """)
test_prompt=ChatPromptTemplate.from_template(  """ Write unit tests for this code: {code}.  """)

code_chain=code_prompt|model|StrOutputParser()
test_chain=test_prompt|model|StrOutputParser()



def generate_code(state:CodeAssistantState) -> CodeAssistantState:
    print(f"Generating code ")
    code=code_chain.invoke({"task":state["task"]})
    #print(f"Generated code: {code}")
    return Command(goto="human_review",update={"code":code})


def human_review(state:CodeAssistantState) -> CodeAssistantState:
    value=interrupt({
        "question":"Are you ok with the code? Type 'y' or 'yes' to continue, otherwise type 'n' or 'no' to end the process:  ",
        "code":state["code"]
    })
    if value.lower()=="y" or value.lower()=="yes":
        return Command(goto="generate_tests")
    else:
        return Command(goto=END)


def generate_tests(state:CodeAssistantState) -> CodeAssistantState:
    print(f"Generating tests ")
    tests=test_chain.invoke({"code":state["code"]})
    #print(f"Generated tests: {tests}")
    return Command(goto="end",update={"tests":tests})


def create_coding_assistant_working():
    workflow=StateGraph(CodeAssistantState)
    workflow.add_node("generate_code",generate_code)
    workflow.add_node("human_review",human_review)
    workflow.add_node("generate_tests",generate_tests)
    workflow.set_entry_point("generate_code")
    return workflow.compile(checkpointer=MemorySaver())


## Run the workflow
coding_assistant=create_coding_assistant_working()
inputs= {'task':'Create a function to reverse a string in python'}
thread={"configurable":{"thread_id":"1"}}
result=coding_assistant.invoke(inputs,config=thread)

print("\n--- Generated Code ---")
print(result.get("code","No code generated"))



tasks= coding_assistant.get_state(config=thread).tasks
print(tasks) 
task=tasks[0]
question=task.interrupts[0].value.get("question")

user_input=input(question)
result=coding_assistant.invoke(Command(resume=user_input),config=thread)

print("\n--- Generated Tests ---")
print(result.get("tests","No code or tests generated"))




