import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from langchain_community.tools import TavilySearchResults
from database import rechercher_client, rechercher_produit
from finance import obtenir_cours_action, calculer_interet, convertir_devise

load_dotenv()

tools = [
    Tool(
        name="rechercher_client",
        func=rechercher_client,
        description="Recherche un client par son nom. Entrée : nom du client (str)."
    ),
    Tool(
        name="rechercher_produit",
        func=rechercher_produit,
        description="Recherche un produit financier par son nom. Entrée : nom du produit (str)."
    ),
    Tool(
        name="obtenir_cours_action",
        func=obtenir_cours_action,
        description="Récupère le cours actuel d'une action. Entrée : symbole boursier (str, ex: AAPL, GOOGL)."
    ),
    Tool(
        name="calculer_interet",
        func=lambda x: calculer_interet(*x.split(",")),
        description="Calcule les intérêts composés. Entrée : montant,taux,durée (séparés par des virgules)."
    ),
    Tool(
        name="convertir_devise",
        func=lambda x: convertir_devise(*x.split(",")),
        description="Convertit un montant entre devises. Entree : montant,devise_source,devise_cible (separes par des virgules)."
    ),
]

tavily_tool = TavilySearchResults(
    max_results=3,
    description="Recherche sur le web des informations financieres, actualites, resultats d'entreprises. Entree : question ou mots-cles."
)
tools.append(tavily_tool)

PROMPT_TEMPLATE = """Tu es un assistant financier intelligent. Tu aides les utilisateurs avec leurs questions bancaires et financières.

Tu as accès aux outils suivants :
{tools}

Noms des outils : {tool_names}

Pour utiliser un outil, utilise le format suivant :

Thought: réfléchis à ce que tu dois faire
Action: nom_de_l_outil
Action Input: entrée de l'outil
Observation: résultat de l'outil

Quand tu as la réponse finale :

Thought: j'ai la réponse
Final Answer: ta réponse complète

Question : {input}

{agent_scratchpad}"""

prompt = PromptTemplate(
    template=PROMPT_TEMPLATE,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
)


def creer_agent():
    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0,
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )
    return agent_executor


def main():
    print("=" * 50)
    print("Agent Financier")
    print("=" * 50)
    print("Tapez 'quit' pour quitter.\n")

    agent = creer_agent()

    while True:
        question = input("Vous : ").strip()
        if question.lower() in ("quit", "exit", "q"):
            print("Au revoir !")
            break
        if not question:
            continue

        try:
            reponse = agent.invoke({"input": question})
            print(f"\nAgent : {reponse['output']}")
        except Exception as e:
            print(f"Erreur : {e}")


if __name__ == "__main__":
    main()
