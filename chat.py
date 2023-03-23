from revChatGPT.V1 import Chatbot
from fastapi import FastAPI, Body
import uvicorn

app = FastAPI()

HOST = "0.0.0.0"
PORT = 8006

chatbot = Chatbot(config={
    "email": "<your email>",
    "password": "your password"
})



@app.post("/chat")
async def chatGPT(body: dict = Body(...)):
    prompt = body["text"]
    session = body["session"]
    print("User({}): {}".format(session, prompt))
    print("Chatbot: ", end="")
    try:
        answer = ""
        for data in chatbot.ask(
            prompt,
            conversation_id=chatbot.config.get("conversation"),
            parent_id=chatbot.config.get("parent_id"),
        ):
            message = data["message"][len(answer):]
            print(message, end="", flush=True)
            answer = data["message"]
        print()
        response = {"text": answer, "session": session}
        return {"data": response}
    except:
        answer = "ERROR"
        pass
    response = {"text": answer, "session": session}
    return {"data": response}

@app.post("/reset")
async def reset_chat():
    chatbot.reset_chat()
    return {"message": "OK"}



if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
