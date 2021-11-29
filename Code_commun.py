import datetime as dt
from pathlib import Path
import pandas as pd

class Dossier_Patient_Informatise:
    """
    name, surname --> str, pas d'accent pour éviter les erreurs de codage
    """
    def __init__(self, name = None, surname = None):
        self.name = name
        self.surname = surname
        file_1 = f"dossiers_patients/{self.name} {self.surname}/infos.txt"
        file_2 = f"dossiers_patients/{self.name} {self.surname}/allergies.txt"
        file_3 = f"dossiers_patients/{self.name} {self.surname}/hospitalisations.csv"
        with open(file_1, 'r') as document:
            lines = document.readlines()
            b_date_string = lines[2]
            b_date_list = b_date_string.split('-')
            self.b_date = dt.date(int(b_date_list[0]), int(b_date_list[1]), int(b_date_list[2]))
            self.sex = lines[3].replace('\n', '')
            self.height = int(lines[4])
            self.weight = lines[5]
        
        with open(file_2, 'r') as document:
            self.allergies = document.read()

        self.data = pd.read_csv(file_3, sep = ';')
        #Ajout d'une colonne 'Type' au tableau 'data
        self.data['Type de document'] = self.data['Document']
        for i, document in zip(self.data.index, self.data['Document']):
            self.data['Type de document'].iloc[i] = from_name_to_type(document)
        #On converti en objet 'date'
        self.data['Date'] = self.data['Date'].transform(from_string_to_date)


    def disp_infos(self):
        print(f"Nom: {self.name}")
        print(f"Prénom: {self.surname}")
        print(f"Sexe: {self.sex}")
        print(f"Date de naissance (AAA-MM-JJ): {self.b_date}")
        print(f"Taille: {self.height} cm")
        print(f"Poids: {self.weight} kg")
        print("________________________________________________________________________")
        print(f"Allergies: \n\n{self.allergies}")
        print("________________________________________________________________________")

    
    def flags(self, date, categories = []):
        """
        date --> la date jusqu'à laquelle on affiche
        categories --> liste de chaines de caractères contenant les types de document que l'on veut visualiser
        """
        output = []
        for ind in self.data.index:
            if self.data['Type de document'].iloc[ind] in categories:
                output.append((self.data['Date'].iloc[ind], 
                    self.data['Document'].iloc[ind], 
                    self.data['Unité'].iloc[ind]))
        return output

def from_string_to_date(x):
    return dt.datetime.strptime(x, "%Y-%m-%d")

def from_name_to_type(string):
    categories = ['BMI', 'RCP', 'CRO', 'CRH']
    for cat in categories:
        if cat in string.upper():
            return cat
    return 'Autre'




A = Dossier_Patient_Informatise('Michu', 'Segolene')



print(A.flags(6, ['BMI', 'CRH']))

