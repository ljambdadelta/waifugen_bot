#!/bin/python3.8
import os, random

class WaifuGen():
   
      def __init__(self, arg_default_level = "easy"):
          self.src = os.path.join(os.path.dirname(os.path.realpath(__file__)), "market.conf")
          self.levels = {'easy':'780', 'medium':'550', 'hard':'450'}
          self.MONEY = 0 
          self.GROUPS = 1
          self.default_level = arg_default_level

      def getListOfTraits(self):
          dict_traits = {} 
          with open(self.src, 'r') as marketplace:
            positions = marketplace.read().split("\n")
            for position in positions: 
                try:
                  if position[0] == "#" :
                    continue
                  lst_position = position.split("|")
                  dict_traits[lst_position[0]] = (int(lst_position[1]), lst_position[2].strip())
                except:
                    pass
          return dict_traits

      def _ifSkipThisRound(self, fet_name, fet_attr, used_groups, lst_fetishes):
         skip = False
         if fet_attr[self.GROUPS] and fet_attr[self.GROUPS] in used_groups:
           skip = True
         elif fet_name in lst_fetishes:
           skip = True
         return skip

      def _addFetish(self, fet_name, fet_attr, used_groups, money, money_spent, lst_fetishes):
          if fet_attr[self.GROUPS]:
            used_groups.append(fet_attr[self.GROUPS])
          money = money - fet_attr[self.MONEY]
          money_spent = money_spent + fet_attr[self.MONEY]
          lst_fetishes.append(fet_name)
          return used_groups, money, money_spent, lst_fetishes 

      def roll(self, level=None, money=None):
          # Init vars
          if not level : 
              level = self.default_level
          used_groups, lst_fetishes = ([],[])
          cnt_failures, money_spent = (0,0)
          money = money if money else int(self.levels[level])  
          dict_traits = self.getListOfTraits()
          # Engine 
          while cnt_failures < 10:
            fet_name, fet_attr = random.choice(list(dict_traits.items()))
            if fet_attr[self.MONEY] > money:
                cnt_failures = cnt_failures + 1
                continue
            if self._ifSkipThisRound(fet_name, fet_attr, used_groups, lst_fetishes):
                continue
            used_groups, money, money_spent, lst_fetishes = self._addFetish(fet_name, fet_attr, used_groups, money, money_spent, lst_fetishes)
          # 
          print("result:")
          print(f"""Level:{level}""")
          print(money_spent)
          for fet in lst_fetishes:
              print(fet)
          return lst_fetishes

if __name__ == "__main__":
  WG = WaifuGen("hard")
  WG.roll()



