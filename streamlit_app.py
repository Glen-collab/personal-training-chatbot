import streamlit as st
import os
import glob
from typing import List
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# Set page config
st.set_page_config(
    page_title="Personal Training AI Assistant",
    page_icon="🏋️",
    layout="wide"
)

class PersonalTrainingChatbot:
    def __init__(self, openai_api_key: str):
        """Initialize the chatbot with OpenAI API key"""
        self.openai_api_key = openai_api_key
        os.environ["OPENAI_API_KEY"] = openai_api_key
        
        # Initialize components
        self.embeddings = OpenAIEmbeddings()
        self.llm = OpenAI(temperature=0.7)
        self.vectorstore = None
        self.qa_chain = None
        
    @st.cache_data
    def load_all_books(_self, folder_path: str = "."):
        """Load all text files from the specified folder"""
        # Find all .txt files in the folder
        txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
        
        if not txt_files:
            st.error("❌ No .txt files found in the folder!")
            return None
        
        st.info(f"📚 Found {len(txt_files)} text files")
        
        all_content = []
        
        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Add a header to identify which book each section comes from
                    book_name = os.path.basename(file_path).replace('.txt', '').replace('_UTF8', '')
                    formatted_content = f"\n\n=== FROM BOOK: {book_name} ===\n\n{content}"
                    all_content.append(formatted_content)
                    st.success(f"✅ Loaded {book_name}: {len(content):,} characters")
            except Exception as e:
                st.error(f"❌ Error loading {file_path}: {e}")
        
        if all_content:
            combined_content = "\n\n".join(all_content)
            st.success(f"✅ Combined all books: {len(combined_content):,} total characters")
            return combined_content
        else:
            return None
    
    def process_content(self, content: str):
        """Split content into chunks and create embeddings"""
        with st.spinner("📚 Processing all book content..."):
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            
            chunks = text_splitter.split_text(content)
            st.info(f"✅ Created {len(chunks)} text chunks from all books")
            
            # Create vector store
            self.vectorstore = Chroma.from_texts(
                texts=chunks,
                embedding=self.embeddings,
                persist_directory="./chroma_db"
            )
            
            # Create Q&A chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),
                return_source_documents=True
            )
            
            st.success("✅ Comprehensive knowledge base created successfully!")
    
    def ask_question(self, question: str):
        """Ask a question to your comprehensive training knowledge base"""
        if not self.qa_chain:
            return "❌ Please load and process your book content first!"
        
        try:
            with st.spinner("🤔 Thinking..."):
                # Get response from the chain
                result = self.qa_chain({"query": question})
                return result['result']
                
        except Exception as e:
            return f"❌ Error getting response: {e}"

def main():
    """Main Streamlit app"""
    
    # Title and description
    st.title("🏋️ Personal Training AI Assistant")
    st.markdown("### Ask questions about training, nutrition, psychology, and more!")
    st.markdown("*Powered by comprehensive training knowledge base*")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("🔑 Setup")
        api_key = st.text_input(
            "Enter your OpenAI API key:",
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys"
        )
        
        if api_key:
            st.success("✅ API key provided!")
        else:
            st.warning("⚠️ Please enter your OpenAI API key to continue")
            st.stop()
    
    # Initialize chatbot
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = None
        st.session_state.knowledge_loaded = False
    
    # Load knowledge base
    if not st.session_state.knowledge_loaded and api_key:
        with st.expander("📚 Loading Knowledge Base", expanded=True):
            chatbot = PersonalTrainingChatbot(api_key)
            content = chatbot.load_all_books()
            
            if content:
                chatbot.process_content(content)
                st.session_state.chatbot = chatbot
                st.session_state.knowledge_loaded = True
                st.rerun()
    
    # Chat interface
    if st.session_state.knowledge_loaded:
        st.header("💬 Ask Your Training Questions")
        
        # Example questions
        with st.expander("💡 Example Questions"):
            st.markdown("""
            - What's the most effective way to build muscle?
            - How do I overcome self-sabotage with my fitness goals?
            - What are the biggest mistakes people make in the gym?
            - How does social media affect body image and training?
            - What's your philosophy on progressive overload?
            - How do I stay motivated when I don't see results?
            """)
        
        # Chat input
        question = st.text_input(
            "Your question:",
            placeholder="Ask me about training, nutrition, psychology, or motivation..."
        )
        
        if st.button("Ask Question", type="primary") and question:
            with st.container():
                st.subheader("🤖 Response:")
                response = st.session_state.chatbot.ask_question(question)
                st.write(response)
                
                # Add to chat history
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                
                st.session_state.chat_history.append({
                    "question": question,
                    "response": response
                })
        
        # Chat history
        if "chat_history" in st.session_state and st.session_state.chat_history:
            st.header("📝 Chat History")
            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):  # Show last 5
                with st.expander(f"Q: {chat['question'][:50]}..."):
                    st.write(f"**Question:** {chat['question']}")
                    st.write(f"**Answer:** {chat['response']}")
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with Streamlit and powered by OpenAI*")

if __name__ == "__main__":
    main()
