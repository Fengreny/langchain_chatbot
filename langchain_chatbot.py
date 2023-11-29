# chatbot_service.py
from fastapi import FastAPI, HTTPException
from langchain.chains import LLMChain
from langchain.llms.openai import OpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from pydantic import BaseModel
import aioredis
import os

app = FastAPI()
openai_api_key = os.environ.get('OPENAI_API_KEY')

# 设置 OpenAI LLM
llm = OpenAI(model_name='text-davinci-003', temperature=0, openai_api_key=openai_api_key)
prompt_template = PromptTemplate(
    input_variables=["history", "user_input"],
    template="{history}\nHuman: {user_input}\nAI:"
)
chatgpt_chain = LLMChain(
    llm=llm,
    prompt=prompt_template,
    memory=ConversationBufferWindowMemory(),
)

class Message(BaseModel):
    user_id: str
    message: str

@app.on_event("startup")
async def startup_event():
    # 初始化 Redis 连接
    app.redis = await aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)

@app.on_event("shutdown")
async def shutdown_event():
    app.redis.close()
    await app.redis.wait_closed()

@app.post("/message")
async def post_message(message: Message):
    context = await app.redis.get(message.user_id) or ""
    # 移除 await
    response = chatgpt_chain.run(history=context, user_input=message.message)
    new_context = update_context(context, message.message, response)
    await app.redis.set(message.user_id, new_context)
    return {"response": response}


@app.get("/history/{user_id}")
async def get_history(user_id: str):
    context = await app.redis.get(user_id)
    if context is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"history": context}


def update_context(context: str, user_message: str, bot_response: str):
    new_dialogue = f"Human: {user_message}\nAI: {bot_response}\n"
    # 只有在用户的新消息不是上下文中的最后一条消息时，才更新上下文
    if not context.endswith(f"Human: {user_message}\n"):
        return context + new_dialogue
    return context


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
