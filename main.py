import openai
import json
import os

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

todos = []
openai.api_key = os.getenv("OPENAI_API_KEY")

class Todo(BaseModel):
    title: str
    completed: bool = False

def get_api_list(router: APIRouter):
    api_list = []
    for route in router.routes:
        api_list.append({
            "path": route.path,
            "method": route.method,
            "summary": route.summary,
        })
    return api_list

def openai_call(func_name: str, args: dict) -> str:

    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "What's your api list?"}]
    functions = [
        {
            "name": "get_api_list",
            "description": "Get all API list",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    ]
    messages = [{"role": "user", "content": "What's your api list?"}]
    openai.api_key = os.getenv('OPENAI_API_KEY')
    print(os.getenv('OPENAI_API_KEY'))
    print(dir(openai))
    completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613", messages=messages)
    print(completion)
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo-0613",
    #     messages=messages,
    #     functions=functions,
    #     function_call="auto",  # auto is default, but we'll be explicit
    # )
    # response_message = response["choices"][0]["message"]

    # # Step 2: check if GPT wanted to call a function
    # if response_message.get("function_call"):
    #     # Step 3: call the function
    #     # Note: the JSON response may not always be valid; be sure to handle errors
    #     available_functions = {
    #         "get_api_list": get_current_weather,
    #     }  # only one function in this example, but you can have multiple
    #     function_name = response_message["function_call"]["name"]
    #     fuction_to_call = available_functions[function_name]
    #     function_args = json.loads(response_message["function_call"]["arguments"])
    #     function_response = fuction_to_call(
    #         location=function_args.get("location"),
    #         unit=function_args.get("unit"),
    #     )

    #     # Step 4: send the info on the function call and function response to GPT
    #     messages.append(response_message)  # extend conversation with assistant's reply
    #     messages.append(
    #         {
    #             "role": "function",
    #             "name": function_name,
    #             "content": function_response,
    #         }
    #     )  # extend conversation with function response
    #     second_response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo-0613",
    #         messages=messages,
    #     )  # get a new response from GPT where it can see the function response
    #     return second_response
    

    # if func_name:
    #     response = openai.Completion.create(
    #     engine="davinci",
    #     prompt=f"Use function {func_name} with arguments {args}",
    #     temperature=0.7,
    #     max_tokens=100,
    # )
    # print(response_message)

    # if response_message.get("function_call"):
    #     print("funcrion_call")
    #     # Step 3: call the function
    #     # Note: the JSON response may not always be valid; be sure to handle errors
    #     available_functions = {
    #         "get_api_list": get_api_list,
    #     }  # only one function in this example, but you can have multiple
    #     function_name = response_message["function_call"]["name"]
    #     fuction_to_call = available_functions[function_name]
    #     function_args = json.loads(response_message["function_call"]["arguments"])
    #     function_response = fuction_to_call(
    #         location=function_args.get("location"),
    #         unit=function_args.get("unit"),
    #     )  

    #     print(function_response)  

    return response["choices"][0]["text"]

app = FastAPI()

@app.get("/todos")
def get_todos():
    return todos

@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return todo

@app.put("/todos/{id}")
def update_todo(id: int, todo: Todo):
    todos[id] = todo
    return todo

@app.delete("/todos/{id}")
def delete_todo(id: int):
    todos.pop(id)
    return


@app.get("/api-list")
def get_api_list():
    return get_api_list(app)

@app.post("/openai")
def openai(func_name: str, args: dict) -> str:
    if not func_name:
        raise HTTPException(status_code=422, detail="func_name is required")
    if not isinstance(args, dict):
        raise HTTPException(status_code=422, detail="args must be a dict")
    
    print(func_name, args)
    return openai_call(func_name, args)

# curl http://localhost:8000/openai?func_name=get_api_list -d 'args={"api_list": true}'