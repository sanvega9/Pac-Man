import pygame
import sys
from pygame.locals import *
import random
import math

pygame.init()
#screen dimensions
screen_width = 448
screen_height = 576
screen_game = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PAC-MAN')

#colors 
Black = (0,0,0)
yellow = (255, 255, 0)
Blue = (0,0,255)
white = (255,255,255)
Red = (255,0,0)

# pac-man 
pos = [224,288]
speed = 4
radius = 10
direction = [0,0]
#Ghost 
pos_ghost=[224,224]
speed_ghost = 2

#drawing maze
Maze = [
  "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "X............XX............X",
  "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
  "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
  "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
  "X..........................X",
  "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
  "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
  "X......XX....XX....XX......X",
  "XXXXXX.XXXXX XX XXXXX.XXXXXX",
  "XXXXXX.XXXXX XX XXXXX.XXXXXX",
  "XXXXXX.XX          XX.XXXXXX",
  "XXXXXX.XX XXXXXXXX XX.XXXXXX",
  "XXXXXX.XX XXXXXXXX XX.XXXXXX",
  "          XXXXXXXX          ",
  "XXXXXX.XX XXXXXXXX XX.XXXXXX",
  "XXXXXX.XX XXXXXXXX XX.XXXXXX",
  "XXXXXX.XX          XX.XXXXXX",
  "XXXXXX.XX XXXXXXXX XX.XXXXXX",
  "XXXXXX.XX XXXXXXXX XX.XXXXXX",
  "X............XX............X",
  "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
  "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
  "X...XX................XX...X",
  "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
  "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
  "X......XX....XX....XX......X",
  "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
  "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
  "X..........................X",
  "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

mazedots = [[(col_idx*16+8, row_idx*16+8)for col_idx,col in enumerate(row) if col == '.'] for row_idx, row in enumerate(Maze)]

def maze_draw():
  for row_idx, row in enumerate(Maze):
    for col_idx, col in enumerate(row):
      if col == "X":
        pygame.draw.rect(screen_game, Blue, (col_idx*16, row_idx*16, 16, 16))

def dotsdraw():
  for row in mazedots:
    for mazedot in row:
      pygame.draw.circle(screen_game, white, mazedot, 3)

def pacman_movement():
    nextpos = [pos[0]+direction[0] * speed, pos[1]+direction[1] * speed]
    row = int(nextpos[1]/16)
    col = int(nextpos[0]/16)
    if Maze[row][col] != "X":
      pos[0] = nextpos[0]
      pos[1] = nextpos[1]

def ghost_movement():
  global pos_ghost
  direction = [[1,0], [-1,0], [0,1], [0,-1]]
  valid_direction = []
  mindist = float('inf')
  best_direction = [0,0]
  for d in direction:
      next_pos = [pos_ghost[0]+d[0]*speed_ghost, pos_ghost[1]+d[1]*speed_ghost]
      row = int (next_pos[1]/16)
      col = int (next_pos[0]/16)
      if 0 <= row < len(Maze) and 0 <= col < len(Maze[0]) and Maze[row][col] != "X":
         valid_direction.append(d)
         dist = math. hypot(next_pos[0] - pos[0], next_pos[1] - pos[1])
         if dist < mindist:
             mindist = dist
             best_direction = d
             
  if valid_direction:
          pos_ghost[0] += best_direction[0]*speed_ghost
          pos_ghost[1] += best_direction[1]*speed_ghost
          print(f"Ghost moved to {pos_ghost} using directions {best_direction}")
  else:
        random_direction = random.choice(direction)
        pos_ghost[0] += random_direction[0] * speed_ghost
        pos_ghost[1] += random_direction[1] * speed_ghost
        print(f"No vaild directions for ghost movement")
          
def checkcollision():
  pacman_rect = pygame.Rect(pos[0] - radius,pos[1]-radius, radius * 2, radius * 2)
  ghost_rect = pygame.Rect(pos_ghost[0] - radius,pos_ghost[1]-radius, radius * 2, radius * 2)
  return pacman_rect.colliderect(ghost_rect)

def food_dots():
  global mazedots
  center = (pos[0], pos[1])
  for row in mazedots:
      for mazedot in row: 
       if(center[0]-mazedot[0])**2+ (center[1]-mazedot[1])**2 < (radius+3)**2:
        row.remove(mazedot)
          
def win():
    for row in mazedots:
       if row:
         return False
    return True

# game loop start pac man playing
def main():
  clock = pygame.time.Clock()
    
  while True:
    for event in pygame.event.get():
      if event.type == QUIT:
         pygame.quit()
         sys.exit()
      elif event.type == KEYDOWN:
       if event.key == K_LEFT:
         direction[0] = -1
         direction[1] = 0 
       elif event.key == K_RIGHT:
         direction[0] = 1
         direction[1] = 0 
       elif event.key == K_UP:
         direction[0] = 0
         direction[1] = -1 
       elif event.key == K_DOWN:
         direction[0] = 0
         direction[1] = 1 

      pacman_movement()
      ghost_movement()
      food_dots()

      if checkcollision(): 
         print("Game Over")
         pygame.quit()
         sys.exit()
          
      if win():
         print("You Win!")
         pygame.quit()
         sys.exit()

      screen_game.fill(Black)
      maze_draw()
      dotsdraw()
      pygame.draw.circle(screen_game, yellow,(int(pos[0]), int(pos[1])), radius)
      pygame.draw.circle(screen_game,Red, (int(pos_ghost[0]), int(pos_ghost[1])), radius)
      pygame.display.update()
      clock.tick(30)

if __name__ == '__main__':
  main()



