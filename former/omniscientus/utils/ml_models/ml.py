from sklearn.externals import joblib
from nakkar.utilities.ml_models.preprocess import preprocess


CLASS_TABLE = {
    0: 'bilgi',
    1: 'destek',
    2: 'eleştiri',
    3: 'fikir',
    4: 'geri_bildirim',
    5: 'hakaret_küfür_cinsellik',
    6: 'istek_beklenti_tavsiye_öneri',
    7: 'izlenim',
    8: 'sevgi_iltifat_duygu',
    9: 'soru',
    10: 'çöp'
}

vectorizer = joblib.load("model_vectorizer.pkl")
classifier = joblib.load("ml_models.pkl")


def predict_class(texts):
    result = []
    texts = [preprocess(text) for text in texts]
    len_of_texts = len(texts)
    classes = list(classifier.predict(vectorizer.transform(texts)))
    for i in range(len_of_texts):
        result.append([CLASS_TABLE[classes[i]], texts[i]])

    return result
