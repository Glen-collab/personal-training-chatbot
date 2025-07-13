import os
import json
import glob
from typing import List
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

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
        
    def load_all_books(self, folder_path: str = "."):
        """Load all text files from the specified folder"""
        # Find all .txt files in the folder
        txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
        
        if not txt_files:
            print("❌ No .txt files found in the folder!")
            return None
        
        print(f"📚 Found {len(txt_files)} text files:")
        for file in txt_files:
            print(f"  - {os.path.basename(file)}")
        
        all_content = []
        
        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Add a header to identify which book each section comes from
                    book_name = os.path.basename(file_path).replace('.txt', '').replace('_UTF8', '')
                    formatted_content = f"\n\n=== FROM BOOK: {book_name} ===\n\n{content}"
                    all_content.append(formatted_content)
                    print(f"✅ Loaded {book_name}: {len(content)} characters")
            except Exception as e:
                print(f"❌ Error loading {file_path}: {e}")
        
        if all_content:
            combined_content = "\n\n".join(all_content)
            print(f"✅ Combined all books: {len(combined_content)} total characters")
            return combined_content
        else:
            return None
    
    def process_content(self, content: str):
        """Split content into chunks and create embeddings"""
        print("📚 Processing all book content...")
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,  # Size of each chunk
            chunk_overlap=200,  # Overlap between chunks
            length_function=len,
        )
        
        chunks = text_splitter.split_text(content)
        print(f"✅ Created {len(chunks)} text chunks from all books")
        
        # Create vector store
        self.vectorstore = Chroma.from_texts(
            texts=chunks,
            embedding=self.embeddings,
            persist_directory="./chroma_db"  # Save locally
        )
        
        # Create Q&A chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 5}),  # Increased to 5 for better results
            return_source_documents=True
        )
        
        print("✅ Comprehensive knowledge base created successfully!")
    
    def ask_question(self, question: str):
        """Ask a question to your comprehensive training knowledge base"""
        if not self.qa_chain:
            return "❌ Please load and process your book content first!"
        
        try:
            # Get response from the chain
            result = self.qa_chain({"query": question})
            
            # Format the response
            response = f"""
🏋️ **Personal Training Assistant Response:**

{result['result']}

📖 **Based on your comprehensive training library**
"""
            return response
            
        except Exception as e:
            return f"❌ Error getting response: {e}"
    
    def save_knowledge_base(self):
        """Save the processed knowledge base"""
        if self.vectorstore:
            self.vectorstore.persist()
            print("✅ Knowledge base saved!")

def main():
    """Main function to run the chatbot"""
    print("🏋️ Personal Training Chatbot - Multi-Book Edition")
    print("=" * 50)
    
    # You'll need to get your OpenAI API key from: https://platform.openai.com/api-keys
    api_key = input("Enter your OpenAI API key: ").strip()
    
    if not api_key:
        print("❌ API key is required!")
        return
    
    # Initialize chatbot
    chatbot = PersonalTrainingChatbot(api_key)
    
    # Load all books from current directory
    print("\n🔍 Looking for text files in current directory...")
    content = chatbot.load_all_books()
    
    if not content:
        print("❌ No content loaded. Make sure you have .txt files in this folder.")
        return
    
    # Process all the books
    chatbot.process_content(content)
    chatbot.save_knowledge_base()
    
    print("\n🎉 Setup complete! Your chatbot now has access to all your training books.")
    print("Type 'quit' to exit.\n")
    
    # Chat loop
    while True:
        question = input("Ask a training question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 Thanks for using your Personal Training Assistant!")
            break
        
        if question:
            response = chatbot.ask_question(question)
            print(response)
            print("-" * 50)

if __name__ == "__main__":
    main()