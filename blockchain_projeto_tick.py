from backtesting import evaluateTick
from strategy import Strategy
from order import Order
from event import Event
import collections
import numpy as np
import random

class BrainyApeTrade(Strategy):
    def __init__(self):
        self.prices = collections.deque(maxlen=10000)
        self.shorttermprices = collections.deque(maxlen=1000)
        self.side = 0


    # Eu não sei exatamente por que, mas ele ta acertando 100% das vezes
    # Mesmo assim, pelo retorno médio e o custo hipotetico de executar cada transação, eu acho que ele não daria lucro
    def push(self, event):
        self.prices.append(event.price)
        self.shorttermprices.append(event.price)
        orders = []
        if event.type == Event.TRADE:
            precos = np.array(list(self.shorttermprices))
            tinyrollingmean = np.mean(precos)
            precos = np.array(list(self.prices))
            rollingmean = np.mean(precos)
            std = np.std(precos)
            upperband = rollingmean + std*2
            lowerband = rollingmean - std*2

            if tinyrollingmean > upperband:
                prob = 100
            elif tinyrollingmean < lowerband:
                prob = 0
            else:
                prob = ((tinyrollingmean - lowerband)/(upperband - lowerband))*100
            
            if ((10 > prob)):
                if (prob == 0):
                    orders.append(Order(event.instrument, 1, 0))
                orders.append(Order(event.instrument, 1, 0))

            if ((70 < prob)):
                if (prob == 1):
                    orders.append(Order(event.instrument, -1, 0))
                orders.append(Order(event.instrument, -1, 0))

        if len(orders) > 0:
            for order in orders:
                print(order.print())

        return orders

    def fill(self, id, instrument, price, quantity, status):
        super().fill(id, instrument, price, quantity, status)
        self.side += quantity
        print(self.position)

print(evaluateTick(BrainyApeTrade(), {'PETR4': '2018-03-07.csv'}))
