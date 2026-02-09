from dotenv import load_dotenv
import argparse
import time
import os

from langchain_classic import hub

from langchain_mistralai import ChatMistralAI

from langchain_chroma import Chroma

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings.ovhcloud import OVHCloudEmbeddings

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_text_splitters import RecursiveCharacterTextSplitter

# access the environment variables from the .env file
load_dotenv()
MAX = 25
batch_size = 25
## Retrieve the OVHcloud AI Endpoints configurations
_OVH_AI_ENDPOINTS_ACCESS_TOKEN = os.environ.get('OVH_AI_ENDPOINTS_ACCESS_TOKEN') 
_OVH_AI_ENDPOINTS_MODEL_NAME = os.environ.get('OVH_AI_ENDPOINTS_MODEL_NAME') 
_OVH_AI_ENDPOINTS_URL = os.environ.get('OVH_AI_ENDPOINTS_URL') 
_OVH_AI_ENDPOINTS_EMBEDDING_MODEL_NAME = os.environ.get('OVH_AI_ENDPOINTS_EMBEDDING_MODEL_NAME')

# Function in charge to call the LLM model.
# Question parameter is the user's question.
# The function print the LLM answer.
def chat_completion(new_message: str):
  # no need to use a token
  model = ChatMistralAI(model=_OVH_AI_ENDPOINTS_MODEL_NAME, 
                        api_key=_OVH_AI_ENDPOINTS_ACCESS_TOKEN,
                        endpoint=_OVH_AI_ENDPOINTS_URL, 
                        max_tokens=1500, 
                        streaming=True)

  # Load documents from a local directory
  loader = DirectoryLoader(
     glob="**/*",
     path="./rag-files/",
     show_progress=True
  )
  docs = loader.load()

  # Split documents into chunks and vectorize them
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200,separators=["\n\n", "\n", "."])
  splits = text_splitter.split_documents(docs)

  if len(splits)>25:
    print("splits are: ",len(splits))
  vectorstore = Chroma.from_documents(documents=splits[:25], embedding=OVHCloudEmbeddings(model_name=_OVH_AI_ENDPOINTS_EMBEDDING_MODEL_NAME, access_token=_OVH_AI_ENDPOINTS_ACCESS_TOKEN))
  print(vectorstore)

  if len(splits)>25:
    print("splits are: ",len(splits))
    for i in range(batch_size, len(splits), batch_size):
        batch = splits[i:i+batch_size]
        vectorstore.add_documents(batch)
        print(i,"-->",batch_size)
  prompt = hub.pull("rlm/rag-prompt")

  rag_chain = (
    {"context": vectorstore.as_retriever(search_kwargs={"k": 1}), "question": RunnablePassthrough()}
    | prompt
    | model
  )

  print("🤖: ")
  for r in rag_chain.stream({"question", new_message}):
    print(r.content, end="", flush=True)
    time.sleep(0.150)

# Main entrypoint
def main():
  # User input
  parser = argparse.ArgumentParser()
  parser.add_argument('--question', type=str, default="What is the meaning of life?")
  args = parser.parse_args()
  chat_completion(args.question)

if __name__ == '__main__':
    main()