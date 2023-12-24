import streamlit as st
import sqlite3
from datetime import date, datetime, timedelta
import random
from itertools import combinations
#from Auth import *
#from chat.main import chat

st.set_page_config(layout='wide')

# Database initialization
def initialize_database():
    conn = sqlite3.connect('cribbage.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Scores (
        user_id INTEGER,
        score INTEGER,
        date DATE
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Gameplay (
        user_id INTEGER,
        last_played_date DATE
    )
    ''')
    conn.commit()
    conn.close()

initialize_database()

def store_score(user_id, score):
    conn = sqlite3.connect('cribbage.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Scores (user_id, score, date) VALUES (?, ?, ?)", (user_id, score, date.today()))
    conn.commit()
    conn.close()

def retrieve_total_score(user_id):
    conn = sqlite3.connect('cribbage.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(score) FROM Scores WHERE user_id=? AND date=?", (user_id, date.today()))
    total_score = cursor.fetchone()[0]
    conn.close()
    return total_score if total_score else 0

# Add a function to get the last play date for a user
def get_last_played_date(user_id):
    conn = sqlite3.connect('cribbage.db')
    cursor = conn.cursor()
    cursor.execute("SELECT last_played_date FROM Gameplay WHERE user_id=?", (user_id,))
    last_played_date = cursor.fetchone()
    conn.close()
    return last_played_date

# Add a function to update the last played date for a user
def update_last_played_date(user_id):
    conn = sqlite3.connect('cribbage.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO Gameplay (user_id, last_played_date) VALUES (?, ?)",
                   (user_id, datetime.now().date().strftime('%Y-%m-%d')))
    conn.commit()
    conn.close()

# Leaderboards
def retrieve_leaderboard(period):
    conn = sqlite3.connect('cribbage.db')
    cursor = conn.cursor()

    if period == 'daily':
        cursor.execute("SELECT user_id, SUM(score) FROM Scores WHERE date=? GROUP BY user_id ORDER BY SUM(score) DESC LIMIT 10", (date.today(),))
    elif period == 'monthly':
        month = date.today().month
        cursor.execute("SELECT user_id, SUM(score) FROM Scores WHERE strftime('%m', date)=? GROUP BY user_id ORDER BY SUM(score) DESC LIMIT 10", (month,))
    else:  # yearly
        year = date.today().year
        cursor.execute("SELECT user_id, SUM(score) FROM Scores WHERE strftime('%Y', date)=? GROUP BY user_id ORDER BY SUM(score) DESC LIMIT 10", (year,))
    
    results = cursor.fetchall()
    conn.close()
    return results

# Achievements
def check_achievements(user_id):
    conn = sqlite3.connect('cribbage.db')
    cursor = conn.cursor()

    # Check Perfect Week
    perfect_week = False
    cursor.execute("SELECT DISTINCT date FROM Scores WHERE user_id=? AND date BETWEEN date('now', '-6 days') AND date('now')", (user_id,))
    if len(cursor.fetchall()) == 7:
        perfect_week = True

    # Cribbage Novice/Master
    cursor.execute("SELECT SUM(score) FROM Scores WHERE user_id=?", (user_id,))
    total_score = cursor.fetchone()[0]
    if total_score >= 1000:
        achievement = "Cribbage Master"
    elif total_score >= 500:
        achievement = "Cribbage Novice"
    else:
        achievement = None

    conn.close()
    return perfect_week, achievement

# Game functions
def generate_daily_community_card():
    random.seed(date.today().isoformat())
    all_cards = [(i, j) for i in range(1, 14) for j in range(1, 4)]
    community_card = random.choice(all_cards)
    return community_card

def generate_player_hand():
    all_cards = [(i, j) for i in range(1, 14) for j in range(1, 4)]
    random.shuffle(all_cards)
    hand_cards = all_cards[:6]
    return hand_cards

# Map numbers to card labels
def card_label(card):
    face_cards = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
    if card[0] in face_cards:
        card_name = face_cards[card[0]]
    else:
        card_name = str(card[0])
    
    suit = ['Spades', 'Hearts', 'Diamonds', 'Clubs'][card[1] - 1]
    return f"{card_name} of {suit}"

# New function to get the image path for each card
def card_image_path(card):
    face_cards = {1: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
    card_name = face_cards.get(card[0], str(card[0]))
    suit = ['Spades', 'Hearts', 'Diamonds', 'Clubs'][card[1] - 1]
    
    return f"card_images/{card_name}_of_{suit}.png"

#from cribbage_scorer import cribbage_scorer

def score_hand(selected_cards, community_card):
    # Convert your card notation to the library's notation
    def convert_card(card):
        value_conversion = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
        value = value_conversion.get(card[0], card[0])
        return int(value), card[1]

    starter = convert_card(community_card)
    hand = [convert_card(card) for card in selected_cards]
    crib = False

    score, msg = cribbage_scorer.show_calc_score(starter, hand, crib)
    return score, msg

def main_page():
    st.markdown("<h1 style='text-align: center;'>Cribbage Daily Challenge</h1>", unsafe_allow_html=True)

    st.sidebar.title("Instructions")

   # chat()

    # Default to not showing the challenge initially
    if "show_challenge" not in st.session_state:
        st.session_state.show_challenge = False

    # Toggle button to display/hide the challenge
    if st.sidebar.button("Toggle Cribbage Daily Challenge"):
        st.sidebar.markdown("""
        - A standard cribbage game is played with a deck of 52 cards.
        - Each player is dealt 6 cards.
        - From these 6 cards, select 4 to use in your hand.
        - The goal is to create combinations of cards that sum up to 15, or pairs, or runs.
        - Your hand is then scored based on these combinations, along with a randomly selected community card.
        - Try to achieve the highest score possible!
        """)
        st.session_state.show_challenge = not st.session_state.show_challenge

    if st.session_state.show_challenge:

        if st.sidebar.button("Show Leaderboard and Achievements"):
            st.write("Leaderboard:")
            daily_leaderboard = retrieve_leaderboard('daily')
            for rank, (user, score) in enumerate(daily_leaderboard, 1):
                st.write(f"{rank}. User {user}: {score} points")

            st.write("Achievements:")
            perfect_week, achievement = check_achievements(user_id)
            if perfect_week:
                st.write("Achievement Unlocked: Perfect Week!")
            if achievement:
                st.write(f"Achievement Unlocked: {achievement}!")

        cards = generate_player_hand()
        community_card = generate_daily_community_card()

        st.write("Your Hand:")

        if "locked_selection" not in st.session_state:
            st.session_state.locked_selection = []

        selected_cards = []

        cols = st.columns(len(cards))
        for col, card in zip(cols, cards):
            if card not in st.session_state.locked_selection:
                if col.checkbox(label="", value=False, key=card):
                    col.image(card_image_path(card), caption=card_label(card), width=150)
                    selected_cards.append(card)
                else:
                    col.image(card_image_path(card), caption=card_label(card), width=150)
            else:
                col.image(card_image_path(card), caption=card_label(card), width=150)
                selected_cards.append(card)

        if len(selected_cards) == 4 and not st.session_state.locked_selection:
            st.session_state.locked_selection = selected_cards.copy()

            community_col, score_col = st.columns(2)

            community_col.write("Community Card:")
            community_col.image(card_image_path(community_card), caption=card_label(community_card), width=150)

            hand_score, breakdown = score_hand(selected_cards, community_card)
            user_id = 1  # this seems to be hardcoded, you might want to fetch the actual user_id in production

            last_played_date = get_last_played_date(user_id)
            if last_played_date:
                last_played_date = datetime.strptime(last_played_date[0], '%Y-%m-%d')
                if last_played_date.date() == datetime.now().date():
                    st.write("Sorry, you've already played today. Come back tomorrow!")
                    return

            store_score(user_id, hand_score)

            score_col.write(f"Your score for this hand: {hand_score}")

            # Check the type of breakdown before iterating
            if isinstance(breakdown, dict):
                for key, value in breakdown.items():
                    if value != 0:
                        score_col.write(f"{key}: {value} points")
            else:
                score_col.write(breakdown)

            update_last_played_date(user_id)

            perfect_week, achievement = check_achievements(user_id)
            if perfect_week:
                st.write("Achievement Unlocked: Perfect Week!")
            if achievement:
                st.write(f"Achievement Unlocked: {achievement}!")

if __name__ == '__main__':
    main_page()
