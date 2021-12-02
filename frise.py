from pathlib import Path
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import datetime as dt
import pandas as pd
import os 
from ttkthemes import ThemedStyle
import lecture_pdf
import re
from pandastable import Table, TableModel

#liste des types de widgets dans canvas
data_list = []
#liste des listes de boutons de lecture de chaque évènement
event_button = []

#Choix des données d'affichage
data_type = ['RCP', 'BMI', 'CRO', 'CRH', 'Evolution médicale', 'CR', 'CS']


class TestApp(tk.Frame):
    """Basic test frame for the table"""
    def __init__(self, parent=None):
        self.parent = parent
        tk.Frame.__init__(self)
        self.main = tk.Toplevel()
        self.main.geometry('1200x800+200+100')
        self.main.title('Table app')
        f = tk.Frame(self.main)
        f.pack(fill=tk.BOTH,expand=1)
        df = pd.read_csv(f"dossiers_patients/{variable_patient.get()}/hospitalisations.csv", sep = ';')
        self.table = pt = Table(f, dataframe=df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
        return

class Dossier_Patient_Informatise:
    """
    name, surname --> str, pas d'accent pour éviter les erreurs de codage
    """
    def __init__(self, name = None, surname = None):
        self.name = name
        self.surname = surname
        self.file_1 = f"dossiers_patients/{self.name} {self.surname}/infos.txt"
        self.file_2 = f"dossiers_patients/{self.name} {self.surname}/allergies.txt"
        self.file_3 = f"dossiers_patients/{self.name} {self.surname}/hospitalisations.csv"
        with open(self.file_1, 'r') as document:
            lines = document.readlines()
            b_date_string = lines[2]
            b_date_list = b_date_string.split('-')
            self.b_date = dt.date(int(b_date_list[0]), int(b_date_list[1]), int(b_date_list[2]))

            self.sex = lines[3].replace('\n', '')
            self.height = int(lines[4])
            self.weight = lines[5]
        
        with open(self.file_2, 'r') as document:
            self.allergies = document.read()

        self.data = pd.read_csv(self.file_3, sep = ';')

        #Ajout d'une colonne 'Type' au tableau 'data
        self.data['Type de document'] = self.data['Document']
        for i, document in zip(self.data.index, self.data['Document']):
            self.data['Type de document'].iloc[i] = from_name_to_type(document)

        #On converti en objet 'date'
        self.data['Date'] = self.data['Date'].transform(from_string_to_date)


def from_string_to_date(x):
    return dt.datetime.strptime(x, "%Y-%m-%d").date()

def from_name_to_type(string):
    categories = data_type
    for cat in categories:
        if cat in string.upper():
            return cat
    return 'Autre'

def disp_data():
    app = TestApp()
    #launch the app
    app.mainloop()


#Récupération des noms des patients

globbing = Path('dossiers_patients')
tuple_name = tuple(P.name for P in list(globbing.glob("*")))

#Chargement des DPI dans un dictionnaire
DPI_dictionnary = {p : Dossier_Patient_Informatise(p.split(' ')[0], p.split(' ')[1]) for p in tuple_name}

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
load_bout_fleche_rouge = Image.open("image/Bout_fleche_rouge.png")
render_bout_fleche_rouge = ImageTk.PhotoImage(load_bout_fleche_rouge)

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
    DPI = DPI_dictionnary[patient]
    beg_frise, end_frise = (130, 386), (1230, 566)

    current_date = dt.date.today()
    choice_time = variable_time.get()
    if choice_time == '30 jours':
        beg_date = current_date - dt.timedelta(days=30)
    elif choice_time == '6 mois':
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

    #Code couleur (à mettre en annexe, en-dehors de la fonction d'affichage de la frise)

    #affiche un rectangle associé à une hospitalisation
    def hospi(date_d, date_f):
        global data_list
        L = end_frise[0]-beg_frise[0] #longueur de la frise
        D = (date_f - date_d).days #durée d'hospitalisation
        plagetps = (current_date-beg_date).days #plage de temps affichée
        x = beg_frise[0] + ((date_d-beg_date).days/plagetps)*L #abscisse du point en haut à gauche du rectangle
        rectangle = canvas.create_line(x, beg_frise[1], x, end_frise[1], fill='red', width=(D/plagetps)*L)
        data_list.append(rectangle)

    #affiche un rectangle associé à un passage aux urgences
    def urg(date):
        global data_list
        L = end_frise[0]-beg_frise[0] #longueur de la frise
        plagetps = (current_date-beg_date).days #plage de temps affichée
        x = beg_frise[0] + ((date-beg_date).days/plagetps)*L #abscisse du point en haut à gauche du rectangle
        rectangle = canvas.create_line(x, beg_frise[1], x, end_frise[1], fill='orange', width=3)
        data_list.append(rectangle)

    #Recherche du CRH associé à un BMI (le plus proche, situé après, en termes de dates)

    #Prend en entrée l'index d'un BMI et retrourne celui du CRH associé
    def id_CRH(id_BMI):
        date_BMI = DPI.data['Date'].iloc[id_BMI] #date du BMI
        data_CRH = DPI.data[(DPI.data['Type de document'] == 'CRH') & (DPI.data['Date']>date_BMI)] #sous-dataframe avec les CRHs après le BMI

        if data_CRH.empty:
            return -1 #s'il n'y a pas de CRH après le BMI, le patient est encore hospitalisé
        else:
            ecart = (data_CRH['Date'][0] - date_BMI).days #on initialise l'écart de dates entre le BMI et le premier CRH
            indice = data_CRH.index[0]
            for i in data_CRH.index:
                if (data_CRH['Date'][i] - date_BMI).days < ecart: #on vérifie que le CRH est plus près du BMI
                    ecart = (data_CRH['Date'][i] - date_BMI).days
                    indice = i
            return indice #l'indice est un entier naturel si on a bien un CRH, c'est -1 si on n'a pas de CRH après le BMI


    def bout_fleche_rouge(id_BMI): #met le bout de la flèche en rouge à partir de la date du BMI
        global data_list
        date_BMI = DPI.data['Date'].iloc[id_BMI]
        L = end_frise[0] - beg_frise[0] #longueur de la frise
        D = (current_date - date_BMI).days #durée d'hospitalisation
        plagetps = (current_date-beg_date).days #plage de temps affichée
        x = beg_frise[0] + ((date_BMI-beg_date).days/plagetps)*L #abscisse du point en haut à gauche du rectangle
        rect_rouge = canvas.create_line(x, beg_frise[1], x, end_frise[1], fill='red', width=(D/plagetps)*L)
        fleche = canvas.create_image(890, 500, anchor='center', image=render_bout_fleche_rouge)
        data_list += [fleche, rect_rouge]

    #Regroupe tous les BMIs d'un patient, leur associe un CRH et fait l'affichage de la plage de couleurs (à mettre dans la fonction affichage)
    def affiche_hospi():
        data_BMI = DPI.data[DPI.data['Type de document'] == 'BMI'] #sous-dataframe avec les BMIs
        for i in data_BMI.index:
            j = id_CRH(i) #index du CRH asocié au BMI
            if j!=-1: #si on a bien un CRH associé au BMI (le patient est sorti)
                date_d = DPI['Date'].iloc[i] #date du BMI
                date_f = DPI['Date'].iloc[j] #date du CRH
                hospi(date_d, date_f) #affichage de la plage rouge d'hospitalisation
            else: #si on n'a pas de CRH (le patient est toujours hospitalisé)
                bout_fleche_rouge(i)

    #Affiche tous les passages aux urgences
    def affiche_urg():
        data_urg = DPI.data[DPI.data['Type de document'] == 'CRU'] #sous-dataframe avec les CRU
        for i in data_urg.index:
            date = data_urg['Date'].iloc[i] #date du CRU
            urg(date)

    #Affichage de la frise vierge
    frise = canvas.create_image(890, 500,anchor='center', image=render_frise)
    data_list.append(frise)
    
    #Fonction d'affichage drapeau et date
    def mark(time, type, draw=False):
        """Prend une date et le type d'un élément et l'affiche 
        sur la frise si draw est True"""
        global data_list
        days_event = abs((time - beg_date).days)
        x_pos = (days_event/((current_date - beg_date).days)) * (end_frise[0] - beg_frise[0]) + beg_frise[0]

        if not draw:
            return x_pos
        else:
            #drapeau
            flag = canvas.create_image(x_pos - 10, beg_frise[1], anchor='center', image=render_flag)

            #date et type d'évènement
            text1 = canvas.create_text(x_pos-30, beg_frise[1]+30, anchor='center', text=time, font=('Arial Black', 8))
            text2 = canvas.create_text(x_pos-30, beg_frise[1]+40, anchor='center', text=type, font=('Arial Black', 10))
            data_list += [flag, text1, text2]
            return (flag, text1, text2, x_pos)


    #Définition des évènements

    event_set = set()
    for c, d in checked.items():
        if d.get():
            df = DPI.data[DPI.data['Type de document']==c]
            for i in df.index:
                time = df['Date'][i]
                type = df['Unité'][i]
                file = df['Fichier lié'][i]
                if (time - beg_date).days > 0:# permet de n'afficher que les event dans la plage de temps considérée
                    event = tuple(list(mark(time, type, draw=True)) + [file] + [time] + [False] + [type])
                    event_set.add(event)






    #Définition de la fonction de lecture à partir des boutons de lecture
    def read_doc(doc):
        os.startfile(doc)

    #fusion des event s'ils sont trop collés
    def merge(event_set, merged=False):
        '''
        si 2 évènements éloignés de moins de 75 pixels on merge en un seul drapeau
        Affichage des évènements et des boutons de lectures associés
        '''
        global event_button
        new_event_set = set()
        
        if merged:
            while event_set != set():

                random_event = list(event_set)[0]#un peu barbare mais j'ai pas trouvé comment récupérer un élément quelconque d'un set
                event_to_merge = [random_event]
                event_set.remove(random_event)
                event_set_copy = event_set.copy()

                for event in event_set_copy:
                    if abs(event[0] - random_event[0]) < 75:
                        event_set.remove(event)
                        event_to_merge.append(event)

                all_time = [event[2] for event in event_to_merge]
                all_file = [event[1] for event in event_to_merge]
                all_type = [event[4] for event in event_to_merge]

                if len(event_to_merge) > 1:
                    Bool = True
                    all_type = ['Zoom'] + all_type

                else:
                    Bool = False
                    new_event_set.add(tuple(list(mark(all_time[0], all_type[0], draw=True)) + [all_file] + [all_time] + [Bool] + [all_type]))
        
            event_set = new_event_set

        counter = {event[5] : 0 for event in event_set}

        for event in event_set:
            flag = event[0]
            x_pos = event[3]
            all_file = event[4]
            all_time = event[5]
            merged = event[6] #s'il y'a eu des évènements fusionnés
            all_type = event[7]
            read_button = [] #liste des boutons de l'évènement
            counter = {all_time : 0} #permet d'évaluer le nombre de boutons à afficher
            counter[all_time] += 1
            button_loc = tk.Button(window, text=c, font=('Arial Black', 10), bg='grey', command= lambda : read_doc(f'dossiers_patients\\{patient}\\{all_file}'))
            button_loc.place(x=x_pos-60, y=beg_frise[1]+150 + 32*counter[all_time])
            read_button.append(button_loc)

            event_button.append(read_button)
    
    merge(event_set)

    #Affichage date de début/fin 
    event_beg, event_current = mark(beg_date,'', draw=True), mark(current_date, '', draw=True)

    #affiche_urg()
    #affiche_hospi()

    #Déplacement de object pour récupérer des coordonnées inutile pour le code final mais sympa pour coder
    object = event_beg
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
frame = tk.LabelFrame(window, text='Sélectionnez les données souhaitées', padx=20, pady=10)
frame.place(x=0, y=0)

#Choix du patient
variable_patient = tk.StringVar(window)
variable_patient.set('Polnareff Jean-Pierre')
menu_time = tk.OptionMenu(frame, variable_patient, *tuple_name, command=affichage)
menu_time.pack()

#Choix durée
variable_time = tk.StringVar(window)
variable_time.set('6 mois')
menu_time = tk.OptionMenu(frame, variable_time, *('30 jours', '6 mois', '1 an', '2 ans', '5 ans', '10 ans'), command=affichage)
menu_time.pack()

#Boutons à cocher
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

#bouton données
bouton3 = tk.Button(frame, text='Données patient', font=(('Arial Black'), 10), bg='White', command=disp_data)
bouton3.pack()

window.mainloop()

