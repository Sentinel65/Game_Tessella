# Deskova hra Tessella pro dva hrace
# © 2019 Michael Lefkowitz
# Vytvoreno s velkou pomoci ChatGPT 4 (chatgpt.com)

# Moznost zapnuti / vypnuti logovani a vypisu hlasek pro ucely testovani a zjistovani funkcnosti programu. na zacatek radku vlozte / smazte tento znak:   #
# Radek [350] Smer pohybu:
# Radek [351] Relevantni primka obsahuje tyto pozice:
# Radek [355] Figurky na primce:
# Radek [359] Vase figurky v primce:
# Radek [370] Podporujici figurky ve smeru {smer}:
# Radek [163] - [177] zde lze pro ucely testovani konkretnich situaci ve hre nastavit rozestaveni figurek podle potreby

import re
class Game:
    def __init__(self):
        # Inicializace herni desky
        self.board_choice = None  # Inicializace atributu board_choice  
        self.board = [[' ' for _ in range(9)] for _ in range(9)]
        self.initialize_board(self.board_choice)
        self.current_player = 'W'  # W pro bileho hrace, B pro cerneho hrace
        self.pieces_remaining = {'W': 7, 'B': 7}  # Zbyle figurky pro kazdeho hrace
        self.move_log = []  # Logovani tahu

    import re

    def load_game(self):
        """Nacte souradnice figurek ze souboru a nahraje je na desku."""
        try:
            with open("tessella_save.txt", "r") as f:
                # Nacist typ hraci desky z prvniho radku
                self.board_choice = int(f.readline().strip())
                print(f"Nacteny typ desky: {self.board_choice}")
                
                # Inicializuj desku podle nacteneho typu
                if self.board_choice == '1':
                    self.initialize_board(self.board_choice)
                    self.setup_standard_board()
                elif self.board_choice == '2':    
                    self.initialize_board(self.board_choice)
                    self.setup_alternative_board() 
                    
                # Regular expression pro extrakci souradnic a hodnoty z radku
                pattern = re.compile(r"self\.board\[(\d+)\]\[(\d+)\] = '([BW.o])'")
                
                # Postupne nacitani jednotlivych pozic
                for line in f:
                    match = pattern.match(line.strip())
                    if match:
                        x, y, value = int(match.group(1)), int(match.group(2)), match.group(3)
                        self.board[x][y] = value
#                        print(f"Nastavuji pozici ({x}, {y}) na hodnotu '{value}'")
                    else:
                        print(f"Chyba pri nacitani radku: {line.strip()} - neplatny format")
    
                print("Hra byla uspesne nactena.")
        except IOError:
            print("Chyba pri nacitani hry nebo soubor nenalezen.")
        except ValueError:
            print("Chyba pri nacitani typu desky ze souboru. Zkontrolujte format souboru.")
        except Exception as e:
            print(f"Nastala neocekavana chyba: {e}")
    
    def save_game(self):
        """Ulozi hru do souboru s pouze relevantnimi souradnicemi."""
        with open("tessella_save.txt", "w") as f:
            # Ulozeni typu hraci desky
            print(f"Ukladam board_choice: {self.board_choice}")  # Debugging
            f.write(f"{self.board_choice}\n")
            
            # Definovani osmiuhelniku a ctvercu pro ukladani
            osmiuhelniky = [(0, 0), (0, 2), (0, 4), (0, 6), (0, 8),
                            (2, 0), (2, 2), (2, 4), (2, 6), (2, 8),
                            (4, 0), (4, 2), (4, 4), (4, 6), (4, 8),
                            (6, 0), (6, 2), (6, 4), (6, 6), (6, 8),
                            (8, 0), (8, 2), (8, 4), (8, 6), (8, 8)]
    
            ctverce = [(1, 1), (1, 3), (1, 5), (1, 7),
                       (3, 1), (3, 3), (3, 5), (3, 7),
                       (5, 1), (5, 3), (5, 5), (5, 7),
                       (7, 1), (7, 3), (7, 5), (7, 7)]
    
            # Ukladani pouze definovanych souradnic
            for x, y in osmiuhelniky + ctverce:
                f.write(f"self.board[{x}][{y}] = '{self.board[x][y]}'\n")
        
        print("Hra byla uspesne ulozena.")

    def initialize_board(self, board_choice):
        # Definujeme osmiuhelniky (o) a ctverce (.):
        osmiuhelniky = [(0, 0), (0, 2), (0, 4), (0, 6), (0, 8),
                        (2, 0), (2, 2), (2, 4), (2, 6), (2, 8),
                        (4, 0), (4, 2), (4, 4), (4, 6), (4, 8),
                        (6, 0), (6, 2), (6, 4), (6, 6), (6, 8),
                        (8, 0), (8, 2), (8, 4), (8, 6), (8, 8)]

        ctverce = [(1, 1), (1, 3), (1, 5), (1, 7),
                   (3, 1), (3, 3), (3, 5), (3, 7),
                   (5, 1), (5, 3), (5, 5), (5, 7),
                   (7, 1), (7, 3), (7, 5), (7, 7)]

        for (x, y) in osmiuhelniky:
            self.board[x][y] = 'o'
        for (x, y) in ctverce:
            self.board[x][y] = '.'

        print("Hra Tessella\n")
        choice = input("Vyberte rozlozeni hraci desky:\nzadejte '1' pro standardni, '2' pro alternativni, '3' pro testovaci: ")
        if choice == '1':
            self.board_choice = 1
            print(f"Nacteny typ desky: {self.board_choice}")
