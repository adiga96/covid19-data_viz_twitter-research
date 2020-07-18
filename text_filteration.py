import re  
import nltk

# Functions for Tweet Filterations
def remove_punct(text):
    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|(RT)|(#[A-Za-z0-9]+)|(_[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
    return text

def tokenization(text):
    text = re.split('\W+', text)
    return text

lang = ['english','spanish','italian','french','german']
stopword = nltk.corpus.stopwords.words(lang)
def remove_stopwords(text):
    text = [word for word in text if word not in stopword]
    return text

ps = nltk.PorterStemmer()
def stemming(text):
    text = [ps.stem(word) for word in text]
    return text


wn = nltk.WordNetLemmatizer()
def lemmatizer(text):
    text = [wn.lemmatize(word) for word in text]
    return text
