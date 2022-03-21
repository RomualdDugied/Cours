import pygame
import random

GAME_AREA_WIDTH = 800
GAME_AREA_HEIGHT = 600
PYGAME_COLOR_BLACK = pygame.Color(50, 50, 50, 255)
PYGAME_COLOR_RED = pygame.Color(213, 50, 80, 255)
PYGAME_COLOR_LIME = pygame.Color(0, 255, 0, 255)
PYGAME_COLOR_WHITE = pygame.Color(255, 255, 255, 255)


class GameOverException(Exception):
    """Exception déclenché lors d'un cas de Game Over"""


class Food:
    """Objet Food

    """
    FOOD_SIZE = 10

    def __init__(self, game_area: pygame.Surface) -> None:
        """Initialisation de l'objet

        Args:
            game_area (pygame.Surface): Surface de jeu où sera  placé l'objet
        """
        self.__x_coord = round(random.randrange(
            0, GAME_AREA_WIDTH - self.FOOD_SIZE) / 10.0) * 10.0
        self.__y_coord = round(random.randrange(
            0, GAME_AREA_HEIGHT - self.FOOD_SIZE) / 10.0) * 10.0
        self.__game_area = game_area

    @property
    def position(self) -> tuple[float, float]:
        return (self.__x_coord, self.__y_coord)

    def redraw(self) -> None:
        """Redessine l'objet dans la surface de jeu
        """
        pygame.draw.rect(self.__game_area, PYGAME_COLOR_RED, [
                         self.__x_coord, self.__y_coord, self.FOOD_SIZE, self.FOOD_SIZE])

    def set_random_position(self) -> None:
        """Defini une position aléatoire de l'objet dans la surface de jeu
        """
        self.__x_coord = round(random.randrange(
            0, GAME_AREA_WIDTH - self.FOOD_SIZE) / 10.0) * 10.0
        self.__y_coord = round(random.randrange(
            0, GAME_AREA_HEIGHT - self.FOOD_SIZE) / 10.0) * 10.0
        self.redraw()


