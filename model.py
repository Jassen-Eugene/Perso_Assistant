from langchain_openai import ChatOpenAI
from speech_to_text import voice_to_text
from read_response import answer

class QueryHandler:
    def __init__(self, base_url, api_key, model_name, max_tokens=100):
        self.llm = ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model_name,
            max_tokens=max_tokens
        )
        self.personal_info_path = "personal_infos/perso1.md"
        self.commands = "musique, image, météo, religion, amour, études :"

    def _is_personal(self, text):
        prompt = (
            "Dans ce texte, est-ce que le locuteur parle d'une chose qui a rapport avec sa vie personnelle ? "
            "Si oui, dis juste OUI. Sinon, dis tout simplement NON : Voici le texte : " + text
        )
        result = self.llm.invoke(prompt)
        return "oui" in result.content.lower()

    def _is_question(self, text):
        prompt = (
            "Si la phrase suivante est une question, dis juste OUI. Sinon, dis tout simplement NON. "
            "Voici la phrase : " + text
        )
        result = self.llm.invoke(prompt)
        return "oui" in result.content.lower()

    def _reformulate_personal_info(self, text):
        prompt = (
            "Reformule cette information personnelle tout juste en une affirmation bien structurée "
            "à la première personne. Donne seulement la phrase : '" + text + "'"
        )
        result = self.llm.invoke(prompt)
        return result.content.strip()

    def _save_personal_info(self, sentence):
        with open(self.personal_info_path, "a", encoding="utf-8") as file:
            file.write("\n" + sentence + "\n")

    def _load_personal_info(self):
        try:
            with open(self.personal_info_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return ""

    def analyze_query(self, user_query):
        if self._is_personal(user_query):
            if not self._is_question(user_query):
                reformulated = self._reformulate_personal_info(user_query)
                self._save_personal_info(reformulated)
            context = self._load_personal_info() or "Aucun contexte."
            return [
                {"role": "system", "content": "Utilise le contexte qui me concerne pour me répondre précisément en une seule phrase à la deuxième personne (Tu)."},
                {"role": "user", "content": f"Contexte : {context}"},
                {"role": "user", "content": f"Question : {user_query}"}
            ]
        else:
            return user_query

    def execute(self):
        text = voice_to_text()
        analyzed_query = self.analyze_query(text)
        response = self.llm.invoke(
            "Réponds en un seul mot. La déclaration suivante a rapport à un unique thème parmi ces 6 éléments qui sont " +
            self.commands + text + ". Choisis-en un."
        )
        #print(analyzed_query)
        print(response.content)
        answer(response.content)
        return text, analyzed_query, response.content


if __name__ == "__main__":
    # Configuration
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = "YOUR_API_KEY"
    MODEL_NAME = "llama-3.3-70b-versatile"

    # Exécution
    handler = QueryHandler(base_url=BASE_URL, api_key=API_KEY, model_name=MODEL_NAME)
    handler.execute()
