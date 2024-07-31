import random
import pandas as pd
import requests
from io import StringIO
import en_core_web_sm
import warnings
warnings.filterwarnings("ignore")


def get_content(kind):
    if kind == "full":
        sheet_id = '1p4h-MCsB_U5kFUNuRyz-_7zx72_i3XKY'
    elif kind == "condensed":
        sheet_id = '1lcreabZBcReMOtmsLz9psz64StLgsKpd'
        
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv'
    response = requests.get(url)
    df = pd.read_csv(
        StringIO(response.text), 
        usecols=["Words", "Forms", "Meaning"]
    )
    return df


def handle_content(df):
    df["Forms"] = df["Forms"].fillna("")

    def combine_values(row):
        if row['Forms'] != "":
            output = f"{row['Words']} - {row['Forms']}"
        else:
            output = row['Words']
        return output

    df["Combine"] = df.apply(combine_values, axis=1)
    contents = list(zip(
        df["Words"].to_list(),
        df["Meaning"].to_list(),
        df["Combine"].to_list()
    ))
    return contents


def nlp_handle_content(contents, max_words, mode):
    if len(contents) < max_words:
        max_words = len(contents)
    
    if mode == "relevant":
        nlp = en_core_web_sm.load()

        words = [c[0] for c in contents]
        output = []

        word = random.choice(words)
        words.remove(word)
        found_set = next((s for s in contents if list(s)[0] == word), None)
        output.append(found_set)

        nlp_word = nlp(word)
        nlp_word_list = sorted(
            [(wword, nlp_word.similarity(nlp(wword))) for wword in words],
            key=lambda x: x[1],
            reverse=True
        )

        for i in range(max_words - 1):
            found_set = next((s for s in contents if list(s)[0] == nlp_word_list[i][0]), None)
            output.append(found_set)
    elif mode == "random":
        output = random.sample(contents, max_words)
        
    return output