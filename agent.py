import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent, create_openai_tools_agent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import TavilySearchResults
from langchain_experimental.tools import PythonREPLTool
from database import rechercher_client, rechercher_produit
from finance import obtenir_cours_action, calculer_interet, convertir_devise
from tools.portefeuille import calculer_portefeuille

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

tools.append(Tool(
    name="calculer_portefeuille",
    func=calculer_portefeuille,
    description="Calcule la valeur totale d'un portefeuille d'actions. Entree : liste au format SYMBOLE:QUANTITE separes par | (ex: AAPL:10|GOOGL:5|MSFT:3)."
))

# ATTENTION SECURITE : cet outil execute du code arbitraire.
# Ne jamais utiliser en production sans sandbox.
python_repl = PythonREPLTool()
python_repl.description = (
    "Execute du code Python pour des calculs complexes ou traitements "
    "de donnees non couverts par les autres outils. "
    "Entree : code Python valide sous forme de chaine."
)
tools.append(python_repl)

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

memory_prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu es un assistant financier intelligent. Tu aides les utilisateurs avec leurs questions bancaires et financieres. Tu te souviens du contexte de la conversation."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])


def creer_agent(with_memory=False):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    if with_memory:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=memory_prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
    else:
        agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
    return agent_executor


def demo_memoire():
    # Scenario de demonstration C2 : 3 questions enchainees
    # Q1 : Donne-moi les infos du client Sophie Bernard
    #   -> L'agent recupere le profil VIP, solde 28 900e
    # Q2 : Quel produit lui recommandes-tu ?
    #   -> L'agent se souvient que c'est une cliente VIP
    # Q3 : Calcule le prix TTC et dis-moi si elle peut se le permettre
    #   -> L'agent se souvient du produit ET du solde

    agent = creer_agent(with_memory=True)
    questions = [
        "Donne-moi les infos du client Sophie Bernard",
        "Quel produit lui recommandes-tu ?",
        "Calcule le prix TTC et dis-moi si elle peut se le permettre",
    ]
    print("=== Demo memoire conversationnelle ===")
    for q in questions:
        print(f"\nVous : {q}")
        try:
            reponse = agent.invoke({"input": q})
            print(f"Agent : {reponse['output']}")
        except Exception as e:
            print(f"Erreur : {e}")


def main():
    print("=" * 50)
    print("Agent Financier")
    print("=" * 50)
    print("Tapez 'quit' pour quitter.")
    print("Tapez 'demo' pour la demo memoire.\n")

    agent = creer_agent()

    while True:
        question = input("Vous : ").strip()
        if question.lower() in ("quit", "exit", "q"):
            print("Au revoir !")
            break
        if question.lower() == "demo":
            demo_memoire()
            continue
        if not question:
            continue

        try:
            reponse = agent.invoke({"input": question})
            print(f"\nAgent : {reponse['output']}")
        except Exception as e:
            print(f"Erreur : {e}")


if __name__ == "__main__":
    main()
