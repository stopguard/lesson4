"""
Написать функцию currency_rates(), принимающую в качестве аргумента код валюты (например, USD, EUR, GBP, ...)
    и возвращающую курс этой валюты по отношению к рублю. Использовать библиотеку requests.
    В качестве API можно использовать http://www.cbr.ru/scripts/XML_daily.asp.
    Рекомендация: выполнить предварительно запрос к API в обычном браузере, посмотреть содержимое ответа.
    Можно ли, используя только методы класса str, решить поставленную задачу?
    Функция должна возвращать результат числового типа, например float.
    Подумайте: есть ли смысл для работы с денежными величинами использовать вместо float тип Decimal?
        Сильно ли усложняется код функции при этом?
    Если в качестве аргумента передали код валюты, которого нет в ответе, вернуть None.
    Можно ли сделать работу функции не зависящей от того, в каком регистре был передан аргумент?
    В качестве примера выведите курсы доллара и евро.
Доработать функцию currency_rates(): теперь она должна возвращать кроме курса дату, которая передаётся в ответе сервера.
    Дата должна быть в виде объекта date.
    Подумайте, как извлечь дату из ответа, какой тип данных лучше использовать в ответе функции?
"""
from decimal import Decimal         # импортируем тип Decimal
from datetime import date           # импортируем функцию преобразования даты времени

from requests import get, utils     # импортируем функции из requests


def currency_rates(code):
    """
    Принимает буквенный код валюты, возвращает список данных курса, стоимость валюты и дату обновления курса
    """
    resp = get('http://www.cbr.ru/scripts/XML_daily.asp')   # забираем данные с сайта
    encode = utils.get_encoding_from_headers(resp.headers)  # ищем кодировку
    valute_string = resp.content.decode(encoding=encode)    # декодируем контент
    # выдёргиваем из контента строку с датой:
    val_curs_date = valute_string[valute_string.find('Date="') + 6:valute_string.find('Date="') + 16].split('.')
    # и преобразовываем ее в формат даты:
    val_curs_date = date(year=int(val_curs_date[2]), month=int(val_curs_date[1]), day=int(val_curs_date[0]))
    find_charcode = valute_string.find(f'<CharCode>{code}')     # ищем начало строки с нужной валютой
    if find_charcode == -1:                                                 # если результатов поиска нет
        return ['ВАЛЮТА НЕ НАЙДЕНА', None, code, None], None, val_curs_date     # возвращаем None
    find_ending = find_charcode + valute_string[find_charcode:].find('</Valute>')   # ищем ее конец
    valute_string = valute_string[find_charcode:find_ending]    # отрезаем ненужное от строки контента
    data_list = []                                          # стартуем список для данных курса
    for num in range(4):                                    # цикл для перебора тегов
        data_start = valute_string.find('>') + 1                # ищем последний символ открытия тега
        data_end = valute_string.find('</')                     # ищем первое закрытие тега
        data_list.append(valute_string[data_start:data_end])    # добавляем данные в список
        valute_string = valute_string[data_end + 12:]           # отрезаем от строки обработанные данные
    data_list[1] = int(data_list[1])                                    # преобразуем множитель валюты
    rate = Decimal(data_list[3].replace(',', '.')) / data_list[1]       # получаем стоимость 1 ед. валюты в рублях
    data_list[3] = round(Decimal(data_list[3].replace(',', '.')), 2)    # преобразуем значение курса валюты
    return data_list, rate, val_curs_date                       # возвращаем полученные список, стоимость и дату


if __name__ == '__main__':
    # вызываем функцию попутно преобразовывая регистр символов:
    result, cur_rate, date_of_rate = currency_rates(input('Введите код валюты: ').upper())
    # собираем результат в строку:
    txt_rate = f'{result[1]} {result[2]} = {result[3]} рублей.\n1 {result[0]} стоит {cur_rate} RUR.' \
               f'\nДата обновления курса {date_of_rate.day:0>2}.{date_of_rate.month:0>2}.{date_of_rate.year}г.'
    print(txt_rate)     # вывод результата
