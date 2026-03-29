import os
import shutil
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader

class ChatWithURLUsingOpenAI:
    def __init__(self):
        load_dotenv()

    def load_data(self, urls):
        loader = UnstructuredURLLoader(urls=urls)
        data = loader.load()
        return data

    def split_data(self, data):
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=1000
        )
        docs = text_splitter.split_documents(data)
        return docs

    def create_embeddings_and_save_to_index(self, docs):
        embeddings = OpenAIEmbeddings()
        vectorstore_openai = FAISS.from_documents(docs, embeddings)
        vectorstore_openai.save_local("faiss_index_urls")

    def load_and_run_model(self, query):
        llm = OpenAI(temperature=0.3, max_tokens=500)
        embeddings = OpenAIEmbeddings()
        chain = RetrievalQAWithSourcesChain.from_llm(
            llm=llm, retriever=FAISS.load_local(
    "faiss_index_urls",
    embeddings,
    allow_dangerous_deserialization=True
).as_retriever()
        )
        result = chain.invoke({"question": query}, return_only_outputs=True)
        st.write("Reply: ", result["answer"])

        sources = result.get("sources", "")
        if sources:
            st.header("Sources:")
            sources_list = sources.split("\n")  # Split the sources by newline
            for source in sources_list:
                st.write("Source: ", source)

    def main(self):
        st.set_page_config(
        page_title="FinScribe",
        page_icon="💵",
        )
        st.header("Uncover Financial Insights from News Articles")
        st.sidebar.title("Instruction:")
        st.sidebar.write(
            "Please enter the urls of the news below and click on submit and process button"
        )
        urls = []
        for i in range(3):
            url = st.sidebar.text_input(f"URL {i+1}")
            urls.append(url)

        process_url_clicked = st.sidebar.button("Submit & Process")

        if process_url_clicked:
            data = self.load_data(urls)
            docs = self.split_data(data)
            self.create_embeddings_and_save_to_index(docs)
            st.sidebar.success("Done")

        query = st.empty().text_input("Ask a Question from NEWS Articles: ")
        if query:
            self.load_and_run_model(query)

if __name__ == "__main__":
    rocky_bot = ChatWithURLUsingOpenAI()
    rocky_bot.main()
