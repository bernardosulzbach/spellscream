import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description="Inspects a file tree for grammar issues")
    parser.add_argument("root", help="the root of the tree SpellScream will walk")
    return parser.parse_args()


def list_files(root):
    return []


def inspect_file(root):
    pass


def main():
    arguments = get_arguments()
    files = list_files(arguments.root)
    for file in files:
        inspect_file(file)


if __name__ == '__main__':
    main()