#            self.initialize_board(self.board_choice)  # Inicializace desky
            self.setup_standard_board()
        elif choice == '2':
            self.board_choice = 2
            print(f"Nacteny typ desky: {self.board_choice}")
#           self.initialize_board(self.board_choice)  # Inicializace desky
            self.setup_alternative_board()
        elif choice == '3':
            self.board_choice = 3
            print(f"Nacteny typ desky: {self.board_choice}")
#           self.initialize_board(self.board_choice)  # Inicializace desky    
            self.setup_test_board()
        else:
            print("Neplatna volba, nastavuje se standardni rozlozeni.")
            self.setup_standard_board()


    def setup_standard_board(self):
        self.board[0][0] = 'B'
        self.board[0][2] = 'B'
        self.board[0][4] = 'B'
        self.board[0][6] = 'B'
        self.board[2][0] = 'B'
        self.board[4][0] = 'B'
        self.board[6][0] = 'B'
        
        self.board[8][2] = 'W'
        self.board[8][4] = 'W'
        self.board[8][6] = 'W'
        self.board[8][8] = 'W'
        self.board[6][8] = 'W'
        self.board[4][8] = 'W'
        self.board[2][8] = 'W'

    def setup_alternative_board(self):
        self.board[0][0] = 'W'
        self.board[0][2] = 'B'
        self.board[0][4] = 'W'
        self.board[0][6] = 'B'
        self.board[2][0] = 'B'
        self.board[4][0] = 'W'
        self.board[6][0] = 'B'
        
        self.board[8][2] = 'W'
        self.board[8][4] = 'B'
        self.board[8][6] = 'W'
        self.board[8][8] = 'B'
        self.board[6][8] = 'W'
        self.board[4][8] = 'B'
        self.board[2][8] = 'W'

    def setup_test_board(self):
        self.board[0][0] = 'B'
        self.board[1][1] = 'B'
        self.board[2][2] = 'B'
        self.board[0][6] = 'B'
        self.board[2][0] = 'B'
        self.board[4][0] = 'B'
        self.board[6][0] = 'B'
        
        self.board[8][2] = 'W'
        self.board[6][6] = 'W'
        self.board[7][7] = 'W'
        self.board[8][8] = 'W'
        self.board[6][8] = 'W'
        self.board[4][8] = 'W'
        self.board[2][8] = 'W'

    def help_menu(self):
        print()
        print("Pravidla hry:\nHraci se stridaji v tazich. Kazdy hrac muze hrat vlastni figurkou nebo vyhodit\nsouperovu figurku. Pohyb figurky lze uskutecnit pouze na sousedni volne pole,\nse kterym ma spolecnou hranu (v graficke podobe to je osmiuhelnik nebo \nctverec, zde znak 'o' nebo '.'). Zjednodusenou podminkou je, aby na primce, kde\nchceme vyhazovat, byly minimalne 3 figurky (2 moje a 1 soupere). Mezi figurkou,\nkterou chci vyhazovat (predni AKTIVNI) a moji druhou figurkou (zadni PODPORA)\nnesmi byt zadna souperova figurka. AKTIVNI smi vyhodit nejblizsi\nfigurku soupere v primce. Vitezi ten, kdo souperi jako prvni sebere 4 figurky.")
        
        self.display_board_with_coordinates('standardni')
        
#        print("\nAlternativni hraci deska:")
#        self.display_board_with_coordinates('alternativni')
        
        choice = input("Chcete se vratit do hry (r) nebo ukoncit (k)? ")
        return choice
        
    def display_board_with_coordinates(self, choice):
        # Vypis hraci desky s cisly souradnic
        if choice == 'standardni':
            print()
