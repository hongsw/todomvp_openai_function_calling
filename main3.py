from fastapi import FastAPI, Request
import json
from myopenai import MyOpenAI
from TodoModel import Todo

app = FastAPI()
todos = []
all_routes = []
logger = []



@app.get("/")
async def root():
    return {"message": "Hello World"}

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

@app.get("/todos", description="할 일 목록을 조회합니다.")
async def get_todos():
    return todos

@app.get("/all_routes")
async def get_all_routes():
    return all_routes   

def _get_all_routes():
    return all_routes   

@app.get("/logger")
async def get_all_routes():
    return json.dumps(logger)

def get_api_list():
    reserved_routes = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]
    for route in app.routes:
        if(route.path not in reserved_routes):
            # get route's method

            if('POST' in route.methods or 'PUT' in route.methods ):
                if route.name is not None:
                    # version = getattr(route.endpoint, "_api_version", (2, 0))
                    # all_routes.append("/v" + str(version[0]) + route.path)
                    all_routes.append(route.path)
                    param_names = [param.name for param in route.dependant.path_params]                    
                    print(f"Path: {route.path}, Methods: {route.methods}, Params: {param_names}")


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     # start_time = time.time()
#     response = await call_next(request)
#     # process_time = time.time() - start_time
#     # response.headers["X-Process-Time"] = str(process_time)
#     # 응답이 200이면 
#     if(response.status_code == 200):
#         # method post, put 만
#         if(request.method == 'POST' or request.method == 'PUT'):
#             # print(request)
#             logger.append(request.url.path)
#     return response


@app.get("/chat")
async def chat(prompt: str = "지금 서울날씨를 섭씨로 알려줘.", output: str = "chat"):
    print('chat : ', prompt)
    return await MyOpenAI.chat(prompt, output)


get_api_list()
openapi_schema = app.openapi()
def get_openapi():
    return openapi_schema
