# Митрополит
import data, ask, say, act
from event import Event
from info import Info

class Church(Event):
    """ Митрополит """
    
    money = 0
    buildings = 0
    price = 100000
    
    generous = [
        'Всевышний благословит ваше правление на долгие годы!',
        'Во всех храмах служат здравицу великому королю!',
        'Слава королю, щедрому и мудрому правителю!'
    ]
    nice = ['Вы чрезмерно скупы, ваше величество!']
    greedy = ['Вы что, насмехаетесь?! Скряга!']
    
    #
    def invoke(self):
        """docstring for invoke"""
        if self.data.money == 0:
            self.data.probability['Church'] = 0
        else:
            self.data.probability['Church'] = self.ask.rand(10, 50)
        super().invoke()
    
    #
    def start(self):
        """ Выделение средств на храм """
        self.say.line("Митрополит ожидает средства на постройку храма.")
        info = Info(self.data)
        info.treasury()
        error = True
        while error:
            spend, error, msg = self.ask.number("Сколько выделяете?", self.data.money)
            if error:
                self.say.line(msg)
        
        percent = spend / (self.data.money + 1) * 100
        self.say.clear_screen()
        if percent > 40:
            self.say.line(self.ask.choice(self.generous))
        elif percent > 20:
            self.say.line(self.ask.choice(self.nice))
        else:
            self.say.line(self.ask.choice(self.greedy))
        
        self.data.money -= spend
        self.money += spend
        
        self.build()
    
    #
    def build(self):
        while self.money > self.price:
            self.say.line(" -=- Воздвигнут храм! -=-")
            self.money -= self.price
