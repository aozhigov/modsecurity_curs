# Запуск наших тестов

 python /script_run.py /path/to/folder <кол-во юзеров> <host> <port> <login> <password>

# Установка 
https://loadtestweb.info/2017/10/17/install-apache-jmeter/

# Структура теста
## Thread Group
Этот элемент отвечает за многопоточность.

(images/StressTestByJMeter$ThreadGroup.png)

- Action to be taken after a Sampler error — действие которое будет выполнено в случае возникновения ошибки:
    - Continue — продолжить выполнение потока.
    - Stop Thread — остановить поток.
    - Stop Test — остановить тест.
- Thread Properties
    - Number of Threads (users) — количество потоков.
    - Ramp-up Period (in seconds) — время, в течении которого будут созданы потоки. Т.е. если мы укажем число потоков 30, а данный период 10, то все 30 потоков будут запущены в течении десяти секунд.
    - Forever — потоки будут выполняться пока тест не будет вручную остановлен или не закончится время выделенное по расписанию.
    - Loop Count — число циклов. Актуально, если не стоит флаг Forever.
    - Scheduler — выполнение теста по расписанию.

## Config Elements (Конфигурационные элементы)
### User Defined Variables
(images/StressTestByJMeter$UserDefinedVariables.png)

- serverIP - вводим IP сервера, на котором находится тестируемое приложение
- portNumber - вводим номер порта, который использует тестируемое приложение
- path - так как используется rpc значение этой переменной /fx/rpc

### HTTP Request Defaults
Параметры HTTP-запросов по умолчанию. Данные настройки будут применяться для всех запросов которые расположены ниже по дереву, если у тех не будут заданы другие параметры.

(images/StressTestByJMeter$HTTPRequestDefaults.png)

Для полей Server Name or IP и Port Number используем заданные в предыдущем пункте переменные: serverIP и portNumber
### HTTP Cookie Manager

(images/StressTestByJMeter$HTTPCookieManager.png)

### HTTP Authorization Manager

(images/StressTestByJMeter$HTTPAuthorizationManager.png)

При помощи заданных ранее переменных serverIP и portNumber указываем ссылку для авторизацции, также указываем логин и пароль для авторизации.
- Logic Controllers (Логические контроллеры)
- Simple Controller (Простой контроллер)

Этот элемент служит для создания ответвлений и группировки элементов по логическим группам.

(images/StressTestByJMeter$SimpleController.png)
## Samplers (Типовые контроллеры)
### HTTP Request
Основной элемент теста. Посылает http-запросы по указанному адресу.

(images/StressTestByJMeter$HTTPRequest.png)
- Method — тип запроса. Чаще всего это GET.
- Path — путь до запрашиваемого файла. В случае использования rpc путь вормируется из определенной ранее переменной path и названия запускаемого скрипта

## Assertions (Соответствия)
### Response Assertion
Проверки соответствия применяются для утверждения того, расценивать ответ как ошибку или нет.

(images/StressTestByJMeter$ResponseAssertion.png)

Если в результате выполнения скрипта на странице появляется OK, скрипт считаем выполненным успешно.
### Listners (Отчеты)
Это элементы, позволяющие вести статистику и сохранять результаты теста в различном представлении.
### View Results Tree
(images/StressTestByJMeter$ViewResultsTree.png)

# Правила написания скриптов
### Запись сценария
Для сложного сценария, создавать который руками не представляется возможным или требует больших усилий, в JMeter существует механизм записи действий в браузере с перехватом GET/POST запросов. Это особенно актуально при необходимости записать сценарий приложения, которое делает множество POST запросов.
### HTTP(S) Test Script Recorder
После создания Thread Group создаем HTTP(S) Test Script Recorder (правый клик по Test Plan -> Add -> Non-Test Elements -> HTTP(S) Test Script Recorder). В созданном HTTP(S) Test Script Recorder оставляем порт 8888, хост ставим localhost. В Target Controller выбираем тот Thread Group, куда надо записать сценарий. В Grouping выбираем Put each new group in a new transaction controller,что означает, что при записи сценария действия будут группироваться - к примеру, при создании запроса будут созданы отдельные группы под заполнение контрагента, услуги, типа и т.д.

(images/HTTPTestScriptRecorder.png)

После настройки на стороне JMeter идем в свой браузер (на примере файерфокса: Настройки -> Параметры сети (Настроить)), где жмем "Ручная настройка прокси", указываем в HTTP Proxy localhost, а в Port тот порт, что указали в JMeter (в нашем случае 8888). Если записываем с https - то ставим галку "Также использовать этот прокси для FTP и HTTPS". Сохраняем и возвращаемся в JMeter.

В JMeter в HTTP(S) Test Script Recorder жмем Start. Может появиться предупреждашка о сертификате, игнорируем ее, появляется такое окошко, запись пошла.

(images/HTTPTestScriptRecorderStart.png)

Идем в браузер и выполняем все действия, которые необходимо впоследствии повторить в виде нагрузочного теста.

Когда решаем, что сценарий прокликан в браузере - жмем кнопку Stop в окошке, что выше, и идем в JMeter, где должны увидеть примерно такую картину:

