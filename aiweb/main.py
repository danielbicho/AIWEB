import argparse

from aiweb.ingest.ingest import ingest_file


def main(args=None):
    """Display help and command lines options."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file',
                        help="specify the input file (csv format).")

    parser.add_argument('-f', '--fields', nargs='+',
                        help="specify the fields on the csv file that will be used. ex: -fields acronym title")

    parser.add_argument('-o', '--output_file', help="specify the output file to write")

    # parser.add_argument('top_results', help="Number of top results to use")
    parser.add_argument("-c", "--custom", metavar='Custom Query',
                        help="customize query with advanced operators (ex: -site:cordis.europa.eu)")

    args = parser.parse_args()

    if not args.custom:
        advanced_operators = ''
    else:
        advanced_operators = args.custom

    ingest_file(args.input_file, args.fields, advanced_operators, args.output_file)


if __name__ == "__main__":
    main()
