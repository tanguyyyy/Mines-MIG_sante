from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk
import datetime as dt
import pandas as pd
import os 
from ttkthemes import ThemedStyle
import lecture_pdf
import re


#liste des types de widgets dans canvas
data_list = []
#liste des listes de boutons de lecture de chaque évènement
event_button = []

#Choix des données d'affichage
data_type = ['RCP', 'BMI', 'CRO', 'CRH', 'Evolution médicale', 'CR', 'CS']
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
        self.data['Type de document'] = self.data['Document'].transform(from_name_to_type)

        #On converti en objet 'date'
        self.data['Date'] = self.data['Date'].transform(from_string_to_date)
        self.data['Date téléversement'] = self.data['Date téléversement'].transform(from_string_to_date)

        #On complète les dates manquantes en lisant les pdf
        #self.fill_dates()

    def fill_dates(self):
        for ind in self.data.index:
            if pd.isna(self.data['Date'].iloc[ind]):
                text = lecture_pdf.from_pdf_to_text(f"dossiers_patients/{self.name} {self.surname}/{self.data['Fichier lié'].iloc[ind]}")
                date_list = re.findall("\d\d[-/]\d\d[-/]\d{2,4}", text)
                if date_list:
                    for i, date in enumerate(date_list):
                        date_list[i] = re.split('/|-', date)
                    for i, date in enumerate(date_list):
                        if len(date[2]) == 2:
                            date[2] = '20' + date[2]
                        date_list[i] = dt.date(int(date[2]), int(date[1]), int(date[0]))                    
                #date_list contient toutes les dates qui apparaissent dans le texte. Il reste à garder celle qui est la plus pertinente
                #On supprime la date de naissance, au cas où c'est la seule qui apparaît
                while self.b_date in date_list:
                    date_list.remove(self.b_date)
                #Ensuite, on choisi de garder la date la plus tardive, ce qui peut être discutable
                if date_list:
                    self.data.loc[ind, 'Date'] = max(date_list)
    


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
        categories --> liste de chaines de caractères contenant les types de document que l'on veut visualiser "CRH", "BMI", etc...
        """
        output = []
        for ind in self.data.index:
            if self.data['Type de document'].iloc[ind] in categories and self.data['Date'].iloc[ind] >= date:
                output.append((self.data['Date'].iloc[ind], 
                    self.data['Document'].iloc[ind], 
                    self.data['Unité'].iloc[ind]))
        return output
        
def from_string_to_date(x):
    if pd.notna(x):
        return dt.datetime.strptime(x, "%Y-%m-%d").date()


def from_name_to_type(string):
    categories = ['BMI', 'RCP', 'CRO', 'CRH']
    for cat in categories:
        if cat in string.upper():
            return cat
    return 'Inconnu'



#Récupération des noms des patients

globbing = Path('dossiers_patients')
tuple_name = tuple(P.name for P in list(globbing.glob("*")))

#génération de l'interface graphique
window = tk.Tk()
window.title('Projet Orbis amélioré')
window.attributes('-fullscreen', True)
window_x = window.winfo_screenwidth()
window_y = window.winfo_screenheight()

#Chargement des images
load_frise = Image.open('image/Frise_fond_tranparent-2.png')       
render_frise = ImageTk.PhotoImage(load_frise)
load_flag = Image.open('image/flag.png').resize((100, 100), Image.ANTIALIAS)
render_flag = ImageTk.PhotoImage(load_flag)
load_main_background = Image.open('image/background_main.jpg').resize((window_x, window_y), Image.ANTIALIAS)
render_main_background = ImageTk.PhotoImage(load_main_background)

#Création du canva
canvas = tk.Canvas(window, height=window_y, width=window_x)
canvas.pack()

#Fond d'écran fenêtre
background = canvas.create_image(window_x/2, window_y/2, anchor='center', image=render_main_background)

#Affichage de la frise dans une nouvelle fenêtre
def affichage(zoubi='42'):
    global data_list
    global event_button
    """affichage de la frise"""
    if data_list!=[]:
        for c in data_list:
            canvas.delete(c)
    if event_button!=[]:
        for c1 in  event_button:
            for c2 in c1:
                c2.place_forget()

    #Initialisation de la nouvelle fenêtre
    patient = variable_patient.get()
    patient_name = patient.split(' ')[0]
    patient_surname = patient.split(' ')[1]

    #données importantes
    length_full_name = len(patient)
    DPI = Dossier_Patient_Informatise(patient_name, patient_surname)
    beg_frise, end_frise = (130, 386), (1230, 566)

    current_date = dt.date.today()
    choice_time = variable_time.get()
    if choice_time == '6 mois':
        beg_date = current_date - dt.timedelta(days=180)
    elif choice_time == '1 an':
        beg_date = current_date - dt.timedelta(days=365)
    elif choice_time == '2 ans':
        beg_date = current_date - dt.timedelta(days=730)
    elif choice_time == '5 ans':
        beg_date = current_date - dt.timedelta(days=1825)
    elif choice_time == '10 ans':
        beg_date = current_date - dt.timedelta(days=3650)

    #Affichage fiche patient
    patient_record = canvas.create_rectangle(565.0, 15.0, 865.0, 215.0, fill='#013220')
    ribbon = canvas.create_rectangle(565.0, 15.0, 595.0, 65.0, fill='#780000')
    data_list.append(patient_record)
    data_list.append(ribbon)

    #Légende dans patient_record
    name_display = canvas.create_text(658, 64,anchor='center', text='Nom, Prénom : ', font=('Arial Black', 10))
    patient_name = canvas.create_text(767+(len(patient)-14)*3, 64, text=patient, font=('Arial Black', 10))
    patient_sex = canvas.create_text(633, 84, text='Sexe : '+DPI.sex, font=('Arial Black', 10))
    patient_birthdate = canvas.create_text(687, 104, anchor='center', text='Naissance : '+str(DPI.b_date), font=('Arial Black', 10))
    patient_height = canvas.create_text(661, 124, anchor='center', text='Taille (cm) : '+str(DPI.height), font=('Arial Black', 10))
    patient_weight = canvas.create_text(654, 144, anchor='center', text='Poids (kg) : '+str(DPI.weight), font=('Arial Black', 10))
    data_list += [name_display, patient_name, patient_sex, patient_birthdate, patient_height, patient_weight]

    #Affichage de la frise vierge
    frise = canvas.create_image(890, 500,anchor='center', image=render_frise)
    data_list.append(frise)
    
    #Fonction d'affichage drapeau et date
    def mark(time, type):
        """Prend une date et le type d'un élément et l'affiche 
        sur la frise"""
        global data_list
        days_event = abs((time - beg_date).days)
        x_pos = (days_event/((current_date - beg_date).days)) * (end_frise[0] - beg_frise[0]) + beg_frise[0]

        #drapeau
        flag = canvas.create_image(x_pos - 10, beg_frise[1], anchor='center', image=render_flag)

        #date et type d'évènement
        text1 = canvas.create_text(x_pos-30, beg_frise[1]+30, anchor='center', text=time, font=('Arial Black', 8))
        text2 = canvas.create_text(x_pos-30, beg_frise[1]+40, anchor='center', text=type, font=('Arial Black', 10))
        data_list += [flag, text1, text2]

        return (flag, text1, text2, x_pos)

    #Définition des évènements



    event_list = [mark(dt.date(2021, 4, 28), 'test')]


    #Définition de la fonction de lecture à partir des boutons de lecture
    def read_doc(doc):
        os.startfile(doc)

    #Affichage des évènements et des boutons de lectures associés
    for event in event_list:
        flag = event[0]
        x_pos = event[3]
        read_button = [] #liste des boutons de l'évènement
        counter = 0 #permet d'évaluer le nombre de boutons à afficher

        for c, d in checked.items():
            if d.get():
                counter = counter + 1
                button_loc = tk.Button(window, text=c, font=('Arial Black', 10), bg='grey')
                button_loc.place(x=x_pos-60, y=beg_frise[1]+150 + 32*counter)
                read_button.append(button_loc)


        event_button.append(read_button)
        

    #Affichage date de début/fin 
    event_beg, event_current = mark(beg_date,''), mark(current_date, '')

    #Déplacement de object pour récupérer des coordonnées inutile pour le code final mais sympa pour coder
    object = flag
    def left(event):
        x = -5
        y = 0
        canvas.move(object, x, y)
        print(canvas.coords(object))

    def right(event):
        x = 5
        y = 0
        canvas.move(object, x, y)
        print(canvas.coords(object))

    def down(event):
        x = 0
        y = 5
        canvas.move(object, x, y)
        print(canvas.coords(object))
    
    def up(event):
        x = 0
        y = -5
        canvas.move(object, x, y)
        print(canvas.coords(object))

    window.bind("<Left>", left)
    window.bind("<Right>", right)
    window.bind("<Down>", down)
    window.bind("<Up>", up)


#Choix des paramètres d'affichage:
frame = tk.LabelFrame(window, text='Sélectionnez les données souhaitées', padx=20, pady=25)
frame.place(x=0, y=0)

#Choix du patient
variable_patient = tk.StringVar(window)
variable_patient.set('Polnareff Jean-Pierre')
menu_time = tk.OptionMenu(frame, variable_patient, *tuple_name, command=affichage)
menu_time.pack()

#Choix durée
variable_time = tk.StringVar(window)
variable_time.set('6 mois')
menu_time = tk.OptionMenu(frame, variable_time, *('6 mois', '1 an', '2 ans', '5 ans', '10 ans'), command=affichage)
menu_time.pack()

#Boutons à cocher
checked = {c : tk.BooleanVar() for c in data_type}
def check():
    """
    Initialise la liste des cases à cocher dans window
    """
    checked = {c : tk.BooleanVar() for c in data_type}
    for c in data_type:
        if c in ['RCP', 'CRH', 'CR']:#choix des types de données à afficher initialement
            checked[c].set(True)
        button_loc = tk.Checkbutton(frame, text=c, var=checked[c], width=20, anchor="w", command=affichage)
        button_loc.pack()
    return checked

checked = check()


#bouton affichage de la frise 
bouton1 = tk.Button(frame, text ='Afficher frise', font=("Arial Black", 10), command=affichage, bg='White')
bouton1.pack()

#bouton de fermeture de la frise
bouton2 = tk.Button(window, text='Fermer', font=(('Arial Black'), 10), command=window.destroy, bg='#94060f')
bouton2.place(x=window_x-60, y=0)

window.mainloop()



