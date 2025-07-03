from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from langchain_core.runnables.graph import MermaidDrawMethod
from langgraph.types import StreamWriter ### only for custom stream mode
import asyncio
from PIL import Image
from io import BytesIO


def display(runnable):
    graph_image = runnable.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API,
        output_file_path="graph.png"
    )
    img = Image.open(BytesIO(graph_image))
    img.show()
    
    
## step 1: define state
class HellowWorldState(TypedDict):
    message: str
    id: int
    
## step 2: define nodes

def hello(state: HellowWorldState,writer:StreamWriter):
    #print(f"Hello Node: {state['message']}")  ## print the message
   # await asyncio.sleep(1)
    writer({"custom_key":"custom_value"})  ##3 custom mode 
    return {"message": "Hello "+state['message']} ## update state

def bye(state: HellowWorldState):
    #print(f"Bye Node: {state['message']}")  ## print the message
   # await asyncio.sleep(1)
    return {"message": "Bye "+state['message']} ## update state


### step 3: define graph
graph = StateGraph(HellowWorldState)  ## initiate graph

graph.add_node("hello", hello)  ## add hello nodes with node name "hello"
graph.add_node("bye", bye) ## add bye nodes with node name "bye"

#graph.add_edge(START, "hello")  ## add edges
graph.add_edge("hello", "bye") ## add edges
graph.add_edge("bye", END)
graph.set_entry_point("hello")

runnable = graph.compile()

# async def main():
#     output = await runnable.ainvoke({"message": "Marcus"})
#     print(output)
    
#asyncio.run(main())

# for chunk in runnable.stream({"message": "Marcus"},stream_mode="values"):  ## values, message (for LLM), updates,custom, debug
#     print(chunk)

# for chunk in runnable.stream({"message": "Marcus"},stream_mode="updates"):  ## values, message (for LLM), updates,custom, debug
#     print(chunk)
    
# for chunk in runnable.stream({"message": "Marcus"},stream_mode="custom"):  ## values, message (for LLM), updates,custom, debug
#     print(chunk)    

for chunk in runnable.stream({"message": "Marcus"},stream_mode="debug"):  ## values, message (for LLM), updates,custom, debug
    print(chunk)        
    
    
#display(runnable)