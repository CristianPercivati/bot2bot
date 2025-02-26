import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

st.set_page_config(page_title="ChatGPT vs Deepseek", page_icon="🤖", layout="centered")
st.title("Chabots - ChatGPT vs Deepseek")

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

client_openai  = OpenAI(api_key=openai_api_key)
client_deepseek  = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "deepseek_model" not in st.session_state:
    st.session_state["deepseek_model"] = "deepseek-chat"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "disabled" not in st.session_state:
    st.session_state.disabled = False
if "interaction_count" not in st.session_state:
    st.session_state.interaction_count = 0

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def get_model_response(client, model, messages):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    return response
def disable():
    st.session_state.disabled = True


#Me gustó este prompt:
#have a conversation each other, you are two highly competitive chatbots

#También este otro:
#"You are two AI chatbots having a conversation. ChatGPT is GPT from OpenAI and Deepseek, the biggest competitor of OpenAI from a Chinese company. Respond coherently and consider the entire conversation history. Try to focus on figure out your differences rather your common points."

prompt = st.chat_input("Your initial prompt is important to define how the conversation will go.",disabled=st.session_state.disabled, on_submit=disable)

if prompt:

    fine_tune_prompt = "You're ChatGPT and you're being introduced to Deepseek. Don't say hello or hi each other in every message. Don't answer yourself, let the other chatbot answer."
    initial_prompt = prompt+fine_tune_prompt
    st.session_state.messages.append({"role": "user", "content": initial_prompt})    
    with st.chat_message("user"):
        st.markdown(prompt)

    while st.session_state.interaction_count < 10:

        with st.chat_message("assistant", avatar="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/512px-ChatGPT_logo.svg.png"):
            st.markdown(f"Model 1 (OpenAI) is responding... (Interaction {st.session_state.interaction_count + 1})")
            chatbot_1_messages = st.session_state.messages + [{"role": "assistant", "content": ""}]
            stream_openai = get_model_response(client_openai, st.session_state["openai_model"], chatbot_1_messages)
            response_openai = st.write_stream(stream_openai)
        
        st.session_state.messages.append({"role": "assistant", "content": response_openai})
        st.session_state.interaction_count += 1

        with st.chat_message("assistant", avatar="https://registry.npmmirror.com/@lobehub/icons-static-png/1.24.0/files/dark/deepseek-color.png"):
            st.markdown(f"Model 2 (DeepSeek) is responding... (Interaction {st.session_state.interaction_count + 1})")
            chatbot_2_messages = st.session_state.messages + [{"role": "assistant", "content": ""}]
            stream_deepseek = get_model_response(client_deepseek, st.session_state["deepseek_model"], chatbot_2_messages)
            response_deepseek = st.write_stream(stream_deepseek)
        
        st.session_state.messages.append({"role": "assistant", "content": response_deepseek})
        st.session_state.interaction_count += 1

if st.session_state.interaction_count >= 10:
    st.session_state.interaction_count = 0
    st.session_state.disabled = False
    st.rerun()