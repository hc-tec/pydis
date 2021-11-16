

from Generic.time import get_cur_time
from Timer.timestamp import Timestamp

def equal(test, answer):
    print(test, answer)
    return abs(test - answer) < 100

H_test = Timestamp(2, 'H')
H_answer = get_cur_time() + 2 * 1000 * 60 * 60

assert equal(H_test.get_time(), H_answer)

M_test = Timestamp(3, 'M')
M_answer = get_cur_time() + 3 * 1000 * 60

assert equal(M_test.get_time(), M_answer)

S_test = Timestamp(4, 'S')
S_answer = get_cur_time() + 4 * 1000

assert equal(S_test.get_time(), S_answer)

MS_test = Timestamp(4000, 'MS')
MS_answer = get_cur_time() + 4000

assert equal(MS_test.get_time(), MS_answer)

