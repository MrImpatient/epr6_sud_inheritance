if __name__ == '__main__':
    from util.getch import getch
    from sudoku_win7 import Sudoku
    
    ## Workaround 4 Pickleing nested classes
    class Item(Sudoku.Item):
        fixit = False
        
    #Neue Klasse Sudoku2
    class Sudoku2(Sudoku, Item):
        def fix_field(self, row:str, col:str, value:int):            
            self.grid = self.get(row, col)
            if not self.grid.fixit:
                self.set(row, col, value)
                self.grid.fixit = True
                print("Feld fixiert!")
                getch()
            else:
                print("Feld schon fixiert!")
                getch()

        def set(self, row:str, col:str, value:int) -> None:
            self.grid = self.get(row, col)
            if self.grid.fixit == True:
                print("Feld fixiert, keine Änderung möglich!")
                getch()
                return None
            value = int(value)
            row, col = self._mapper(row, col)
            self[row][col].set(value)
            if self.is_valid_row(row) or self.is_valid_col(col) or self.is_valid_submarix(row, col):
                return "Conflited value {0}!\n".format(value)        
            return None

        def remove(self, row:str, col:str) -> None:
            self.grid = self.get(row, col)
            if self.grid.fixit == True:
                print("Feld fixiert, keine Änderung möglich!")
                getch()
                return None
            row, col = self._mapper(row, col)
            self[row][col] = self.get_empty()
        
        #Aufruf z. B. mit note b1 "hallo"
        def get_note(self, row:str, col:str):
            print("Hier get_note")
            getch()
            
        #Aufruf z. B. mit note b1 dies_ist_ein_text
        def set_note(self, row:str, col:str, hint:str):
            print("Hier set_note")
            print(hint)
            getch()
        pass

    #Jetzt erbt Sudoku wieder von dieser neuen Klasse...
    Sudoku2(Item).mainloop()
