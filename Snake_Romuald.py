import pygame
import random


GAME_AREA_WIDTH = 800
GAME_AREA_HEIGHT = 600

PYGAME_COLOR_BLACK = (0, 0, 0)
PYGAME_COLOR_RED = (213, 50, 80)
PYGAME_COLOR_LIME = (0,255,0)
PYGAME_COLOR_WHITE = (255,255,255)
    
class Food:
    
    FOOD_SIZE = 10
    
    def __init__(self, game_area: pygame.Surface):
        self.__x_coord = round(random.randrange(0, GAME_AREA_WIDTH - self.FOOD_SIZE) / 10.0) * 10.0
        self.__y_coord = round(random.randrange(0, GAME_AREA_HEIGHT - self.FOOD_SIZE) / 10.0) * 10.0
        self.__game_area = game_area
        
    @property
    def position(self):
        return (self.__x_coord, self.__y_coord)
    
    def redraw(self) -> None:
        pygame.draw.rect(self.__game_area, PYGAME_COLOR_RED, [self.__x_coord, self.__y_coord, self.FOOD_SIZE, self.FOOD_SIZE])    
        
    def change_position(self) -> None:
        self.__x_coord = round(random.randrange(0, GAME_AREA_WIDTH - self.FOOD_SIZE) / 10.0) * 10.0
        self.__y_coord = round(random.randrange(0, GAME_AREA_HEIGHT - self.FOOD_SIZE) / 10.0) * 10.0
        self.redraw()
 
        
