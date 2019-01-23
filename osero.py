import sys
import tkinter as tk

WHITE = 0
BLACK = 1
BOARD_SIZE = 8

class ReversiBoard(object):
    def __init__(self):
        # 2次元リストを生成する
        # 各要素の初期値はNone
        self.cells = []
        for i in range(BOARD_SIZE):
            self.cells.append([None for i in range(BOARD_SIZE)])

        # 4つの石を初期配置する
        self.cells[3][3] = WHITE
        self.cells[3][4] = BLACK
        self.cells[4][3] = BLACK
        self.cells[4][4] = WHITE


    def put_disk(self, x, y, player):
        """指定した座標に指定したプレイヤーの石を置く"""

        # 既にほかの石があれば置くことができない
        if self.cells[y][x] is not None:
            return False

        # 獲得できる石がない場合も置くことができない
        flippable = self.list_flippable_disks(x, y, player)
        if flippable == []:
            return False

        # 実際に石を置く処理
        self.cells[y][x] = player
        for x,y in flippable:
            self.cells[y][x] = player
            
        return True

    def list_flippable_disks(self, x, y, player):
        """指定した座標に指定したプレイヤーの石を置いた時、ひっくりかえせる全ての石の座標（タプル）をリストにして返す"""

        PREV = -1
        NEXT = 1
        DIRECTION = [PREV, 0, NEXT]
        flippable = []

        for dx in DIRECTION:
            for dy in DIRECTION:
                if dx == 0 and dy == 0:
                    continue

                tmp = []
                depth = 0
                while(True):
                    depth += 1

                    # 方向 × 深さ(距離)を要求座標に加算し直線的な探査をする
                    rx = x + (dx * depth)
                    ry = y + (dy * depth)

                    # 調べる座標(rx, ry)がボードの範囲内ならば
                    if 0 <= rx < BOARD_SIZE and 0 <= ry < BOARD_SIZE:
                        request = self.cells[ry][rx]

                        # Noneを獲得することはできない
                        if request is None:
                            break

                        if request == player:  # 自分の石が見つかったとき
                            if tmp != []:      # 探査した範囲内に獲得可能な石があれば
                                flippable.extend(tmp) # flippableに追加

                        # 相手の石が見つかったとき
                        else:
                            # 獲得可能な石として一時保存
                            tmp.append((rx, ry))
                    else:
                        break
        return flippable

    def show_board(self):
        """ボードを表示する"""
        
        for x,i in enumerate(self.cells):
            for y,cell in enumerate(i):
                if cell == WHITE:
                    canvas.create_oval(100*x+10,100*y+10,100*x+90,100*y+90,fill = "white")
                elif cell == BLACK:
                    canvas.create_oval(100*x+10,100*y+10,100*x+90,100*y+90,fill = "black")


    def list_possible_cells(self, player):
        """指定したプレイやーの石を置くことができる、すべてのマスの座標をリストにして返す"""

        possible = []
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.cells[y][x] is not None:
                    continue
                if self.list_flippable_disks(x, y, player) == []:
                    continue
                else:
                    possible.append((x, y))
        return possible



def callback(event):
    i = int(event.x/100)
    j = int(event.y/100)
    if(board.put_disk(j, i, WHITE)):
        print(board.list_possible_cells(BLACK))
        show_possible_cells(board.list_possible_cells(BLACK))
    elif(board.put_disk(j, i, BLACK)):
        print(board.list_possible_cells(WHITE))
        show_possible_cells(board.list_possible_cells(WHITE))
    board.show_board()
    

def show_possible_cells(cells):
    canvas.delete("cells")
    for y,x in cells:
        canvas.create_oval(100*x+10,100*y+10,100*x+90,100*y+90,fill = "yellow",tag="cells")
        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("オセロ")
    root.geometry("900x900")

    #初期キャンバス
    canvas = tk.Canvas(root,width = 800,height = 800)
    canvas.create_rectangle(0,0,800,800,fill = "green")
    for i in range(1,8):
        canvas.create_line(100*i,0,100*i,800)
        canvas.create_line(0,100*i,800,100*i)

    #UI
    ui = tk.Canvas(root,width = 800,height = 80)
    ui.create_oval(250,10,320,80,fill = "white")   
    ui.create_oval(550,10,620,80,fill = "black")
    ui.create_line(340,45,380,45,arrow="first",width=10)
    ui.pack()
    ui.place(x = 0,y = 0)

    board = ReversiBoard()
    board.show_board()

    #オセロの呼び出し
    canvas.bind("<Button-1>",callback)
    canvas.pack()

    canvas.place(x = 50,y = 90)
    root.mainloop()
