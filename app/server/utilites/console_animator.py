#===============================================================
# @author:  nityanarayan44@live.com
# @written: 08 December 2021
# @desc:    Console usility for prining the messages on console.
#===============================================================

from time import sleep
from typing import overload

class ConsoleAnimator:
    def __init__(self) -> None:
        pass
    
    def print_with_delay(self, main_string=None, loading_string='', delay_time=0.5) -> None:
        print(main_string, end='')
        for i in range(len(loading_string)):
            print(loading_string[i], sep='', end='', flush=True); sleep(delay_time)
        print('')

    def print_msg_with_title(self, title, msg, dash_length=30) -> None:
        print('\n\n+'+'-'*dash_length+'['+title+']'+'-'*dash_length+'+\n|', msg)
        

