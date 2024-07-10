forma = """{0}
Ссылка: {1}
Компания: {2}
Город: {3}
Образование: {4}
Заработная плата: {5}
Опыт работы: {6}
Формат занятости: {7}
Описание: {8}
Ключевые навыки: {9}
"""

start_text = """Здравствуйте! Данный бот осуществляет парсинг данных о вакансиях с сайта hh.ru
Воспользуйтесь командой /search, чтобы получить данные в виде файла с расширением txt(для удобства вывода большого количества текста)."""

search_text = """Парсинг происходит по вашим параметрам:
* профессия (обязательный параметр, ожидается текст)
* код региона - Москва 1, Санкт-Петербург 2, Подмосковье 2019 (необязательный параметр, ожидается полное название города или одно число - код) 
* образование (необязательный параметр, может быть \"высшее\" или \"среднее профессиональное\" или \"не требуется или не указано\")
* ожидаемая заработная плата (необязательный параметр, ожидается одно число - минимальная подходящая вам зарплата)
Если не хотите вводить необязательный параметр, вводите знак минуса -
А если не ввести обязательный параметр, то парсинг производиться не будет.
Параметры следует разделять переносом строки, если не разделить или поставить перенос не между параметрами, то параметры введутся некорректно, это приведет к неверному результату."""

show_text = """Данная команда выводит все вакансии, которые есть в базе данных."""

request_accepted = "Запрос принят, идет его обработка..."

found_vacancies = "Вакансии по вашему запросу:"

err_text = "Введите профессию, это обязательный параметр."
err_area = "Некорректный ввод данных о городе, попробуйте снова, введите корректное название города(Москва, Санкт-Петербург или Московская область) или его код(1, 2 или 2019 соответственно)."
err_education = "Некорректный ввод данных об образовании, введите слово \"высшее\" или \"среднее профессиональное\" или \"не требуется или не указано\"."
err_salary = "Некорректный ввод данных о заработной плате, введите одно число."
err = "Попробуйте снова."
