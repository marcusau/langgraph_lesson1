from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode

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


tools=[get_restaurant_recommendations]
tool_node=ToolNode(tools)

llm=ChatDeepSeek(model="deepseek-chat",temperature=0)
llm_with_tools=llm.bind_tools(tools)


messages=[HumanMessage(content="I am in munich. What are some good restaurants to visit?")]

print("deepseek processing...")
llm_output=llm_with_tools.invoke(messages)


tool_call=llm_output.tool_calls

messages_with_tool_calls=AIMessage(content="",tool_calls=tool_call  )

print("tool node processing...")
result=tool_node.invoke({"messages":[messages_with_tool_calls]})

print(result["messages"][0].content)