#        elif choice == 'alternativni':
#            print("Alternativni rozlozeni:")
            
        board = [[f'{i},{j}' if (i+j) % 2 == 0 else '.' for j in range(9)] for i in range(9)]
        
#        for row in board:
#            print(' '.join(row))    

#    def display_board_with_coordinates(self):
        print("Hraci deska se souradnicemi pro pohyb a vyhazovani figurek\n")
        for row in range(9):
            if row % 2 == 0:
                # Radky s hexagony (osmuhelniky)
                print('   '.join(f"{row},{col}" for col in range(9) if col % 2 == 0))
            else:
                # Radky se ctverci maji odsazeni 4 znaky doprava
                print('   ' + '   '.join(f"{row},{col}" for col in range(1, 9, 2)))
        print("\n")

        
    def display_current_board(self):
        for row in self.board:
            print(' '.join(row))
            
            
    def print_board(self):
        print("Hra Tessella\n")
        for row in self.board:
            print(' '.join(row))
        print()

    def count_pieces(self):
        # Spocitat zbyvajici figurky pro kazdeho hrace
        count_w = sum(row.count('W') for row in self.board)
        count_b = sum(row.count('B') for row in self.board)
        self.pieces_remaining['W'] = count_w
        self.pieces_remaining['B'] = count_b

    def is_valid_move(self, x1, y1, x2, y2):
        # Kontrola, zda jsou souradnice v ramci desky
        if not (0 <= x1 < 9 and 0 <= y1 < 9 and 0 <= x2 < 9 and 0 <= y2 < 9):
            return False

        # Zkontrolovat, zda je puvodni pole obsazeno hracovou figurkou
        if self.board[x1][y1] != self.current_player:
            return False

        # Zkontrolovat, zda je cilove pole volne
        if self.board[x2][y2] not in ['o', '.']:
            return False

        # Logika pro platne pohyby
        if x1 == x2:  # Stejna rada
            if (y1 % 2 == 0 and y2 % 2 == 0):  # Osmiuhelnik na osmiuhelnik
                return abs(y1 - y2) == 2  # Dva sloupce
            if (y1 % 2 == 1 and y2 % 2 == 1):  # Ctverec na ctverec (zakazano)
                return False
            return abs(y1 - y2) == 1  # Mezi sousednimi

        if y1 == y2:  # Stejny sloupec
            if (x1 % 2 == 0 and x2 % 2 == 0):  # Osmiuhelnik na osmiuhelnik
                return abs(x1 - x2) == 2  # Dva rady
            if (x1 % 2 == 1 and x2 % 2 == 1):  # Ctverec na ctverec (zakazano)
                return False
            return abs(x1 - x2) == 1  # Mezi sousednimi

        # Ruzne rady a sloupce
        if abs(x1 - x2) == 1 and abs(y1 - y2) == 1:
            return True  # Pohyb na sousedni policko

        return False
    
    def get_lines(self):
        """Vraci diagonalni, horizontalni a vertikalni primky na hernim planu."""
        diagonals = {
            'd1': [(6,0), (7,1), (8,2)],
            'd2': [(4,0), (5,1), (6,2), (7,3), (8,4)],
            'd3': [(2,0), (3,1), (4,2), (5,3), (6,4), (7,5), (8,6)],
            'd4': [(0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8)],
            'd5': [(0,2), (1,3), (2,4), (3,5), (4,6), (5,7), (6,8)],
            'd6': [(0,4), (1,5), (2,6), (3,7), (4,8)],
            'd7': [(0,6), (1,7), (2,8)],
            'd8': [(2,0), (1,1), (0,2)],
            'd9': [(4,0), (3,1), (2,2), (1,3), (0,4)],
            'd10': [(6,0), (5,1), (4,2), (3,3), (2,4), (1,5), (0,6)],
            'd11': [(8,0), (7,1), (6,2), (5,3), (4,4), (3,5), (2,6), (1,7), (0,8)],
            'd12': [(8,2), (7,3), (6,4), (5,5), (4,6), (3,7), (2,8)],
            'd13': [(8,4), (7,5), (6,6), (5,7), (4,8)],
            'd14': [(8,6), (7,7), (6,8)]
        }
    
        horizontals = {
            'h1': [(0,0), (0,2), (0,4), (0,6), (0,8)],
            'h2': [(2,0), (2,2), (2,4), (2,6), (2,8)],
            'h3': [(4,0), (4,2), (4,4), (4,6), (4,8)],
            'h4': [(6,0), (6,2), (6,4), (6,6), (6,8)],
            'h5': [(8,0), (8,2), (8,4), (8,6), (8,8)]
        }
    
        verticals = {
            'v1': [(0,0), (2,0), (4,0), (6,0), (8,0)],
            'v2': [(0,2), (2,2), (4,2), (6,2), (8,2)],
            'v3': [(0,4), (2,4), (4,4), (6,4), (8,4)],
            'v4': [(0,6), (2,6), (4,6), (6,6), (8,6)],
            'v5': [(0,8), (2,8), (4,8), (6,8), (8,8)]
        }
    
        return diagonals, horizontals, verticals

    
    def is_valid_capture(self, x1, y1, x2, y2):
        """Kontroluje, zda je vyhozeni platne, a loguje vsechny kroky vcetne smeru a podpory."""
        opponent_piece = 'B' if self.current_player == 'W' else 'W'
        player_piece = self.current_player
    
        # Zkontroluj, zda je na pozici x2, y2 souperova figurka
        if self.board[x2][y2] != opponent_piece:
            print(f"Neplatne vyhozeni: Na {x2},{y2} neni souperova figurka.")
            return False
    
        # Definice diagonalnich, horizontalnich a vertikalnich primek
        diagonals, horizontals, verticals = self.get_lines()
    
        # Najit relevantni primku
        relevant_line = []
        line_name = ''
        for name, line in diagonals.items():
            if (x1, y1) in line and (x2, y2) in line:
                relevant_line = line
                line_name = name
                break
        if not relevant_line:
            for name, line in horizontals.items():
                if (x1, y1) in line and (x2, y2) in line:
                    relevant_line = line
                    line_name = name
                    break
        if not relevant_line:
            for name, line in verticals.items():
                if (x1, y1) in line and (x2, y2) in line:
                    relevant_line = line
                    line_name = name
                    break
    
        if not relevant_line:
            print("Vyhozeni neni platne: Zadane souradnice nepatri do zadne primky.")
            return False
    
        # Ziskani indexu pro aktivni (x1, y1) a cilovou (x2, y2) figurku
        start_idx = relevant_line.index((x1, y1))
        target_idx = relevant_line.index((x2, y2))
    
        # Urceni smeru na zaklade vychozi a cilove pozice
        smer = f"primka {line_name} smer ({x1}, {y1}) - ({x2}, {y2})"
    
        print(f"Smer pohybu: {smer}")
        print(f"Relevantni primka obsahuje tyto pozice: {relevant_line}")
    
        # Logovani figurek v primce (ignorujeme prazdna pole)
        line_status = [(pos, self.board[pos[0]][pos[1]]) for pos in relevant_line]
        print(f"Figurky na primce: {line_status}")
    
        # Urceni vsech hracovych figurek v primce
        player_pieces = [pos for pos in relevant_line if self.board[pos[0]][pos[1]] == player_piece]
        print(f"Vase figurky v primce: {player_pieces}")
    
        # Podporujici figurky jsou ty, ktere jsou za vychozim bodem smerem k cilovemu
        support_pieces = []
        if start_idx < target_idx:
            # Hledame figurky za vychozim bodem
            support_pieces = [pos for pos in player_pieces if relevant_line.index(pos) < start_idx]
        else:
            # Hledame figurky za vychozim bodem na opacne strane
            support_pieces = [pos for pos in player_pieces if relevant_line.index(pos) > start_idx]
    
        print(f"Podporujici figurky ve smeru {smer}: {support_pieces}")
    
        # Zkontroluj, zda mezi aktivni a cilovou figurkou nejsou zadne jine figurky (neprazdna pole)
        line_between = relevant_line[min(start_idx, target_idx) + 1:max(start_idx, target_idx)]
        for pos in line_between:
            # Pokud je mezi pozicemi jina figurka (neni prazdne pole), vyhozeni neni mozne
            if self.board[pos[0]][pos[1]] not in ['.', 'o']:
                print(f"Neplatne vyhozeni: Mezi pozicemi {x1},{y1} a {x2},{y2} lezi figurka na {pos}.")
                return False
    
        # Pokud jsou splneny vsechny podminky, je tah platny
        print(f"Vyhazujete platne figurku {x2},{y2} s figurkou {x1},{y1}.")
        return True




    def log_move(self, action, x1, y1, x2, y2):
        self.move_log.append(f"Hrac {self.current_player}: {action} z {x1},{y1} na {x2},{y2}")

    def print_move_log(self):
        print("\nLog tahu:")
        for log in self.move_log:
            print(log)
        print()

    def make_move(self, x1, y1, x2, y2):
        if self.is_valid_move(x1, y1, x2, y2):
            # Aktualizace hraci desky
            self.board[x2][y2] = self.board[x1][y1]  # Umisteni figurky na cilove pole
            self.board[x1][y1] = 'o' if (x1+y1) % 2 == 0 else '.'  # Puvodni pole se stava osmiuhelnikem nebo ctvercem

            # Snizeni poctu zbyvajicich figurek
            self.count_pieces()
            self.log_move("pohyb", x1, y1, x2, y2)  # Log pohybu
            self.check_game_over()  # Zkontrolovat, zda hra skoncila

            print(f"Tah uspesny: Z {x1},{y1} na {x2},{y2}.")
            print(f"Zbyvajici figurky - Hrac W: {self.pieces_remaining['W']}, Hrac B: {self.pieces_remaining['B']}.")
            self.current_player = 'B' if self.current_player == 'W' else 'W'
        else:
            print(f"Tah neni platny: Z {x1},{y1} na {x2},{y2}.")

    def make_capture(self, x1, y1, x2, y2):
        if self.is_valid_capture(x1, y1, x2, y2):
            # Predpokladame, ze x1, y1 je blize k x2, y2 a provede se vyhazovani
            self.board[x2][y2] = self.board[x1][y1]  # Premistime figurku
            self.board[x1][y1] = 'o' if (x1+y1) % 2 == 0 else '.'  # Puvodni pole se stava osmiuhelnikem nebo ctvercem
            self.count_pieces()
            self.log_move("vyhozeni", x1, y1, x2, y2)  # Log vyhozeni
            self.check_game_over()  # Zkontrolovat, zda hra skoncila
            print(f"Vyhozeni uspesne: Z {x1},{y1} na {x2},{y2}.")
            print(f"Zbyvajici figurky - Hrac W: {self.pieces_remaining['W']}, Hrac B: {self.pieces_remaining['B']}.")
            self.current_player = 'B' if self.current_player == 'W' else 'W'
        else:
            print(f"Vyhozeni neni platne: Z {x1},{y1} na {x2},{y2}.")

    def check_game_over(self):
        if self.pieces_remaining['W'] < 4 or self.pieces_remaining['B'] < 4:    # Kontrola na 4 vyhozene figurky
