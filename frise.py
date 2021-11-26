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



A = Dossier_Patient_Informatise('Michu', 'Segolene')


A.disp_infos()