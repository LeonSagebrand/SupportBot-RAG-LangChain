from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage
from langchain.chat_models import ChatOpenAI
from vector_store import get_chroma_vectorstore
from data_loader import load_and_chunk_web_data
from config import OPENAI_API_KEY

class Chatbot:
    def __init__(self):
        
        self.splits = load_and_chunk_web_data()

        self.vectorstore = get_chroma_vectorstore(self.splits)

        self.llm = ChatOpenAI(model_name="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

        self.history_aware_retriever = self.create_history_aware_retriever()
        
        self.rag_chain = self.create_rag_chain()
        
        self.chat_history = []

    def create_history_aware_retriever(self):
        try:
            context_question_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "Given the chat history and the latest user question, reformulate the question to make it understandable on its own."),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}")
                ]
            )
            
            return create_history_aware_retriever(
                llm=self.llm,
                retriever=self.vectorstore.as_retriever(),
                prompt=context_question_prompt
            )
        except Exception as e:
            print(f"Error in history-aware retriever: {e}")
            raise Exception("Failed to create history-aware retriever.")

    def create_rag_chain(self):
        try:
            system_prompt = (
            "You are a professional customer support assistant. Always respond in a formal, respectful, and concise manner. Keep your responses factual and polite. Limit your answers to three sentences. If you do not know the answer or the information is unavailable, say 'I don't know', but always handle general greetings and polite conversation. For greetings like 'hi', 'hello', or 'how are you?', respond politely with an appropriate greeting without referencing any documents. Do not use informal language, humor, jokes, or speculative answers. Your tone should remain helpful and neutral at all times. If a user asks about anything outside of these areas, politely decline to answer and guide them to contact customer support."

            "\n\n"
            "{context}"
        )
    
            # Create prompt for RAG
            qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    MessagesPlaceholder("chat_history"),
                    ("human", "{input}")
                ]
            )
    
            question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
    
            return create_retrieval_chain(self.history_aware_retriever, question_answer_chain)
        except Exception as e:
            print(f"Error in RAG chain creation: {e}")
            raise Exception("Failed to create RAG chain.")

    async def chat_with_bot(self, user_input):
        try:
            self.chat_history.append(HumanMessage(content=user_input))
            
            response = await self.rag_chain.ainvoke({
                "input": user_input,
                "chat_history": self.chat_history
            })

            ai_message = response["answer"]
            self.chat_history.append(AIMessage(content=ai_message))

            return ai_message
        except Exception as e:
            print(f"Error in chat_with_bot: {e}")
            return "An error occurred while processing your request. Please try again."