#            self.pieces_remaining['B'] < 4:  # Kontrola na 4 vyhozene figurky cerneho
            self.print_move_log()  # Vypis logovani tahu pred ukoncenim hry
            print(f"Hrac {self.current_player} vyhral, souperi zustaly pouze 3 figurky! Hra konci.")
            self.play_again()   # Dotaz na dalsi hru
            exit()
    
    def play_again(self):
#        self.print_move_log()  # Vypis logovani tahu pred ukoncenim hry
        """Zeptejte se hracu, zda chteji hrat znovu."""
        while True:
            choice = input("Chteji hraci zahajit novou hru? (ano/ne): ").strip().lower()
            if choice == 'ano':
                self.__init__()  # Znovu inicializujeme hru
                self.play()  # Zahajime novou hru
                break
            elif choice == 'ne':
                print("Dekujeme za hru!")
                exit()
            else:
                print("Neplatny vstup. Zadejte 'ano' nebo 'ne'.")

    
    def play(self):
        while True:
            self.print_board()
            try:
                move_type = input(f"Hrac {self.current_player}, zadejte 'p' pro pohyb nebo 'v' pro vyhozeni, 'h' pro napovedu,,\n's' pro ulozeni hry, 'l' pro nacteni hry, 'k' pro konec hry: ")
                if move_type == 'p':
                    x1, y1, x2, y2 = map(int, input("Zadejte souradnice jako 'x1 y1 x2 y2': ").split())
                    self.make_move(x1, y1, x2, y2)
                    self.move_log.append((self.current_player, (x1, y1), (x2, y2)))  # Logovani tahu
                elif move_type == 'v':
                    x1, y1, x2, y2 = map(int, input("Zadejte souradnice jako 'x1 y1 x2 y2': ").split())
                    self.make_capture(x1, y1, x2, y2)
                    self.move_log.append((self.current_player, (x1, y1), (x2, y2)))  # Logovani vyhazovani
                elif move_type == 'h':
                        help_choice = self.help_menu()
                        if help_choice == 'k':
                            print("Hra ukoncena.")
                            break
                elif move_type == 's':
                    self.save_game()
                elif move_type == 'l':
                # Spravne prirazeni volby pro nacteni desky
                    self.load_game()
                elif move_type == 'k':
                        print("Hra ukoncena.")
                        break
                else:
                    print("Neplatny vstup. Prosim, zkuste to znovu.")
            except ValueError:
                print("Neplatny vstup. Ujistete se, ze zadavate cisla.")

if __name__ == "__main__":
    game = Game()
    game.play()



