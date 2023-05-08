# Распределение зерна на еду и на посев
import re
import data, ask, act
from event import Event

class Distribute(Event):
    """Распределение зерна"""

    def __init__ (self, data, say, ask):
        self.data = data
        self.say = say
        self.ask = ask
        self.input_func = lambda: input().strip().lower()

    #
    def start(self):
        """docstring for start"""
        self.min_for_food = self.data.resources['peasant'] + self.data.resources['soldier'] + 1
        self.min_for_seed = min(self.data.resources['peasant'], self.data.resources['land'])
    
        if self.ask.yesno("Желаете сами распорядиться запасами зерна?") \
           or self.min_for_food + self.min_for_seed > self.data.resources['corn']:
               self.manually()
               msg = "Остаток зерна в амбарах: {:>10n} тонн"
        else:
            self.automatically()
            msg = "Излишки зерна в амбарах: {:>10n} тонн"
        
        self.data.resources['corn'] -= self.data.corn_for_food
        self.data.resources['corn'] -= self.data.corn_for_seed
        self.say.line(msg.format(self.data.resources['corn']))
    
    #
    def automatically(self):
        """ Дефолтная раздача """
        
        data.corn_for_food = self.min_for_food
        data.corn_for_seed = self.min_for_seed
        self.say.erase_line()
        self.say.line("--> Выделена норма: {:>10n} тонн зерна".format(self.min_for_food + self.min_for_seed))
        
    #
    def manually(self):
        """ Сколько зерна на еду, сколько на посев """
        
        [self.data.corn_for_food, self.data.corn_for_seed] = self.corn(self.data.resources['corn'])
    
    
    #
    def corn(self, max, try_once=False):
        """ Сколько зерна на еду, сколько на посев """
    
        done = False
        while not done:
            self.say.erase_line()
            self.say.word("Сколько тонн зерна на еду, сколько на посев?")
            answer = re.findall('[0-9]+', self.input_func())
        
            try:
                food = int(answer[0])
                seed = int(answer[1])
            
                if food > max:
                    done = try_once
                    food = -1
                    seed = -1
                elif food + seed > max:
                    done = True
                    seed = max - food
                else:
                    done = True
            except ValueError:
                done = try_once
            
        return [food, seed]
        
