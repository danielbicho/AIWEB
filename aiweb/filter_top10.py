import csv
# TODO Change to load important module functions with __init__
from classifier.bernoulliNB import Classifier
from classifier.feature_extractor import fetch_website


def main():
    process_results('./top10_results.txt')


def process_results(file_path):
    # open csv
    with open(file_path, 'rb') as csv_file:
        reader = csv.DictReader(csv_file,
                                fieldnames=['acronym', 'title', 'blank', 'url1', 'url2', 'url3', 'url4', 'url5', 'url6',
                                            'url7',
                                            'url8', 'url9', 'url10'])

        for row in reader:
            filter_row_result = ''
            for i in range(1, 11):
                field = 'url' + str(i)
                url = row[field]
                # Classify Website
                cl = Classifier()
                data = fetch_website(url)
                if data != None:
                    features = cl.extract_features(data)
                    classification_result = cl.classify(features)
                    if classification_result:
                        filter_row_result = url
                        break
            print filter_row_result
            # classify

            # if top1 result 1 next

            # else iterate from row until find rd website

            # write result back


if __name__ == '__main__':
    main()
