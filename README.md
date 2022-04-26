#DZ3.4

1.
Поставил раза с третьего, после очередного перекуривания мануала 
помещение в автозапуск 
vagrant@vagrant:~$ sudo systemctl enable node_exporter
процесс корректно стартуется и завершается. после перезапуска так же работает 

vagrant@vagrant:~$ Connection to 127.0.0.1 closed by remote host.
Connection to 127.0.0.1 closed.
PS D:\netology\vagrant\varconf> vagrant ssh
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon 25 Apr 2022 09:07:32 PM UTC

  System load:  0.95               Processes:             146
  Usage of /:   12.0% of 30.88GB   Users logged in:       0
  Memory usage: 5%                 IPv4 address for eth0: 10.0.2.15
  Swap usage:   0%


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Mon Apr 25 20:30:26 2022 from 10.0.2.2
vagrant@vagrant:~$ sudo systemctl status node_exporter
● node_exporter.service - Node Exporter
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2022-04-25 21:07:15 UTC; 35s ago
   Main PID: 681 (node_exporter)
      Tasks: 5 (limit: 4616)
     Memory: 14.5M
     CGroup: /system.slice/node_exporter.service
             └─681 /usr/local/bin/node_exporter


2.
node_cpu_seconds_total - общая загрузка CPU в секунду в разных режимах.
go_memstats_alloc_bytes_total - общее кол-во выделенной памяти в байтах
node_filesystem_avail_bytes - пространство файловой системы, доступное пользователям (не рутовым)
node_disk_io_time_seconds_total - общее затраченное время на input|output
node_network_receive_bytes_total - среднесетевой трафик полученый в секунду за [время]

3.
установил, в конфиге заменил, порты пробросил - релоад сделал
все работает скрин по ссылке
https://skr.sh/sDdxkncF9GA?a

4.
можно  третья строка дает понять что крутится на виртуалбоксе
[   30.361702] 21:54:07.770024 main     OS Release: 5.4.0-91-generic
[   30.361728] 21:54:07.770056 main     OS Version: #102-Ubuntu SMP Fri Nov 5 16:31:28 UTC 2021
[   30.361763] 21:54:07.770081 main     Executable: /opt/VBoxGuestAdditions-6.1.30/sbin/VBoxService
               21:54:07.770082 main     Process ID: 894
               21:54:07.770083 main     Package type: LINUX_64BITS_GENERIC
[   30.362314] 21:54:07.770637 main     6.1.30 r148432 started. Verbose level = 0

5.
Есть два типа ограничений 
«Жесткое ограничение» для открытых файлов статически заданное значение, и может быть изменен только «корневым» пользователем Linux;
«Мягкое ограничение» — это ограничение, которое может изменяться процессами динамически, т. е. во время выполнения, если процессу требуется больше открытых файлов, чем разрешено мягким пределом.

стоит 1048576 - максимальное колличество дискриптеров файлов, которое процесс может выделить.
vagrant@vagrant:~$ sysctl -n fs.nr_open
1048576
vagrant@vagrant:~$ ulimit -a
open files                      (-n) 1024
vagrant@vagrant:~$ ulimit -aH
open files                      (-n) 1048576

6.
root@vagrant:~# unshare -f --pid --mount-proc /usr/bin/sleep 1h
^Z
[1]+  Stopped                 unshare -f --pid --mount-proc /usr/bin/sleep 1h

root@vagrant:~# ps aux | grep sleep
root        3273  0.0  0.0   5480   592 pts/0    T    05:25   0:00 unshare -f --pid --mount-proc /usr/bin/sleep 1h
root        3274  0.0  0.0   5476   592 pts/0    S    05:25   0:00 /usr/bin/sleep 1h
root        3292  0.0  0.0   6432   672 pts/0    S+   05:28   0:00 grep --color=auto sleep

root@vagrant:~# nsenter -t 3274 -p -m
root@vagrant:/# ps
    PID TTY          TIME CMD
      1 pts/0    00:00:00 sleep
      2 pts/0    00:00:00 bash
     13 pts/0    00:00:00 ps
root@vagrant:/#

7.
:(){ :|:& };:
https://linux-notes.org/sozdanie-fork-bomb-v-unix-linux/
так называемая fork-bomb - функция рекурсивно запускает сама себя, занимая ресурсы системы 

помог автоматической стабилизации 
cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-4.scope

механизм ядра Linux, который ограничивает и изолирует вычислительные ресурсы (процессорные, сетевые, ресурсы памяти, ресурсы ввода-вывода) для групп процессов
понравилось как описано тут
https://linux-notes.org/ustanovka-cgroups-v-unix-linux/


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#DZ 3.3

1.

vagrant@vagrant:~$ touch strace.log
vagrant@vagrant:~$ strace /bin/bash -c 'cd /tmp' > strace.log 2>&1
vagrant@vagrant:~$ cat strace.log | grep /tmp
execve("/bin/bash", ["/bin/bash", "-c", "cd /tmp"], 0x7ffc165b5b00 /* 23 vars */) = 0
stat("/tmp", {st_mode=S_IFDIR|S_ISVTX|0777, st_size=4096, ...}) = 0
chdir("/tmp")                           = 0
vagrant@vagrant:~$

2.
man FILE 

     /usr/share/misc/magic.mgc  Default compiled list of magic.
     /usr/share/misc/magic      Directory containing default magic files.

