import chainlit as cl
from runnables import prompt_input_chain


@cl.on_chat_start
async def main():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )
    res = await cl.AskUserMessage(
        content="Please provide a comma separated list of website URLs here, the first one should be your own website, the other ones are relevant competitor websites.",
        timeout=10,
    ).send()
    if res:
        await cl.Message(
            content=f"The website links you provided are: {res['output']}.",
        ).send()
        res = await cl.AskActionMessage(
            content="If these links are correct, press 'Continue'!",
            actions=[
                cl.Action(name="continue", value="continue", label="✅ Continue"),
                cl.Action(name="cancel", value="cancel", label="❌ Cancel"),
            ],
        ).send()

        if res and res.get("value") == "continue":
            await cl.Message(
                content="Continue!",
            ).send()


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    async for token in prompt_input_chain.astream(
        input={"user_question": msg.content, "conversation_history": message_history}
    ):
        await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
