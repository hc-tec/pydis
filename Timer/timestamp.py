
import time

class Timestamp:

    def __init__(self, _time, format='MS'):
        '''

        :param time: time provide by caller
        :param format: 'H' or 'M' or 'S' or 'MS'
        '''
        self.__time = time.time() * 1000
        format_func = getattr(self, f'_format_from_{format}')
        self.__time += format_func(_time)

    def get_time(self):
        return self.__time

    def _format_from_MS(self, _time):
        return _time

    def _format_from_S(self, _time):
        return _time * 1000

    def _format_from_M(self, _time):
        return _time * 1000 * 60

    def _format_from_H(self, _time):
        return _time * 1000 * 60 * 60
