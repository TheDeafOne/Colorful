from LeXmo import LeXmo

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
    emo = LeXmo.LeXmo(text)
    emo.pop('text', None)
    emo.pop('negative', None)
    emo.pop('positive', None)
    return emo

def get_text_emotion(text: str):
    emo = get_text_emotions(text)
    m = max(emo.keys(), key=lambda x: emo[x])
    return m