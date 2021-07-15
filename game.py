import pygame
import random
from network import Network
import uuid

pygame.init()
pygame.display.set_caption('Game')
game_display = pygame.display.set_mode((800,600))
game_exit = True
state = {'fruits':[], 'players':[]}
my_id = str(uuid.uuid4())
name = input('what is your nickname? ')
ARENA_SIZE = 600
OBJ_SIZE = 20

class Player():
    def __init__(self):
        self.reply = {'id':my_id, 'name':name, 'score':0, 'collided':False, 'x':random.randint(0, 580), 'y':random.randint(0, 580)}
        self.SPEED = 0.5
    
    def move_player(self):
        keys = pygame.key.get_pressed()
        if self.reply['id'] == my_id:
            if keys[pygame.K_UP] and self.reply['y'] + OBJ_SIZE / 2 > 10:
                self.reply['y'] = self.reply['y'] - self.SPEED
            if keys[pygame.K_DOWN] and self.reply['y'] - OBJ_SIZE / 2 < 570:
                self.reply['y'] = self.reply['y'] + self.SPEED 
            if keys[pygame.K_LEFT] and self.reply['x'] + OBJ_SIZE / 2 > 10:
                self.reply['x'] = self.reply['x'] - self.SPEED 
            if keys[pygame.K_RIGHT] and self.reply['x'] - OBJ_SIZE / 2 < 570:
                self.reply['x'] = self.reply['x'] + self.SPEED
    
    def player_collision(self):
        try:
            fruit = state['fruits'][0]
            if (self.reply['y'] + OBJ_SIZE / 2 > fruit['y'] - OBJ_SIZE / 2 and  self.reply['y'] - OBJ_SIZE / 2 < fruit['y'] + OBJ_SIZE / 2 
                and self.reply['x'] - OBJ_SIZE / 2 < fruit['x'] + OBJ_SIZE / 2 and self.reply['x'] + OBJ_SIZE / 2 > fruit['x'] - OBJ_SIZE / 2):
                    self.reply['collided'] = True
                    self.reply['score'] = self.reply['score'] + 10
        except Exception:
            pass

def draw_game(display):
    try:
        my_font = pygame.font.SysFont("monospace", 15)

        for fruit in state['fruits']:
            pygame.draw.rect(game_display, (0,255,0), [fruit['x'], fruit['y'], OBJ_SIZE, OBJ_SIZE])

        for index, player in enumerate(sorted(state['players'], key=lambda k: k['score'], reverse=True)):
            display.blit(my_font.render(f'{index + 1}. {player["name"]}: {player["score"]}', 1, (255,255,255)), (610, (index + 1) * 50))
            color = (100, 100, 100)
            if player['id'] == my_id:
                color = (255, 200, 0)
            pygame.draw.rect(game_display, color, [player['x'], player['y'], OBJ_SIZE, OBJ_SIZE])
    except Exception:pass

def game(player):
    global state, game_exit
    game_display.fill((0,0,0))
    pygame.draw.rect(game_display, (255,255,255), [0, 0, ARENA_SIZE, ARENA_SIZE])

    draw_game(game_display)
    player.move_player()
    player.player_collision()
    
    try:
        data = client.send_reply(player.reply)
        state = data
    except Exception:
        pass    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = False
            pygame.quit()

if __name__ == '__main__':
    player = Player()
    client = Network(('192.168.1.67', 12010))

    client.connect(player.reply)

    while game_exit:
        
        game(player)
        player.reply['collided'] = False
        pygame.display.update()    