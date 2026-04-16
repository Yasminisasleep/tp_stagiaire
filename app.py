import streamlit as st
from agent import creer_agent, tools

st.set_page_config(page_title="Agent Financier", layout="wide")
st.title("Agent Financier")

with st.sidebar:
    st.header("Outils disponibles")
    for tool in tools:
        st.write(f"- {tool.name}")
    if st.button("Reinitialiser la conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = creer_agent()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

question = st.chat_input("Posez votre question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            reponse = st.session_state.agent.invoke({"input": question})
            output = reponse["output"]
        except Exception as e:
            output = f"Erreur : {e}"
        st.write(output)
    st.session_state.messages.append({"role": "assistant", "content": output})
