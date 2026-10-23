from openai import OpenAI
import json
from src.ai.query import query
import src.ai.config as cf

client = OpenAI(
    api_key=cf.API_KEY,
    base_url=cf.BASE_URL,
)

def ask_ai(question, data):
    messages = [
        {
            "role": "system",
            "content": (
                "Answer questions about store data using the query function. "
                "Never invent tables, columns, or results. "
                "Use exact names of the tables and columns. "
                f"Available tables and columns: {cf.TABLE_DESCRIPTIONS}. "
                "After each query result, decide whether another query is needed. "
                "If more data is needed, call the query function again. "
                "Then provide the final answer."
            ),
        },
        {"role": "user", "content": question},
    ]
    while True:
        try:
            response = client.chat.completions.create(
                model=cf.MODEL,
                messages=messages,
                tools=[cf.QUERY_TOOL],
                tool_choice="auto",
            )
        except Exception as exc:
            if getattr(exc, "status_code", None) == 413:
                return (
                    "Sorry, your request requires more tokens than the free AI model "
                    "currently supports. Please simplify your question by aggregating "
                    "the data, for example, ask for the number of records instead "
                    "of requesting all records."
                )
            return "Sorry, something went wrong."
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
