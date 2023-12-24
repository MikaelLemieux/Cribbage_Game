import streamlit as st

def Comp_Game():
    st.title("Comp Cribbage Game Embed")

    # Specify the URL to embed
    embed_url = "https://cribbage-online.net/"

    # Create an iframe to embed the URL
    st.markdown(f'<iframe src="{embed_url}" width="800" height="600"></iframe>', unsafe_allow_html=True)

if __name__ == "__main__":
    Comp_Game()
