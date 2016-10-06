#!/usr/bin/python
import re
import urllib2

import BeautifulSoup
from sklearn.externals import joblib


def tokenize(text):
    words = re.sub(r'[\W_\d]', ' ', text).lower().split()
    return words


def fetch_website(url):
    """Download url to file."""
    try:
        u = urllib2.urlopen(url)
        data = u.read()
        return data
    except:
        return None


def extract_features(data):
    vectorizer = joblib.load('vectorizer_docs.joblib')
    # nbb = joblib.load('bernoulliNB.pkl')

    soup = BeautifulSoup.BeautifulSoup(data, 'lxml')

    # remove all scrit and style elements
    for junk in soup(["script", "style"]):
        junk.extract()

    # pageText = soup.find_all('p').getText()
    pageText = soup.get_text(separator=' ')
    lines = (line.strip() for line in pageText.splitlines())
    chunks = (phrase.strip()
              for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # generate features vector
    toclassify_text = []
    toclassify_text.append(text)

    toclassify_data = vectorizer.transform(toclassify_text)

    return toclassify_data
