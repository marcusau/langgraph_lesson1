from typing import TypedDict, List,Annotated

from langchain_core.messages import AnyMessage,AIMessage,HumanMessage

from langgraph.graph import StateGraph, START, END,MessageState

from operator import add


    
# class ChatBotState(TypedDict):
#     messages: Annotated[List[AnyMessage],add]
#     discount: Annotated[int,add]

    
class ChatBotState(MessageState):
    discount: Annotated[int,add]    
    
    

def connect_to_sales(state: ChatBotState) :
    return {'messages':[AIMessage(content="Great! Let me connect you with our sales team. ")],
            "discount": 10}
    

def sales_responses(state: ChatBotState) :
    return {'messages':[AIMessage(content="We have the best offers for you. ")],
            "discount": 20}
    

graph_builder = StateGraph(ChatBotState)

graph_builder.add_node("connect_to_sales",connect_to_sales)
graph_builder.add_node("sales_responses",sales_responses)

graph_builder.add_edge(START,"connect_to_sales")
graph_builder.add_edge("connect_to_sales","sales_responses")
graph_builder.add_edge("sales_responses",END)

chatbot= graph_builder.compile()

test_input="I want to buy your product"

messages=chatbot.invoke({"messages": [HumanMessage(content=test_input)]})

for message in messages["messages"]:
    print("chatbot:",message.content)
    
print("Discount: ",messages["discount"])