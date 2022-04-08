DZ3_1


5.
Выделено 
оперативная память 1024МБ
процессоры          2
порядок загрузки жестк. диск, опт . диск
64 ГБ на HDD и т.д.

6.

Vagrant.configure("2") do |config|
config.vm.box = "bento/ubuntu-20.04"
   config.vm.provider "virtualbox" do |vb|
    # указание на колличество RAM и проца
     vb.memory = 4096
     vb.cpus = 4
   end
end

8.
не совсем понятен вопрос, что имеется ввиду.
Описание HISTORY идет на 3009 строке
максимальное колличество строк в файле истории ? тогда - HISTFILESIZE (846)
если колличество команд в истории команд, то HISTSIZE (862)

ignoreboth - не записывает в историю команды начинающиеся с пробела и команды которые дублируют предыдущую

9.
257 строка
в фигурных скобках указывается перечень переменных, которые по очереди подставляются в указаный запрос. как пример создание ряда папок mkdir {1,2,3}_folder

10. 
vagrant@vagrant:/test$ touch {000001..300000}.txt
-bash: /usr/bin/touch: Argument list too long
300 тыс не получилось создать, ругается на то, что список аргументов слишком длинный
для создания 100 тыс vagrant@vagrant:/test$ touch {000001..100000}.txt

11.

в двойных квадратных скобках вычисляется выражение, стоящее в них, т.е. проводится тест. 
Что делает конструкция [[ -d /tmp ]]  - в данном варианте проверяется существует ли каталог (папка) с именем tmp.

12.
Создаю папку - mkdir /tmp/new_path_directory
копирую баш - cp /bin/bash /tmp/new_path_directory
указываю новый путь в PATH - export PATH=/tmp/new_path_directory:$PATH

результат 
vagrant@vagrant:~$ type -a bash
bash is /tmp/new_path_directory/bash
bash is /usr/bin/bash
bash is /bin/bash



13.
at      executes commands at a specified time. - выполнение команды по указаному времени

batch   executes commands when system load levels permit; in other words, when the load  average  drops  below
1.5, or the value specified in the invocation of atd. - выполняет команды, когда уровень загрузки падает ниже 1,5 по умолчанию (или можно указать уровень загрузки в atd)











1.
#git show aefea
aefead2207ef7e2aa5dc81a34aedf0cad4c32545
Update CHANGELOG.md


2.
#git show 85024d3
tag: v0.12.23

3. 2 родителя
#git show -s --pretty=%P b8d720

56cd7859e05c36c06b56d013b55a252d0bb7e158 
9ea88f22fc6269854151c571162c5bcf958bee2b

4.
#git log --pretty=oneline v0.12.23..v0.12.24
33ff1c03bb960b332be3af2e333462dde88b279e (tag: v0.12.24) v0.12.24
b14b74c4939dcab573326f4e3ee2a62e23e12f89 [Website] vmc provider links
3f235065b9347a758efadc92295b540ee0a5e26e Update CHANGELOG.md
6ae64e247b332925b872447e9ce869657281c2bf registry: Fix panic when server is unreachable
5c619ca1baf2e21a155fcdb4c264cc9e24a2a353 website: Remove links to the getting started guide's old location
06275647e2b53d97d4f0a19a0fec11f6d69820b5 Update CHANGELOG.md
d5f9411f5108260320064349b757f55c09bc4b80 command: Fix bug when using terraform login on Windows
4b6d06cc5dcb78af637bbb19c198faff37a066ed Update CHANGELOG.md
dd01a35078f040ca984cdd349f18d0b67e486c35 Update CHANGELOG.md
225466bc3e5f35baa5d07197bbc079345b77525e Cleanup after v0.12.23 release

5.
#git log -S 'func globalPluginDirs('
commit 8c928e83589d90a031f811fae52a81be7153e82f

6.
#первый шаг git log -S 'func globalPluginDirs('  - выдает один коммит смотрим его вторым шагом
#git show 8364383c3 - в конце коммита есть строка +func globalPluginDirs() [  - искомая функция добавлена в файл b/plugins.go делаем поиск изменения функции в файле
#git log -L :globalPluginDirs:plugins.go


commit 78b12205587fe839f10d946ea3fdc06719decb05
commit 52dbf94834cb970b510f2fba853a5b49ad9b1a46
commit 41ab0aef7a0fe030e84018973a64135b11abcd70
commit 66ebff90cdfaa6938f26f908c7ebad8d547fea17
commit 8364383c359a6b738a436d1b7745ccdce178df47

7.
#git log -S 'func synchronizedWriters('    --- Martin Atkins

выдало два комита - автора взял с более раннего по дате 
Martin Atkins