vagrant@vagrant:~$ strace -o dz33.2 file /dev/tty
/dev/tty: character special (5/0)
vagrant@vagrant:~$ grep magic dz33.2
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libmagic.so.1", O_RDONLY|O_CLOEXEC) = 3
stat("/home/vagrant/.magic.mgc", 0x7fff3a79f2b0) = -1 ENOENT (No such file or directory)
stat("/home/vagrant/.magic", 0x7fff3a79f2b0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
stat("/etc/magic", {st_mode=S_IFREG|0644, st_size=111, ...}) = 0
openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
vagrant@vagrant:~$

3.
кинул пинг - логи в файл тест пинг и файл сразу удалил 
процесс пинг запущен
vagrant@vagrant:~$ ping ya.ru > test_ping & rm test_ping
[1] 6929
vagrant@vagrant:~$ ps
    PID TTY          TIME CMD
   6919 pts/0    00:00:00 bash
   6929 pts/0    00:00:00 ping
   6934 pts/0    00:00:00 ps

видим, что размер фувеличивается у файла
vagrant@vagrant:~$ sudo lsof -p 6929
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
ping    6929 vagrant    1w   REG  253,0     5570 1048639 /home/vagrant/test_ping (deleted)

vagrant@vagrant:~$ sudo lsof -p 6929
COMMAND  PID    USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
ping    6929 vagrant    1w   REG  253,0    31885 1048639 /home/vagrant/test_ping (deleted)


вариантов наверное несколько - если нам сам процесс не нужен, то можем убить процесс 
vagrant@vagrant:~$ kill -9 6929
vagrant@vagrant:~$ sudo lsof | grep deleted
[1]+  Killed                  ping ya.ru > test_ping
второй вариан ограничить размер файла нулем 
sudo truncate -s 0 /proc/6929/fd/1


4. 
Зомби процес освобождает свои ресурсы, но не освобождает запись в таблице процессов.

5.

vagrant@vagrant:~$ dpkg -L bpfcc-tools | grep sbin/opensnoop
/usr/sbin/opensnoop-bpfcc
vagrant@vagrant:~$ sudo /usr/sbin/opensnoop-bpfcc
PID    COMM               FD ERR PATH
630    irqbalance          6   0 /proc/interrupts
630    irqbalance          6   0 /proc/stat
630    irqbalance          6   0 /proc/irq/20/smp_affinity
630    irqbalance          6   0 /proc/irq/0/smp_affinity
630    irqbalance          6   0 /proc/irq/1/smp_affinity
630    irqbalance          6   0 /proc/irq/8/smp_affinity
630    irqbalance          6   0 /proc/irq/12/smp_affinity
630    irqbalance          6   0 /proc/irq/14/smp_affinity
630    irqbalance          6   0 /proc/irq/15/smp_affinity
917    vminfo              4   0 /var/run/utmp
621    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
621    dbus-daemon        23   0 /usr/share/dbus-1/system-services
621    dbus-daemon        -1   2 /lib/dbus-1/system-services
621    dbus-daemon        23   0 /var/lib/snapd/dbus-1/system-services/
917    vminfo              4   0 /var/run/utmp
621    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
621    dbus-daemon        23   0 /usr/share/dbus-1/system-services
621    dbus-daemon        -1   2 /lib/dbus-1/system-services
621    dbus-daemon        23   0 /var/lib/snapd/dbus-1/system-services/


6.

vagrant@vagrant:~$ strace uname -a > uname_log 2>&1
vagrant@vagrant:~$ nano uname_log
vagrant@vagrant:~$ cat uname_log | grep uname
execve("/usr/bin/uname", ["uname", "-a"], 0x7fff68a30178 /* 24 vars */) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
vagrant@vagrant:~$


uname()
Part of the utsname information is also accessible  via  /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}
нашел не в мане, а в интернете. в инете везде идет ссылка именно на man 2 uname
vagrant@vagrant:~$ man 2 uname
No manual entry for uname in section 2

7.
; - Оператор точка с запятой позволяет запускать несколько команд за один раз, и выполнение команды происходит последовательнj
&& - будет выполнять вторую команду только в том случае, если состояние выхода первой команды равно «0» — программа выполнена успешно.
set -e - прекращает выполнение если результат отличен от нуля. функционал схож с &&, но в моментах отладки смысл использования похоже есть 

8.
-e - прекращает выполнение скрипта если команда завершилась ошибкой
-u - прекращает выполнение скрипта, если встретилась несуществующая переменная
-x - выводит выполняемые команды в stdout перед выполненинем
-o pipefail - прекращает выполнение скрипта, даже если одна из частей пайпа завершилась ошибкой
при использовании в сценариях хорошо тем, что происходит поиск ошибок. Можно назвать наверное встроеной отладкой 

9.
STAT
Ss
R+

PROCESS STATE CODES
       Here are the different values that the s, stat and state output specifiers (header "STAT" or "S") will display
       to describe the state of a process:

               D    uninterruptible sleep (usually IO)
               I    Idle kernel thread
               R    running or runnable (on run queue)
               S    interruptible sleep (waiting for an event to complete)
               T    stopped by job control signal
               t    stopped by debugger during the tracing
               W    paging (not valid since the 2.6.xx kernel)
               X    dead (should never be seen)
               Z    defunct ("zombie") process, terminated but not reaped by its parent

       For BSD formats and when the stat keyword is used, additional characters may be displayed:

               <    high-priority (not nice to other users)
               N    low-priority (nice to other users)
               L    has pages locked into memory (for real-time and custom IO)
               s    is a session leader
               l    is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)
               +    is in the foreground process group




#DZ 3.2

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

