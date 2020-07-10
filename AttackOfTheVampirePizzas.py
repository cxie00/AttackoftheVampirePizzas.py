# Code This Game by Meg Ryan, 2019
# Coded by Chloe Xie 2020
import pygame
from pygame import *
from random import randint
 
# initialize pygame
pygame.init()
 
clock = time.Clock()
#----------------------------------
# define constant variables
 
# define game window parameters
WINDOW_WIDTH = 1100 # make 800 for repl.it
WINDOW_HEIGHT = 600
WINDOW_RES = (WINDOW_WIDTH, WINDOW_HEIGHT)
 
# define tile parameters
WIDTH = 100
HEIGHT = 100
 
# define colors
WHITE = (255, 255, 255)
 
# define rates
SPAWN_RATE = 360
FRAME_RATE = 60
 
# set up counters
STARTING_BUCKS = 15
BUCK_RATE = 120
STARTING_BUCK_BOOSTER = 1
 
# set up win/lsoe conditions
MAX_BAD_REVIEWS = 3
WIN_TIME = FRAME_RATE * 60 * 3
 
# chapter 9: define speeds
REG_SPEED = 2
SLOW_SPEED = 1
 
#------------------------------------
# load assets!
# create a game window
GAME_WINDOW = display.set_mode(WINDOW_RES)
display.set_caption('Attack of the Vampire Pizzas!')
 
# set up the background image
background_img = image.load('restaurant.jpg')
background_surf = Surface.convert_alpha(background_img)
BACKGROUND = transform.scale(background_surf, WINDOW_RES)
 
# set up the enemy image
pizza_img = image.load('vampire.png')
pizza_surf = Surface.convert_alpha(pizza_img)
VAMPIRE_PIZZA = transform.scale(pizza_surf, (WIDTH, HEIGHT))
 
garlic_img = image.load('garlic.png')
garlic_surf = Surface.convert_alpha(garlic_img)
GARLIC = transform.scale(garlic_surf, (WIDTH, HEIGHT))
 
cutter_img = image.load('pizzacutter.png')
cutter_surf = Surface.convert_alpha(cutter_img)
CUTTER = transform.scale(cutter_surf, (WIDTH, HEIGHT))
 
pepperoni_img = image.load('pepperoni.png')
pepperoni_surf = Surface.convert_alpha(pepperoni_img)
PEPPERONI= transform.scale(pepperoni_surf, (WIDTH, HEIGHT))
#-----------------------------
# chapter 6: set up class for vampire sprite
 
# VampireSprite is a subclass of Sprite,  a class of objects in Pygame lib
class VampireSprite(sprite.Sprite):
  def __init__(self):
    # inherit behaviors from the Sprite clas and use them for VampireSprite
    super().__init__()
    self.speed = REG_SPEED
    self.lane = randint(0, 4)
    all_vampires.add(self)
    self.image = VAMPIRE_PIZZA.copy()
    y = 50 + self.lane * 100
    self.rect = self.image.get_rect(center = (1100, y))
    self.health = 100
 
  # set up enemy movement
  def update(self, game_window, counters):
    game_window.blit(BACKGROUND, (self.rect.x, self.rect.y), self.rect)
    self.rect.x -= self.speed
    if self.health <= 0 or self.rect.x <= 100:
      self.kill()
      if self.rect.x <= 100:
        counters.bad_reviews += 1
    else:
      game_window.blit(self.image, (self.rect.x, self.rect.y))
 
  def attack(self, tile):
    if tile.trap == SLOW:
      self.speed = SLOW_SPEED
    if tile.trap == DAMAGE:
      self.health -= 1
 
