# Модуль наследства
import random
import data
from event import Event
from info import Info

info = Info(data)

class Inheritance(Event):
    """docstring for Inheritance"""

    def start(self):
        """docstring for start"""
        money = round(self.data.money * random.uniform(0.1, 2))
        resources = {
            'gold': round(self.data.resources['gold'] * random.uniform(0.1, 2)),
            'land': round(self.data.resources['land'] * random.uniform(0.1, 2)),
            'corn': round(self.data.resources['corn'] * random.uniform(0.1, 2)),
            'peasant': round(self.data.resources['peasant'] * random.uniform(0.1, 2)),
            'soldier': round(self.data.resources['soldier'] * random.uniform(0.1, 2))
        }
        
        self.say.line("\nВам досталось наследство:")
        info.small_table(money, resources)
        
        self.data.money += money
        self.data.resources['gold'] += resources['gold']
        self.data.resources['land'] += resources['land']
        self.data.resources['corn'] += resources['corn']
        self.data.resources['peasant'] += resources['peasant']
        self.data.resources['soldier'] += resources['soldier']
        
        
        