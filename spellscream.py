import argparse
import os


class InspectionReport:
    """
    The result of an inspection.
    """

    def __init__(self, filename):
        self.filename = filename
        self.issues = []

    def __len__(self):
        return len(self.issues)

    def __str__(self):
        lines = [self.filename + ":"]
        for issue in self.issues:
            lines.append("  " + str(issue))
        return "\n".join(lines)


class Issue:
    """
    An issue in a file.
    """

    def __init__(self, line, text):
        self.line = line
        self.text = text

    def __str__(self):
        return str(self.line) + ": " + self.text


dictionary = None


def init_dictionary():
    global dictionary
    dictionary = set()
    with open("dictionary/english.txt") as dictionary_file:
        for line in dictionary_file.readlines():
            dictionary.add(line.strip())


def get_dictionary():
    if dictionary is None:
        init_dictionary()
    return dictionary


def is_valid_word(word):
    return word in get_dictionary()


def list_files(root):
    for root, directories, files in os.walk(root):
        for file in files:
            yield os.path.join(root, file)


def clean_word(word):
    return word.strip("*_,:;.!?(){}[]'\"").lower()


def clean_file_words(file):
    """
    Produces a generator of clean file words.
    :param file: a file
    """
    line_number = 0
    for line in file.readlines():
        line_number += 1
        words = line.replace("--", " ").split()
        for word in words:
            yield line_number, word


def inspect_word(line, word, report):
    """
    Inspects a single word from a text file.
    :param line: the line of the file on which the word was found
    :param word: the word to be inspected
    :param report: the InspectionReport object relevant to the inspection
    """
    word = clean_word(word)
    if len(word) > 0:
        if not word.isnumeric() and not is_valid_word(word):
            report.issues.append(Issue(line, word))


def inspect_file(filename):
    """
    Inspects a text file for grammar issues.
    :param filename: the name of the file
    :return: a InspectionResult object with all the issues found
    """
    with open(filename) as open_file:
        report = InspectionReport(filename)
        for line, word in clean_file_words(open_file):
            inspect_word(line, word, report)
        return report


def get_arguments():
    parser = argparse.ArgumentParser(description="Inspects a file tree for grammar issues")
    parser.add_argument("root", help="the root of the tree SpellScream will walk")
    return parser.parse_args()


def main():
    arguments = get_arguments()
    files = list_files(arguments.root)
    for file in files:
        print(inspect_file(file))


if __name__ == "__main__":
    main()
