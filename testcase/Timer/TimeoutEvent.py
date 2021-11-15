
import heapq

from Timer.timestamp import Timestamp
from Timer.event import TimeoutEvent

ts1 = Timestamp(1)
ts2 = Timestamp(3)
ts5 = Timestamp(5)
ts3 = Timestamp(2)
ts4 = Timestamp(4)

te1 = TimeoutEvent(ts1)
te2 = TimeoutEvent(ts2)
te3 = TimeoutEvent(ts3)
te4 = TimeoutEvent(ts4)
te5 = TimeoutEvent(ts5)

heap = [te1, te2, te3, te4, te5]
heapq.heapify(heap)
print(heap)
smallest = heapq.nsmallest(5, heap)
print(smallest)
