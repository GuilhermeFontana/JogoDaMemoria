import arcade
import random
import sys
import socket
import time

if len(sys.argv) != 3:
    print("%s <ip> <porta>" % sys.argv[0])
    sys.exit(0)

ip = sys.argv[1]
porta = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip,porta))

playerId = int(client_socket.recv(1024).decode('utf-8'))
if playerId == 1:
    print("Aguardando seu adversário...")

# Game window parameters
WIDTH = 1000
HEIGHT = 800

# some globals
# TODO: por enquanto o grid nao esta centralizado em tela

GRID_Y = HEIGHT - 200
GRID_X = 0 + 100
GRID_GAP = 10

CARD_COUNT = 40
CARD_COUNT_WITHOUT_DIPLICATES = int(CARD_COUNT / 2)

COLUMN_COUNT = 8
ROW_COUNT = int(CARD_COUNT / COLUMN_COUNT)

CARD_WIDTH = 65
CARD_HEIGHT = 120

CARDS = []
for ascii_code in range(65, CARD_COUNT_WITHOUT_DIPLICATES + 65):
    # append 2 times
    CARDS.append(chr(ascii_code))
    CARDS.append(chr(ascii_code))

random.shuffle(CARDS)

STATES = {
    'WAITING_PLAYER': 'Aguardando segundo jogador...',
    'WAITING_TURN': 'Vez do adversário',
    'WAITING_FIRST_CARD': 'Escolha a primeira carta',
    'WAITING_SECOND_CARD': 'Escolha a segunda carta',
    'PLAYER_WON': 'Você venceu!',
    'PLAYER_LOST': 'Você perdeu!',
    'WAITING_CURRENT_PLAYER_SELECTION': 'Verificando o resultado...'
}

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.GAME_STATE = STATES['WAITING_PLAYER']
        self.cards = []
        self.first_selected_card_number = None
        self.second_selected_card_number = None

        self.current_player = playerId
        self.is_screen_filled = False

        self.selected_card_1 = None # { 'card': '', 'coords': (-1,-1) }
        self.selected_card_2 = None # { 'card': '', 'coords': (-1,-1) }
        self.grid = []

        # inicializando grid em forma de matriz
        for r in range(0, ROW_COUNT):
            self.grid.append([])
            for c in range(0, COLUMN_COUNT):
                self.grid[r].append('_X_')

        arcade.set_background_color(arcade.color.WHEAT)

    def set_cards(self, cards):
        self.cards = cards
        for r in range(0, ROW_COUNT):
            for c in range(0, COLUMN_COUNT):
                card_index = c + r * COLUMN_COUNT
                self.grid[r][c] = self.cards[card_index]

    def update_grid_based_on_movement(self, move):
        card_number, card_value = move.split('-')
        card_index = int(card_number) - 1

        col = card_index % COLUMN_COUNT
        row = card_index // COLUMN_COUNT

        print(f'row = card_index % COLUMN_COUNT  --- row = {card_index} % {COLUMN_COUNT}')
        print(f'col = card_index // COLUMN_COUNT  --- col = {card_index} // {COLUMN_COUNT}')

        self.grid[row][col] = card_value
        print(f'card_number={card_number}')
        print(f'card_index={card_index}')
        print(f'self.grid[row][col] = card_value: self.grid[{row}][{col}] = {card_value}')

    def setup(self):
        card_counter = 0
        for row in range(0, ROW_COUNT):
            for col in range(0, COLUMN_COUNT):
                self.grid[row][col] = CARDS[card_counter]
                card_counter += 1

    def on_draw(self):
        arcade.start_render()
        self.is_screen_filled = True

        arcade.draw_text(self.GAME_STATE, 350, HEIGHT - 50, arcade.color.BLACK)

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

        time.sleep(3)

    def update(self, delta_time):
        if self.GAME_STATE == STATES['WAITING_TURN'] and self.is_screen_filled:
            # ficaremos esperando a jogada do oponente
            print('pre socket.recv opponent move')
            opponent_move = client_socket.recv(1024).decode('utf-8')
            self.update_grid_based_on_movement(opponent_move)
            print(f'pos socket.recv opponent move: {opponent_move}')
            # TODO: checar o proximo fluxo quando o processo chega neste estado
            #       depois daqui o fluxo entra no if abaixo, ficando preso no recv do currentPlayer
            #       o correto seria ficar preso esperando o segundo movimento do oponente

        if self.GAME_STATE == STATES['WAITING_PLAYER'] or self.GAME_STATE == STATES['WAITING_TURN'] or self.GAME_STATE == STATES['WAITING_CURRENT_PLAYER_SELECTION']:
            print('pre socket.recv currentPlayer')
            self.currentPlayer = int(client_socket.recv(1024).decode('utf-8'))
            print(f'pos socket.recv self.currentPlayer: {self.currentPlayer}')

            print('pre socket.recv cards')  
            data = client_socket.recv(1024).decode('utf-8')
            data = data.replace('[', '').replace(']', '').split(',')
            self.set_cards(data)
            print(f'pos socket.recv cards: {self.cards}')

            if playerId == self.currentPlayer:
                self.GAME_STATE = STATES['WAITING_FIRST_CARD']
            else:
                self.GAME_STATE = STATES['WAITING_TURN']


        if self.GAME_STATE == STATES['WAITING_FIRST_CARD'] and self.first_selected_card_number != None:
            print(f'pre socket send first card: {self.first_selected_card_number}')
            time.sleep(2)
            client_socket.send(str(self.first_selected_card_number).encode('utf-8'))
            print(f'pos socket send first card')
            
            print('pre socket.recv move')
            move = client_socket.recv(1024).decode('utf-8')
            print(f'pos socket.recv move: {move}')

            self.update_grid_based_on_movement(move)
            self.GAME_STATE = STATES['WAITING_SECOND_CARD']
            time.sleep(2)

        if self.GAME_STATE == STATES['WAITING_SECOND_CARD'] and self.second_selected_card_number != None:
            print(f'pre socket send second card: {self.second_selected_card_number}')
            time.sleep(2)
            client_socket.send(str(self.second_selected_card_number).encode('utf-8'))
            print(f'pos socket send second card')
            
            print('pre socket.recv second move')
            move = client_socket.recv(1024).decode('utf-8')
            print(f'pos socket.recv second move: {move}')

            self.update_grid_based_on_movement(move)
            
            self.GAME_STATE = STATES['WAITING_CURRENT_PLAYER_SELECTION']
            time.sleep(2)
        
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        print('on_mouse_motion')

    def on_mouse_press(self, mouse_x, mouse_y, button, key_modifiers):
        if button != 1: # button != left_click
            return
        
        print('MOUSE_PRESS')
        time.sleep(2)

        grid_x_start = GRID_X - (CARD_WIDTH / 2)
        grid_y_start = GRID_Y + (CARD_HEIGHT / 2)

        grid_x_end = grid_x_start + COLUMN_COUNT * CARD_WIDTH + GRID_GAP * (COLUMN_COUNT - 1)
        grid_y_end = grid_y_start - CARD_HEIGHT * ROW_COUNT - GRID_GAP * (ROW_COUNT - 1)
        
        mouse_click_inside_grid = mouse_x >= grid_x_start and mouse_x <= grid_x_end and mouse_y <= grid_y_start and mouse_y >= grid_y_end

        if not mouse_click_inside_grid:
            print('MOUSE_PRESS *NOT* INSIDE THE GRID')
            time.sleep(2)
            self.selected_card_1 = None
            self.selected_card_2 = None
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

                print(f'CARD CLICKED {card}, index = {card_number}')
                time.sleep(2)

                # daqui para baixo eu so tenho que dar send no socket da carta clicada

                if self.first_selected_card_number == None:
                    print(f'setando first_selected_card_number para: {card_number}')
                    self.first_selected_card_number = card_number
                elif self.second_selected_card_number == None:
                    print(f'setando second_selected_card_number para: {card_number}')
                    self.second_selected_card_number = card_number

                time.sleep(2)

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
