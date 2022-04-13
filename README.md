DZ 3.2

1 
vagrant@vagrant:~$ type cd
cd is a shell builtin  --не является самостоятельной программой, а встроеная команда оболочки, служит для перехода по каталогам.

2. 
команда должна посчитать колличество строк с указанными совпадениями.
по описанию в man, будет соответствовать 
   General Output Control
       -c, --count
              Suppress normal output; instead print a count of matching lines for each input file.  With the -v, --invert-match option
              (see below), count non-matching lines.
т.е. grep <some_string> <some_file> -с - альтернатива

3.
vagrant@vagrant:~$ pstree -p
systemd(1)─┬─VBoxService(893)─┬─{VBoxService}(894)
           │                  ├─{VBoxService}(895)
           │                  ├─{VBoxService}(896)
           │                  ├─{VBoxService}(897)
           │                  ├─{VBoxService}(898)
           │                  ├─{VBoxService}(899)
           │                  ├─{VBoxService}(900)
           │                  └─{VBoxService}(901)
           ├─accounts-daemon(673)─┬─{accounts-daemon}(729)
           │                      └─{accounts-daemon}(794)
           ├─agetty(723)
           ├─atd(709)
           ├─cron(705)

ответ systemd является родителем всех проц-в 

-p используется в соответствии с описанием в man pstree

4.
в первом терминале ввод
vagrant@vagrant:~$ tty
/dev/pts/0
vagrant@vagrant:~$ ls -l \test123 2>/dev/pts/1

вывод второго
vagrant@vagrant:~$ tty
/dev/pts/1
vagrant@vagrant:~$ ls: cannot access 'test123': No such file or directory

5.

vagrant@vagrant:~$ grep -n Finished < /var/log/syslog > 11.file


в итоговом файле отфильтровалось 

4:Apr 12 00:00:46 vagrant systemd[1]: Finished Daily man-db regeneration.
13:Apr 12 01:55:48 vagrant systemd[1]: Finished Refresh fwupd metadata and update motd.
19:Apr 12 03:34:46 vagrant systemd[1]: Finished Message of the Day.
24:Apr 12 05:04:06 vagrant systemd[1]: Finished Ubuntu Advantage Timer for running repeated jobs.
34:Apr 12 08:26:36 vagrant systemd[1]: Finished Cleanup of Temporary Directories.
41:Apr 12 11:15:46 vagrant systemd[1]: Finished Ubuntu Advantage Timer for running repeated jobs.
54:Apr 12 14:23:46 vagrant systemd[1]: Finished Refresh fwupd metadata and update motd.
71:Apr 12 18:06:38 vagrant systemd[1]: Finished Refresh fwupd metadata and update motd.
74:Apr 12 18:15:46 vagrant systemd[1]: Finished Ubuntu Advantage Timer for running repeated jobs.

6.
Данные вывести получиться, но для наблюдения выводимых данных надо будет переключиться из графического эмулятора в эмулятор терминала

7.

bash 5>&1 - создаст дискриптор 5 и перенаправит его в stdout
echo netology > /proc/$$/fd/5   - выводит на экран netology. Происходит так, потому что перенаправили echo netology > 
в дискриптор 5. Который ранее был перенаправлен в stdout

8.

vagrant@vagrant:~$ ls -l /root 5>&2 2>&1 1>&5 |grep denied -c
1

5>&2 - новый дескриптор, перенаправили в stderr
2>&1 - stderr перенаправили в stdout 
1>&5 - stdout - перенаправили в в новый дескриптор


9.

Выводит переменные окружения. Можно заменить командой env (у меня вывело в более читабельном виде именно командой env
командой из задания вывело сплошным текстом)

10.

/proc/<PID>/cmdline - полный путь до исполняемого файла процесса [PID]  
/proc/<PID>/exe - содержит ссылку до файла запущенного для процесса [PID]

 в мане не получилось найти данную информацию, нагуглил. Подскажите плз строку запроса для корректного поиска

 11. 
vagrant@vagrant:~$ grep sse /proc/cpuinfo
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 cx16 pcid
sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single pti fsgsbase avx2 invpcid rdseed clflushopt md_clear flush_l1d
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 cx16 pcid
sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single pti fsgsbase avx2 invpcid rdseed clflushopt md_clear flush_l1d

версия 4_2

12.
 поправить можно ключем -t
 vagrant@vagrant:~$ ssh -t localhost 'tty'
vagrant@localhost's password:
/dev/pts/2
 
 If an interactive session is requested ssh by default will only request a pseudo-terminal (pty) for interactive
     sessions when the client has one.  The flags -T and -t can be used to override this behaviour.
 
 
 -t      Force pseudo-terminal allocation.  This can be used to execute arbitrary screen-based programs on a re‐
             mote machine, which can be very useful, e.g. when implementing menu services.  Multiple -t options force
             tty allocation, even if ssh has no local tty.

Почему не работает не очень ясно, но скорее всего при отправке команды по ssh (без ключа) псевдотерминал не создается.

13.
reptyr -T <PID>
получилось... после рекомендованных изменений 
reptyr depends on the ptrace(2) system call to attach to the  remote  program.  On  Ubuntu
       Maverick  and  higher,  this  ability is disabled by default for security reasons. You can
       enable it temporarily by doing

               # echo 0 > /proc/sys/kernel/yama/ptrace_scope

Хотелось бы, что б reptyr был еще раз разобран более подробно 

14.
tee - одновременно осуществляет вывод и в файл, указаный в качестве 
параметра и в stdout.
vagrant@vagrant:~$ echo string | sudo tee /root/new_file
string
В данном варианте команда получает вывод из stdin, перенаправленный через pipe от stdout команды echo
плюс команда запущена под пользователем sudo, у которого есть права на запись в файл 






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

