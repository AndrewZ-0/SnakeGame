from tkinter import *
import random
import threading
import time

class boardException(Exception):
    def __init__(self, errorMessage):
        print(errorMessage)
class gamequitException(Exception):
    def __init__(self):
        print("game has been quit --> can not start a quitted game")

class snakeGame():
    def __init__(self, boardwidth: int, boardheight: int, speed: float):
        self.setup_status = False
        self.gameclass_status = True
        self.boardwidth = boardwidth
        self.boardheight = boardheight
        self.speed = speed
        self.end = False
        self.snake = []
        self.food_tile = []
        self.gamescore = 0
        f = open("snakeGame_highscore.txt", "r")
        self.highscore = int(f.readline())
        f.close()

        self.window = Tk()

        if self.boardwidth > self.window.winfo_screenwidth() // 25:
            raise boardException("snakeGame board height is too long")
        elif self.boardheight > (self.window.winfo_screenheight() - 30) // 25:
            raise boardException("snakeGame board length is too long")
        elif self.boardwidth < 5:
            raise boardException("snakeGame board height is too short")
        elif self.boardheight < 5:
            raise boardException("snakeGame board length is too short")

        self.window.title("snake game")
        self.window.geometry(f"{self.boardwidth * 25}x{self.boardheight * 25 + 50}+0+0")

    def start(self):
        def setup_game():
            self.frame_width = (self.boardwidth * 25) // 1.4
            if self.frame_width < 120:
                self.frame_width = 120
            elif self.frame_width > 220:
                self.frame_width = 220

            self.frame_height = (self.boardheight * 25) // 2.6
            if self.frame_height < 40:
                self.frame_height = 40
            elif self.frame_height > 200:
                self.frame_height = 200

            if self.frame_height > 100 or self.frame_height * 1.8 < self.frame_width:
                self.frame_height = self.frame_width // 1.8
            elif self.frame_width > 120 and self.frame_width * 1.2 < self.frame_height:
                self.frame_width  = self.frame_height // 1.2

            self.object_width = self.frame_width // 2.8
            if self.object_width < 50:
                self.object_width = 50
            elif self.object_width > 80:
                self.object_width = 80

            self.object_height = self.frame_height // 4.5
            if self.object_height < 18:
                self.object_height = 18
            elif self.object_height > 30:
                self.object_width = 30

            self.create_board()

        def start_game(vector):
            self.inputs.append(vector)
            self.window.bind("<Up>", lambda event: self.record_input(0, -1))
            self.window.bind("<Down>", lambda event: self.record_input(0, 1))
            self.window.bind("<Left>", lambda event: self.record_input(-1, 0))
            self.window.bind("<Right>", lambda event: self.record_input(1, 0))
            self.window.unbind("<space>")
            self.refresh_thread.start()

        if self.gameclass_status == True:
            self.inputs = []
            self.window.bind("<Up>", lambda event: start_game((0, -1)))
            self.window.bind("<Left>", lambda event: start_game((-1, 0)))
            self.window.bind("<Right>", lambda event: start_game((1, 0)))
            self.window.bind("<space>", lambda event: start_game((0, -1)))

            if self.setup_status == False:
                setup_game()
                self.setup_status = True

            self.grow(self.boardwidth // 2, self.boardheight // 2 + 2)
            self.grow(self.boardwidth // 2, self.boardheight // 2 + 1)

            x_index = (self.boardwidth // 2)
            y_index = (self.boardheight // 2 - 2)
            x_pos = x_index * 25
            y_pos =  y_index * 25
            tile_coords = (x_pos, y_pos, x_pos + 25, y_pos + 25)
            self.food_tile = [
                (x_index, y_index), self.board.create_rectangle(tile_coords, fill = "#ff0000", outline = "")
            ]

            self.refresh_thread = threading.Thread(target = self.global_refresh)

            self.window.mainloop()
        else:
            raise gamequitException

    def quitGame(self):
        self.gameclass_status = False
        self.window.destroy()

    def retryGame(self):
        self.gameEnd_frame.destroy()

        for tile in self.snake:
            self.board.delete(tile[0])
        self.board.delete(self.food_tile[1])
        
        self.end = False
        self.snake = []
        self.food_tile = []
        self.gamescore = 0

        self.start()

    def gameEnd(self):
        self.window.unbind("<Up>")
        self.window.unbind("<Down>")
        self.window.unbind("<Left>")
        self.window.unbind("<Right>")

        if self.gamescore > self.highscore:
            self.highscore = self.gamescore
            f = open("C:/Users/ANDREW/snakeGame_highscore.txt", "w")
            f.write(str(self.highscore))
            f.close()

        self.gameEnd_frame = Frame(self.window, bg = "#bbbbbb")
        self.gameEnd_frame.place(
            x = self.window.winfo_width() // 2, 
            y = (self.window.winfo_height() // 2) + 25, 
            width = self.frame_width, 
            height = self.frame_height, 
            anchor = "center"
            )

        self.score_title_label = Label(
            self.gameEnd_frame, text = "score", 
            font = ("Helevetica", int(self.object_height // 1.8) - 1)
            )
        self.score_title_label.place(
            relx = 0.05, rely = 0.08, 
            width = self.object_width, height = self.object_height
            )

        self.highscore_title_label = Label(
            self.gameEnd_frame, text = "highscore", 
            font = ("Helevetica", int(self.object_height // 1.8) - 1)
            )
        self.highscore_title_label.place(
            relx = 0.95, rely = 0.08, 
            width = self.object_width, height = self.object_height, anchor = NE
            )

        self.score_data_label = Label(
            self.gameEnd_frame, text = self.gamescore, 
            font = ("Helevetica", int(self.object_height // 1.8))
            )
        self.score_data_label.place(
            relx = 0.05, rely = 0.3, 
            width = self.object_width, height = self.object_height * 1.2
            )

        self.highscore_data_label = Label(
            self.gameEnd_frame, text = self.highscore, 
            font = ("Helevetica", int(self.object_height // 1.8))
            )
        self.highscore_data_label.place(
            relx = 0.95, rely = 0.3, 
            width = self.object_width, height = self.object_height * 1.2, anchor = NE
            )

        self.quit_button = Button(
            self.gameEnd_frame, text = "quit", font = ("Helevetica", int(self.object_height // 1.8)), 
            relief = "solid", borderwidth = 1, command = self.quitGame
            )
        self.quit_button.place(relx = 0.05, rely = 0.7, width = self.object_width, height = self.object_height)

        self.retry_button = Button(
            self.gameEnd_frame, text = "retry", font = ("Helevetica", int(self.object_height // 1.8)), 
            relief = "solid", borderwidth = 1, command = self.retryGame
            )
        self.retry_button.place(relx = 0.95, rely = 0.7, width = self.object_width, height = self.object_height, anchor = NE)

    def create_board(self):
        def swap_colour(tileColour):
            if tileColour == "#ffffff":
                tileColour = "#cccccc"
            else:
                tileColour = "#ffffff"
            return tileColour
        self.board = Canvas(self.window, bg = "#ffffff", borderwidth = 1, highlightbackground = "#000000")
        self.board.place(x = 0, y = 50, width = self.boardwidth * 25, height = self.boardheight * 25)

        tileColour = "#ffffff"
        for y_count in range(self.boardheight):
            if self.boardwidth % 2 == 0:
                tileColour = swap_colour(tileColour)
            for x_count in range(self.boardwidth):
                x_coord = x_count * 25
                y_coord = y_count * 25
                coords = [x_coord, y_coord, x_coord + 25, y_coord + 25]
                tileColour = swap_colour(tileColour)
                self.board.create_rectangle(coords, fill = tileColour, outline = "")

        self.scoreboard_title_label  = Label(
            self.window, text = "score", 
            font = ("Helevetica", int(self.object_height // 1.8) - 1), 
            relief = "solid", borderwidth = 1
            )
        self.scoreboard_title_label.place(x = 5, y = 5, width = self.object_width, height = 18)

        self.scoreboard_data_label = Label(
            self.window, text = self.gamescore, 
            font = ("Helevetica", int(self.object_height // 1.8)), 
            relief = "solid", borderwidth = 1
            )
        self.scoreboard_data_label.place(x = 5, y = 22, width = self.object_width, height = 23)

        self.highscoreboard_title_label  = Label(
            self.window, text = "highscore", 
            font = ("Helevetica", int(self.object_height // 1.8) - 1), 
            relief = "solid", borderwidth = 1
            )
        self.highscoreboard_title_label.place(
            x = self.boardwidth * 25 - 5, y = 5, 
            width = self.object_width, height = 18, anchor = NE
            )

        self.highscoreboard_data_label = Label(
            self.window, text = self.highscore, 
            font = ("Helevetica", int(self.object_height // 1.8)), 
            relief = "solid", borderwidth = 1
            )
        self.highscoreboard_data_label.place(
            x = self.boardwidth * 25 - 5, y = 22, 
            width = self.object_width, height = 23, anchor = NE
            )
    
    def record_input(self, x_movement, y_movement):
        if (self.inputs[-1] != (x_movement, y_movement) 
            and self.inputs[-1][0] * x_movement == 0 
            and self.inputs[-1][1] * y_movement == 0
            ):
            self.inputs.append((x_movement, y_movement))
    
    def make_food_tile(self):
        snake_tiles = []
        blank_tiles = []
        
        for tile in self.snake:
            snake_tiles.append(tile[1])
        for x in range(self.boardwidth):
            for y in range(self.boardheight):
                if ((x, y) in snake_tiles) == False:
                    blank_tiles.append((x, y))

        food_tile_pos = random.choice(blank_tiles)
        x_pos = food_tile_pos[0] * 25
        y_pos = food_tile_pos[1] * 25
        food_tile_coords = (x_pos, y_pos, x_pos + 25, y_pos + 25)
        self.food_tile = [
            (
                food_tile_pos[0], food_tile_pos[1]), 
                self.board.create_rectangle(food_tile_coords, fill = "#ff0000", outline = "")
        ]

    def grow(self, x_pos, y_pos):
        x_coord = x_pos * 25
        y_coord = y_pos * 25
        coords = [x_coord, y_coord, x_coord + 25, y_coord + 25]
        tile_id = self.board.create_rectangle(coords, fill = "#00ff00", outline = "")
        self.snake.insert(0, [tile_id, (x_pos, y_pos)])

    def move(self, vector):
        old_head_coords = self.snake[0][1]
        new_head_coords = (old_head_coords[0] + vector[0], old_head_coords[1] + vector[1])

        if new_head_coords != self.snake[1][1]:
            for tile in self.snake[1: ]:
                if new_head_coords == tile[1]:
                    self.end = True
            if (new_head_coords[0] < 0 
                or new_head_coords[1] < 0 
                or new_head_coords[0] > self.boardwidth - 1 
                or new_head_coords[1] > self.boardheight - 1
                ):
                self.end = True
            elif new_head_coords == self.food_tile[0]:
                self.grow(new_head_coords[0], new_head_coords[1])
                self.board.delete(self.food_tile[1])
                self.gamescore += 1
                self.scoreboard_data_label.configure(text = self.gamescore)
                self.make_food_tile()
            else:
                self.board.moveto(self.snake[-1][0], new_head_coords[0] * 25 - 1, new_head_coords[1] * 25 - 1)
                self.snake.insert(0, [self.snake[-1][0], new_head_coords])
                del self.snake[-1]

    def global_refresh(self):
        while self.end == False:
            if len(self.inputs) > 1:
                del self.inputs[0]
            self.move(self.inputs[0])
            time.sleep(self.speed) 
        self.gameEnd()

sg = snakeGame(30, 25, 0.1)
sg.start()
