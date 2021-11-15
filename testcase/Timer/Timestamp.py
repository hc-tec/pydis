
import time

from Timer.timestamp import Timestamp

def equal(test, answer):
    print(test, answer)
    return abs(test - answer) < 100

H_test = Timestamp(2, 'H')
H_answer = time.time() * 1000 + 2 * 1000 * 60 * 60

assert equal(H_test.get_time(), H_answer)

M_test = Timestamp(3, 'M')
M_answer = time.time() * 1000 + 3 * 1000 * 60

assert equal(M_test.get_time(), M_answer)

S_test = Timestamp(4, 'S')
S_answer = time.time() * 1000 + 4 * 1000

assert equal(S_test.get_time(), S_answer)

MS_test = Timestamp(4000, 'MS')
MS_answer = time.time() * 1000 + 4000

assert equal(MS_test.get_time(), MS_answer)