(images/HTTPTestScriptRecorderStartSc.png)
### Данные из CSV
JMeter позволяет брать данные, необходимые для теста (user-defined variables) из внешнего источника, а именно из csv - файла. К примеру, требуется, открыть некий известный список url-ов, или же залогиниться под определенными пользователями. Можно сохранить все данные для этих действий (url, login, password) в файл и использовать его как источник в ходе теста.

Форматирование сценария
Обычно требуется сделать сценарий независимым от изменяемых параметров, к примеру таких как логин/пароль/CSRF/порт и т.д., для этих целей используем запись необходимого значения в переменную и последующую подстановку значения именно из переменной. На примере CSRF

1. Записываем значение в переменную

(images/HTTPTestScriptRecorderStartCSRF1.png)

2. Используем переменную везде, где раньше использовалось сырое значение.

(images/HTTPTestScriptRecorderStartCSRF2.png)

Аналогично можно записать и использовать любое значение, которое может изменяться или должно вычисляться. К примеру, проваливание в элемент списка, когда на уровень джметра приходит лишь респонс с уидами всех элементов списка, что требует от нас сперва выбрать любое рандомное значение, потом записать его в переменную и позже использовать для "проваливания" и операций внутри элемента списка. Для этих целей служат многочисленные Post processors (правый клик по элементу сценария -> add -> post processors), где с помощью скриптового языка (груви) можно писать простенькие скрипты для обработки респонса http-запроса.

(images/VariablesJmeter.png)

### Pre processor (подготовка действия)
Элементами данной группы являются действия, которые выполняются перед запросом.

- HTTP User Parameter Modifier (вариатор параметров запроса) -- Вариатор рараметров запроса позволяет для запроса (запросов), к которому он относится, брать значения передаваемых параметров из заранее подготовленного списка. Файл со списком указывается в поле File Name.

(images/Stress_tests$parammodafier.png)

Обычно данный элемент применяется для хранения данных учетных записей (логин-пароль), чтобы тестирование проходило под разными пользователями (все учетки приходиться готовить заранее). Список значений параметров задается в виде xml дерева:


    <thread>
       <parameter>
           <paramname>login</paramname>
           <paramvalue>pikachu</paramvalue>
       </parameter>

       <parameter>
          <paramname>password</paramname>
          <paramvalue>golouslomaeshhaker</paramvalue>
       </parameter>
    </thread>


Каждый поток берет очередной блок с тегом <thread>. Для каждого параметра (блок с тегом <parameter>) задается имя параметра <paramname> и значение — <paramvalue>. В запросе, к которому привязан вариатор, должны быть соответствующие параметры (значения их не обязательны, т.к. они будут браться из из указанного xml-файла).

### Post processor (обработчики результата действия)
Элементы этой группы позволяют обрабатывать полученный на запрос ответ. Например, извлекать текст.

- Regular Expression Extractor (извлечение текста с использование регулярных выражений)
Для извлечения текста используются PHP-совместимые регулярные выражения.

(images/Stress_tests$regexp.png)

- Response Field to check — часть ответа, из которой достаем текст:
    - Body — тело ответа.
    - Headers — заголовки.
    - URL — адрес.
- Параметры
    - Reference Name — имя ссылки на выражение , т.е. имя перемнной, в которую будет записан результат. Оно используется так же, как имена пользовательских переменных — ${ref_name}
    - Regular Expression — само выражение.
    - Template — шаблон. Используется для извлечения сразу нескольких подстрок используя одно выражение. Например,



Чтобы извлечь uuid для данной ссылки и ее идентификатор id в одну переменню matrixRef, можно применить выражение

    ?uuid=(.+?)&activeComponent=[[AccessMatrix]]" id="(.+?)">

и указать шаблон `$1$$2$`, тогда при обращении к

- matrixRef — вернется строка, содержащая оба извлеченных параметра corecl18gg9ig0000gv0dm47k8isnlioAccessMatrix.
- matrixRef_g0 — вернется строка, содержащая текст самого регулярного выражени.
- matrixRef_g1 — вернется строка, содержащая uuid — corecl18gg9ig0000gv0dm47k8isnlio.
- matrixRef_g2 — вернется строка, содержащая id — AccessMatrix.
- Match No. (0 for Random) — номер в списке найденных (на странице может быть больше одного найденного текста). Если стоит 0, то берется случайный из списка.
- Default Value — значение по умолчанию, оно возвращается в случае, если строка не найдена.

# Запуск теста
После того, как тест отлажен и проходит запуск в один/2/10 потоков в gui-режиме, настоящий тест необходимо выполнять в режиме терминала.

Примерная команда запуска из папки с JMeter:

./bin/jmeter -Jduration=600 -Jrampup=600 -Jthreads=1000 -Jhost=sm-sue.fsfk.local -Juser=user -Jpassword=password -n -t ./path_to_test.jmx -l ./path_to_file_with_result.csv -e -o ./path_to_folder_for_report

имена параметров, которые указываем с префикосм -J должны задаваться в скрипте как ${__P(name_parameter)}