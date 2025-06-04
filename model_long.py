from langchain_openai import ChatOpenAI
from read_response import answer

class LLMExecutor:
    def __init__(self, base_url, api_key, model_name, max_tokens=1000):
        self.llm = ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model_name,
            max_tokens=max_tokens
        )

    def execute(self, text):
        response = self.llm.invoke(text)
        print(response.content)
        answer(response.content)
