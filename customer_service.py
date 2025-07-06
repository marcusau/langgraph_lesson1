from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, START, END

class SupportRequest(TypedDict):
    message: str
    priority: int   ## 1 is high priority, 2 is medium, 3 is low
    

# def categorize_request(request: SupportRequest) -> str:
#     print(f"Routing function receiving request: {request}")
#     if "urgent" in request["message"].lower() and request["priority"]== 1:
#         return "urgent"
#     return "standard"

def categorize_request(request: SupportRequest) -> str:
    print(f"Routing function receiving request: {request}")
    if "urgent" in request["message"].lower() and request["priority"]== 1:
        return "high"
    return "low"



def handle_urgent(request: SupportRequest) -> str:
    print(f"routing to urgent supprt team: {request}")
    return request

def handle_standard(request: SupportRequest) -> str:    
    print(f"routing to standard support queue: {request}")
    return request


graph = StateGraph(SupportRequest)

graph.add_node("urgent", handle_urgent)
graph.add_node("standard", handle_standard)

#graph.add_conditional_edges(START,categorize_request)  ## categorize_request is a routing function that returns the node to route to based on the request p
graph.add_conditional_edges(START,categorize_request,path_map={"high": "urgent", "low": "standard"})
graph.add_edge("urgent", END)
graph.add_edge("standard", END)

runnable = graph.compile()

print(runnable.invoke({"message": "My Account is hacked. Urgent help needed", "priority": 1}))
print("--------------------------------")
print(runnable.invoke({"message": "I need help with password reset", "priority": 3}))
print("--------------------------------")






