import streamlit as st

def WC():
    # Title and description
    st.title("Welcome to the Cribbage Suite of Games!")
    st.write("Experience the classic card game of cribbage in various exciting formats.")

    # Introduction and overview
    st.header("About Cribbage")
    st.write(
        "Cribbage is a timeless card game known for its combination of skill and luck. "
        "In this suite, you can enjoy different versions and variations of cribbage games. "
        "Whether you're a seasoned pro or new to cribbage, there's something for everyone."
    )

    # Game options
    st.header("Game Options")
    st.write("Choose from the following cribbage games:")

    # Game options list
    games = [
        "1. Standard 2-Player Cribbage",
        "2. 3-Player Cribbage",
        "3. 4-Player Cribbage",
        "4. Cribbage Variations",
    ]

    # Display game options
    st.markdown("\n".join(games))

    # Getting started
    st.header("Getting Started")
    st.write("To start playing, simply select a game option from the list above. Each game option will have its own set of rules and instructions to follow.")

    # About the suite
    st.header("About the Suite")
    st.write(
        "The Cribbage Suite of Games is designed to provide you with an enjoyable cribbage experience. "
        "You can play against friends, family, or even test your skills against computer opponents. "
        "Feel free to explore the different game modes and have fun!"
    )

    # Footer
    st.write("---")
    st.write("Created with ❤️ by Your Name")

    # You can customize this welcome page further by adding images, links, or additional information as needed.
if __name__ == "__main__":
    CR()