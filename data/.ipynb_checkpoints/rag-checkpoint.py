import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

with open("cleaned_docs.pkl", "rb") as f:
    cleaned_documents = pickle.load(f)


splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(cleaned_documents)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

faiss_index = FAISS.from_documents(chunks, embedding_model)

faiss_index.save_local("faiss_gym_index")
print(" FAISS index saved successfully from cleaned unified file.")
