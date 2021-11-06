"""
Run GBS Toolkit from the CLI.
"""
import argparse
import sys
import tkinter

from dsl.util import PrintProgressTracker
from projectconverter import Application, format_project, parse_project

def run_cli():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # running from a bundle!
        root = tkinter.Tk()
        app = Application(root)
        app.master.title("GBS Toolkit")
        app.mainloop()
    else:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="action")
        parser_gui = subparsers.add_parser("gui", help="Run as a GUI application instead.")
        parser_format = subparsers.add_parser("format", help="Format a .gbsproj file into a tree of .kdl files.")
        parser_format.add_argument("file", help="The .gbsproj file to read from.")
        parser_format.add_argument("dir", help="The directory to write the .kdl tree to.")
        parser_parse = subparsers.add_parser("parse", help="Parse a tree of .kdl files into a .gbsproj file.")
        parser_parse.add_argument("dir", help="The directory to read the .kdl tree from.")
        parser_parse.add_argument("file", help="The .gbsproj file to write to. Will be backed up if exists.")
        args = parser.parse_args()
        if args.action == "gui":
            root = tkinter.Tk()
            app = Application(root)
            app.master.title("GBS Toolkit")
            app.mainloop()
        elif args.action == "format":
            format_project(args.file, args.dir, PrintProgressTracker())
        elif args.action == "parse":
            parse_project(args.file, args.dir, PrintProgressTracker())