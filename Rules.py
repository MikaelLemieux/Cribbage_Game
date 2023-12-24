import streamlit as st

def Rules():
    # Define cribbage rules
    basic_rules = [
        "Cribbage is a classic card game played with a standard 52-card deck.",
        "The game is typically played by 2 players, but variations exist for 3 or 4 players.",
        "The goal of cribbage is to be the first player to reach a set number of points, often 121.",
    ]

    deck_setup = [
        "A standard deck consists of 52 cards, with 4 suits (hearts, diamonds, clubs, spades) and 13 ranks (2-10, Jack, Queen, King, Ace).",
        "Players are dealt 6 cards each, and they choose 4 cards to keep and 2 to place in the 'crib' (a separate hand for the dealer).",
    ]

    playing_turns = [
        "Players take turns playing one card at a time from their hand.",
        "The non-dealer plays the first card, and the running total starts at 0.",
        "The player announces the total after playing a card, and the next player adds to it.",
        "If a player cannot play a card without exceeding 31 points, they say 'go,' and the other player continues.",
    ]

    scoring_rules = [
        "Points are scored for specific card combinations and actions:",
        "- **Pairs**: Pairs are worth 2 points. For example, two 5s would score 2 points.",
        "- **Runs**: A run is a sequence of consecutive cards. Runs are worth 1 point per card in the run. For example, 3-4-5 is worth 3 points.",
        "- **Fifteens**: A combination of cards that adds up to 15 is worth 2 points. For example, a 7 and an 8 would score 2 points.",
        "- **Flush**: A flush is when all cards in a player's hand (including the crib) are of the same suit. This is worth 4 points.",
        "- **Nobs**: If a player has a Jack in their hand that matches the suit of the starter card, they score 1 point.",
    ]

    winning_rules = [
        "The game is won by the first player to reach a set number of points, typically 121.",
    ]

    additional_rules = [
        "Cribbage has many additional rules and nuances:",
        "- The starter card is drawn after players discard to the crib.",
        "- Players must say 'go' if they cannot play a card without exceeding 31 points.",
        "- Players receive a point for each card played that brings the total to exactly 15.",
        "- The dealer gets to score the points in the crib, which can be an advantage.",
    ]

    # Streamlit UI layout
    st.title("Cribbage Rules")
    st.header("Basic Rules")
    for rule in basic_rules:
        st.write(rule)

    st.header("Deck Setup")
    for rule in deck_setup:
        st.write(rule)

    st.header("Playing Turns")
    for rule in playing_turns:
        st.write(rule)

    st.header("Scoring Rules")
    for rule in scoring_rules:
        st.markdown(rule)

    st.header("Winning the Game")
    for rule in winning_rules:
        st.write(rule)

    st.header("Additional Rules")
    for rule in additional_rules:
        st.write(rule)

    # You can add more rules, examples, or details as needed
if __name__ == '__main__':
    Rules()
