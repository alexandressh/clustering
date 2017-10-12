from time import time
import pandas
import re

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans

from replacers import RegexpReplacer

url = 'data-pre-processing.csv'
dataframe = pandas.read_csv(url)

tokenizer = RegexpTokenizer("[\w']+")
replacer = RegexpReplacer()
english_stops = set(stopwords.words('english'))
stemmer = PorterStemmer()
vectorizer = CountVectorizer()

corpus = []

print("Removing contraction - replacer.replace")
print("Removing special chars - re.sub")
print("Getting tokens from comment and iterating through it - tokenizer.tokenizer")
print("Removing stopwords - word not in english_stops")
print("Steeming words - steemer.stem")
for videoId,author,date,content,classification in dataframe.values:
    comment = []
    content = content.lower()
    # Replace contractions such as as I'm to I am
    content = replacer.replace(content)
    # Remove special chars
    content = re.sub('[^A-Za-z0-9\s]+', '', content)
    # Iterate through words from content
    for word in tokenizer.tokenize(content):
        # Steem only and add only non stopwords
        if word not in english_stops:
            word = stemmer.stem(word)
            comment.append(word)
    corpus.append(" ".join(comment))

print("Creating bag of words - vectorizer.fit_transform")
print()
print()
vectorized =  vectorizer.fit_transform(corpus)

true_k = 2
km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1,
                verbose=False)

print("Clustering sparse data with %s" % km)
t0 = time()
km.fit(vectorized.toarray())
print("done in %0.3fs" % (time() - t0))


print()
print("Top terms per cluster:")
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print()