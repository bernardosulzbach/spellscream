import argparse
import collections
import os


class InspectionReport:
    """
    The result of an inspection.
    """

    def __init__(self, filename):
        self.filename = filename
        self.word_count = 0
        self.warnings = []
        self.issues = []

    def __len__(self):
        return len(self.issues)

    def __str__(self):
        lines = [self.get_report_heading()]
        for warning in self.warnings:
            lines.append(warning)
        for issue in self.issues:
            if hasattr(issue, "line"):
                lines.append("{:-6}: {}".format(issue.line, issue.text))
            else:
                lines.append(" {}".format(issue.line, issue.text))
        return "\n".join(lines)

    def increment_word_count(self):
        self.word_count += 1

    def add_issue(self, issue):
        self.issues.append(issue)

    def analyze_issues(self):
        """
        Analyzes the issues of this Report, possibly generating warnings and removing issues.
        """
        typo_counter = collections.defaultdict(lambda: 0)
        for issue in self.issues:
            typo_counter[issue.text] += 1
        # Typos that appear more than max(words / 10000, 10) times are assumed to be names
        name_threshold = max(self.word_count / 10000, 10)
        ignored_typos = []
        for key, count in typo_counter.items():
            if count > name_threshold:
                ignored_typos.append((count, key))
        ignored_typos.sort()
        ignored_typos.reverse()
        for typo in ignored_typos:
            self.warnings.append("considering '" + typo[1] + "' a name as it was detected " + str(typo[0]) + " times")
        self.remove_issues_based_on_text(set(typo[1] for typo in ignored_typos))

    def remove_issues_based_on_text(self, typos):
        new_issue_list = []
        for issue in self.issues:
            if issue.text not in typos:
                new_issue_list.append(issue)
        self.issues = new_issue_list

    def get_report_heading(self):
        """
        Creates a proper heading for this report.
        """
        issue_count = len(self.issues)
        issue_count_string = "(1 issue)" if issue_count == 1 else "(" + str(issue_count) + " issues)"
        return self.filename + " " + issue_count_string + ":"


class Issue:
    """
    A simple issue in a file.
    """

    def __init__(self, line, text, issue_type='typo'):
        self.line = line
        self.text = text
        self.type = issue_type

    def __str__(self):
        return self.text


# The shared word set used as a dictionary
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
    """
    Simply checks if the word is in the global dictionary or not.
    :param word: the input word
    """
    return word in get_dictionary()


def clean_word(word):
    """
    Sanitizes the input word as to maximize the fairness of the dictionary check.
    :param word: the input word
    """
    word = word.strip("*_,:;.!?(){}[]'\"")  # Stripping periods this way is problematic because "U.S." becomes "U.S"
    word = word.lower()  # May bring up issues with names, but is necessary for now for words that come after a period.
    if word.endswith("'s"):
        return word[:-2]
    return word


def clean_file_words(file):
    """
    Produces a generator of clean file words.
    :param file: a file
    """
    line_number = 0
    for line in file.readlines():
        line_number += 1
        words = line.replace("--", " ").translate(str.maketrans("‘’“”", "''\"\"")).split()
        for word in words:
            yield line_number, word


def is_number(word):
    """
    Detects if the word is a number. This function also detects monetary values and negative numbers.
    :param word: a text word
    :return: True if the word is considered to be a number, False otherwise
    """
    # The first check is only needed for formal correctness. If performance requirements demand, it may be removed.
    return len(word) > 0 and len(word.strip('0123456789,.-$')) == 0


def inspect_word(line, word, report):
    """
    Inspects a single word from a text file.
    :param line: the line of the file on which the word was found
    :param word: the word to be inspected
    :param report: the InspectionReport object relevant to the inspection
    """
    word = clean_word(word)
    if len(word) > 0:
        report.increment_word_count()
        if not is_number(word) and not is_valid_word(word):
            report.add_issue(Issue(line, word))


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
        report.analyze_issues()
        return report


def list_files(root):
    for root, directories, files in os.walk(root):
        for file in files:
            yield os.path.join(root, file)


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
