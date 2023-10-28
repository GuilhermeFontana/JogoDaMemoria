import arcade
import xmlrpc.client
import sys
import time

if len(sys.argv) != 3:
    print("%s <host> <porta>" % sys.argv[0])
    sys.exit(0)

host = sys.argv[1]
porta = sys.argv[2]

server = xmlrpc.client.ServerProxy("http://" + host + ":" + porta)

playerId = server.connect()
print("ID: %s" % playerId )

if playerId == 0:
    exit()

currentPlayer = server.getCurrenPlayer()

# Game window parameters
WIDTH = 600
HEIGHT = 650

GRID_Y = HEIGHT - 140
GRID_X = 0 + 50
GRID_GAP = 10

CARD_COUNT = 8
CARD_COUNT_WITHOUT_DIPLICATES = int(CARD_COUNT / 2)

COLUMN_COUNT = 8
ROW_COUNT = int(CARD_COUNT / COLUMN_COUNT)

CARD_WIDTH = 60
CARD_HEIGHT = 95

STATES = {
    'WAITING_PLAYER': 'Aguardando segundo jogador...',
    'WAITING_TURN': 'Vez do adversário',
    'WAITING_FIRST_CARD': 'Escolha a primeira carta',
    'WAITING_SECOND_CARD': 'Escolha a segunda carta',
    'PLAYER_WON': 'Você venceu!',
    'PLAYER_LOST': 'Você perdeu!',
    'WAITING_CURRENT_PLAYER_SELECTION': 'Verificando o resultado...',
    'END_GAME': 'O jogo acabou!'
}

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.GAME_STATE = STATES['WAITING_PLAYER']
        self.first_selected_card_number = None
        self.second_selected_card_number = None
        self.end_game_msg = ''

        self.current_player = currentPlayer

        self.grid = []

        # inicializando grid em forma de matriz
        for r in range(0, ROW_COUNT):
            self.grid.append([])
            for c in range(0, COLUMN_COUNT):
                self.grid[r].append('X')

        arcade.set_background_color(arcade.color.WHEAT)

    def update_grid(self, cards):
        for r in range(0, ROW_COUNT):
            for c in range(0, COLUMN_COUNT):
                card_index = c + r * COLUMN_COUNT
                self.grid[r][c] = cards[card_index]

    def setup(self):
        pass

    def update_game_grid_from_server(self):
        game = server.getCurrentGame(playerId)
        data = game.replace('[', '').replace(']', '').split(',')
        self.update_grid(data)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(self.GAME_STATE, 350, HEIGHT - 50, arcade.color.BLACK, anchor_x='center')

        if self.GAME_STATE == STATES['END_GAME']:
            arcade.draw_text(self.end_game_msg, 350, HEIGHT/2, arcade.color.BLACK, anchor_x='center')
        else:
            for row in range(0, ROW_COUNT):
                y = GRID_Y - (row * CARD_HEIGHT) - (GRID_GAP * row)

                for col in range(0, COLUMN_COUNT):
                    x = GRID_X + (col * CARD_WIDTH) + (GRID_GAP * col)

                    color = arcade.color.ORANGE
                    card = self.grid[row][col]

                    if card != 'X':
                        color = arcade.color.BLUE

                    arcade.draw_rectangle_filled(x, y, CARD_WIDTH, CARD_HEIGHT, color)
                    arcade.draw_text(card, x - 3, y)

                    card_number = (col + row * COLUMN_COUNT) + 1
                    arcade.draw_text(card_number, x - CARD_WIDTH/2, y - 15 + CARD_HEIGHT/2)
        arcade.finish_render()

    def update(self, _dt):
        if self.current_player != 0:
            time.sleep(0.3)
            self.update_game_grid_from_server()
            self.current_player = server.getCurrenPlayer()

        if self.current_player == 3:
            self.GAME_STATE = STATES['END_GAME']
            score = server.getScores()
            finalScore = "Placar: " + str(score[0]) + "x" + str(score[1])
            if (score[0] == score[1]):
                finalScore += ". Empatou!"
            else:
                if (score[0] > score[1]):
                    if playerId == 1:
                        finalScore += ". Você venceu! :D"
                    else:
                        finalScore += ". Você perdeu :,C"
                else:
                    if playerId == 2:
                        finalScore += ". Você venceu! :D"
                    else:
                        finalScore += ". Você perdeu :,C"
            self.end_game_msg = finalScore

        if self.GAME_STATE == STATES['WAITING_TURN']:
            if self.current_player == playerId:
                self.GAME_STATE = STATES['WAITING_FIRST_CARD']
            else:
                self.GAME_STATE = STATES['WAITING_TURN']
        
        if self.GAME_STATE == STATES['WAITING_PLAYER']:
            self.current_player = server.getCurrenPlayer()
            if self.current_player != 0:
                # temos 2 players!
                if self.current_player == playerId:
                    self.GAME_STATE = STATES['WAITING_FIRST_CARD']
                else:
                    self.GAME_STATE = STATES['WAITING_TURN']
        
        if self.GAME_STATE == STATES['WAITING_CURRENT_PLAYER_SELECTION']:
            self.first_selected_card_number = None
            self.second_selected_card_number = None
            
            if self.current_player == 3:
                self.GAME_STATE = STATES['END_GAME']
            elif self.current_player == playerId:
                self.GAME_STATE = STATES['WAITING_FIRST_CARD']
            else:
                self.GAME_STATE = STATES['WAITING_TURN']

        if self.GAME_STATE == STATES['WAITING_FIRST_CARD'] and self.first_selected_card_number != None:
            server.sendGuess(playerId, self.first_selected_card_number)
            self.GAME_STATE = STATES['WAITING_SECOND_CARD']
            
        if self.GAME_STATE == STATES['WAITING_SECOND_CARD'] and self.second_selected_card_number != None:
            server.sendGuess(playerId, self.second_selected_card_number)
            self.GAME_STATE = STATES['WAITING_CURRENT_PLAYER_SELECTION']

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """

    def on_mouse_press(self, mouse_x, mouse_y, button, _key_modifiers):
        if button != 1: # button != left_click
            print(f'GAME_STATE: {self.GAME_STATE}')
            print(f'GRID: {self.grid}')
            return
    
        if self.GAME_STATE != STATES['WAITING_FIRST_CARD'] and self.GAME_STATE != STATES['WAITING_SECOND_CARD']:
            return
        
        print('MOUSE_PRESS')

        grid_x_start = GRID_X - (CARD_WIDTH / 2)
        grid_y_start = GRID_Y + (CARD_HEIGHT / 2)

        grid_x_end = grid_x_start + COLUMN_COUNT * CARD_WIDTH + GRID_GAP * (COLUMN_COUNT - 1)
        grid_y_end = grid_y_start - CARD_HEIGHT * ROW_COUNT - GRID_GAP * (ROW_COUNT - 1)
        
        mouse_click_inside_grid = mouse_x >= grid_x_start and mouse_x <= grid_x_end and mouse_y <= grid_y_start and mouse_y >= grid_y_end

        if not mouse_click_inside_grid:
            print('MOUSE_PRESS *NOT* INSIDE THE GRID')
            return

        for row in range(0, ROW_COUNT):
            card_y_start = GRID_Y - (row * CARD_HEIGHT) - (GRID_GAP * row)
            card_y_start += CARD_HEIGHT / 2 # offset para deixar o Y no canto superior do card

            card_y_end = card_y_start - CARD_HEIGHT

            for col in range(0, COLUMN_COUNT):
                card_x_start = GRID_X + (col * CARD_WIDTH) + (GRID_GAP * col)
                card_x_start -= CARD_WIDTH / 2 # offset para deixar o X no canto esquerdo
                
                card_x_end = card_x_start + CARD_WIDTH
                
                click_inside_card = mouse_x >= card_x_start and mouse_x <= card_x_end and mouse_y <= card_y_start and mouse_y >= card_y_end
                if not click_inside_card:
                    continue
                    
                card = self.grid[row][col]
                card_number = (col + row * COLUMN_COUNT) + 1


                invalid_card = card != 'X'
                if invalid_card:
                    return

                print(f'CARD CLICKED {card}, number = {card_number}')

                if self.first_selected_card_number == None:
                    print(f'setando first_selected_card_number para: {card_number}')
                    self.first_selected_card_number = card_number
                elif self.second_selected_card_number == None:
                    print(f'setando second_selected_card_number para: {card_number}')
                    self.second_selected_card_number = card_number

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

def main():
    game = MyGame(WIDTH, HEIGHT, "Jogo da memória 🐘")
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()