class Snake:
    
    SNAKE_BLOCK_SIZE = 10
    INITIAL_POSITION_X = 400
    INITIAL_POSITION_Y = 300
    INITIAL_SNAKE_SPEED = 15
    DONT_MOVE = (0,0)
    MOVE_LEFT = (-SNAKE_BLOCK_SIZE, 0)
    MOVE_RIGHT = (SNAKE_BLOCK_SIZE, 0) 
    MOVE_UP = (0, -SNAKE_BLOCK_SIZE)
    MOVE_DOWN = (0, SNAKE_BLOCK_SIZE)    
    
    def __init__(self, game_area: pygame.Surface):
        self.__game_area = game_area
        self.speed = self.INITIAL_SNAKE_SPEED
        self.__x_coord = self.INITIAL_POSITION_X
        self.__y_coord = self.INITIAL_POSITION_Y
        self.__motion = self.DONT_MOVE
        self.__body = [(self.INITIAL_POSITION_X, self.INITIAL_POSITION_Y)]
        self.__is_extendable = False
        
    @property
    def size(self)->int:
        return len(self.__body)
    
    @property
    def position(self):
        return (self.__x_coord, self.__y_coord)
        
    def change_direction(self, direction):        
        if (direction == pygame.K_LEFT) and (self.__motion != self.MOVE_RIGHT):
                self.__motion = self.MOVE_LEFT
        elif (direction == pygame.K_RIGHT) and (self.__motion != self.MOVE_LEFT):
                self.__motion = self.MOVE_RIGHT
        elif (direction == pygame.K_UP) and (self.__motion != self.MOVE_DOWN):
                self.__motion = self.MOVE_UP
        elif (direction == pygame.K_DOWN) and (self.__motion != self.MOVE_UP):
                self.__motion = self.MOVE_DOWN
                 
    def grow_up(self) -> None:
        self.__is_extendable = True
        self.speed = ((self.size - 1)//5)*5 + self.INITIAL_SNAKE_SPEED
                
    def is_out_of_game_area(self) -> bool:
        return not ((0<=self.__x_coord<GAME_AREA_WIDTH) and (0<=self.__y_coord<GAME_AREA_HEIGHT))
    
    def is_bite_tail(self) -> bool:
        return any(body_part == self.position for body_part in self.__body[:-1])     
    
    def redraw(self) -> None:
        for x in self.__body:
            pygame.draw.rect(self.__game_area, PYGAME_COLOR_LIME, [x[0], x[1], self.SNAKE_BLOCK_SIZE, self.SNAKE_BLOCK_SIZE])  
        if self.is_out_of_game_area() or self.is_bite_tail():
            raise Exception()    
    
    def update_position(self):
        if self.__motion!=self.DONT_MOVE:
            self.__x_coord += self.__motion[0]
            self.__y_coord += self.__motion[1]
            self.__body.append((self.__x_coord , self.__y_coord))
            
            if not self.__is_extendable:
                del self.__body[0]
            else:
                self.__is_extendable = False
        
class Game:
    def __init__(self):
        pygame.init() 
        self.game_surface = pygame.display.set_mode((GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()    
        self.show_commands()
        self.on_running = False
        
    def start(self):
        self.snake = Snake(self.game_surface)
        self.food = Food(self.game_surface) 
        self.on_running = True
        
    def get_event(self):
        for event in pygame.event.get(): 
            if event.type==pygame.KEYDOWN:  
                return event.key
        return None
                
    def play(self, key):
        self.snake.change_direction(key) 
        
    def run(self): 
        try:
            if self.on_running:              
                self.game_surface.fill(PYGAME_COLOR_BLACK)
                self.snake.update_position()              
                self.snake.redraw()             
                self.food.redraw()                              
                self.verify_food_eat()                    
                self.refresh_score()
                pygame.display.update()       
                self.clock.tick(self.snake.speed)
        except:
            self.game_over()
            
    def pause(self):
        self.on_running = not self.on_running
        self.game_surface.fill(PYGAME_COLOR_BLACK) 
        score_font = pygame.font.SysFont(None, 50)
        value = score_font.render("PAUSE", True, PYGAME_COLOR_LIME)
        self.game_surface.blit(value, [350, 250])
        pygame.display.update() 
        
    def game_over(self):
        self.on_running = False 
        del(self.snake)
        del(self.food)  
        self.show_message("Game Over", PYGAME_COLOR_RED)           
        
    def verify_food_eat(self):
        if self.snake.position == self.food.position:
            self.food.change_position()
            self.snake.grow_up()  
            
    def show_message(self, msg, color):  
        self.game_surface.fill(PYGAME_COLOR_BLACK)  
        font_style = pygame.font.SysFont(None, 50)
        mesg = font_style.render(msg, True, color)
        self.game_surface.blit(mesg, [330, 250])
        pygame.display.update()  
        
    def show_commands(self):  
        self.game_surface.fill(PYGAME_COLOR_BLACK)  
        font_style = pygame.font.SysFont(None, 90)
        mesg = font_style.render("SNAKE", True, PYGAME_COLOR_WHITE)
        self.game_surface.blit(mesg, [290, 40])
        font_style = pygame.font.SysFont(None, 30)
        mesg = font_style.render("COMMANDS:", True, PYGAME_COLOR_WHITE)
        self.game_surface.blit(mesg, [240, 240])
        mesg = font_style.render("ENTER : to start game", True, PYGAME_COLOR_WHITE)
        self.game_surface.blit(mesg, [280, 280])
        mesg = font_style.render("UP/DOWN/LEFT/RIGHT: playing", True, PYGAME_COLOR_WHITE)
        self.game_surface.blit(mesg, [280, 320])
        mesg = font_style.render("SPACE: pause/unpause", True, PYGAME_COLOR_WHITE)
        self.game_surface.blit(mesg, [280, 360])
        mesg = font_style.render("ESC: exit", True, PYGAME_COLOR_WHITE)
        self.game_surface.blit(mesg, [280, 400])
        font_style = pygame.font.SysFont(None, 24)
        mesg = font_style.render("Romuald DUGIED - 2022 - Cours POO FSS", True, PYGAME_COLOR_WHITE)
        self.game_surface.blit(mesg, [30, 580])
        pygame.display.update()  

    def refresh_score(self):
        score_font = pygame.font.SysFont(None, 26)
        value = score_font.render(f"Your Score: {self.snake.size-1}", True, PYGAME_COLOR_WHITE)
        self.game_surface.blit(value, [0, 0])


def main() -> None:
    game = Game()
    while True:
        game.run()
        key = game.get_event()
        if key :
            if key==pygame.K_SPACE:
                game.pause()
            elif key==pygame.K_RETURN:
                game.start()
            elif key==pygame.K_ESCAPE:
                break
            else:
                game.play(key)
            
    pygame.quit()
    quit()  

if __name__ == "__main__":
    main()