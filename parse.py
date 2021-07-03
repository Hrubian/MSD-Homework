#!/usr/bin/env python3


import sys

def PrintOutput(ID, Description, SequenceLength):
    if ID == "":
        return
    print(f"ID: {ID}")
    print(f"Description: {Description}")
    print(f"Sequence length: {SequenceLength}")
    print()


def ManageFile(filename, OutputFile, wrap):
    try:
        f = open(filename, "r")
        print("Filename: " + filename)
        line = f.readline()
        ID = ""
        Description = ""
        SequenceLength = 0
        OutputLine = ""
        while line:
            if line[0] == "%":
                PrintOutput(ID, Description, SequenceLength)
                ParsedHeader = line.split()
                ID = ParsedHeader[1]
                Description = " ".join(ParsedHeader[2:])
                SequenceLength = 0
                if OutputFile:
                    while len(OutputLine) > 0:
                        OutputFile.write(OutputLine[:min(wrap, len(OutputLine))] + '\n')
                        OutputLine = OutputLine[min(wrap, len(OutputLine)):]
                    OutputFile.write('% ' + ID + " " + Description + '\n')
            else:
                SequenceLength += len(line) - (1 if line[-1] == '\n' else 0)
                if OutputFile:
                    OutputLine += line[:-1 if line[-1] == '\n' else None]
                    while len(OutputLine) > wrap:
                        OutputFile.write(OutputLine[:wrap] + '\n')
                        OutputLine = OutputLine[wrap:]
            line = f.readline()
        if OutputFile:
            while len(OutputLine) > 0:
                OutputFile.write(OutputLine[:min(wrap, len(OutputLine))] + '\n')
                OutputLine = OutputLine[min(wrap, len(OutputLine)):]
        PrintOutput(ID, Description, SequenceLength)
        f.close()
    except FileNotFoundError:
        print(f"File '{filename}' does not exist.", file=sys.stderr)


def FindOptions(args):
    if "--output" in args:
        try:
            OutputIndex = args.index("--output")
            output, _ = args.pop(OutputIndex + 1), args.pop(OutputIndex)
            OutputFile = open(output, "w")
        except FileNotFoundError:
            OutputFile = None
            print("Output file does not exist.", file=sys.stderr)
        except IndexError:
            OutputFile = None
            print("No output file specified.", file=sys.stderr)
            args.pop(OutputIndex)
    else:
        OutputFile = None
    if "--wrap" in args:
        try:
            WrapIndex = args.index("--wrap")
            wrap, _ = (int(args.pop(WrapIndex + 1)), args.pop(WrapIndex))
            if wrap < 1:
                raise ValueError
        except (ValueError, IndexError):
            print("Invalid wrap number. Default value (80) will be used instead.", file=sys.stderr)
            wrap = 80
    else:
        wrap = 80 #default value
    return OutputFile, wrap



def main(args):
    OutputFile, wrap = FindOptions(args)
    for file in args:
        ManageFile(file, OutputFile, wrap)
    if OutputFile:
        OutputFile.close()

if __name__ == "__main__":
    main(sys.argv[1:])


#Author: Jan Hruby