class Snake:
    """Objet Serpent

    Raises:
        GameOverException: Lancé lors d'un cas de Game Over détecté
    """
    SNAKE_BLOCK_SIZE = 10
    INITIAL_POSITION_X = 400
    INITIAL_POSITION_Y = 300
    INITIAL_SNAKE_SPEED = 15
    DONT_MOVE = (0, 0)
    MOVE_LEFT = (-SNAKE_BLOCK_SIZE, 0)
    MOVE_RIGHT = (SNAKE_BLOCK_SIZE, 0)
    MOVE_UP = (0, -SNAKE_BLOCK_SIZE)
    MOVE_DOWN = (0, SNAKE_BLOCK_SIZE)

    def __init__(self, game_area: pygame.Surface) -> None:
        """Initialisation de l'objet

        Args:
            game_area (pygame.Surface): Surface de jeu où sera  placé l'objet
        """
        self.__game_area = game_area
        self.speed = self.INITIAL_SNAKE_SPEED
        self.__x_coord = self.INITIAL_POSITION_X
        self.__y_coord = self.INITIAL_POSITION_Y
        self.__motion = self.DONT_MOVE
        self.__body = [(self.INITIAL_POSITION_X, self.INITIAL_POSITION_Y)]
        self.__is_extendable = False

    @property
    def size(self) -> int:
        return len(self.__body)

    @property
    def position(self) -> tuple[float, float]:
        return (self.__x_coord, self.__y_coord)

    def set_new_direction(self, direction: int) -> None:
        """Change la direction du serpent

        Args:
            direction (int): _description_
        """
        if (direction == pygame.K_LEFT) and (self.__motion != self.MOVE_RIGHT):
            self.__motion = self.MOVE_LEFT
        elif (direction == pygame.K_RIGHT) and (self.__motion != self.MOVE_LEFT):
            self.__motion = self.MOVE_RIGHT
        elif (direction == pygame.K_UP) and (self.__motion != self.MOVE_DOWN):
            self.__motion = self.MOVE_UP
        elif (direction == pygame.K_DOWN) and (self.__motion != self.MOVE_UP):
            self.__motion = self.MOVE_DOWN

    def grow_up(self) -> None:
        """Agrandi le serpent d'un élément
        """
        self.__is_extendable = True
        self.speed = ((self.size - 1)//5)*5 + self.INITIAL_SNAKE_SPEED

    def is_out_of_game_area(self) -> bool:
        """Vérifie si le serpent est sorti de la surface de jeu

        Returns:
            bool: Résultat de la méthode
        """
        return not ((0 <= self.__x_coord < GAME_AREA_WIDTH) and (0 <= self.__y_coord < GAME_AREA_HEIGHT))

    def is_bite_tail(self) -> bool:
        """Vérifie si le serpent se mord la queue

        Returns:
            bool: Résultat de la méthode
        """
        return any(body_part == self.position for body_part in self.__body[:-1])

    def redraw(self) -> None:
        """Redessine le serpent dans la zone de jeu

        Raises:
            GameOverException: Levé quand GameOver détecté
        """
        for element in self.__body:
            pygame.draw.rect(self.__game_area, PYGAME_COLOR_LIME, [
                             element[0], element[1], self.SNAKE_BLOCK_SIZE, self.SNAKE_BLOCK_SIZE])
        if self.is_out_of_game_area() or self.is_bite_tail():
            raise GameOverException()

    def update_position(self) -> None:
        """Mise à jour de la position du serpent
        """
        if self.__motion != self.DONT_MOVE:
            self.__x_coord += self.__motion[0]
            self.__y_coord += self.__motion[1]
            self.__body.append((self.__x_coord, self.__y_coord))

            if not self.__is_extendable:
                del self.__body[0]
            else:
                self.__is_extendable = False
        self.redraw()


class Game:
    """Objet Game
    """

    def __init__(self) -> None:
        """Initiatilsaiton de la classe
        """
        pygame.init()
        self.game_surface = pygame.display.set_mode(
            (GAME_AREA_WIDTH, GAME_AREA_HEIGHT))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.show_commands()
        self.on_running = False

    def start(self) -> None:
        """Lancement du jeu 
        """
        self.snake = Snake(self.game_surface)
        self.food = Food(self.game_surface)
        self.on_running = True

    def pause(self) -> None:
        """Mets le jeu en pause
        """
        self.on_running = not self.on_running
        self.game_surface.fill(PYGAME_COLOR_BLACK)
        score_font = pygame.font.SysFont(None, 50)
        value = score_font.render("PAUSE", True, PYGAME_COLOR_LIME)
        self.game_surface.blit(value, [350, 250])
        pygame.display.update()

    def stop(self) -> None:
        """Gestion du game over
        """
        self.on_running = False
        del(self.snake)
        del(self.food)
        self.show_message("Game Over", PYGAME_COLOR_RED)

    def get_event(self) -> int:
        """Attrape les évènements clavier durant le jeu

        Returns:
            int: Code de la touche appuyée ou None sinon 
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return event.key
        return None

    def play(self, key: int) -> None:
        """_summary_

        Args:
            key (int): code de la touche détectée
        """
        self.snake.set_new_direction(key)

    def run(self) -> None:
        """_summary_
        """
        while True:
            self.execute()
            key = self.get_event()
            if key:
                if key == pygame.K_SPACE:
                    self.pause()
                elif key == pygame.K_RETURN:
                    self.start()
                elif key == pygame.K_ESCAPE:
                    break
                else:
                    self.play(key)

    def execute(self) -> None:
        """Lance le jeu
        """
        try:
            if self.on_running:
                self.game_surface.fill(PYGAME_COLOR_BLACK)
                self.snake.update_position()
                self.food.redraw()
                self.verify_food_reached()
                self.refresh_score()
                pygame.display.update()
                self.clock.tick(self.snake.speed)
        except:
            self.stop()

    def verify_food_reached(self) -> None:
        """Verifie si l'aliment a été trouvé
        """
        if self.snake.position == self.food.position:
            self.food.set_random_position()
            self.snake.grow_up()

    def show_message(self, msg: str, color: pygame.Color) -> None:
        """Affichage d'un message pour le joueur

        Args:
            msg (str): Message à afficher
            color (pygame.Color): Couleur du texte à afficher
        """
        self.game_surface.fill(PYGAME_COLOR_BLACK)
        font_style = pygame.font.SysFont(None, 50)
        mesg = font_style.render(msg, True, color)
        self.game_surface.blit(mesg, [330, 250])
        pygame.display.update()

    def show_commands(self) -> None:
        """Affichage les commandes du jeu
        """
        self.game_surface.fill(PYGAME_COLOR_BLACK)
        self.write_message("SNAKE", 90, [290, 40])
        self.write_message("COMMANDS:", 30, [240, 240])
        self.write_message("ENTER : to start game", 30, [280, 280])
        self.write_message("UP/DOWN/LEFT/RIGHT: playing", 30, [280, 320])
        self.write_message("SPACE: pause/unpause", 30, [280, 360])
        self.write_message("ESC: exit", 30, [280, 400])
        self.write_message(
            "Romuald DUGIED - 2022 - Cours POO FSS", 24, [30, 580])
        pygame.display.update()

    def write_message(self, msg: str, size: int, position: list[int, int]):
        """Ecrire un message sur la surface de jeu

        Args:
            msg (str): message à ecrire
            size (int): taille de la police
            position (list[int, int]): position [x, y] du message
        """
        font_style = pygame.font.SysFont(None, size)
        msg_surface = font_style.render(msg, True, PYGAME_COLOR_WHITE)
        self.game_surface.blit(msg_surface, position)

    def refresh_score(self) -> None:
        """Rafraichi le score
        """
        font_style = pygame.font.SysFont(None, 26)
        value = font_style.render(
            f"Your Score: {self.snake.size-1}", True, PYGAME_COLOR_WHITE)
        self.game_surface.blit(value, [0, 0])


def main() -> None:
    """Fonction principale du programme
    """
    game = Game()
    game.run()
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
