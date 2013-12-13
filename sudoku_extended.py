if __name__ == '__main__':
    from util.getch import getch
    from sudoku_win7 import Sudoku
    
    ## Workaround 4 Pickleing nested classes
    class Item(Sudoku.Item):
        fixit = False
        note = ""
        def getnote(self):
            print(self.note)
            getch()
        def setnote(self,s:str):
            self.note += s
        
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
        
        #Aufruf z. B. mit note b1
        def get_note(self, row:str, col:str):
            self.grid = self.get(row, col)
            #print(self.grid.note)
            self.grid.getnote()
            #def set(self, row:str, col:str, value:int)
            
        #Aufruf z. B. mit note b1 157
        def set_note(self, row:str, col:str, hint:str):
            self.grid = self.get(row, col)
            #self.grid.note = str(hint)
            self.grid.setnote(hint)
            print("Notiz gesetzt!")
            getch()
        

        def generate_notes(self):
            print("generate notes")
            for value in range (1,10):
                for col in range(self._size):
                      for row in range(self._size):
                          if self[row][col].get()== 0:
                              self[row][col].set(value)
                              if self.is_valid_row(row) or self.is_valid_col(col) or self.is_valid_submarix(row, col):
                                 self[row][col].set(0)
                              else:
                                 #append number at hint
                                 self[row][col].note += str(value)
                                 self[row][col].set(0)
                                  

    #Hier wird das Objekt der neuen Item-Klasse dem Konstuktor
    #__init__(Grid.Item) übergeben und der mainloop gestartet
    #Letzterer Konstruktor übergibt das Item-Objekt an den Grid
    #Konstruktor
    Sudoku2(Item).mainloop()
