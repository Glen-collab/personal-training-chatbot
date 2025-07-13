import streamlit as st
import os
import glob
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA

# Set page config
st.set_page_config(
    page_title="Personal Training AI Assistant",
    page_icon="🏋️",
    layout="wide"
)

def load_all_books(folder_path: str = "."):
    """Load all text files from the specified folder"""
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    
    if not txt_files:
        st.error("❌ No .txt files found!")
        return None
    
    st.info(f"📚 Found {len(txt_files)} text files")
    
    all_content = []
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                book_name = os.path.basename(file_path).replace('.txt', '').replace('_UTF8', '')
                formatted_content = f"\n\n=== FROM BOOK: {book_name} ===\n\n{content}"
                all_content.append(formatted_content)
                st.success(f"✅ Loaded {book_name}")
        except Exception as e:
            st.error(f"❌ Error loading {file_path}: {e}")
    
    if all_content:
        combined_content = "\n\n".join(all_content)
        st.success(f"✅ Combined all books: {len(combined_content):,} characters")
        return combined_content
    return None

def create_qa_chain(content: str, api_key: str):
    """Create the Q&A chain"""
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(content)
    st.info(f"✅ Created {len(chunks)} chunks")
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(chunks, embeddings)
    
    # Create LLM and chain
    llm = OpenAI(temperature=0.7)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
    )
    
    return qa_chain

def main():
    st.title("🏋️ Personal Training AI Assistant")
    st.markdown("### Ask questions about training, nutrition, psychology, and more!")
    
    # API Key input
    with st.sidebar:
        st.header("🔑 Setup")
        api_key = st.text_input(
            "Enter your OpenAI API key:",
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys"
        )
    
    if not api_key:
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar")
        return
    
    # Initialize session state
    if "qa_chain" not in st.session_state:
        st.session_state.qa_chain = None
        st.session_state.setup_complete = False
    
    # Setup knowledge base
    if not st.session_state.setup_complete:
        st.header("📚 Setting up knowledge base...")
        
        content = load_all_books()
        if content:
            with st.spinner("Creating knowledge base..."):
                try:
                    qa_chain = create_qa_chain(content, api_key)
                    st.session_state.qa_chain = qa_chain
                    st.session_state.setup_complete = True
                    st.success("✅ Setup complete!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
                    return
    
    # Chat interface
    if st.session_state.setup_complete:
        st.header("💬 Ask Your Questions")
        
        question = st.text_input("Your question:", placeholder="Ask about training, nutrition, or motivation...")
        
        if st.button("Ask", type="primary") and question:
            with st.spinner("Thinking..."):
                try:
                    result = st.session_state.qa_chain({"query": question})
                    st.subheader("🤖 Answer:")
                    st.write(result['result'])
                except Exception as e:
                    st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
