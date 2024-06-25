# You can find this code for Chainlit python streaming here (https://docs.chainlit.io/concepts/streaming/python)

import chainlit as cl  # importing chainlit for our app
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import tiktoken
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from utils.custom_retriver import CustomQDrant
#from starters import set_starters


load_dotenv()




RAG_PROMPT = """
CONTEXT:
{context}

QUERY:
{question}

Answer questions first based on provided context and if you can't find answer in provided context, use your previous knowledge. 
In your answer never mention phrases like Based on provided context, From the context etc.

At the end of each answer add CONTEXT CONFIDENCE tag -> answer vs. context similarity score -> faithfulness - answer in percent e.g. 85%.
Also add CONTEXT vs PRIOR tag: break answer to what you find in provided context and what you build from your prior knowledge.
"""

data_path = "data/airbnb_midterm.pdf"
docs = PyPDFLoader(data_path).load()
openai_chat_model = ChatOpenAI(model="gpt-4o", streaming=True) #gpt-4o

def tiktoken_len(text):
    tokens = tiktoken.encoding_for_model("gpt-4o").encode(
        text,
    )
    return len(tokens)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 200,
    chunk_overlap = 10,
    length_function = tiktoken_len,
)

split_chunks = text_splitter.split_documents(docs)

rag_prompt = ChatPromptTemplate.from_template(RAG_PROMPT)

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


qdrant_vectorstore = CustomQDrant.from_documents(
    split_chunks,
    embedding_model,
    location=":memory:",
    collection_name="air bnb data",
    score_threshold=0.3
    
)

qdrant_retriever = qdrant_vectorstore.as_retriever()

from operator import itemgetter
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

retrieval_augmented_qa_chain = (
    # INVOKE CHAIN WITH: {"question" : "<<SOME USER QUESTION>>"}
    # "question" : populated by getting the value of the "question" key
    # "context"  : populated by getting the value of the "question" key and chaining it into the base_retriever
    {"context": itemgetter("question") | qdrant_retriever, "question": itemgetter("question")}
    # "context"  : is assigned to a RunnablePassthrough object (will not be called or considered in the next step)
    #              by getting the value of the "context" key from the previous step
    | RunnablePassthrough.assign(context=itemgetter("context"))
    # "response" : the "context" and "question" values are used to format our prompt object and then piped
    #              into the LLM and stored in a key called "response"
    # "context"  : populated by getting the value of the "context" key from the previous step
    | {"response": rag_prompt | openai_chat_model, "context": itemgetter("context")}
)


"""@cl.author_rename
async def rename(orig_author: str):
    rename_dict = {"User": "You", "Chatbot": "Airbnb"}
    return rename_dict.get(orig_author, orig_author)"""



@cl.on_chat_start  # marks a function that will be executed at the start of a user session
async def start_chat():



    cl.user_session.set("chain", retrieval_augmented_qa_chain, )





@cl.on_message  # marks a function that should be run each time the chatbot receives a message from a user
async def main(message: cl.Message):
    chain = cl.user_session.get("chain")

    resp = await chain.ainvoke({"question" : message.content})
    source_documents = resp["context"] 

    text_elements = []  # type: List[cl.Text]

    resp_msg = resp["response"].content

    #print(source_documents)

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"

            # Create the text element referenced in the message
            #text_elements.append(
            #    cl.Text(content=source_doc.page_content, name="{}".format(source_name), display="side")
            #)
            text_elements.append(
                cl.Text(content=source_doc[0].page_content, name="{} (scr: {})".format(source_name, round(source_doc[1],2)), display="side")
            )
        source_names = [text_el.name for text_el in text_elements]

    if source_names:
        resp_msg += f"\n\nSources: {', '.join(source_names)}"
    else:
        resp_msg += "\nNo sources found"

    msg = cl.Message(content=resp_msg, elements=text_elements)

    #print(msg.content)
    await msg.send()


    """async for chunk in msg.content:
    
        if token := chunk.choices[0].delta.content or "":
            await msg.stream_token(token)

    await msg.update()"""

    #async for chunk in chain:
    #    if token:=
