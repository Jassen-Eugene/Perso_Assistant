from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage
import json
import os
from datetime import datetime

class PersistentMemory(ConversationBufferMemory):
    def __init__(self, memory_file, **kwargs):
        super().__init__(**kwargs)
        self._memory_file = memory_file
        self._load_memory()

    def _save_memory(self):
        messages = []
        for m in self.chat_memory.messages:
            msg = m.dict()
            # Ajouter un timestamp s’il est absent
            if "timestamp" not in msg:
                msg["timestamp"] = datetime.utcnow().isoformat()
            messages.append(msg)

        with open(self._memory_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

    def _load_memory(self):
        if os.path.exists(self._memory_file):
            with open(self._memory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.chat_memory.messages = [
                    AIMessage(**m) if m['type'] == 'ai' else HumanMessage(**m)
                    for m in data
                ]

    def save_context(self, inputs, outputs):
        super().save_context(inputs, outputs)
        self._save_memory()

#  Configuration du LLM 
base_url = "https://api.groq.com/openai/v1"
api_key = "YOUR_API_KEY"
model_name = "llama-3.3-70b-versatile"

llm = ChatOpenAI(
    base_url=base_url,
    api_key=api_key,
    model=model_name,
    temperature=0
)

#  Initialisation mémoire avec timestamp 
memory = PersistentMemory(memory_file="conversation_history.json", return_messages=True)

#  Chaîne de conversation 
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

#  Interaction utilisateur 
while True:
    texte = input()
    response = conversation.predict(input=texte)
    print("Réponse :", response)

    #  Affichage de l'historique horodaté 
    for msg in memory.chat_memory.messages:
        timestamp = msg.__dict__.get("timestamp", "⏱️ Inconnu")
        print(f"[{timestamp}] {msg.type.upper()}: {msg.content}")
