# Описание структуры проекта
- logmaker.py - скрипт для приведения логов dump_io в нормальный вид, умеет разделять по временным меткам следующие запросы: GET, POST, HEAD, OPTIONS

    ```bash
    python logmaker.py [файл_с_логами_dumpio] [выходной_файл]
  ```
- logseparator.py - cкрипт для разделения (нормальных) логов разных сайтов (после работы скрипта logmaker.py). Разделяет логи для myhost123.test и opencart.test в файлы соответственно wp.log, oc.log

    ```bash
    python logseparator.py [файл_с_логами]
  ```
- parse_logs.py - скрипт для обработки логов после приведения их в нормальный вид. Создает датафрейм из логов.

    ```bash
    python logmaker.py [файл_с_логами] [выходной_csv_файл]
  ```
- script_run.py - скрипь, запускающий jmeter тесты в рандомном порядке. 

    ```bash
    python script_run.py [путь_к_папке_со_скриптами] [количество_запусков_каждого_теста] [хост] [порт] [логин_пользователя_для_теста] [пароль_пользователя_для_теста]
  ```
- Jmeter Instruction.md - гайд по Jmeter
- scripts - папка со скриптами для Jmeter
- logs - папка с распарсенными логами (сформированы по приложениям)
- csv - папка с готовыми датафреймами (сформированы по приложениям)

#  Автоматизация атак для Wordpress (nmap)

Этапы поиска уязвимостей в Wordpress. Или можно использовать WPScan
- **Индексирование сайта**
    выполнить запрос Google Dorks типа `site:example.com intitle:"index of" inurl:/wp-content/`
    . В операторе `inurl:`
     можно указать следующие директории:
    - /wp-content/
    - /wp-content/languages/plugins
    - /wp-content/languages/themes
    - /wp-content/plugins/ (если сможем эту инфу посмотреть, то половина дела сделана и дальше не собираем инфу)
    - /wp-content/themes/
    - /wp-content/uploads/
- **Определение версии WordPress**
    - Найти в исходном коде страницы. Она указана в метатеге `generator`
    - Найти в файле `readme.html`
    - Найти в файле ru_RU.po, который входит в состав установочного пакета и расположен по адресу /wp-content/languages/
    ```
    "Project-Id-Version: WordPress 4.1.1\n"
    ```
    ```bash
    nmap -sV --script http-wordpress-info
    ```
