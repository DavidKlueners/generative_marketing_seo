from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from config import (
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
)
from langchain.chains.openai_functions import (
    create_structured_output_runnable,
)

#### OpenAI model to use
model = ChatOpenAI(model=OPENAI_MODEL, temperature=OPENAI_TEMPERATURE)

#### Prompt input chain
prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant for the topic of SEO. Answer the following user question: {user_question}. Also include knowledge from the prior conversation history if necessary: {conversation_history}"
)
prompt_input_chain = prompt | model | StrOutputParser()
