import textdumper
import vardumper
import sys

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        print("Usage: python gbstoolkit.py [dumptext|dumpvars|loadvars] [project file] <var input file>")
    elif args[1] == "dumptext":
        textdumper.dump_text(args[2])
    elif args[1] == "dumpvars":
        vardumper.dump_vars(args[2])
    elif args[1] == "loadvars":
        if len(args) < 4:
            print("Usage: python gbstoolkit.py loadvars [project file] [var input file]")
        else:
            vardumper.load_vars(args[2], args[3])