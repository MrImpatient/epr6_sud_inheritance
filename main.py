if __name__ == '__main__':
    from util.getch import getch
    from sudoku_win7 import Sudoku
    
    ## Workaround 4 Pickleing nested classes
    class Item(Sudoku.Item):
        pass

    #Neue Klasse Item2
    class Item2(Item):
        pass

    #Neue Klasse Sudoku2
    class Sudoku2(Sudoku):
        
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
    Sudoku2(Item2).mainloop()
