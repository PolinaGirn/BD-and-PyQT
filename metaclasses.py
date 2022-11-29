import dis


class ServerVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        """
        :param clsname: экземпляр метакласса - Server
        :param bases: кортеж базовых классов - ()
        :param clsict: словарь атрибутов и методов экземпляра метакласса
        {'__module__': '__main__',
        '__qualname__': 'Server',
        'port': <descrptrs.Port object at 0x000000DACC8F5748>,
        '__init__': <function Server.__init__ at 0x000000DACCE3E378>,
        'init_socket': <function Server.init_socket at 0x000000DACCE3E400>,
        'main_loop': <function Server.main_loop at 0x000000DACCE3E488>,
        'process_message': <function Server.process_message at 0x000000DACCE3E510>,
        'process_client_message': <function Server.process_client_message at 0x000000DACCE3E598>}
        """

        methods = []    # список методов, используемых в функциях класса
        attrs = []      # атрибуты, используемые в функциях классов

        # перебираем ключи
        for func in clsdict:
            # проверяем, функция ли
            try:
                # итератор по инструкциям в предоставленной функции
                ret = dis.get_instructions(clsdict[func])
            except TypeError:   # если не функция - исключение
                pass

            else:               # если функция
                # перебираем код, получаем методы и атрибуты (записываем в массивы)
                for i in ret:
                    print(i)
                    # i - Instruction(opname='LOAD_GLOBAL', opcode=116, arg=9, argval='send_message',
                    # argrepr='send_message', offset=308, starts_line=201, is_jump_target=False)
                    # opname - имя для операции

                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)    # заполняем список методами
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            attrs.append(i.argval)      # заполняем список атрибутами
        print(methods)

        if 'connect' in methods:
            raise TypeError('Нельзя использовать метод connect в серверном классе')

        # если сокет не инициализировался константами SOCK_STREAM(TCP) AF_INET(IPv4) - исключение
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета')

        # вызываем конструктор предка (обязательно)
        super().__init__(clsname, bases, clsdict)



class ClientVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        """
        :param clsname: экземпляр метакласса - Server
        :param bases: кортеж базовых классов - ()
        :param clsict: словарь атрибутов и методов экземпляра метакласса
        {'__module__': '__main__',
        '__qualname__': 'Server',
        'port': <descrptrs.Port object at 0x000000DACC8F5748>,
        '__init__': <function Server.__init__ at 0x000000DACCE3E378>,
        'init_socket': <function Server.init_socket at 0x000000DACCE3E400>,
        'main_loop': <function Server.main_loop at 0x000000DACCE3E488>,
        'process_message': <function Server.process_message at 0x000000DACCE3E510>,
        'process_client_message': <function Server.process_client_message at 0x000000DACCE3E598>}
        """

        methods = []    # список методов, используемых в функциях класса

        # перебираем ключи
        for func in clsdict:
            # проверяем, функция ли
            try:
                # итератор по инструкциям в предоставленной функции
                ret = dis.get_instructions(clsdict[func])
            except TypeError:  # если не функция - исключение
                pass

            else:  # если функция
                # перебираем код, получаем методы и атрибуты (записываем в массивы)
                for i in ret:
                    print(i)
                    # i - Instruction(opname='LOAD_GLOBAL', opcode=116, arg=9, argval='send_message',
                    # argrepr='send_message', offset=308, starts_line=201, is_jump_target=False)
                    # opname - имя для операции

                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)  # заполняем список методами

            # далее проверки
            for evil in ('accept', 'listen', 'socket'):
                if evil in methods:
                    raise TypeError('Нельзя использовать методы accept, listen, socket в клиентском классе')

            if 'get_message' in methods or 'send_message' in methods:
                pass
            else:
                raise TypeError('Нет функций, работающих с сокетами')

            super().__init__(clsname, bases, clsdict)

































