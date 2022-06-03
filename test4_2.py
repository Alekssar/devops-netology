#!/usr/bin/env python3
import os
bash_command = ["cd d:/netology/homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
pwd = os.popen(bash_command[0]).read().rstrip()
for result in result_os.split('\n'):
    if result.find('изменено') != -1:
        prepare_result = result.replace('\tизменено:      ', '')
        print(pwd + "/" + prepare_result)
        is_change = True
if is_change == False:
    print("Modifieded files not found.")