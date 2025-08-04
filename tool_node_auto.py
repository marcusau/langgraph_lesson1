from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import START, END, MessagesState,StateGraph
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv
load_dotenv(override=True)
import os

os.environ["DEEPSEEK_API_KEY"]=os.getenv("DEEPSEEK_API_KEY")

@tool
def get_restaurant_recommendations(location:str) -> list[str]:
    """Returns a list of recommended restaurants for a given location.
    
    Args:
        location: The city to get restaurant recommendations for.
        
    Returns:
        A list of restaurant names.
    """
    
    recommendations = {
        
        "munich":["Biergarten", "Schwabing", "Maxvorstadt"],
        "new york":["The Modern", "Le Bernardin", "Eleven Madison Park"],
        "paris":["Le Meurice", "Le Cinq", "Le Meurice"]
        
    }
    return recommendations.get(location.lower(),["No recommendations found"])


def book_table(restaurant:str,time:str) -> str:
    """ Book a table at the specific restaurant and time """
    return f"booked table at {restaurant} at {time}"




tools=[get_restaurant_recommendations,book_table]
model=ChatDeepSeek(model="deepseek-chat",temperature=0).bind_tools(tools)
tool_node=ToolNode(tools)




def call_model(state:MessagesState) :
    messages=state["messages"]
    response=model.invoke(messages)
    return {'messages':response}


def should_continue(state:MessagesState) :
    messages=state["messages"]
    last_message=messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


### define nodes
workflow=StateGraph(MessagesState)
workflow.add_node("agent",call_model)
workflow.add_node("tools",tool_node)


## define edges
workflow.add_edge(START,"agent")
workflow.add_conditional_edges("agent",should_continue,)
workflow.add_edge("tools","agent")


checkpointer=MemorySaver()
graph=workflow.compile(checkpointer=checkpointer)
#graph=workflow.compile()
######
config={"configurable": {"thread_id": "1"}}
messages=[HumanMessage(content="Can you recommend just one top restaurant in Paris?, The response should just the name of restaurant")]
responses=graph.invoke({"messages":messages},config=config)
recommendated_restaurant=responses["messages"][-1].content
print(recommendated_restaurant)


messages=[HumanMessage(content="book a table at the restaurant at 9:00pm.")]
final_responses=graph.invoke({"messages":messages},config=config)
final_responses=final_responses["messages"][-1].content
print(final_responses)




