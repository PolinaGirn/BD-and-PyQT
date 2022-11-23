import os
from ipaddress import ip_address, IPv4Address, AddressValueError
from socket import gethostbyname, gaierror
from subprocess import Popen, PIPE

from tabulate import tabulate
import sys
from random import randint
from termcolor import colored


# делаю список с некоторыми адресами
arr_rand_ip = ['google.com', 'yandex.ru', '192.168.199.1', "kjlkjlk", 'localhost', '192.168.1.1']

# добавляю в этот список ещё некоторое кол-во рандомных
for i in range(10):
    rand_ip = str(randint(0, 225)) + '.' + str(randint(0, 225)) + '.' + str(randint(0, 225)) + '.' + str(
        randint(0, 225))
    arr_rand_ip.append(ip_address(rand_ip))


# задание 1
def host_ping(arr_ip, timeout=100, requests=1):
    """
    host_ping() - функция, проверяет доступность ip-адресов из данного ей списка
    :param arr_ip: список ip-адресов
    :param timeout: время ожидания ответа
    :param requests: кол-во запросов
    :return: словарь с результатом проверки
    """
    result = {'Узел доступен': [], 'Узел недоступен': []}

    # перебираю элементы списка
    for elem in arr_ip:
        # тут проверка на корректность адреса
        try:
            _ = ip_address(elem)  # Проверка элемента списка на соответствие IP4/IP6 адресу.
        except ValueError:  # Сюда попадут предположительно хостнеймы.
            try:
                elem = gethostbyname(elem)  # Пытаюсь получить ip-адрес из host name.
            except gaierror:  # В случае неудачи вывожу сообщение в консоль.
                print(f'Attention! Address "{elem}" is not valid!', file=sys.stderr)

        # проверяем доступность узла
        response = Popen(f"ping {elem} -w {timeout} -n {requests}", shell=False, stdout=PIPE)
        response.wait()

        # записываем адреса в словарь
        if response.returncode == 0:
            result['Узел доступен'].append(str(elem))
        else:
            result['Узел недоступен'].append(str(elem))

    return result


# проверяет адреса в диапазоне. можно задать параметры при вызове, либо он сам их попросит с клавиатуры.
# Может проверять как часть адресов, так и их все от 0 до 225, понимает хостнеймы,
# при неправильном указании параметров просит их вновь, пока не получит те, с которыми можно работать.
# (моя гордость)
# задание 2
def host_range_ping(start_ip=None, check_all=False, count=None):
    """
    host_range_ping() - функция, проверяющая доступность ip-адресов в диапазоне
    :param start_ip:    начальный ip. можно задать при вызове функции, если не задан - попросит у юзера
    :param check_all:   если True - проверяем все адреса, от 0 до 255 (последний октет), иначе используем count
    :param count:       количество проверяемых адресов. можно задать при вызове функции, если не задан - попросит у юзера
    :return:            словарь с результатом проверки адресов
    """

    arr_ip = []

    # тут добываю/проверяю начальный адрес
    while True:
        # если не задан стартовый адрес, просим у пользователя
        if start_ip is None:
            start_ip = input('\nВведите ip-адрес: ')

        # в любом случае этот адрес проверяем
        try:
            _ = ip_address(start_ip)  # Проверка элемента списка на соответствие IP4/IP6 адресу.
        except ValueError:  # Сюда попадут предположительно хостнеймы.
            try:
                start_ip = gethostbyname(start_ip)  # Пытаюсь получить ip-адрес из host name.
            except gaierror:  # В случае неудачи вывожу сообщение в консоль.
                print(colored(f'Attention! Address "{start_ip}" is not valid!', 'red'))
                start_ip = None     # раз адрес не подходит, уничтожаю его
                continue            # и прошу у юзера пока не получу нормальный
        break

    # переменная с последним октетом, для читабельности кода
    last_okt = int(start_ip.split('.')[-1])

    # добываем/проверяем count
    # если нужно проверить все адреса - говорим что count = 225 и переходим к созданию списка
    if check_all is True:
        count = 225
    # если же нужно проверять только кусок, если число не задано или неверно - берем его у пользователя пока не
    # получим верное
    else:
        while True:
            if count is None:
                count = int(input('введите кол-во ip-адресов для проверки: '))
            if count > 0:
                # если count выходит за границу, уменьшаем его, чтобы в список попали только нужные адреса
                if last_okt + count > 225:
                    count = 225 - last_okt
            else:
                print('Пожалуйста, введите положительное число!')
                count = None
                continue
            break

    # если нам нужно проверить все адреса - начальному адресу последний октет меняем на 0
    if check_all is True:
        start_ip = ip_address(start_ip) - last_okt

    start_ip = ip_address(start_ip)

    # создаем список адресов
    for n in range(count + 1):
        arr_ip.append(ip_address(start_ip + n))

    # возвращаем словарь - результат проверки списка адресов функцией host_ping
    return host_ping(arr_ip)


# эта функция красиво выодит результат проверки адресов
# задание 3
def host_range_ping_tab(start_ip=None, check_all=False, count=None):
    """
    host_range_ping_tab() - функция, которая красиво выводит результат проверки доступности ip-адресов
    :param start_ip: начальный ip-адрес
    :param check_all: проверять все от 0 до 225 или проверять только часть, опираясь на count
    :param count: кол-во проверяемых адресов (игнорируется, если check_all=True)
    :return: ретерна нет, просто красиво выводится словарь
    """
    dict_ip = host_range_ping(start_ip, check_all, count)
    print(tabulate(dict_ip, headers='keys', tablefmt='pipe', stralign="center"))


host_range_ping_tab('google.com', count=20)


