import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Float, Integer, text
from sqlalchemy.orm import declarative_base, sessionmaker
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_classic.tools import Tool
from langchain_classic.prompts import PromptTemplate

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///portfolio.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbole = Column(String, nullable=False)
    quantite = Column(Integer, nullable=False)
    prix_achat = Column(Float, nullable=False)
    secteur = Column(String)


Base.metadata.create_all(engine)


def init_sample_data():
    session = SessionLocal()
    count = session.execute(text("SELECT COUNT(*) FROM positions")).scalar()
    if count == 0:
        positions = [
            Position(symbole="AAPL", quantite=50, prix_achat=150.0, secteur="Tech"),
            Position(symbole="GOOGL", quantite=30, prix_achat=130.0, secteur="Tech"),
            Position(symbole="TSLA", quantite=20, prix_achat=200.0, secteur="Auto"),
            Position(symbole="MSFT", quantite=40, prix_achat=350.0, secteur="Tech"),
            Position(symbole="AMZN", quantite=15, prix_achat=170.0, secteur="E-commerce"),
        ]
        session.add_all(positions)
        session.commit()
    session.close()


init_sample_data()


def get_positions(query=""):
    session = SessionLocal()
    positions = session.query(Position).all()
    session.close()
    result = []
    for p in positions:
        result.append(f"{p.symbole} : {p.quantite} actions, prix achat {p.prix_achat}$, secteur {p.secteur}")
    return "\n".join(result) if result else "Aucune position trouvee."


def get_position_detail(symbole):
    symbole = symbole.upper().strip()
    session = SessionLocal()
    p = session.query(Position).filter(Position.symbole == symbole).first()
    session.close()
    if p:
        return f"{p.symbole} : {p.quantite} actions, prix achat {p.prix_achat}$, secteur {p.secteur}"
    return f"Pas de position pour {symbole}"


api_tools = [
    Tool(name="lister_positions", func=get_positions, description="Liste toutes les positions du portefeuille."),
    Tool(name="detail_position", func=get_position_detail, description="Detail d'une position par symbole. Entree : symbole (str)."),
]

API_PROMPT = """Tu es un analyste financier. Tu reponds aux questions sur le portefeuille d'investissement.

Outils : {tools}
Noms : {tool_names}

Format :
Thought: reflexion
Action: outil
Action Input: entree
Observation: resultat

Reponse finale :
Thought: j'ai la reponse
Final Answer: reponse

Question : {input}
{agent_scratchpad}"""

api_prompt = PromptTemplate(
    template=API_PROMPT,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
)


def creer_api_agent():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    agent = create_react_agent(llm=llm, tools=api_tools, prompt=api_prompt)
    return AgentExecutor(
        agent=agent, tools=api_tools, verbose=True,
        handle_parsing_errors=True, max_iterations=10
    )


app = FastAPI(title="Agent Portefeuille API")
agent_executor = creer_api_agent()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    answer: str


@app.post("/api/agent/query", response_model=QueryResponse)
def query_agent(req: QueryRequest):
    try:
        result = agent_executor.invoke({"input": req.question})
        return QueryResponse(question=req.question, answer=result["output"])
    except Exception as e:
        return QueryResponse(question=req.question, answer=f"Erreur : {str(e)}")


@app.get("/api/positions")
def list_positions():
    session = SessionLocal()
    positions = session.query(Position).all()
    session.close()
    return [{"symbole": p.symbole, "quantite": p.quantite, "prix_achat": p.prix_achat, "secteur": p.secteur} for p in positions]
