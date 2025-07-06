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


messages_with_tool_calls=AIMessage(content="",
                                       tool_calls=[
                                            {'name': 'get_restaurant_recommendations', 
                                             'args': {'location': 'munich'}, 
                                               'id': 'call_0_8c0a9ea6-71cb-4eef-9562-b41fd5df939e', 
                                             'type': 'tool_call'}
                                               ]
                           )

result=tool_node.invoke({"messages":[messages_with_tool_calls]})

print(result)