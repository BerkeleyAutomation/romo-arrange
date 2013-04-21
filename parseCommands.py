import re
import sys
import math

#driveWithLeftMotorVelocityRightMotorVelocity(left, right, time)
#driveWithVelocity(speed, time)

def parseCommands(text_file_path):
    f = open(text_file_path)
    commands = []
    for command in f:
        command_info = []
        name_match = re.search('(.)*\(', command)
        name = name_match.group(0)[:-1]
        argMatch = re.search('\((.)*\)', command)
        args = argMatch.group(0)[1:-1].split(',')
        map(strip, args)
        commands.append([name, args])
    return commands

def strip(string_arg):
    string_arg = string_arg.strip()

class Romo:
    angle = 45

def interpretCommands(commands, Romo):
    for c in commands:
        name = c[0]
        args = c[1]
        if (name == "driveWithSpeed"):
            left = float(args[0])
            right = float(args[0])
            time = float(args[1])
            print left, right, time
        elif (name == "driveWithLeftMotorSpeedRightMotorSpeed"):
            left = float(args[0])
            right = float(args[1])
            time = float(args[2])
            print left, right, time
        else:
            error_msg = "Invalid command " + name
            for a in args:
                error_msg = error_msg + " " + a
            print error_msg
            sys.exit(0)
        
            


r = Romo()
interpretCommands(parseCommands("example.txt"), r)
