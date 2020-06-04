class Line:
    def __init__(self,direction,indice):
        self.direction=direction
        self.indice=indice
        self.state = False
    def __str__(self):
        return 'Hint : ' + self.indice + ' Direction : ' + self.direction