# create an object for tracking the game state 
class Counters(object):
 
  def __init__(self, pizza_bucks, buck_rate, buck_booster, timer):
    self.loop_count = 0
    self.display_font = font.Font('pizza_font.ttf', 25)
    self.pizza_bucks = pizza_bucks
    self.buck_rate = buck_rate
    self.buck_booster = buck_booster
    self.bucks_rect = None
    self.timer = timer
    self.timer_rect = None
    self.bad_reviews = 0
    self.bad_rev_rect = None
 
  # set the rate that the player earns pizza bucks
  def increment_bucks(self):
    if self.loop_count % self.buck_rate == 0:
      self.pizza_bucks += self.buck_booster
    
  # display pizza bucks total on the screen
  def draw_bucks(self, game_window):
    if bool(self.bucks_rect):
      game_window.blit(BACKGROUND, (self.bucks_rect.x, self.bucks_rect.y), self.bucks_rect)
    bucks_surf = self.display_font.render(str(self.pizza_bucks), True, WHITE)
    self.bucks_rect = bucks_surf.get_rect()
    self.bucks_rect.x = WINDOW_WIDTH - 50
    self.bucks_rect.y = WINDOW_HEIGHT - 50
    game_window.blit(bucks_surf, self.bucks_rect)
 
  # display bad reviews total on the screen
  def draw_bad_reviews(self, game_window):
    if  bool(self.bad_rev_rect):
      game_window.blit(BACKGROUND, (self.bad_rev_rect.x, self.bad_rev_rect.y), self.bad_rev_rect)
    bad_rev_surf = self.display_font.render(str(self.bad_reviews), True, WHITE)
    self.bad_rev_rect = bad_rev_surf.get_rect()
    self.bad_rev_rect.x = WINDOW_WIDTH - 150
    self.bad_rev_rect.y = WINDOW_HEIGHT - 50
    game_window.blit(bad_rev_surf, self.bad_rev_rect)
    
  # display the time remaining on the screen
  def draw_timer(self, game_window):
    if bool(self.timer_rect):
      game_window.blit(BACKGROUND, (self.timer_rect.x, self.timer_rect.y), self.timer_rect)
    timer_surf = self.display_font.render(str((WIN_TIME - self.loop_count) // FRAME_RATE), True, WHITE)
    self.timer_rect = timer_surf.get_rect()
    self.timer_rect.x = WINDOW_WIDTH - 250
    self.timer_rect.y = WINDOW_HEIGHT - 50
    game_window.blit(timer_surf, self.timer_rect)
    
  # increment the game loop counter and call the other Counters methods
  def update(self, game_window):
    self.loop_count += 1
    self.increment_bucks()
    self.draw_bucks(game_window)
    self.draw_bad_reviews(game_window)
    self.draw_timer(game_window)
 
# create a trap object
class Trap(object):
 
  # set up instances of each kind of trap
  def __init__(self, trap_kind, cost, trap_img):
    self.trap_kind = trap_kind
    self.cost = cost
    self.trap_img = trap_img
 
# create a object that activates traps
class TrapApplicator(object):
 
  # set up TrapApplicator instances
  def __init__(self):
    self.selected = None
  
  # activate a trap button
  def select_trap(self, trap):
    if trap.cost <= counters.pizza_bucks:
      self.selected = trap
  
  # lay a trap on a specific tile
  def select_tile(self, tile, counters):
    self.selected = tile.set_trap(self.selected, counters)
 
#-----------------------------
# class for tiles that will have traps sets on them
class BackgroundTile(sprite.Sprite):
  def __init__(self, rect):
    super().__init__()
    self.trap = None
    self.rect = rect
 
# create a subclass for tiles in the play area
class PlayTile(BackgroundTile):
 
  # lay traps on tiles in the play area
  def set_trap(self, trap, counters):
    if bool(trap) and not bool(self.trap):
      counters.pizza_bucks -= trap.cost
      self.trap = trap
      if trap == EARN:
        counters.buck_booster += 1
    return None
 
  def draw_trap(self, game_window, trap_applicator):
    if bool(self.trap):
      game_window.blit(self.trap.trap_img, (self.rect.x, self.rect.y))
 
# subclass of tiles that are trap buttons
class ButtonTile(BackgroundTile):
 
  # click on a trap button to select the trap
  def set_trap(self, trap, counters):
    if counters.pizza_bucks >= self.trap.cost:
        return self.trap
    else:
      return None
 
  # highlight the trap button that was clicked
  def draw_trap(self, game_window, trap_applicator):
    if bool(trap_applicator.selected):
      if trap_applicator.selected == self.trap:
        draw.rect(game_window, (238, 190, 47), (self.rect.x, self.rect.y, WIDTH, HEIGHT), 5)
 
# create a subclass for tiles that are not interactive
class InactiveTile(BackgroundTile):
 
  # do nothing if clicked
  def set_trap(self, trap, counters):
    return None
  
  # do not display anything
  def draw_trap(self, game_window, trap_applicator):
    pass
 
#-------------------------------------------------- 
# create  instances
all_vampires = sprite.Group()
 
counters = Counters(STARTING_BUCKS, BUCK_RATE, STARTING_BUCK_BOOSTER, WIN_TIME)
 
SLOW = Trap('SLOW', 5, GARLIC)
DAMAGE = Trap('DAMAGE', 3, CUTTER)
EARN = Trap('Earn', 7, PEPPERONI)
 
trap_applicator = TrapApplicator()
#-----------------------------
# initialize and draw background grid
 
# we create an empty tile list to overlay invisible sprite tiles
tile_grid = []
 
tile_color = WHITE
 
for row in range(6):
  row_of_tiles = []
  tile_grid.append(row_of_tiles)
  for column in range(11):
    tile_rect = Rect(WIDTH * column, HEIGHT * row, WIDTH, HEIGHT)
    # first two columns are inactive tiles
    if column <= 1:
      new_tile = InactiveTile(tile_rect)
    else:
      if row == 5:
        if 2 <= column <= 4: 
          new_tile = ButtonTile(tile_rect)
          new_tile.trap = [SLOW, DAMAGE, EARN][column - 2]
        else:
          new_tile = InactiveTile(tile_rect)
      else: 
        # label as PlayTile if not first two columns or bottom row
        new_tile = PlayTile(tile_rect)
    row_of_tiles.append(new_tile)
    # row 5 and column 2, 3, and 4 are button tiles
    if row == 5 and 2 <= column <= 4:
      # tests if the tile is one of the three buttons and displays the correct image on each button
      BACKGROUND.blit(new_tile.trap.trap_img, (new_tile.rect.x, new_tile.rect.y))
    # tests anywhere OTHER than a button and displays the background image
    if column != 0 and row != 5:
      if column != 1:
        draw.rect(BACKGROUND, tile_color, (WIDTH * column, HEIGHT * row, WIDTH, HEIGHT), 1)
 
#displays images on the screen
GAME_WINDOW.blit(BACKGROUND, (0, 0))
 
#--------------------------------
# game loop
game_running = True
program_running = True
 
while game_running:
 
  # ------------------
  # check for events 
 
  # main game loop to check and hadnle events
  for event in pygame.event.get():
    # exit loop when game window closes
    if event.type == QUIT:
      game_running = False
      program_running = False
    # respond to mouse click
    elif event.type == MOUSEBUTTONDOWN:
      # get the (x,y) coord where mouse was clicked on screen
      coordinates = mouse.get_pos()
      x = coordinates[0]
      y = coordinates[1]
      # find the background tile at the location where the mouse was clicked and change the value of the effect to True
      tile_x = x // 100
      tile_y = y // 100
      trap_applicator.select_tile(tile_grid[tile_y][tile_x], counters)
 
  # spawn vampire pizza sprites 
  if randint(1, SPAWN_RATE) == 1:
    VampireSprite()
 
  #---------------------------------
  # set up collison detection
  
  # draw background grid
  for tile_row in tile_grid:
    for tile in tile_row:
      if bool(tile.trap):
        GAME_WINDOW.blit(BACKGROUND, (tile.rect.x, tile.rect.y), tile.rect)
  
  # set up detection for collision with background tiles
  for vampire in all_vampires:
    tile_row = tile_grid[vampire.rect.y // 100]
    vamp_left_side = vampire.rect.x // 100
    vamp_right_side = (vampire.rect.x + vampire.rect.width) // 100
 
    if 0 <= vamp_left_side <= 10:
      left_tile = tile_row[vamp_left_side]
    else: 
      # return no column if sprite isn't on grid
      left_tile = None
    if 0 <= vamp_right_side <= 10:
        right_tile = tile_row[vamp_right_side]
    else:
      right_tile = None
 
    # test if the left side of sprite is touching a tile and if that tile has been clicked
    if bool(left_tile):
      vampire.attack(left_tile)
    # test if the right side of the sprite is touching a tile and if that tile has been clicked
    if bool(right_tile):
      if right_tile != left_tile:
        vampire.attack(right_tile)
 
  #-----------------------
  # set win/lose conditions
 
  # test for lose conditions
  if counters.bad_reviews >= MAX_BAD_REVIEWS:
    game_running = False
  # test for win condition
  if counters.loop_count > WIN_TIME:
    game_running = False
  
  #-----------------------
  # update displays
  for vampire in all_vampires:
    vampire.update(GAME_WINDOW, counters)
 
  for tile_row in tile_grid:
    for tile in tile_row:
      tile.draw_trap(GAME_WINDOW, trap_applicator)
 
  # update counters
  counters.update(GAME_WINDOW)
 
  # update all images on the screen
  display.update()
 
  clock.tick(FRAME_RATE)
 
#-------------------------------
 
# set up end game messages
end_font = font.Font('pizza_font.ttf', 50)
if program_running:
  if counters.bad_reviews >= MAX_BAD_REVIEWS:
    end_surf = end_font.render('Game Over', True, WHITE)
  else:
    end_surf = end_font.render('You win!', True, WHITE)
  GAME_WINDOW.blit(end_surf, (350, 200))
  display.update()
 
# enable exit from end game message screen
while program_running:
  for event in pygame.event.get():
    program_running = False
  clock.tick(FRAME_RATE)
#-------------------------------
# close the main game loop
pygame.quit()

