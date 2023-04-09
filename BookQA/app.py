import os

# for loading docs
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# for embeddings
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone

# for answers from llm
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

# loading docs
loader = UnstructuredPDFLoader("data/field-guide-to-data-science.pdf")

data = loader.load()

print(f"Number of docs in data: {len(data)}")
print(f"Number of documents in data: {len(data[0].page_content)}")

# splitting docs
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(data)

print(f"New number of documents: {len(texts)}")

# embeddings and indexing
embeddings = OpenAIEmbeddings()

PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_API_ENV = os.environ["PINECONE_API_ENV"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment=PINECONE_API_ENV
)
index_name = "book-qa"

# searching through docs
docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)

# llm and chain
llm = OpenAI(temperature=0)
chain = load_qa_chain(llm, chain_type="stuff")

# query
query = input("Question: ")
docs = docsearch.similarity_search(query, include_metadata=True)

# answer
result = chain.run(input_documents=docs, question=query)
print(result)