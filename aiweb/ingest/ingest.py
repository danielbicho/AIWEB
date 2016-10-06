import csv

from aiweb.query.search import search


def concatenate(row, fields):
    """concatenate csv fields in a unique string."""
    print row
    str = None
    for field in fields:
        if str == None:
            str = row[field]
        else:
            str += ' ' + row[field]
    return str


def ingest_file(input, fields, advanced_operators, output, delimiter=',', quotechar='"'):
    """Function that reads from a csv."""
    with open(input, 'rb') as csv_file:
        reader = csv.DictReader(csv_file)

        with open(output, 'a') as write_csvfile:
            fieldnames = ['acronym', 'title', 'projectUrl',
                          'foundProjectUrl1', 'foundProjectUrl2',
                          'foundProjectUrl3', 'foundProjectUrl4',
                          'foundProjectUrl5', 'foundProjectUrl6',
                          'foundProjectUrl7', 'foundProjectUrl8',
                          'foundProjectUrl9', 'foundProjectUrl10']

            writer = csv.DictWriter(write_csvfile, fieldnames=fieldnames)
            writer.writeheader()  # this method only available at python 2.7

            # iterate reader
            for row in reader:
                query_string = str(concatenate(row, fields))

                response = search(query_string, advanced_operators)

                projectsUrl = []
                results_size = len(response)

                # TODO print with logger
                print "INFO: RESULT SIZE - %s" % results_size

                for i in range(10):
                    if i < results_size:
                        projectsUrl.append(response[i]['Url'])
                    else:
                        projectsUrl.append('')

                # TODO print with logger
                print "INFO: FIRST RESULT - %s" % projectsUrl[0]
                writer.writerow(dict(acronym=row['acronym'], title=row['title'], projectUrl=row['projectUrl'],
                                     foundProjectUrl1=projectsUrl[0], foundProjectUrl2=projectsUrl[1],
                                     foundProjectUrl3=projectsUrl[2], foundProjectUrl4=projectsUrl[3],
                                     foundProjectUrl5=projectsUrl[4], foundProjectUrl6=projectsUrl[5],
                                     foundProjectUrl7=projectsUrl[6], foundProjectUrl8=projectsUrl[7],
                                     foundProjectUrl9=projectsUrl[8], foundProjectUrl10=projectsUrl[9]))
