from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from config import (
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
)
from langchain.chains.openai_functions import (
    create_structured_output_runnable,
)
from data_models import SEOKeywords, SEOMetadata

#### OpenAI model to use
model = ChatOpenAI(model=OPENAI_MODEL, temperature=OPENAI_TEMPERATURE)

#### Prompt input chain
prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant for the topic of SEO. Answer the following user question: {user_question}. Also include knowledge from the prior conversation history if necessary: {conversation_history}"
)
prompt_input_chain = prompt | model | StrOutputParser()


#### chain to generate SEO keywords
model_gpt4 = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
seo_keyword_generator_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                """
                You are extracting keywords from html, that can be used in website content to improve SEO.
                Use the following html to extract the keywords: {html_input}
                """
            ),
        ),
    ]
)
seo_keyword_generator_runnable = create_structured_output_runnable(
    SEOKeywords, model_gpt4, seo_keyword_generator_prompt
)

#### chain to generate SEO metadata based on keywords
model_gpt4 = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
seo_metadata_generator_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                """
                You are generating SEO metadata for a users webpage based on user provided keywords, competitor keywords and the webpage content.
                User provided keyowrds: {user_keywords}
                Competitor keywords: {competitor_keywords}
                Webpage content: {webpage_content}
                """
            ),
        ),
    ]
)
seo_metadata_generator_runnable = create_structured_output_runnable(
    SEOMetadata, model_gpt4, seo_metadata_generator_prompt
)
