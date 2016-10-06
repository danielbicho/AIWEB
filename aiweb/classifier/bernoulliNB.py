import codecs
import os
import re

import dill
import numpy as np
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB


class Classifier(object):
    def __init__(self, sites_ok_path='sites_html_ok/', sites_nok_path='sites_html_nok/'):
        self.sites_ok = sites_ok_path
        self.sites_nok = sites_nok_path

    def set_sites_ok(self, path):
        sites_ok = path

    def set_sites_nok(self, path):
        sites_nok = path

    def tokenize(self, text):
        words = re.sub(r'[\W_\d]', ' ', text).lower().split()
        return words

    def extract_features(self, data):

        with open('vectorizer_docs', 'r') as f:
            vectorizer = dill.load(f)

        soup = BeautifulSoup(data, 'lxml')

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

    def train(self):
        fp7projects_docs = []
        nofp7projects_docs = []

        for htmlfile in os.listdir(self.sites_ok):
            html_entry_path = os.path.join(self.sites_ok, htmlfile)
            if os.path.isfile(html_entry_path):
                with codecs.open(html_entry_path, 'r') as html_doc:
                    soup = BeautifulSoup(html_doc.read(), 'lxml')
                    # remove all scrit and style elements
                    for junk in soup(["script", "style"]):
                        junk.extract()
                    # pageText = soup.find_all('p').getText()
                    pageText = soup.get_text(separator=' ')
                    lines = (line.strip() for line in pageText.splitlines())
                    chunks = (phrase.strip()
                              for line in lines for phrase in line.split("  "))
                    text = '\n'.join(chunk for chunk in chunks if chunk)
                    fp7projects_docs.append(text)

        for htmlfile in os.listdir(self.sites_nok):
            html_entry_path = os.path.join(self.sites_nok, htmlfile)
            if os.path.isfile(html_entry_path):
                with codecs.open(html_entry_path, 'r') as html_doc:
                    soup = BeautifulSoup(html_doc.read(), 'lxml')
                    # remove all scrit and style elements
                    for junk in soup(["script", "style"]):
                        junk.extract()
                    # pageText = soup.find_all('p').getText()
                    pageText = soup.get_text(separator=' ')
                    lines = (line.strip() for line in pageText.splitlines())
                    chunks = (phrase.strip()
                              for line in lines for phrase in line.split("  "))
                    text = '\n'.join(chunk for chunk in chunks if chunk)
                    nofp7projects_docs.append(text)

        docs = np.hstack((fp7projects_docs, nofp7projects_docs))

        # TODO Make sample dynamic
        train_docs = np.hstack((fp7projects_docs[:1000], nofp7projects_docs[:300]))

        vectorizer = CountVectorizer(stop_words='english', tokenizer=self.tokenize, max_features=800)
        vectorizer.fit(docs)

        with open('vectorizer_docs', 'wb') as f:
            dill.dump(vectorizer, f)  # save the object to a file

        train_data = vectorizer.transform(train_docs)
        train_labels = np.hstack((np.ones(1000, int), np.zeros(300, int)))

        nbb = BernoulliNB()
        nbb.fit(train_data, train_labels)

        # save trained classifier
        with open('trained_classifier', 'wb') as f:
            dill.dump(nbb, f)

    def classify(self, features_vector):
        # load classifier
        with open('trained_classifier', 'r') as f:
            nbb = dill.load(f)
        predicted_class = nbb.predict(features_vector)
        return predicted_class


def main():
    cl = Classifier('/home/dbicho/Research-Websites-Preservation/classifier/sites_html_ok/',
                    '/home/dbicho/Research-Websites-Preservation/classifier/sites_html_nok/')
    cl.train()


if __name__ == "__main__":
    main()
