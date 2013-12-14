if __name__ == '__main__':
    from util.getch import getch
    from sudoku_win7 import Sudoku
    
    #new item class
    class Item(Sudoku.Item):
        fixit = False
        note = ""
        def getnote(self):
            print(self.note)
            getch()
        def setnote(self,s:str):
            self.note += s
        
    #new class Sudoku2
    class Sudoku2(Sudoku, Item):
        rowverbal = ["A","B","C","D","E","F","G","H","I"]
        printflag = True
        counter = 0

        #called with command "fix b1 5" e.g.
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

        #called with command "set b1 5" e.g.
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

        #called with command "del b1" e. g.
        def remove(self, row:str, col:str) -> None:
            self.grid = self.get(row, col)
            if self.grid.fixit == True:
                print("Feld fixiert, keine Änderung möglich!")
                getch()
                return None
            row, col = self._mapper(row, col)
            self[row][col] = self.get_empty()
        
        #Called with command "note b1" e.g.
        def get_note(self, row:str, col:str):
            self.grid = self.get(row, col)
            self.grid.getnote()
            
        #Called with command "note b1 157" e.g.
        def set_note(self, row:str, col:str, hint:str):
            self.grid = self.get(row, col)
            self.grid.setnote(hint)
            print("Notiz gesetzt!")
            getch()
        
        #Called with command "notes"
        #Generates a note for each free field which
        #contains the numbers this field can legally
        #take
        def generate_notes(self):
            #Display this remark only if this function
            #is directly called with "notes". 
            if self.printflag:
                print("Lege Notizen an...")
            #deleting old notes
            for col in range(self._size):
                      for row in range(self._size):
                           self[row][col].note = ""
            #generating new notes
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

        #Called with command "hint"
        #Displays all free fields which can
        #take only one single number
        def get_free(self):
            self.printflag = False
            self.generate_notes()
            self.printflag = True
            foundone = False
            for col in range(self._size):
                      for row in range(self._size):
                          if self[row][col].get()== 0:
                              if len(self[row][col].note) == 1:
                                   print("Feld ", self.rowverbal[row], col+1, "Lösung = ",self[row][col].note )
                                   foundone = True
                                   pass
            if foundone == False:
                print("Kein Feld mit nur einem Hint gefunden!")
            getch()

        #Called with command "next" or "next [1-9]"
        def solve(self, count = 1):
            try:
                count = int(count)
            except:
                print("Bitte nach next Integerzahl (1-9) eingeben!")
            if count not in range(1,10):
                print("Bitte nach next Integerzahl (1-9) eingeben!")
                return
            found = False
            counterx = 0
            self.printflag = False
            self.generate_notes()
            self.printflag = True
            while (self.set_one()):
                counterx += 1
                print("Durchlauf ", counterx)
                if counterx == count:
                    break
                self.printflag = False
                self.generate_notes()
                self.printflag = True
            if counterx < int(count):
                print("Konnte nicht alle Werte setzen!")
            else:
                print("Alle Werte gesetzt!")
            getch()
            
        #Called by solve. Sets only one value because
        #after setting new notes have to be generated
        def set_one(self):
            for col in range(self._size):
                for row in range(self._size):
                    if self[row][col].get()== 0:
                        if len(self[row][col].note) == 1:
                            value = int(self[row][col].note)
                            self[row][col].set(value)
                            print("Wert gesetzt")
                            return 1

           
            

    #Hier wird das Objekt der neuen Item-Klasse dem Konstuktor
    #__init__(Grid.Item) übergeben und der mainloop gestartet
    #Letzterer Konstruktor übergibt das Item-Objekt an den Grid
    #Konstruktor
    Sudoku2(Item).mainloop()
