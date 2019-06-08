#! /usr/bin/env python 

import json as j
import sys

def create_project():
    return {
        'name': input("Project Name: "), 
        'start': input("Proect Start: "), 
        'end': input("Project End: "), 
        'description': input("Project Description: ")
    }


def create_trial():
    project = input("Project Name: ")
    name = input("Trial Name: ")
    start = input("Trial Start: ")
    end = input("Trial End: ")
    description = []
    print("Description (BREAK on a newline to finish):")
    while True:
        inp = input("\t")
        if inp == 'BREAK':
            break
        description.append(inp)
    return {
        'name': name,
        'start': start,
        'end': end,
        'description': description,
        'project': project,
    }


def create_sensor():
    return {
            'name': input("Name: "),
            'description': input("Description: "),
            'samplerate': input("Samplerate: ")
    }

USAGE = "usage: datasetutil FILENAME [project|trial|sensor]"
args = sys.argv[1:]
if len(args) < 2:
    print(USAGE)
    sys.exit(1)

data = json.load(open(args[0]))
if args[1] == 'project':
    data.append(create_project())
elif args[1] == 'trial':
    data.append(create_trial())
elif args[1] == 'sensor':
    data.append(create_sensor())
else:
    print(USAGE)
    print(f"Arg 2 ({args[1]}) not recognised")
    sys.exit(2)
json.dump(data, open(args[0], indent=2)

