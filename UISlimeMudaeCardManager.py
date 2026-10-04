import pandas as pd
import streamlit as st

from io import StringIO
from numpy.random import default_rng as rng

# ── Functions ──────────────────────────────────────────────────────────────────

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

def nbr_duplicate(cards, list_characters):
    dict_nbr_duplicate = {}
    for k in list_characters:
        dict_nbr_duplicate[k] = len(df_cards[df_cards["Name"].str.contains(k)])
    return dict_nbr_duplicate

conditions_dict = {'★☆☆☆☆':"Very poor",'★★☆☆☆':"Poor", "★★★☆☆":'Good', "★★★★☆":'Very good', '★★★★★':'Mint'}
list_characters = ['Ciel', 'Ivarage', 'Veldanava', 'Rimuru', 'Twilight', 'Michael', 'Demon', 'Guy', 'Milim', 'Veldora', 'Velzard', 'Velgrynd', 'Luminous', 'Diablo', 'Testarossa', 'Ultima', 'Carrera', 'Leon', 'Ramiris', 'Feldway', 'Zelanus', 'Zalario', 'Misery', 'Rain', 'Chloe', 'Hinata', 'Granbell', 'Dino', 'Dagruel', 'Gazel', 'Shizue', 'Masayuki', 'Granville', 'Kagali', 'Chronoa', 'Ifrit', 'Damrada', 'Moss', 'Benimaru', 'Shion', 'Souei', 'Hakurou', 'Shuna', 'Gabiru', 'Laplace', 'Clayman', 'Viola', 'Carrion', 'Frey', 'Yuuki', 'Beretta', 'Zegion', 'Apito', 'Kumara', 'Adalmann', 'Charybdis', 'Glenda', 'Orc', 'Elmesia', 'Youm', 'Mariabel', 'Hiiro', 'Gaia', 'Roy', 'Louis', 'Leonard', 'Arnaud', 'Saare', 'Jaine', 'Venom', 'Albis', 'Treyni', 'Gobta', 'Ranga', 'Rigurd', 'Kaijin', 'Vesta', 'Mjurran', 'Middray', 'Orc', 'Kaede', 'Momiji', 'Garm', 'Dord', 'Myrd', 'Gard', 'Grucius', 'Edmaris', 'Reyhiem', 'Towa', 'Yura', 'Zodon', 'Ellen', 'Kirara', 'Shōgo', 'Kyōya', 'Misha', 'Hermes', 'Nikolaus', 'Razen', 'Henrietta', 'Satoru', 'Ayn', 'Lizardman', 'Tempest', 'Holy', 'Orc', 'Abiru', 'Kaido', 'Kabal', 'Gido', 'Gunther', 'Bacchus', 'Fritz', 'Grigori', 'Kenya', 'Alice', 'Meuse', 'Gobwa', 'Kurobe', 'Touka', 'Saika', 'Veyron', 'Zonda', 'Esprit', 'Agera', 'Cien', 'Dolf', 'Fuze', 'Kazak', 'Drum', 'Elric', 'Mezul', 'Gozul', 'Footman', 'Tear', 'Eva', 'Yamza', 'Jeff', 'Tiss', 'Jinrai', 'Bernie', 'Jiwu', 'Chikuan', 'Lete', 'Barak', 'Aslan', 'Zenobia', 'Tedron', 'Gustav', 'Rogurd', 'Direwolf', 'Ordinary', 'Gobzo', 'Rigur', 'Haruna', 'Doris', 'Takt', 'Edward', 'Lester', 'Daggra', 'Liura', 'Ryota', 'Gale', 'Guratol', 'Ulamuth', 'Gesdar', 'Anne', 'Ukya', 'Elizabeth', 'Oloy', 'Tamura', 'Miho', 'Pirino', 'Pizu', 'Yori', 'Mio', 'Fuji', 'Kikyō', 'Chiffon', 'Paulo', 'Carl', 'Maria', 'Souka', 'Geld', 'Phobio', 'Suphia', 'Orthos', 'Gelmud']

# txtcards = open("cards.txt", encoding="utf8")
# cards = txtcards.read()
# txtcards.close()

# list_cards = create_list_cards(cards)

# df_cards = pd.DataFrame(list_cards, columns=["ID", "Condition", "Name", "Level", "Rarity"])

# ── Interface ──────────────────────────────────────────────────────────────────


uploaded_file = st.file_uploader("Choose a file", type="txt")

if uploaded_file is not None:
    cards = uploaded_file.getvalue().decode("utf-8")
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
        df_cards = df_cards[df_cards["Rarity"].str.contains(sort_rarity)]
    
    df_cards["Number of duplicate"] = 0
    dict_nbr_duplicate = nbr_duplicate(cards, list_characters)
    for k in list_characters:
        df_cards.loc[df_cards["Name"].str.contains(k), "Number of duplicate"] = dict_nbr_duplicate[k]

    st.write(f"{len(df_cards)} characters found.")

    st.dataframe(df_cards)