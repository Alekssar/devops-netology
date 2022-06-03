#!/usr/bin/env python3

import os

print ('Enter the path to the repository')
DIR = input()

#DIR = 'd:\\netology\homeworks'

bash_command = [f"cd {DIR}", "git status"]

print("searching for modifieded files", DIR)

result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
#pwd = os.popen(bash_command[0]).read().rstrip()
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(os.path.join(DIR, prepare_result))
        is_change = True
if is_change == False:
    print ("Modifieded files not found or the wrong directory is specified.")
