__author__ = "1224270: Frank Kramer, 3402993: Sascha Reynolds"
__version__ = "1.0"
__email__ = "frkramer@stud.uni-frankfurt.de, sreynold@stud.uni-frankfurt.de"

if __name__ == '__main__':
    import collections
    from util.getch import getch
    from sudoku_win7 import Sudoku
    from sudoku_win7 import Grid
    
  
    class Item2(Grid.Item):
        """Item2 class which inherits from Grid.Item.
        (alternatively could also have been inherited from
        Sudoku.Item, but we think this is better to understand)
        Adds the attributes "fixit" and "note" and the
        function getnote and setnote. During game item-objecs are
        created for each sudoku field. Therfore each field
        has the attributes fixit and note. If fixit is True
        the field is "fixed" which means that if cannot be
        deleted any more. Note is initialized with an empty string.
        The user can add notes to the field (setnote) or
        view the notes (getnote). 
        """
        fixit = False
        note = ""
        def getnote(self):
            if self.note == "":
                print("Keine Notiz vorhanden!")
            else:
                print(self.note)
            getch()
        def setnote(self,s:str):
            self.note += s
        
    #new class Sudoku2
    class Sudoku2(Sudoku):
        """Class Sudoku2 inherits from Sudoku. It implements
        the attributes and methods for the follwing commands
        (in the listed order): undo, redo, fix, set (changes due to fix
        and undo), remove (changes due to fix), get_note, set_note,
        generate_notes, get_free, set_one, level, check_for_win"""
        rowverbal = ["A","B","C","D","E","F","G","H","I"] #used by get_free
        printflag = True #print or don't print a message when using generate_notes
        max_length = 6 #maximum length of undo/redo list (using collections.deque)
        undolist=collections.deque([],max_length) #undolist using collections.deque
        redolist=collections.deque([],max_length) #redolist using collections.deque

        def writeundolist(self,x,y,value):
            self.undolist.append([x,y,int(value)])
            
        def writeredolist(self,x,y,value):
            self.redolist.append([x,y,int(value)])

        def undo(self, count = 1):
            """invoked if the user enters undo or undo [1-6] in the
            commandline. count gives number of undo steps. Only
            values which were added to the board with method set are
            put into the undo-list"""
            count = int(count)
            if count > len(self.undolist):
                count = len(self.undolist)
            if count == 0:
                print("Undo-Liste ist leer!")
                getch()
            for i in range(count):
                temp = self.undolist.pop()
                #write redo-entry, so to be able to redo an undo command:
                redo = self[temp[0]][temp[1]].get()
                self.writeredolist(temp[0],temp[1],redo)
                #undo last command:
                self[temp[0]][temp[1]].set(temp[2])

        def redo(self, count = 1):
            """invoked if the user enters redo or redo [1-6] in the
            commandline. count gives number of redo steps. Only
            values which were removed from the board with method undo are
            put into the redo-list""" 
            count = int(count)
            if count > len(self.redolist):
                count = len(self.redolist)
            if count == 0:
                print("Redo-Liste ist leer!")
                getch()
            for i in range(count):
                temp = self.redolist.pop()
                #possibility to undo redo-moves:
                redo = self[temp[0]][temp[1]].get()
                self.writeundolist(temp[0],temp[1],redo)
                #redo move
                self[temp[0]][temp[1]].set(temp[2])
           
        def fix_field(self, row:str, col:str, value:int):
            """invoked if the user enters fix [field] [value]
            into the command line. Sadly no fix [field] alone 
            can be entered, as the second argument is required
            by the original implementation..."""
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
            """overridden method which was already implemented
            in the original code. Overriding was necessary to
            take care of the commands fix and undo. invoked
            if the user enters set [field] [value] into the
            command line."""
            self.grid = self.get(row, col)
            #if field is fixed, do nothing:
            if self.grid.fixit == True:
                print("Feld fixiert, keine Änderung möglich!")
                getch()
                return None
            value = int(value)
            row, col = self._mapper(row, col) #convert coordinates
            value_prev = self[row][col].get() #get value bevore it is overwritten
            self.writeundolist(row,col,value_prev)#write previous value into undolist
            #write new value into board:
            self[row][col].set(value)
            #check if move is legal. 
            if self.is_valid_row(row) or self.is_valid_col(col) or self.is_valid_submarix(row, col):
                #if move is illegal write message to warn user
                return "Wert nicht legal, undo benutzen!\n".format(value)        
            return None

        def remove(self, row:str, col:str) -> None:
            """overridden method which was already implemented
            in the original code. Overriding was necessary to
            take care of the command fix. invoked if the user
            enters del [field] into the command line"""
            self.grid = self.get(row, col)
            if self.grid.fixit == True:
                print("Feld fixiert, keine Änderung möglich!")
                getch()
                return None
            row, col = self._mapper(row, col)
            self[row][col] = self.get_empty()
        
        def get_note(self, row:str, col:str):
            """Reads the note attached to a field which is
            set either by user or by generate_notes. Invoked
            if the user enters note [field] in the
            commandline"""
            self.grid = self.get(row, col)
            self.grid.getnote()
            
        def set_note(self, row:str, col:str, hint:str):
            """Adds a note to a certain field. Invoked
            if the user enters note [field] [string]
            in the commandline"""
            self.grid = self.get(row, col)
            self.grid.setnote(hint)
            print("Notiz gesetzt!")
            getch()
        
        def generate_notes(self):
            """Called if the user enters "notes"
            into the commandline. Generates a note for each
            free field. Note contains the numbers this field
            can legally take. If a user defined note exists
            it will be overridden. This is necessary because
            the automatically generated notes are used by other
            methods (solve, get_free)."""
            #Display the remark "Lege Notizen an..." only if
            #this function is directly called by entering "notes". 
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

        
        def get_free(self):
            """Called if the user enters "hint" in
            the commandline. Displays a list of all free
            fields which can take only one single number
            """
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
        
        def solve(self, count = 1):
            """
            Called if the user enters "next" or "next [1-9]"
            into the commandline. Fills free fields which can take
            only one number with this number. 
            """
            try:
                count = int(count)
            except:
                print("Bitte nach next Integerzahl (1-9) eingeben!")
            if count not in range(1,10):
                print("Bitte nach next Integerzahl (1-9) eingeben!")
                return
            counterx = 0
            #generate notes
            self.printflag = False #notes should print no message here
            self.generate_notes()
            self.printflag = True
            #solve each 1-number-choice fields
            #on the board by putting in the correct number
            while (self.set_one()): #sets one number
                counterx += 1
                print("Durchlauf ", counterx)
                if counterx == count:
                    break
                #generate new notes after setting a number
                self.printflag = False
                self.generate_notes()
                self.printflag = True
            #if not as many 1-number-choices on the board
            #as set in the note command check for win
            if counterx < int(count):
                if self.check_for_win():
                    print("\nSudoku gelöst!")
                else:
                    print("Konnte nicht alle Werte setzen!")
            #all numbers cut be set...
            else:
                if self.check_for_win():
                    print("\nSudoku gelöst!")
                else:
                    print("Alle Werte gesetzt!")
            getch()
            
        def set_one(self):
            """Called by solve. Sets only one value because
            after setting this value new notes have to
            be generated"""
            for col in range(self._size):
                for row in range(self._size):
                    if self[row][col].get()== 0:
                        if len(self[row][col].note) == 1:
                            value = int(self[row][col].note)
                            self[row][col].set(value)
                            print("Wert gesetzt")
                            return 1

        def level(self):
            """Calculates a difficulty level for a sudoku.
            This difficulty level is based on the number
            of values which can theoretically be entered into
            each free field. A Sudoku is considered most
            difficult if 81*9 values are possible and
            most easy if 0 values are possible, e. g. if
            the Sudoku is solved ;)"""
            cl = [0]*9
            emptyfields = 0
            #Calculate notes
            self.printflag = False
            self.generate_notes()
            self.printflag = True
            #Counting 1er, 2er, 3er, 4er, 5er,... choices
            for col in range(self._size):
                for row in range(self._size):
                    if self[row][col].get()== 0:
                        emptyfields +=1
                        if len(self[row][col].note) == 1:
                            cl[0] += 1
                        if len(self[row][col].note) == 2:
                            cl[1] += 1
                        if len(self[row][col].note) == 3:
                            cl[2] += 1
                        if len(self[row][col].note) == 4:
                            cl[3] += 1
                        if len(self[row][col].note) == 5:
                            cl[4] += 1
                        if len(self[row][col].note) == 6:
                            cl[5] += 1
                        if len(self[row][col].note) == 7:
                            cl[6] += 1
                        if len(self[row][col].note) == 8:
                            cl[7] += 1
                        if len(self[row][col].note) == 9:
                            cl[8] += 1
          
            weightedchoices= cl[1]*2+cl[2]*3+cl[3]*4+cl[4]*5+cl[5]*6+cl[5]*6+cl[6]*7+cl[7]*8+cl[8]*9
            choicesindex = weightedchoices/(81*9) #== 1 if all fields 9er-choices, 0 if S. solved

            temp = choicesindex
            
            levelvalue = 10 - (10 * temp)

            levelvalue = round(levelvalue, 2)
            
            print("\nlevel = ", levelvalue)
            print("\n0/1/2/3 schwer")
            print("4/5/6/7 mittel")
            print("8/9/10 einfach")
            getch()

        def check_for_win(self):
            emptyfields = 0
            for col in range(self._size):
                for row in range(self._size):
                    if self[row][col].get()== 0:
                        emptyfields +=1
            fields = 81-emptyfields
            if fields == 81:
                return True
            else:
                return False
            
    #Necessary to insure correct pickling of .lev-files
    class Item(Item2):
        pass

    
    Sudoku2(Item).mainloop()
