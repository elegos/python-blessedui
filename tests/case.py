from typing import Sized
from unittest import TestCase as TC


class TestCase(TC):
    '''
    TestCase extension class
    '''

    def assertLen(self, expected: int, lst: Sized, msg: str = ''):
        length = len(lst)
        if length != expected:
            message = f'{length} != {expected}'
            if msg != '':
                message += f' {msg}'

            raise AssertionError(message)
