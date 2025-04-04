from flask import Blueprint, jsonify, request
from langchain_ollama import ChatOllama
from langchain.schema import AIMessage, HumanMessage, SystemMessage

llm = ChatOllama(
    model="tinyllama",
    temperature=0,
)

chat_history = []


bp = Blueprint('chat', __name__)


@bp.post("/")
def llm_chat():
    body = request.get_json()

    prompt = "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise."

    system_message = SystemMessage(content=prompt)
    chat_history.append(system_message)

    chat_history.append(HumanMessage(content=body["query"]))

    result = llm.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))

    return jsonify({
        "ai_response": response
    })
