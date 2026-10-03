import pandas as pd
import streamlit as st

from io import StringIO
from numpy.random import default_rng as rng

def create_list_cards(cards):
    list_cards = []
    list_str_cards = cards.split("\n")
    for k in list_str_cards:
        param_card = k.split(" · ")
        id = param_card[1]
        conditions = conditions_dict[param_card[2]]
        name = " ".join(param_card[3].split(" ")[:-1])
        level = param_card[3].split(" ")[-1]
        rarity = param_card[4]
        card_k = [id, conditions, name, level, rarity]
        list_cards.append(card_k)
    return list_cards

conditions_dict = {'★☆☆☆☆':"Very poor",'★★☆☆☆':"Poor", "★★★☆☆":'Good', "★★★★☆":'Very good', '★★★★★':'Mint'}

# ── Interface ──────────────────────────────────────────────────────────────────

uploaded_file = st.file_uploader("Choose a file", type="txt")

if uploaded_file is not None:
    data = StringIO(uploaded_file.getvalue().decode("utf-8"))
    cards = data.read()
    list_cards = create_list_cards(cards)
    df_cards = pd.DataFrame(list_cards, columns=["ID", "Condition", "Name", "Level", "Rarity"])

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        sort_condition = st.text_input("Condition")
    with col2:
        sort_name = st.text_input("Name")
    with col3:
        sort_level = st.text_input("Level")
    with col4:
        sort_rarity = st.text_input("Rarity")

    if sort_condition:
        df_cards = df_cards[df_cards["Condition"] == sort_condition]
    if sort_name:
        df_cards = df_cards[df_cards["Name"].str.contains(sort_name)]
    if sort_level:
        df_cards = df_cards[df_cards["Level"] == sort_level]
    if sort_rarity:
        df_cards = df_cards[df_cards["Rarity"] == sort_rarity]

    st.dataframe(df_cards)  