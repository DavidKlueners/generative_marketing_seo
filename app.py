import chainlit as cl
from runnables import prompt_input_chain
import asyncio  # Required for asynchronous sleep


async def process_links(links):
    """
    Dummy function to simulate processing of links.
    """
    # Simulate processing time
    await asyncio.sleep(5)  # Waits for 5 seconds


@cl.on_chat_start
async def main():
    # Create the TaskList
    task_list = cl.TaskList()
    task_list.status = "Running..."

    # ADDING TASKS THAT THE AI WILL GO THROUGH
    asking_task_1 = cl.Task(
        title="Asking for website links...", status=cl.TaskStatus.RUNNING
    )
    await task_list.add_task(asking_task_1)
    # Create another task that is in the ready state
    looking_task_2 = cl.Task(
        title="Looking through the websites...", status=cl.TaskStatus.READY
    )
    await task_list.add_task(looking_task_2)
    # Update the task list in the interface
    await task_list.send()

    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )

    while True:
        res = await cl.AskUserMessage(
            content="Please provide a comma separated list of website URLs here, the first one should be your own website, the other ones are relevant competitor websites.",
        ).send()
        if res:
            urls = res["output"].split(",")
            urls = [url.strip() for url in urls]

            await cl.Message(
                content=f"The website links you provided are: {urls}.",
            ).send()

            res = await cl.AskActionMessage(
                content="If these links are correct, press 'Continue'! If you want to enter them again, press 'Cancel'.",
                actions=[
                    cl.Action(name="continue", value="continue", label="✅ Continue"),
                    cl.Action(name="cancel", value="cancel", label="❌ Cancel"),
                ],
            ).send()

            if res and res.get("value") == "continue":
                # Update the task statuses
                asking_task_1.status = cl.TaskStatus.DONE
                looking_task_2.status = cl.TaskStatus.RUNNING
                await task_list.send()

                # Call the dummy function to process links
                await process_links(urls)
                looking_task_2.status = cl.TaskStatus.DONE
                task_list.status = "DONE"

                await task_list.send()

                break


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
