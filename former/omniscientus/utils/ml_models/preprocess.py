import re

from unicodedata import name
from os.path import join


def preprocess(data):
    # data word list
    data = str(data)
    words = data.split()
    
    # shorten words which has repeating chars
    tmp = []
    for word in words:
        tmp.append(re.sub(r'(.)\1+', r'\1\1', word, re.UNICODE | re.I))
    data = " ".join(tmp)
    del tmp
    
    # remove [,],(,),-,*
    for char in ["[","]","(",")","-","*", ",","_", "."]:
        pattern = r"(\{})".format(char)
        data = re.sub(pattern, ' ', data, re.UNICODE | re.I | re.M)
    
    # standardize some patterns
    # like :)
    data = re.sub(r'(:+\)+|\(+:+|=+\)+|\(+=+)', ' [SMILING] ', data, re.UNICODE | re.I | re.M)
    # :D, :d
    data = re.sub(r':(d|D)+', ' [SMILING] ', data, re.UNICODE | re.I | re.M)
    # ahaha or hahaha
    data = re.sub(r'((ha){2,}|(ah){2,})', ' [SMILING] ', data, re.UNICODE | re.I | re.M)
    # 7/24
    data = re.sub(r'7\s?/\s?24+', ' [FOREVER] ', data, re.UNICODE | re.I | re.M)
    # <3
    data = re.sub(r'<3+', ' [HEART] ', data, re.UNICODE | re.I | re.M)
    # ...
    data = re.sub(r'(\.\.\.)+', ' [THREE_DOT] ', data, re.UNICODE | re.I | re.M)
    # time like 12:43
    data = re.sub(r'\d{1,2}\s?:\s?\d{1,2}', r' [TIME] ', data, re.UNICODE | re.I | re.M)
    # +1
    data = re.sub(r'(\+[1-9]+|[1-9]\++)', r' [AGREE] ', data, re.UNICODE | re.I | re.M)
    # ?!?!?!? --> ?! or !?!?!?! --> !?
    data = re.sub(r'(\?!|!\?)+', r' \1 ', data, re.UNICODE | re.I | re.M)
    # ??????????? --> ?
    data = re.sub(r'(\?){2,}', r' \1 ', data, re.UNICODE | re.I | re.M)
    # !!!!!! --> !
    data = re.sub(r'(!){2,}', r' \1 ', data, re.UNICODE | re.I | re.M)
    # !? --> [UNLEM_SORUISARETI]
    data = re.sub(r'(!\?|\?!)', r' [UNLEM_SORUISARETI] ', data, re.UNICODE | re.I | re.M)
    # ! --> [UNLEM]
    data = re.sub(r'(!)', r' [UNLEM] ', data, re.UNICODE | re.I | re.M)
    # ? --> [SORU_ISARETI]
    data = re.sub(r'(\?)', r' [SORU_ISARETI] ', data, re.UNICODE | re.I | re.M)
    # ctrl+c, ctrl+v
    data = re.sub(r'ctrl\+c', r' [COPY] ', data, re.UNICODE | re.I | re.M)
    data = re.sub(r'ctrl\+v', r' [PASTE] ', data, re.UNICODE | re.I | re.M)
    # yha, yaa --> ya
    data = re.sub(r'(\s?yh?a+\s)', r' ya ', data, re.UNICODE | re.I | re.M)
    # mıyo, mıyoo, mıyoor --> mıyor
    data = re.sub(r'(mıyo+r*|mı+o+)', r'mıyor', data, re.UNICODE | re.I | re.M)
    # inşallah
    data = re.sub(r'(in[sş]|in[sş]allah)', r'inşALLAH', data, re.UNICODE | re.I | re.M)
    # can
    data = re.sub(r'(can+)', r'can', data, re.UNICODE | re.I | re.M)
    # herşey
    data = re.sub(r'(her[sş]ey)', r'herşey', data, re.UNICODE | re.I | re.M)
    # kopek
    data = re.sub(r'(k[oö]pek)', r'köpek', data, re.UNICODE | re.I | re.M)
    # hashtag
    data = re.sub(r'\s?([@#]\s?[\w_-]+)', r' [HASHTAG] ', data, re.UNICODE | re.I | re.M)
    # url
    data = re.sub(r'https?://.+[ ]?', r' [URL] ', data, re.UNICODE | re.I | re.M)
    data = re.sub(r'\w*\.\w*\.com/\w*', r' [URL] ', data, re.UNICODE | re.I | re.M)
    data = re.sub(r'url', r' [URL] ', data, re.UNICODE | re.I | re.M)
    # emoji
    emojis = None
    with open("emojis.txt", "r", encoding="utf-8") as f:
        emojis = f.read().strip()
    
    for emoji in emojis:
        _name = " [" + "_".join(name(emoji).split()) + "] "
        if '-' in _name:
            _name = _name.replace("-", "_")
        data = re.sub(emoji, _name, data, re.UNICODE | re.I | re.M)
    # percantage
    items = re.findall(r'(%\s?\d+|\d+\s?%)',  data)
    for item in items:
        tmp = ""
        try:
            num = int(item.split("%")[1])
        except ValueError:
            num = int(item.split("%")[0])
        if num < 25:
            tmp = " [VERY_BAD] "
        elif 25 <= num < 50:
            tmp = " [BAD] "
        elif 50 <= num < 75:
            tmp = " [NORMAL] "
        elif 75 <= num < 100:
            tmp = " [GOOD] "
        else:
            tmp = " [VERY_GOOD] "
        
        data = re.sub(item, tmp, data)
    # numbers
    data = re.sub(r'\d+(\.|/)?\d*', r' [NUMBER] ', data, re.UNICODE | re.I | re.M)
    
    # standardize random chars
    def isRandom(word):
       if "[" not in word:
            matches = re.findall(r'[qwrtypğsdfghjklşzxcvbnmç]{4,}', word,  re.UNICODE | re.I | re.M)
            acc, rej = 0, 0
            for match in matches: 
                if len(set(match)) > 1:
                    acc += 1
                else:
                    rej += 1
            
            if acc >= rej and acc != 0:
                return True
            else:
                return False
    
    for word in words:
        if isRandom(word):
            data = data.replace(word, " [RANDOM] ")
    
    # convert to casefold
    data = data.casefold()
    
    # remove illegal chars
    legals = "QWERTYUIOPĞÜASDFGHJKLŞIZXCVBNMÖÇqwertyuıopğüasdfghjklşizxcvbnmöç" +\
             "1234567890_".casefold()
    pattern = "[^(" + "|".join(legals) + "|" + "".join(['\{}|'.format(char) for char in "s[]()!?".casefold()]) + ")]"

    
    data = re.sub(pattern, r'', data, re.UNICODE | re.I | re.M)
    
    # shorten whitespaces
    data = re.sub('\s+', ' ', data, re.UNICODE | re.I | re.M)
    
    if data.strip() != "":
        return data.strip()
    else:
        return None
