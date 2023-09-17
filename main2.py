
import openai
import json
import os

from fastapi import FastAPI, APIRouter, Request
from pydantic import BaseModel
# from fastapi_versioning import VersionedFastAPI, version
import uvicorn

openai.api_key = os.getenv("OPENAI_API_KEY")
todos = []
app = FastAPI()
logger = []
router = APIRouter()
all_routes = []

class Todo(BaseModel):
    title: str
    completed: bool = False

def get_api_list():
    reserved_routes = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]
    for route in app.routes:
        if(route.path not in reserved_routes):
            if route.name is not None:
                # version = getattr(route.endpoint, "_api_version", (2, 0))
                # all_routes.append("/v" + str(version[0]) + route.path)
                all_routes.append(route.path)

@router.get("/")
def index():
    return { "endpoints": all_routes }

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # start_time = time.time()
    response = await call_next(request)
    # process_time = time.time() - start_time
    # response.headers["X-Process-Time"] = str(process_time)
    # 응답이 200이면 
    if(response.status_code == 200):
        logger.append(response)
    return response



@app.get("/todos", description="할 일 목록을 조회합니다.")
async def get_todos():
    return todos

@app.post("/todos")
async def create_todo(todo: Todo):
    todos.append(todo)
    return todo

@app.put("/todos/{id}")
async def update_todo(id: int, todo: Todo):
    todos[id] = todo
    return todo

@app.delete("/todos/{id}")
async def delete_todo(id: int):
    todos.pop(id)
    return

@app.get("/chat")
async def chat(prompt: str = "지금 서울날씨를 섭씨로 알려줘."):
    print('chat : ', prompt)
    return _chat(prompt)

def _chat(prompt: str = "지금 서울날씨를 섭씨로 알려줘."):
    return MyOpenAI.chat(prompt)

# def _get_api_list() -> list:
#     api_list = []
#     for route in app.routes:
#         print(route.name)
#         # if isinstance(route, APIRoute):
#         api_list.append({
#             "name": route.name,
#             "path": route.path,
#             # "description": route.description
#         })
#     return api_list



@app.get("/")
async def root():
    return {"message": "Hello World"}


def get_all_routes():
    return all_routes

get_api_list()
app.include_router(router)


class MyOpenAI:
    def get_current_weather(location, unit="섭씨"):
        weather_info = {
            "location": location,
            "temperature": "24",
            "unit": unit,
            "forecast": ["sunny", "windy"],
        }
        return weather_info

    def chat(ask: str = "지금 서울날씨를 섭씨로 알려줘."):
        print("ask : ", ask)
        messages = [{"role": "user", "content": ask}]
        functions = [
            {
                "name": "get_current_weather",
                "description": "특정 지역의 날씨를 알려줍니다.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "지역이름 eg. 서울, 부산, 제주도",
                        },
                        "unit": {"type": "string", "enum": ["섭씨", "화씨"]},
                    },
                    "required": ["location"],
                },
            },
            {
                "name": "get_all_routes",
                "description": "현재 서버에 등록된 API 목록을 보여줍니다.",
                "parameters": {"type": "object", "properties": {}},
            },
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions,
            function_call="auto",
            )
        response_message = response["choices"][0]["message"]

        print("response_message1 : ", response_message)

        if response_message.get("function_call"):
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "get_all_routes": get_all_routes,
                "get_current_weather": MyOpenAI.get_current_weather,
            }
            function_name = response_message["function_call"]["name"]
            fuction_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = ''
            if("get_current_weather" == function_name):
                function_response = fuction_to_call(
                    location=function_args.get("location"),
                    unit=function_args.get("unit"),
                )
            elif("get_all_routes" == function_name):
                function_response = fuction_to_call()
            else:
                raise Exception("Unknown function name")
            
            messages.append(response_message)
            messages.append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(function_response),
                }
            )
            
            print("\n second : ", messages)
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=messages,
            )  # get a new response from GPT where it can see the function response

            json_data = json.dumps(second_response, ensure_ascii=False)

            print("second_response : ", second_response)
            print("second_response message : ", second_response.choices[0].message.content)


app = FastAPI()
# MyOpenAI.chat('지금 서울날씨를 알려줘')
MyOpenAI.chat('서버에 등록된 API 목록')

# curl http://localhost:8000/?prompt="지금 서울날씨를 섭씨로 알려줘.""


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)