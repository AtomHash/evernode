import sys
import argparse
from evernode.bin import Create
from evernode.bin import Module


class Evernode:

    parser = None
    args = None

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='EverNode helper.',
            usage="""evernode <command> [<args>]

EverNode commands are:
   init      Create a fresh evernode app structure
   module    Create a module structure
""")
        self.parser.add_argument('command', help='run evernode commands')
        self.args = self.parser.parse_args(sys.argv[1:2])
        getattr(self, self.args.command.lower(), 'help')()

    def init(self):
        parser = argparse.ArgumentParser(
            description='make evernode_<name>')
        parser.add_argument('name')
        args = parser.parse_args(sys.argv[2:])
        Create(args.name)

    def module(self):
        parser = argparse.ArgumentParser(
            description='module commands')
        parser.add_argument('command', help='run module commands')
        args = parser.parse_args(sys.argv[2:3])
        if hasattr(args, 'command'):
            command = args.command.lower()
            if command == 'init':
                parser = argparse.ArgumentParser(
                    description='module commands')
                parser.add_argument('name', help='name of module')
                args = parser.parse_args(sys.argv[3:4])
                Module(args.name, 'init')
            else:
                self.help()

    def help(self):
        print('Need some help?')
        self.parser.print_help()
        exit(1)


def main():
    Evernode()
