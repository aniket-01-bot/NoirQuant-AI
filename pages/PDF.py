import os
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter


class ChatWithPDFUsingOpenAI:
    def __init__(self):
        load_dotenv()
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    def get_pdf_text(self, pdf_docs):
        text = ""
        for pdf in pdf_docs:
            reader = PdfReader(pdf)
            for page in reader.pages:
                text += page.extract_text()
        return text

    def get_text_chunks(self, text):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        return splitter.split_text(text)

    def get_vector_store(self, chunks):
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_texts(chunks, embedding=embeddings)
        db.save_local("faiss_index_pdf")

    def get_chain(self):
        prompt = PromptTemplate.from_template("""
        Answer the question based only on the context below.
        If answer not found, say "Not available".

        Context:
        {context}

        Question:
        {question}
        """)

        llm = ChatOpenAI(temperature=0.3)

        chain = create_stuff_documents_chain(llm, prompt)
        return chain

    def user_input(self, question):
        embeddings = OpenAIEmbeddings()

        db = FAISS.load_local(
            "faiss_index_pdf",
            embeddings,
            allow_dangerous_deserialization=True
        )

        docs = db.similarity_search(question)

        chain = self.get_chain()
        response = chain.invoke({
            "context": docs,
            "question": question
        })

        st.write("Reply:", response)

    def main(self):
        st.set_page_config(page_title="PDF Chat Bot")

        st.header("Chat with PDF (OpenAI Latest)")

        user_question = st.text_input("Ask a question")

        if user_question:
            self.user_input(user_question)

        with st.sidebar:
            pdf_docs = st.file_uploader("Upload PDFs", accept_multiple_files=True)

            if st.button("Submit & Process"):
                with st.spinner("Processing..."):
                    text = self.get_pdf_text(pdf_docs)
                    chunks = self.get_text_chunks(text)
                    self.get_vector_store(chunks)
                    st.success("Done")


if __name__ == "__main__":
    app = ChatWithPDFUsingOpenAI()
    app.main()