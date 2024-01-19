import chainlit as cl
from runnables import prompt_input_chain


@cl.on_chat_start
def start_chat():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    async for token in prompt_input_chain.astream(input={"user_question": msg.content, "conversation_history" : message_history}):
        await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
