import streamlit as st

def Game():
    st.title("Cribbage Game Embed")

    # Specify the URL to embed
    embed_url = "https://buddyboardgames.com/cribbage"

    # Create an iframe to embed the URL
    st.markdown(f'<iframe src="{embed_url}" width="800" height="600"></iframe>', unsafe_allow_html=True)

if __name__ == "__main__":
    Game()
