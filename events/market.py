# Торговля
import random, re
import data, ask, act
from event import Event
from info import Info



class Market(Event):
    """docstring for Market"""
    
    def invoke(self):
        if self.data.embargo:
            self.data.probability['Market'] = 0
            self.say.line("   ЧП! Экономическая блокада!\n")
        else:
            self.data.probability['Market'] = 100
            self.say.line("   Торговля - двигатель прогресса\n")
        super().invoke()
    
    
    def start(self):
        info = Info(self.data)
        """docstring for start"""
        complete = False
        self.say.line("\n")
        while not complete:
            self.say.erase_line(2)
            self.broker_wants = round(self.data.money * random.uniform(0.2, 0.99))
            self.say.line("   Маклер просит {:>10n} руб.".format(self.broker_wants))
            if self.ask.yesno("Желаете использовать маклера?"):
                complete = self.broker()
                continue
            
            self.say.erase_line(2)
            if self.ask.yesno("Желаете сами торговать?"):
                complete = self.manual()
            else:
                self.say.erase_line()
                break
        else:
            self.say.clear_screen()
            info.big_table()
    
    
    def manual(self):
        """ Сколько чего продать/купить """
        debet = self.data.money
        credit = 0
        self.say.erase_line()
        self.say.line("            (+) Покупайте / Продавайте (-):")
        self.say.word("Золото (кг), земля (га), зерно (т), рабочие, солдаты (чел)? ")
        answer = re.search(r"""(?P<gold>[-+]?\d+)     # 1 золото
                               ([^0-9+-]+)? # delimiter
                               (?P<land>[-+]?\d+)?    # 3 земля
                               ([^0-9+-]+)? # delimiter
                               (?P<corn>[-+]?\d+)?    # 5 зерно
                               ([^0-9+-]+)? # delimiter
                               (?P<peasant>[-+]?\d+)? # 7 рабочие
                               ([^0-9+-]+)? # delimiter
                               (?P<soldier>[-+]?\d+)? # 9 солдаты
                               """,
                      input().strip(),
                      re.VERBOSE)
        if answer:
            # проверить достаточность товаров и рассчитать предварительный итог
            for resource in self.data.resources.keys():
                value = int(answer.group(resource) or 0)
                if value > 0:
                    credit += value * self.data.prices[resource]
                elif value < 0:
                    if abs(value) > self.data.resources[resource]:
                        self.say.erase_line(2)
                        print("Вы продаёте товара больше, чем у вас есть!")
                        return not ask.yesno("Повторить?")
                    else:
                        debet += abs(value) * self.data.prices[resource]
            # проверка достаточности денег
            if debet - credit < 0:
                self.say.erase_line(2)
                print("Сделка расторгнута - нехватает {:>10n} руб.".format(debet - credit))
                return not self.ask.yesno("Повторить?")
            else:
                # всё верно - завершить сделку
                for resource in self.data.resources.keys():
                    self.data.money = debet - credit
                    value = int(answer.group(resource) or 0)
                    self.data.resources[resource] += value
                return True
        else:
            return False
                
    
    def broker(self):
        """ Маклер """
        pass