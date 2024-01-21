import chainlit as cl
from runnables import (
    prompt_input_chain,
    seo_keyword_generator_runnable,
    seo_metadata_generator_runnable,
    webpage_improvement_runnable,
)
import asyncio  # Required for asynchronous sleep
from link_processing import (
    fetch_page_content,
    extract_text_from_html,
    extract_md_from_webpage,
)
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
    # link_tasks_dict = await add_links_to_task_list(links, task_list)
    keywords = []
    # Simulate processing for each link
    for link in links:
        # link_task = link_tasks_dict[link]
        # link_task.status = cl.TaskStatus.RUNNING
        # await task_list.send()
        keywords.append(await process_individual_link(link=link, task_list=task_list))
        # link_task.status = cl.TaskStatus.DONE
        # await task_list.send()
    return keywords


async def get_user_input(
    question_for_user: str, task, task_list, optional_input: bool = False
):
    while True:
        actions = [cl.Action(name="input", value="input", label="💬 Enter Input")]

        if optional_input:
            actions.append(cl.Action(name="skip", value="skip", label="❌ Skip"))

        res = await cl.AskActionMessage(
            content=question_for_user, actions=actions, timeout=6000
        ).send()

        # Handle the skip action
        if res and res.get("value") == "skip":
            task.status = cl.TaskStatus.DONE
            await task_list.send()
            return None

        # If user wants to enter input, ask for it
        if res and res.get("value") == "input":
            res = await cl.AskUserMessage(content="Please enter your input:").send()

            if res:
                urls = res["output"].split(",")
                urls = [url.strip() for url in urls]

                await cl.Message(
                    content=f"The input you provided is: {urls}.",
                ).send()

                actions = [
                    cl.Action(name="continue", value="continue", label="✅ Continue"),
                    cl.Action(name="repeat", value="repeat", label="🔁 Repeat"),
                ]

                res = await cl.AskActionMessage(
                    content="If this input is correct, press 'Continue'! If you want to enter the input again, press 'Repeat'.",
                    actions=actions,
                ).send()

                if res and res.get("value") == "continue":
                    task.status = cl.TaskStatus.DONE
                    await task_list.send()
                    return urls


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

    creating_task_6 = cl.Task(
        title="Creating SEO metadata based on keywords...", status=cl.TaskStatus.READY
    )
    await task_list.add_task(creating_task_6)

    creating_task_7 = cl.Task(
        title="Creating webpage content based on keywords and SEO metadata...",
        status=cl.TaskStatus.READY,
    )
    await task_list.add_task(creating_task_7)

    returning_task_8 = cl.Task(
        title="Returning content based on keywords...", status=cl.TaskStatus.READY
    )
    await task_list.add_task(returning_task_8)

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
    asking_task_1.status = cl.TaskStatus.DONE
    await task_list.send()

    ## returning webpage content as markdown
    markdown_content = await extract_md_from_webpage(webpage_url)
    elements = [cl.Text(content=markdown_content, display="inline")]

    await cl.Message(
        content="This is your current webpage content:",
        elements=elements,
    ).send()
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
    asking_task_2.status = cl.TaskStatus.DONE
    returning_task_3.status = cl.TaskStatus.RUNNING
    await task_list.send()

    if competitor_urls:
        ## returning the keywords extracted from competitor websites
        competitor_keyword_list = await process_links(competitor_urls, task_list)
        await cl.Message(
            content="This is a list of keywords extracted from the competitor websites your provided.",
        ).send()
        # Extract the list of keywords from each SEOKeywords object in the list and flatten into a single list
        all_keywords = [
            keyword
            for seo_keyword_obj in competitor_keyword_list
            for keyword in seo_keyword_obj.dict().get("seo_keywords", [])
        ]
        # Join the list of keywords into a single string
        competitor_keyword_list_string = ", ".join(all_keywords)
        await cl.Message(
            content=competitor_keyword_list_string,
        ).send()
        returning_task_3.status = cl.TaskStatus.DONE
        await task_list.send()
    else:
        competitor_keyword_list = []
        returning_task_3.status = cl.TaskStatus.FAILED
        await task_list.send()
    asking_task_4.status = cl.TaskStatus.RUNNING
    await task_list.send()

    ## getting user input: focused keywords they want to optimize for
    question_for_user = "If you want, you can now provide additional relevant keywords, separated by commata:"
    user_keywords = await get_user_input(
        question_for_user=question_for_user,
        task=asking_task_4,
        task_list=task_list,
        optional_input=True,
    )
    asking_task_4.status = cl.TaskStatus.DONE
    creating_task_5.status = cl.TaskStatus.RUNNING
    creating_task_6.status = cl.TaskStatus.RUNNING
    await task_list.send()

    ## generating metadata
    await task_list.send()
    metadata = await seo_metadata_generator_runnable.ainvoke(
        input={
            "user_keywords": user_keywords,
            "competitor_keywords": competitor_keyword_list,
            "webpage_content": markdown_content,
        }
    )
    creating_task_6.status = cl.TaskStatus.DONE
    creating_task_7.status = cl.TaskStatus.RUNNING
    await task_list.send()

    # generating content
    improved_content = await webpage_improvement_runnable.ainvoke(
        input={
            "user_keywords": user_keywords,
            "competitor_keywords": competitor_keyword_list,
            "seo_title": metadata.seo_title,
            "seo_description": metadata.seo_description,
            "webpage_content": markdown_content,
        }
    )
    creating_task_7.status = cl.TaskStatus.DONE
    creating_task_5.status = cl.TaskStatus.DONE
    await task_list.send()

    await cl.Message(
        content="The following is your improved SEO content:",
        elements=elements,
    ).send()

    ## Sending the SEO title for the webpage
    text_content = metadata.seo_title
    elements = [cl.Text(content=text_content, display="inline")]

    await cl.Message(
        content="This could be your seo title:",
        elements=elements,
    ).send()
    ## Sending the meta description for the webpage
    text_content = metadata.seo_description
    elements = [cl.Text(content=text_content, display="inline")]

    await cl.Message(
        content="This could be your metadata description:",
        elements=elements,
    ).send()
    ## Sending the final improved website content.
    text_content = improved_content.improved_website_content
    elements = [cl.Text(content=text_content, display="inline")]

    await cl.Message(
        content="This could be your improved website content:",
        elements=elements,
    ).send()

    returning_task_8.status = cl.TaskStatus.DONE
    # setting overall status to done
    task_list.status = "DONE"
    await task_list.send()


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
