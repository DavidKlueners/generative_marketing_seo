import chainlit as cl
from runnables import prompt_input_chain, seo_keyword_generator_runnable
import asyncio  # Required for asynchronous sleep
from link_processing import fetch_page_content, extract_text_from_html
from typing import Literal


async def add_links_to_task_list(links, task_list):
    link_tasks_dict = {}
    for link in links:
        link_task = cl.Task(
            title=f"Checking website: {link}", status=cl.TaskStatus.READY
        )
        await task_list.add_task(link_task)
        link_tasks_dict[link] = link_task
    await task_list.send()
    return link_tasks_dict


async def process_individual_link(link, task_list):
    content, headers = await fetch_page_content(link)
    text = await extract_text_from_html(content)
    seo_keywords = await seo_keyword_generator_runnable.ainvoke(
        input={"html_input": text}
    )
    return seo_keywords


async def process_links(links, task_list):
    """
    Function to process the list of links.
    """
    # Add links to task list and get the dictionary of tasks
    link_tasks_dict = await add_links_to_task_list(links, task_list)
    keywords = []
    # Simulate processing for each link
    for link in links:
        link_task = link_tasks_dict[link]
        link_task.status = cl.TaskStatus.RUNNING
        await task_list.send()
        keywords.append(await process_individual_link(link=link, task_list=task_list))
        link_task.status = cl.TaskStatus.DONE
        await task_list.send()
    print(keywords)


async def get_user_input(
    question_for_user: str, task, task_list, optional_input: bool = False
):
    while True:
        res = await cl.AskUserMessage(
            content=question_for_user,
        ).send()
        if res:
            urls = res["output"].split(",")
            urls = [url.strip() for url in urls]

            await cl.Message(
                content=f"The input you provided is: {urls}.",
            ).send()

            # Define the base actions
            actions = [
                cl.Action(name="continue", value="continue", label="✅ Continue"),
                cl.Action(name="repeat", value="repeat", label="🔁 Repeat"),
            ]

            # Add the 'Skip' action only if optional_input is True
            if optional_input:
                actions.append(cl.Action(name="skip", value="skip", label="❌ Skip"))

            # Adapt the action message based on optional_input
            action_message_content = "If this input is correct, press 'Continue'! If you want to enter the input again, press 'Repeat'."
            if optional_input:
                action_message_content += (
                    " If you want to skip this optional input, press 'Skip'."
                )

            res = await cl.AskActionMessage(
                content=action_message_content,
                actions=actions,
            ).send()

            if res and res.get("value") == "continue":
                # Update the task statuses
                task.status = cl.TaskStatus.DONE
                await task_list.send()

                return urls

            if res and res.get("value") == "skip":
                # Update the task statuses
                task.status = cl.TaskStatus.DONE
                await task_list.send()

                return None


@cl.on_chat_start
async def main():
    # Create the TaskList
    task_list = cl.TaskList()
    task_list.status = "Running..."

    # ADDING TASKS THAT THE AI WILL GO THROUGH
    asking_task_1 = cl.Task(
        title="Asking for webpage to optimize...", status=cl.TaskStatus.RUNNING
    )
    await task_list.add_task(asking_task_1)

    asking_task_2 = cl.Task(
        title="Asking for competitor webpages to extract keywords from...",
        status=cl.TaskStatus.READY,
    )
    await task_list.add_task(asking_task_2)

    returning_task_3 = cl.Task(
        title="Returning competitor webpage keywords...", status=cl.TaskStatus.READY
    )
    await task_list.add_task(returning_task_3)

    asking_task_4 = cl.Task(
        title="Asking for additional keywords from the user...",
        status=cl.TaskStatus.READY,
    )
    await task_list.add_task(asking_task_4)

    creating_task_5 = cl.Task(
        title="Creating content based on keywords...", status=cl.TaskStatus.READY
    )
    await task_list.add_task(creating_task_5)

    returning_task_6 = cl.Task(
        title="Returning content based on keywords...", status=cl.TaskStatus.READY
    )
    await task_list.add_task(returning_task_6)

    # Update the task list in the interface
    await task_list.send()

    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )

    ## getting user input: their own website to optimize content for
    question_for_user = "Hi there, I am here to help you with the SEO content for your webpage. Please provide the webpage that you want to generate content for below:"
    webpage_url = await get_user_input(
        question_for_user=question_for_user,
        task=asking_task_1,
        task_list=task_list,
        optional_input=False,
    )
    asking_task_2.status = cl.TaskStatus.RUNNING
    await task_list.send()

    ## getting user input: competitor websites to extract keywords from
    question_for_user = "If you want, you can now provide relevant competitor webpages, separated by commata:"
    competitor_urls = await get_user_input(
        question_for_user=question_for_user,
        task=asking_task_2,
        task_list=task_list,
        optional_input=True,
    )
    returning_task_3.status = cl.TaskStatus.RUNNING
    await task_list.send()

    ## getting user input: focused keywords they want to optimize for
    

    # Call the dummy function to process links
    await process_links(webpage_url, task_list)
    returning_task_3.status = cl.TaskStatus.DONE
    task_list.status = "DONE"

    await task_list.send()

    ## Sending the SEO title for the webpage
    text_content = "### Hello, this is a text element showing the SEO title."
    elements = [cl.Text(content=text_content, display="inline")]

    await cl.Message(
        content="This could be your improved website content:",
        elements=elements,
    ).send()
    ## Sending the meta description for the webpage
    text_content = "### Hello, this is a text element showing the SEO meta description."
    elements = [cl.Text(content=text_content, display="inline")]

    await cl.Message(
        content="This could be your improved website content:",
        elements=elements,
    ).send()
    ## Sending the final improved website content.
    text_content = (
        "### Hello, this is a text element showing the final website content."
    )
    elements = [cl.Text(content=text_content, display="inline")]

    await cl.Message(
        content="This could be your improved website content:",
        elements=elements,
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
