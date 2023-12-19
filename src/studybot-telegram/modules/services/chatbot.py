import os

from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext

class ChatBot: 
    def __init__(self) -> None:
        os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_KEY')
        self.save_path = "src/studybot-telegram/data/index_data"
        self.take_path = "src/studybot-telegram/data/input_data"
        print('[+] Connect language model — all-MiniLM-L12-v2')
        self.embed_model = HuggingFaceBgeEmbeddings(model_name = "all-MiniLM-L12-v2")
    
    def build_vectors(self) -> None: 
        print('[+] Build a vector representation of the words... Please, wait')
        self.documents = SimpleDirectoryReader(self.take_path).load_data()
        self.service_context = ServiceContext.from_defaults(embed_model = self.embed_model)
        self.index = VectorStoreIndex.from_documents(documents = self.documents, service_context=self.service_context)
        self.index.storage_context.persist(persist_dir = self.save_path)
    
    async def query(self, request: str) -> str: 
        query_eng = self.index.as_query_engine()
        response: str = await query_eng.aquery('ответь на русском языке, ответь не отклоняясь от контекста. ' + request)
        return response

# def load_vectors(self):  # загрузка пространства (не работает)
#     storage_context = StorageContext.from_defaults(persist_dir=save_path)
#     index = load_index_from_storage(storage_context, embed_model=embed_model)