class GameState:
    def __init__(self,pos_start,lines):
        self.pos_start = pos_start
        self.pos=pos_start
        self.lines= lines
        self.pos_list = [pos_start]

    def print_lines(self):
        for i in range(len(self.lines)):
            print("Ligne "+str(i)+" " +self.lines[i].direction+" "+self.lines[i].indice)

    def last_step(self):
        for i in range(len(self.lines)):
            if self.lines[i].indice == "?":
                return self.lines[i-1]