- **Определение установленных компонентов**
    [скрипт](https://github.com/nmap/nmap/blob/894bfd4976cf2035e44634543046c67c3305b142/scripts/http-wordpress-enum.nse) для определение установленных тем и плагинов
    ```bash
    nmap -sV --script http-wordpress-enum example.com
    ```
- **Брутфорс wp-login**
    - **Определение имени пользователей**
    `example.com/?author=1`, где 1 — admin, так как это id  пользователя
    определение логинов, [скрипт](https://github.com/nmap/nmap/blob/894bfd4976cf2035e44634543046c67c3305b142/scripts/http-wordpress-users.nse) для брут форса логинов
    ```bash
    nmap -p80 --script http-wordpress-users <target>
    ```
    `wp-login.php` сам нам говорит что неверно
    [скрипт](https://github.com/nmap/nmap/blob/894bfd4976cf2035e44634543046c67c3305b142/scripts/http-wordpress-brute.nse) для брут форса, [описание](https://nmap.org/nsedoc/scripts/http-wordpress-brute.html)
    ```bash
    nmap -p80 --script http-wordpress-brute --script-args 'userdb=users.txt,passdb=passwords.txt' example.com
    ```
- **Уязвимости**
    - [Скрипт](https://github.com/nmap/nmap/blob/894bfd4976cf2035e44634543046c67c3305b142/scripts/http-vuln-cve2017-1001000.nse), обнаруживающий уязвимость с повышением привилегий в Wordpress 4.7.0 и 4.7.1, которые
    позволяют пользователям, не прошедшим проверку подлинности, добавлять контент в сообщения
    ```bash
    nmap --script http-vuln-cve2017-1001000 example.com
    ```
    - [Скрипт](https://github.com/nmap/nmap/blob/894bfd4976cf2035e44634543046c67c3305b142/scripts/http-vuln-cve2014-8877.nse), обнаруживающий уязвимость удаленного внедрения кода (CVE-2014-8877) в Wordpress CM (Б2.0?)
    ```bash
    nmap --script http-vuln-cve2014-8877 example.com
    ```
    уязвимость с повышением привилегий в Wordpress 4.7.0 и 4.7.1, которые
    позволяют пользователям, не прошедшим проверку подлинности, добавлять контент в сообщения.
- **Стандартные проверки**
    - Базовое сканирование с использование IP-адреса или имени хоста
    ```bash
    nmap example.com
    ```
    - Сканирование определенных портов или диапазонов портов на локальном или удаленном сервере
    ```bash
    # сканирование всех 65535 портов нашей локальной машины
    nmap -p 1-65535 localhost
    
    # сканирование портов 80 и 443 на удаленном сервере с IP-адресом 8.8.8.8
    nmap -p 80,443 8.8.8.8
    ```
    - Сканирование нескольких IP-адресов
    ```bash
    nmap 1.1.1.1 8.8.8.8
    
    # сканирование адресов 1.1.1.1, 1.1.1.2, 1.1.1.3 и 1.1.1.4
    nmap -p 1.1.1.1,2,3,4
    
    # сканирование диапазона адресов начиная с 8.8.8.1 до 8.8.8.14
    nmap -p 8.8.8.0/28
    nmap 8.8.8.1-14
    
    # исключить некоторые IP-адреса из диапазона сканирования
    nmap -p 8.8.8.* --exclude 8.8.8.1
    ```
    - Сканирование наиболее популярных портов
    ```bash
    # сканирование 20 наиболее популярных портов на удаленном IP-адресе 192.168.1.106
    nmap --top-ports 20 192.168.1.106
    ```
    - Сканирование хостов и IP-адресов из списка в текстовом файле
    ```bash
    nmap -iL list.txt
    ```
    - Сохранение результатов сканирования Nmap в файл
    ```bash
    # txt
    nmap -oN output.txt yandex.ru
    # xml
    nmap -oX output.xml yandex.ru
    ```
    - Отключение разрешения доменных имен
    
    ```bash
    # опция -n
    nmap -p 80 -n 8.8.8.8
    ```
    - Сканирование с определением операционной системы и сервисов
    ```bash
    # A позволит определить операционную систему и приложения, выполняемые на удаленном сервере
    nmap -A 10.10.10.1
    ```
    - Сканирование с использованием протоколов TCP и UDP
    ```bash
    nmap -sV localhost
    ```
    - Поиск и обнаружение уязвимостей с помощью Nmap
    ```bash
    # TCP
    nmap -sT 192.168.1.1
    # UDP
    nmap -sU localhost
    ```
    - Запуск DoS-атаки с помощью Nmap
    ```bash
    # атака меленными сессиями (SlowLoris Session Attack)
    nmap 192.168.1.105 -max-parallelism 800 -Pn --script http-slowloris --script-args http-slowloris.runforever=true
    ```
    - Обнаружение вредоносных программ на удаленных узлах
    ```bash
    # обнаружить вредоносные программы и бэкдоры в Identd, Proftpd, Vsftpd, IRC, SMB, и SMTP
    nmap -sV --script=http-malware-host 192.168.1.105
    # использьзуя антивирусные базы сервисов Google’s Safe Browsing и VirusTotal
    nmap -p80 --script http-google-malware infectedsite.com
    ```
  
# Включение расширенного логирования Apache
1. В `./apache2/apache2.conf` добавить: 
```LogFormat “\”%r\” \n Date-time: %t \n Host: %h \n Referer: %{Refer}i \n Cache: %{cache-status}o \n Status: %>s \n Content-Type: %{Content-Type}o \n User-Agent: {User-agent}i \n” project```
2. В файле конфигурации `./sites-enabled/000-default.conf` поменял конец строчки `CustomLog` с `common (или combined)` на `project`
3. Перезагрузил сервер 
    ```bash
    apache2 sudo service apache2 reload
    ```
   
# Включение логирования POST

1. подключил dumpio, чтобы логировать контент от POST
    1. посмотрел, есть ли в директории `/etc/apache2/mods-enabled` файл `mod_dumpio.load` - его там не оказалось
    2. сделал символьную ссылку на файл из `mods-available`
        ```bash
        sudo ln -s ../mods-available/mod_dumpio.load ../mods-enabled/mod_dumpio.load
        ```
    3. подключил модуль: `a2enmod dumpio`
    4. ```bash
       sudo service apache2 reload
       ```
2. теперь логи с постом складываются в другой файл: `error.log.wp` (для вордпресса), но там ничего не понятно и много лишнего.
3. написал скрипт на питоне, который приводит лог к нужному виду. Он лежит в домашней папке и запускается из терминала, принимая на вход в качестве аргументов файл, где хранятся логи от dumpio (error.log.wp для нашего вордпресса) и выходной файл (сами выбираем).
Формат логов немного изменился, потому что на сайте за секунду происходит несколько запросов (на каждое время указывается в начале 1 раз, а потом может быть несколько запросов - они относятся к этому времени)