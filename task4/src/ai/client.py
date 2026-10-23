from openai import OpenAI
import json
from src.ai.query import query
import src.ai.config as cf

client = OpenAI(
    api_key=cf.API_KEY,
    base_url=cf.BASE_URL,
)

# def ask_ai(question, data):
#     messages = [
#         {
#             "role": "system",
#             "content": (
#                 "You answer questions about store data. "
#                 "Use query function to calculate answers. "
#                 "Never invent columns, tables, or results. "
#                 "Use exact names of the tables and columns. "
#                 "Available tables and columns: "
#                 f"{cf.TABLE_DESCRIPTIONS}. "
#                 "The query specification must follow the query engine's "
#                 "supported operations. Explain the returned result briefly."
#             ),
#         },
#         {"role": "user", "content": question},
#     ]
#     response = client.chat.completions.create(
#         model=cf.MODEL,
#         messages=messages,
#         tools=[cf.QUERY_TOOL],
#         tool_choice="auto",
#     )
#     message = response.choices[0].message
#     messages.append(message)
#     if not message.tool_calls:
#         return message.content or "I couldn't answer the question."
#     for tool_call in message.tool_calls:
#         try:
#             arguments = json.loads(tool_call.function.arguments)
#             print("--------------------")
#             print(arguments)
#             result = query(data, arguments["argvs"])
#             print("--------------------")
#             print(result)
#             if hasattr(result, "to_dict"):
#                 result = result.to_dict(orient="records")
#             result_json = json.dumps(result, default=str)
#         except Exception as exc:
#             result_json = json.dumps({"error": str(exc)})
#         messages.append({
#             "role": "tool",
#             "tool_call_id": tool_call.id,
#             "content": result_json,
#         })
#     final_response = client.chat.completions.create(
#         model=cf.MODEL,
#         messages=messages,
#     )
#     return (
#         final_response.choices[0].message.content
#         or "I couldn't generate an answer."
#     )

def ask_ai(question, data):
    messages = [
        {
            "role": "system",
            "content": (
                "You answer questions about store data. "
                "Use the query function to calculate answers. "
                "Never invent columns, tables, or results. "
                "Use exact names of the tables and columns. "
                "Available tables and columns: "
                f"{cf.TABLE_DESCRIPTIONS}. "
                "The query specification must follow the query engine's "
                "supported operations. "
                "After receiving a query result, decide whether you need "
                "another query or whether you can answer the user. "
                "If more data is needed, call the query function again. "
                "When you have enough information, provide the final answer "
                "to the user."
            ),
        },
        {"role": "user", "content": question},
    ]
    while True:
        response = client.chat.completions.create(
            model=cf.MODEL,
            messages=messages,
            tools=[cf.QUERY_TOOL],
            tool_choice="auto",
        )
        message = response.choices[0].message
        messages.append(message)
        if not message.tool_calls:
            return message.content or "I couldn't answer the question."
        for tool_call in message.tool_calls:
            try:
                arguments = json.loads(tool_call.function.arguments)
                print("--------------------")
                print(arguments)
                result = query(data, arguments["argvs"])
                print("--------------------")
                print(result)
                if hasattr(result, "to_dict"):
                    result = result.to_dict(orient="records")
                result_json = json.dumps(result, default=str)
            except Exception as exc:
                result_json = json.dumps({"error": str(exc)})
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result_json,
            })