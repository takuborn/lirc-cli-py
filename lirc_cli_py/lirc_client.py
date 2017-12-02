import socket
import time
from threading import Lock

from .exceptions import LircClientException


class LircClient():
    """
    LIRC Client
    """
    __host = None
    __port = None
    __socket = None
    __socket_file = None
    __lock = None
    __cmdRes = None
    
    def __init__(self, host='localhost', port=8765):
        self.__host = host
        self.__port = port

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((host, port))
        self.__socket_file = self.__socket.makefile()

        self.__lock = Lock()

    def __send(self, command):
        """ Send command to LIRC socket """
        cmd = command.strip()

        begin_line_num = 0
        cmd_line_num = 1
        res_line_num = 2
        end_line_num = 3
        end_with_data_line_num = 4
        
        with self.__lock:
            self.__socket.send((cmd + '\n').encode())
            
            line_num = 0
            data_lines = []
            cmd_res = False
            
            while True:
                line = self.__socket_file.readline().strip()
                print(line)

                if line_num == begin_line_num:
                    self.__check_res_begin(line)
                elif line_num == cmd_line_num:
                    self.__check_res_command(line, cmd)
                elif line_num == res_line_num:
                    cmd_res = self.__check_res_cmd_result(line)
                elif line_num == end_line_num:
                    if self.__is_end(line):
                        break
                    
                    self.__check_res_data(line)
                elif line_num == end_with_data_line_num:
                    end_line_num = self.__end_line_num(line)
                elif line_num < end_line_num:
                    data_lines.append(line)

                line_num += 1

        data = '\n'.join(data_lines)
        
        if not cmd_res:
            raise LircClientException('Socket return ERROR ... ' + data)

        return data

    def close(self):
        """ Close socket """
        self.__socket.close()

    def send_once(self, remote, button, repeats = 1):
        """ command SEND_ONCE """
        if repeats > 1:
            bufRepeats = str(repeats)
            
        return self.__send(' '.join(('SEND_ONCE', remote, button, bufRepeats)))

    def send_start(self, remote, button):
        """ command SEND_START """
        return self.__send(' '.join(('SEND_START', remote, button)))

    def send_stop(self, remote, button):
        """ command SEND_STOP """
        return self.__send(' '.join(('SEND_STOP', remote, button)))

    def list(self, remote, button):
        """ command LIST """
        return self.__send(' '.join(('LIST', remote, button)))


    def __check_res_begin(self, line):
        if line != 'BEGIN':
            raise LircClientException('Socket did not return BEGIN.')

    def __check_res_command(self, line, command):
        if line != command:
            raise LircClientException('Socket did not return command name.')

    def __check_res_cmd_result(self, line):
        if line not in ('SUCCESS', 'ERROR'):
            raise LircClientException('Socket did not return SUCCESS or ERROR')

        return True if line == 'SUCCESS' else False

    def __is_end(self, line):
        return True if line == 'END' else False

    def __check_res_data(self, line):
        if line != 'DATA':
            raise LircClientException('Socket did not return DATA')

    def __end_line_num(self, line):
        if not line.isdigit():
            raise LircClientException('Socket did not return end line number')

        return 5 + int(line)
