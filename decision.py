from model import QueryHandler
from model_long import LLMExecutor
from musics import play_music
from image import ImageGenerator  
from langchain_openai import ChatOpenAI
from langchain.agents import tool, initialize_agent
from langchain.agents.agent_types import AgentType

# Initialisation de l'image generator
image_gen = ImageGenerator(
    cache_dir=r"C:\Users\maserati\.cache\huggingface\hub", use_gpu=False
    )

# Environnement LLM 
base_url = "https://api.groq.com/openai/v1"
api_key = "YOUR_API_KEY"
model_name = "llama-3.3-70b-versatile"

queryhandle = QueryHandler(
    base_url=base_url, api_key=api_key, model_name=model_name
    )

deep_answer = LLMExecutor(
    base_url=base_url, api_key=api_key, model_name=model_name
    )

llm = ChatOpenAI(
    base_url=base_url,
    api_key=api_key,
    model=model_name,
    max_tokens=1000
)

# Définition des Tools 
@tool
def musique_tool(text: str) -> str:
    """Extrait le titre et l'auteur d'une musique à partir d'un texte, puis joue la musique."""
    response = llm.invoke(
        "extrait le titre et l'auteur de la musique dans le texte suivant si tu les trouves. Dis-les simplement : " + text
    )
    play_music(response.content)
    return f"Musique jouée : {response.content}"

@tool
def image_tool(text: str) -> str:
    """Génère une image à partir d'une description."""
    image_gen.generate(text)
    return "Image générée."

@tool(description="Donne une réponse synthétisée à une question complexe nécessitant une analyse approfondie.")
def long_tool(demande: str) -> str:
    result = deep_answer.execute(demande)
    return f"Final Answer: {result}"


# Initialisation de l'agent
tools = [musique_tool, image_tool, long_tool]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=1
)

# Entrée utilisateur 
text, demand, demand_type = queryhandle.execute()

# Appel de l'agent 
agent.run(f"Voici une demande de type {demand_type} : {demand}. Texte associé : {text}")
