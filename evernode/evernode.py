import sys
import argparse
from evernode.bin import Create


class Evernode:

    args = None

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='EverNode helper.',
            usage="evernode <command> [<args>]")
        parser.add_argument('create', help='make evernode app folder')
        self.args = parser.parse_args(sys.argv[1:2])
        self.execute_commands()

    def execute_commands(self):
        if hasattr(self.args, self.args.create):
            parser = argparse.ArgumentParser(
                description='make evernode_<name>')
            parser.add_argument('name')
            args = parser.parse_args(sys.argv[2:])
            Create(args.name)
        else:
            print('Need some help?')
            parser.print_help()
            exit(1)


def main():
    Evernode()
