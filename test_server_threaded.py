""""
Просьба выполнить тестовое задание: необходимо сделать tcp сервер, который распознаёт заданный формат данных и отображает его в требуемом формате.
Обязательна запись данных во внешний файл. Интерфейс и способ отображения на выбор разработчика.

Формат данных BBBBxNNxHH:MM:SS.zhqxGGCR
Где BBBB - номер участника x - пробельный символ NN - id канала HH - Часы MM - минуты SS - секунды zhq - десятые сотые тысячные GG - номер группы CR - «возврат каретки» (закрывающий символ)

Пример данных: 0002 C1 01:13:02.877 00[CR] Выводим «спортсмен, нагрудный номер BBBB прошёл отсечку NN в «время»" до десятых, сотые и тысячные отсекаются.
Только для группы 00. Для остальных групп данные не отображаются, но пишутся в лог полностью.

Передача данных должна поддерживаться с помощью telnet клиента.
"""

import socket
import telnetlib
import threading

class Server:

    def __init__(self):

        self.host = socket.gethostbyname(socket.gethostname())
        port = 23
        self.__raw_data_collector = []
        self.__formated_data = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, port))
        print(f'Server has being started at IP {self.host} with opened port number {port}')
        self.server.listen(5)

    def __receiving_data(self, conn):

        while True:
            data = conn.recv(4096)
            if not data:
                break
            else:
                print('Data recieved')
                self.__raw_data_collector.append(data.decode('utf8'))

    def __formating_data(self):

        self.__formated_data.append(self.__raw_data_collector[-1].split())

    def __printing_data(self):

        current = self.__formated_data[-1]
        if '00' in current[3]:
            print('#######################################################################################')
            print(f'спортсмен, нагрудный номер {current[0]} прошёл отсечку {current[1]} в {current[2][:10]}')
            print('#######################################################################################')
        else:
            pass

    def __writing_data(self):

        try:
            with open('server_log.txt', 'a') as log_file:
                log_file.write(self.__raw_data_collector[-1] + '\n')
        except FileNotFoundError:
            with open('server_log.txt', 'w') as log_file:
                log_file.write(self.__raw_data_collector[0] + '\n')

    def send_to_telnet(self, host=None, message=None):

        if host and message == None:
            pass
        else:
            telnet = telnetlib.Telnet(host)
            telnet.write(message.encode('utf8'))

    def function_arranger(self, conn, adr):
        self.__receiving_data(conn)
        self.__formating_data()
        self.__printing_data()
        self.__writing_data()

    def run_connection(self):

        while True:
            print(' --- Awaiting for connection --- ')
            conn, adr = self.server.accept()
            try:
                print(f'Connected to {self.host}')
                thread_start = threading.Thread(target=self.function_arranger, args=(conn, adr))
                thread_start.run()
            finally:
                conn.close()


if __name__ == '__main__':

    server = Server()
    server.run_connection()

