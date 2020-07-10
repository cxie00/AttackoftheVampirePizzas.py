# from Code This Game by Meg Ryan 2019
# Chloe Xie for CN 
# Chapter 5

class Monster(object):
  eats = 'food'
  def __init__(self, name):
    self.name = name
  def speak(self):
    print(self.name + ' speaks')
  def eat(self, meal):
    if meal == self.eats:
      print('yum!')
    else:
      print('blech!')
"""
my_monster = Monster('Spooky Snack')
my_monster.speak()
my_monster.eat('food')"""

# subclass of Monster
class FrankenBurger(Monster):
  eats = 'hamburger patties'
  # define any attributes that are different from the superclass
  # this speak OVERRIDES the Monster method speak
  def speak(self): 
    print('My name is ' + self.name + 'Burger')
"""
my_frankburger = FrankenBurger('Veggiesaurus')
my_frankburger.speak()
my_frankburger.eat('pickles') """

class WereWatermelon(Monster):
    eats = 'watermelon juice'
    def speak(self):
        print('My name is Were' + self.name)

monster_selection = input('What kind of monster do you want to create? Select: frankenburger or werewatermelon? ')
monster_name = input('What do you want to name your monster? ')
monster_meal = input('What will you feed your monster? ')

if monster_selection == 'frankenburger':
    monster_type = FrankenBurger
elif monster_type == 'werewatermelon':
    monster_type = WereWatermelon
else:
    monster_type = Monster

my_monster = monster_type(monster_name)
my_monster.speak()
my_monster.eat(monster_meal)