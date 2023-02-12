


import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

nltk.download('omw-1.4')
nltk.download('wordnet')
nltk.download('stopwords')

class TextPreprocessor():
    def __init__(
        self,
        stopwords: bool,
        stemming: bool,
        lemmatization: bool,
        html_tags: bool,
        urls: bool,
        punctuation: bool,
        digits: bool,
        max_word_lenth: int = 3
    ):
        self.stopwords = stopwords
        self.stemming = stemming
        self.lemmatization = lemmatization
        self.html_tags = html_tags
        self.urls = urls
        self.punctuation = punctuation
        self.digits = digits
        self.max_word_lenth = max_word_lenth

    def __text_preprocess(self, text: str):
        # remove digits
        text = re.sub(r'\d+', ' ', text) if self.digits else text
        # lowercase
        text = text.lower()
        # remove urls
        text = re.sub('http://\S+|https://\S+', '', text) if self.urls else text
        # remove tags 
        text = re.sub(r'<.*?>', '', text) if self.html_tags else text
        # remove punctuations 
        text = re.sub(r'[^\w\s]', ' ', text) if self.punctuation else text
        # remove non letters
        text = re.sub('[^a-zA-Z]', ' ', text)
        # remove white spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def __text_tokens(self, text: str):
        # splitting text to make tokens
        tokens = text.split()
        # removing stopeords
        if self.stopwords:
            stop_words = stopwords.words('english')
            stopwords_dict = Counter(stop_words)
            tokens = [word for word in tokens if word not in stopwords_dict]
        # stemming tokens
        if self.stemming:
            potter_stemmer = PorterStemmer()
            tokens = [potter_stemmer.stem(word) for word in tokens]
        # lemmatizing tokens
        if self.lemmatization:
            word_net_lemmatizer = WordNetLemmatizer()
            tokens = [word_net_lemmatizer.lemmatize(word) for word in tokens]

        tokens = [word for word in tokens if len(word) >= self.max_word_lenth]

        return ' '.join(tokens)

    def preprocess(self, text: str):
        text = self.__text_preprocess(text)
        text = self.__text_tokens(text)
        return text