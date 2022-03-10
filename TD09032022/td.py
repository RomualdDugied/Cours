class SudoGrid:
    def __init__(self, filename):
        self._values = []
        with open(filename) as input_file:
            for rows_from_file in input_file.read().split():
                self._values.append(rows_from_file.split(';'))
                
    def cell(self, index)->str:
        pass
    
    def row(self, index)->list:
        return self._values[index]
    
    def column(self, index)->list:
        export_list =[]
        for i in range(0,9):
            export_list.append(self._values[i][index])
        return export_list
    
    def block(self, index)->list:
        pass
    
            
            
grille = SudoGrid('input.csv')

print(grille.column(0))
