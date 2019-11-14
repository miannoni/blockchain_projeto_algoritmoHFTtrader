from backtesting import evaluateHist
from strategy import Strategy
from order import Order
from event import Event
import numpy as np
import collections
import random

class BrainyApeTrade(Strategy):
    def __init__(self):
        self.prices = collections.deque(maxlen=30)
        self.shorttermprices = collections.deque(maxlen=3)
        self.side = 0
        self.repeating = collections.deque(maxlen=5)

    # A gente tentou só usar Bollinger bands, mas foi necessario aperfeicoar o metodo
    # de boillinger bands pra obter o melhor resultado
    def push(self, event):
        self.prices.append(event.price)
        self.shorttermprices.append(event.price)
        orders = []
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
        
        if ((30 > prob) and (sum(self.repeating) != -5)):
            self.repeating.append(-1)
            if (prob == 0):
                orders.append(Order(event.instrument, -1, 0))
            orders.append(Order(event.instrument, -1, 0))

        if ((70 < prob) and (sum(self.repeating) != 5)):
            self.repeating.append(1)
            if (prob == 1):
                orders.append(Order(event.instrument, 1, 0))
            orders.append(Order(event.instrument, 1, 0))

        if len(orders) > 0:
            for order in orders:
                print(order.print())

        return orders

    def fill(self, id, instrument, price, quantity, status):
        super().fill(id, instrument, price, quantity, status)
        self.side += quantity
        print(self.position)

print(evaluateHist(BrainyApeTrade(), {'IBOV': '^BVSP.csv'}))
