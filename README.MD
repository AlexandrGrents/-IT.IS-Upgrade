{ITIS UPGRADE} Тестовое задание “Анализатор логов”
=======================================

Требуется изучить логи сервера, спроектировать базу данных, которая будет хранить информацию о товарах, транзакциях и действиях пользователей. После проектирования распарсите логи и положите их в только что спроектированную базу. На основе полученной базы данных, вам нужно разработать web-приложение, которое будет генерировать и выводить аналитические отчеты с возможностью задания входных параметров. 

Типы генерируемых отчётов:
------------------------------
1. Посетители из какой страны совершают больше всего действий на сайте?
2. Посетители из какой страны чаще всего интересуются товарами из определенных категорий? (категория выбирается)
3. В какое время суток чаще всего просматривают определенную категорию товаров? (категория выбирается)

Структура репозитория:
---------------------------
* [**Input data**](https://github.com/AlexandrGrents/log-analyzer-IT.IS-Upgrade/tree/master/Input%20data) - папка с исходными данными. Содержит лог-файл
* [**output examples**](https://github.com/AlexandrGrents/log-analyzer-IT.IS-Upgrade/blob/master/output%20examples) - примеры генерируемых отчётов
* [**docs**](https://github.com/AlexandrGrents/log-analyzer-IT.IS-Upgrade/tree/master/docs) - папка с документами. Содержит задание и описание базы данных
* [**parser**](https://github.com/AlexandrGrents/log-analyzer-IT.IS-Upgrade/tree/master/parser) - папка, содержащая всё, связанное с парсером логов, который переносить информацию из лог-файла в базу данных
* [**web**](https://github.com/AlexandrGrents/log-analyzer-IT.IS-Upgrade/tree/master/web) - папка, содержащая всё, связанное с web-приложением, предоставляющим отчёты и визуализацию
* [**alToTheBottomDB.py**](https://github.com/AlexandrGrents/log-analyzer-IT.IS-Upgrade/blob/master/alToTheBottomDB.py) - декларативное представление классов таблиц базы данных.
* [**all_to_the_bottom.db**](https://github.com/AlexandrGrents/log-analyzer-IT.IS-Upgrade/blob/master/all_to_the_bottom.db) - база данных

### Используемые технологии:
* [Flask](https://www.palletsprojects.com/p/flask/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [geoip2](https://github.com/maxmind/GeoIP2-python)
* [Google Charts](https://developers.google.com/chart/interactive/docs/quick_start)
