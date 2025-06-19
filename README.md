## -Workmate
for Workmate company
- python csv_processor.py phones.csv --filter "price,>,300" - фильтрация по цене
- python csv_processor.py phones.csv --aggregate "price,avg" - Агрегация (средняя цена):
- python csv_processor.py phones.csv --filter "brand,==,xiaomi" --aggregate "rating,min" - Фильтрация + агрегация (минимальный рейтинг для Xiaomi)
- pytest test_csv_processor.py -v - для тестов
