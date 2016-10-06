import argparse

from aiweb.classifier.bernoulliNB import Classifier
from aiweb.classifier.feature_extractor import fetch_website


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="URL address of the website you want to classify.")

    args = parser.parse_args()

    # get website data
    data = fetch_website(args.url)

    if data != None:
        cl = Classifier()
        # extract features
        features_vector = cl.extract_features(data)

        # classify website
        result = cl.classify(features_vector)
        if result:
            print "It's a R&D website!!"
        else:
            print "It's not a R&D website"
    else:
        print "Could not classify the website."


if __name__ == "__main__":
    main()
