import nltk
nltk.download('punkt')
import pandas as pd
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer

_nrc_f = open('nrc.txt', 'r+')
_lex_df = pd.read_csv(_nrc_f, names=["word", "emotion", "association"],
                            sep=r'\t', engine='python')
_lex_words = _lex_df.pivot(index='word',
                                   columns='emotion',
                                   values='association').reset_index()
_lex_words.drop(_lex_words.index[0])
_emotions = _lex_words.columns.drop('word')

color_map = {
    'anger': "#FF0000",
    'anticipation': "#FF8888",
    'disgust': "#00FF00",
    'fear': "#000000",
    'joy': "#FFFF00",
    'sadness': "#0000FF",
    'surprise': "#FF8800",
    'trust': "#333300"
}

def get_text_emotions(text: str):
    emo = {}
    document = word_tokenize(text)

    word_count = len(document)
    rows_list = []
    for word in document:
        word = word.lower()
        emo_score = (_lex_words[_lex_words.word == word])
        rows_list.append(emo_score)
    
    df = pd.concat(rows_list)
    df.reset_index(drop=True)
    
    for emotion in list(_emotions):
        emo[emotion] = df[emotion].sum() / word_count


    emo.pop('text', None)
    emo.pop('negative', None)
    emo.pop('positive', None)

    return emo

def get_text_emotion(text: str):
    emo = get_text_emotions(text)
    m = max(emo.keys(), key=lambda x: emo[x])
    return m