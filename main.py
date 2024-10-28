from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils import generate_response

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = generate_response(data)
            if data == "":
                response = "Please enter some text"
            await websocket.send_text(f"{response}")
    except WebSocketDisconnect:
        print("Client disconnected")


"""

Sample JS code to connect to the WebSocket server:
--------------------------------------------------

const ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.onopen = () => {
    console.log("Connected to WebSocket server");
};

ws.onmessage = (event) => {
    document.getElementById("response").innerText = event.data;
};

const input = document.getElementById("messageInput");
input.addEventListener("input", function(event) {

    ws.send(event.target.value)

});

ws.onclose = () => {
    console.log("Disconnected from WebSocket server");
};
"""

# uvicorn main:app --reload
