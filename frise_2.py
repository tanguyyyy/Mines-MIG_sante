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
from functools import partial

#liste des types de widgets dans canvas
data_list = []
#liste des listes de boutons de lecture de chaque évènement
event_button = []


#Choix des données d'affichage
data_type = ['RCP', 'BMI', 'CRO', 'CRH', 'CRU', 'CR', 'Autre']


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
        #df = pd.read_csv(f"dossiers_patients/{variable_patient.get()}/hospitalisations.csv", sep = ';')
        df = DPI_dictionnary[variable_patient.get()].data
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
        self.data['Date téléversement'] = self.data['Date téléversement'].transform(from_string_to_date)
        #On vérifie les dates
        
        self.fill_dates()

    def fill_dates(self):
        for ind in self.data.index:
            if pd.isna(self.data['Date'].iloc[ind]):
                text = lecture_pdf.from_pdf_to_text(f"dossiers_patients/{self.name} {self.surname}/{self.data['Fichier lié'].iloc[ind]}")
                text = text.lower()
                date_list = re.findall("\d\d[-]\d\d[-]\d{2,4}", text)
                date_list += re.findall("\d\d[/]\d\d[/]\d{2,4}", text)
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
                else:
                    self.data.loc[ind, 'Date'] = self.data.loc[ind, 'Date téléversement']
            else:
                self.data.loc[ind, 'Date'] = from_string_to_date(self.data.loc[ind, 'Date'])


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
load_frise = Image.open('image/Frise_fond_tranparent-3.png')       
render_frise = ImageTk.PhotoImage(load_frise)
render_flag = []
load_cursor = Image.open('image/curseur.png').resize((70, 70), Image.ANTIALIAS)
render_flag.append(ImageTk.PhotoImage(load_cursor))

load_1 = Image.open('image/img_1.png').resize((50, 50), Image.ANTIALIAS)
render_flag.append(ImageTk.PhotoImage(load_1))

load_2 = Image.open('image/img_2.png').resize((50, 50), Image.ANTIALIAS)
render_flag.append(ImageTk.PhotoImage(load_2))

load_3 = Image.open('image/img_3.png').resize((50, 50), Image.ANTIALIAS)
render_flag.append(ImageTk.PhotoImage(load_3))

load_4 = Image.open('image/img_4.png').resize((50, 50), Image.ANTIALIAS)
render_flag.append(ImageTk.PhotoImage(load_4))

load_5 = Image.open('image/img_5.png').resize((50, 50), Image.ANTIALIAS)
render_flag.append(ImageTk.PhotoImage(load_5))

load_6 = Image.open('image/img_6.png').resize((50, 50), Image.ANTIALIAS)
render_flag.append(ImageTk.PhotoImage(load_6))

load_7 = Image.open('image/img_7.png').resize((50, 50), Image.ANTIALIAS)
render_flag.append(ImageTk.PhotoImage(load_7))

load_8 = Image.open('image/img_8.png').resize((50, 50), Image.ANTIALIAS)
render_flag.append(ImageTk.PhotoImage(load_8))

load_9 = Image.open('image/img_9.png').resize((50, 50), Image.ANTIALIAS)
render_flag.append(ImageTk.PhotoImage(load_9))

load_10 = Image.open('image/img_9+.png').resize((50, 50), Image.ANTIALIAS)
render_flag.append(ImageTk.PhotoImage(load_10))


load_main_background = Image.open('image/background_2.png').resize((window_x, window_y), Image.ANTIALIAS)
render_main_background = ImageTk.PhotoImage(load_main_background)
load_bout_fleche_rouge = Image.open("image/Bout_fleche_rouge.png")
render_bout_fleche_rouge = ImageTk.PhotoImage(load_bout_fleche_rouge)
load_event_counter = Image.open('image/img_1.png').resize((50, 50), Image.ANTIALIAS)
render_event_counter = ImageTk.PhotoImage(load_event_counter)

#Création du canva
canvas = tk.Canvas(window, height=window_y, width=window_x)
canvas.pack()

#Fond d'écran fenêtre
background = canvas.create_image(window_x/2, window_y/2, anchor='center', image=render_main_background)

#Affichage de la frise dans une nouvelle fenêtre
def affichage():
    global data_list
    global event_button
    """
    affichage de la frise
    """
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
    patient_record = canvas.create_rectangle(565.0, 15.0, 865.0, 215.0, fill='#6f716e')
    ribbon = canvas.create_rectangle(565.0, 15.0, 595.0, 65.0, fill='#780000')

    #Affichage legende code couleur
    legend_urgency = canvas.create_rectangle(575, 165, 605, 185, fill='#e73200')
    legend_hosp = canvas.create_rectangle(575, 190, 605, 210, fill='#c10404')
    data_list.append(patient_record)
    data_list.append(ribbon)
    data_list.append(legend_urgency)
    data_list.append(legend_hosp)

    #Légende dans patient_record
    name_display = canvas.create_text(658, 64,anchor='center', text='Nom, Prénom : ', font=('Arial Black', 10))
    patient_name = canvas.create_text(767+(len(patient)-14)*3, 64, text=patient, font=('Arial Black', 10))
    patient_sex = canvas.create_text(633, 84, text='Sexe : '+DPI.sex, font=('Arial Black', 10))
    patient_birthdate = canvas.create_text(687, 104, anchor='center', text='Naissance : '+str(DPI.b_date), font=('Arial Black', 10))
    patient_height = canvas.create_text(661, 124, anchor='center', text='Taille (cm) : '+str(DPI.height), font=('Arial Black', 10))
    patient_weight = canvas.create_text(654, 144, anchor='center', text='Poids (kg) : '+str(DPI.weight), font=('Arial Black', 10))
    data_list += [name_display, patient_name, patient_sex, patient_birthdate, patient_height, patient_weight]
    
    #Legende dans code couleur
    urgency_txt = canvas.create_text(645, 175, text='Urgences', font=('Arial Black', 10))
    hospi_txt = canvas.create_text(675, 200, text='Séjour à l\'hôpital', font=('Arial Black', 10))


    #Code couleur (à mettre en annexe, en-dehors de la fonction d'affichage de la frise)

    #affiche un rectangle associé à une hospitalisation
    def hospi(date_d, date_f):
        global data_list
        L = end_frise[0]-beg_frise[0] #longueur de la frise
        D = (date_f - date_d).days #durée d'hospitalisation
        plagetps = (current_date-beg_date).days #plage de temps affichée
        x = beg_frise[0] + ((date_d-beg_date).days/plagetps)*L #abscisse du point en haut à gauche du rectangle
        #rectangle = canvas.create_line(x, beg_frise[1], x, end_frise[1], fill='red', width=(D/plagetps)*L)
        width = max(20, (D/plagetps)*L)
        rectangle = canvas.create_rectangle(x, beg_frise[1]-1, x + width, end_frise[1]+4, fill='#c10404')
        data_list.append(rectangle)

    #affiche un rectangle associé à un passage aux urgences
    def urg(date):
        global data_list
        L = end_frise[0]-beg_frise[0] #longueur de la frise
        plagetps = (current_date-beg_date).days #plage de temps affichée
        x = beg_frise[0] + ((date-beg_date).days/plagetps)*L #abscisse du point en haut à gauche du rectangle
        rectangle = canvas.create_rectangle(x, beg_frise[1], x+20, end_frise[1]+4, fill='#e73200')
        data_list.append(rectangle)

    #Recherche du CRH associé à un BMI (le plus proche, situé après, en termes de dates)

    #Prend en entrée l'index d'un BMI et retrourne celui du CRH associé
    def id_CRH(id_BMI):
        date_BMI = DPI.data['Date'][id_BMI] #date du BMI
        data_CRH = DPI.data[(DPI.data['Type de document'] == 'CRH') & (DPI.data['Date']>date_BMI)] #sous-dataframe avec les CRHs après le BMI
        if data_CRH.empty:
            return -1 #s'il n'y a pas de CRH après le BMI, le patient est encore hospitalisé
        else:
            ecart = (data_CRH['Date'].iloc[0] - date_BMI).days #on initialise l'écart de dates entre le BMI et le premier CRH
            index = data_CRH.index[0]
            for i in data_CRH.index:
                if (data_CRH['Date'][i] - date_BMI).days < ecart: #on vérifie que le CRH est plus près du BMI
                    ecart = (data_CRH['Date'][i] - date_BMI).days
                    index = i
            return index #l'indice est un entier naturel si on a bien un CRH, c'est -1 si on n'a pas de CRH après le BMI


    def bout_fleche_rouge(id_BMI): #met le bout de la flèche en rouge à partir de la date du BMI
        global data_list
        date_BMI = DPI.data['Date'][id_BMI]
        L = end_frise[0] - beg_frise[0] #longueur de la frise
        D = (current_date - date_BMI).days #durée d'hospitalisation
        plagetps = (current_date-beg_date).days #plage de temps affichée
        x = beg_frise[0] + ((date_BMI-beg_date).days/plagetps)*L #abscisse du point en haut à gauche du rectangle
        if (date_BMI - beg_date).days > 0:
            rect_rouge = canvas.create_rectangle(x, beg_frise[1]-1, 1280, end_frise[1]+4, fill='#c10404')
        else:
            rect_rouge = canvas.create_rectangle(beg_frise[0] - 80, beg_frise[1]-1, 1280, end_frise[1]+4, fill='#c10404')
        fleche = canvas.create_image(890, 500, anchor='center', image=render_bout_fleche_rouge)
        data_list += [fleche, rect_rouge]

    #Regroupe tous les BMIs d'un patient, leur associe un CRH et fait l'affichage de la plage de couleurs (à mettre dans la fonction affichage)
    def affiche_hospi():
        data_BMI = DPI.data[DPI.data['Type de document'] == 'BMI'] #sous-dataframe avec les BMIs
        for i in data_BMI.index:
            j = id_CRH(i) #index du CRH asocié au BMI
            if j!=-1: #si on a bien un CRH associé au BMI (le patient est sorti)
                date_d = DPI.data['Date'][i] #date du BMI
                date_f = DPI.data['Date'][j] #date du CRH
                if (date_d - beg_date).days > 0:
                    hospi(date_d, date_f) #affichage de la plage rouge d'hospitalisation
                elif (date_d - beg_date).days < 0 and (date_f - beg_date).days > 0:
                    hospi(beg_date, date_f)
            else: #si on n'a pas de CRH (le patient est toujours hospitalisé)
                bout_fleche_rouge(i)

    #Affiche tous les passages aux urgences
    def affiche_urg():
        data_urg = DPI.data[DPI.data['Type de document'] == 'CRU'] #sous-dataframe avec les CRU
        for i in data_urg.index:
            date = data_urg['Date'][i] #date du CRU
            urg(date)

    #Affichage de la frise vierge
    frise = canvas.create_image(890, 500,anchor='center', image=render_frise)
    data_list.append(frise)

    affiche_hospi()
    affiche_urg()
    
    #Fonction d'affichage drapeau et date
    def pos(time):
        days_event = abs((time - beg_date).days)
        x_pos = (days_event/((current_date - beg_date).days)) * (end_frise[0] - beg_frise[0]) + beg_frise[0]
        return x_pos

    def mark(time, n):
        """
        Prend une date et le type d'un élément et l'affiche 
        sur la frise
        """
        global data_list
        days_event = abs((time - beg_date).days)
        x_pos = (days_event/((current_date - beg_date).days)) * (end_frise[0] - beg_frise[0]) + beg_frise[0]
        #drapeau
        cursor =  canvas.create_image(x_pos - 30, beg_frise[1] - 30, anchor='center', image=render_flag[0])
        if n < 10:
            flag = canvas.create_image(x_pos - 30, beg_frise[1] - 45, anchor='center', image=render_flag[n])
        else :
            flag = canvas.create_image(x_pos - 30, beg_frise[1] - 45, anchor='center', image=render_flag[10])
        #date et type d'évènement
        text1 = canvas.create_text(x_pos-30, beg_frise[1]+30, anchor='center', text=time, font=('Arial Black', 10))
        data_list += [flag, text1, cursor]
        return (cursor, flag, text1)

    #Définition des évènements

    event_list = []
    for c, d in checked.items():
        if d.get():
            df = DPI.data[DPI.data['Type de document']==c]
            for i in df.index:
                time = df['Date'][i]
                type = df['Unité'][i]
                file_30min = df['Fichier lié'][i]
                if (time - beg_date).days > 0:# permet de n'afficher que les event dans la plage de temps considérée
                    event = tuple([pos(time)] + [file_30min] + [time] + [i])
                    event_list.append(event)


    #FONCTION MERGED (flags)
    def flags(event_list_entry):
        delta_min = 75 #Ecartement minimal entre les drapeaux
        event_list_entry.sort(key  = lambda Y : Y[0])
        output = []
        while event_list_entry:
            event0 = event_list_entry.pop(0)
            x0 = event0[0]
            date0 = event0[2]
            index0 = event0[3]
            list_of_index = [index0]
            for X in event_list_entry[:]:
                if X[0] - x0 < delta_min:
                    list_of_index.append(X[3])
                    event_list_entry.pop(0)
            output.append((date0, list_of_index))
        return output

    new_event_list = flags(event_list)
    #new_event_list = [(dt.date(2021, 10, 27), [10, 11, 12])]

    counter = {event[0] : 0 for event in new_event_list}

    for event in new_event_list:
        read_button = [] #liste des boutons de l'évènement
        date = event[0]
        x_pos = pos(date)
        n = len(event[1])
        cursor_loc, flag_loc, date_loc = mark(date, n)
        for index in event[1]:
            file = DPI.data['Fichier lié'].iloc[index]
            c = DPI.data['Type de document'].iloc[index]
            button_loc = tk.Button(window, text=c, font=('Arial Black', 10), bg='grey', command=partial(os.startfile, f'dossiers_patients\\{patient}\\{file}'))
            button_loc.place(x=x_pos-60, y=beg_frise[1]+150 + 32*counter[date])
            counter[date] += 1
            read_button.append(button_loc)
        event_button.append(read_button)

    
    #Affichage date de début/fin 
    #event_beg, event_current = mark(beg_date), mark(current_date)

    #Déplacement de object pour récupérer des coordonnées inutile pour le code final mais sympa pour coder
    object = flag_loc
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
frame = tk.LabelFrame(window, text='Sélectionnez les données souhaitées', padx=20, pady=0, bg='#6e706e')
frame.place(x=0, y=0)

#Choix du patient
variable_patient = tk.StringVar(window)
variable_patient.set('Polnareff Jean-Pierre')
menu_patient = tk.OptionMenu(frame, variable_patient, *tuple_name)
menu_patient.pack()

#Choix durée
variable_time = tk.StringVar(window)
variable_time.set('6 mois')
menu_time = tk.OptionMenu(frame, variable_time, *('30 jours', '6 mois', '1 an', '2 ans', '5 ans', '10 ans'))
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
        button_loc = tk.Checkbutton(frame, text=c, var=checked[c], width=20, anchor="w", command=affichage, bg='#6e706e')
        button_loc.pack()
    return checked

checked = check()


#bouton affichage de la frise 
bouton1 = tk.Button(frame, text ='Afficher frise', font=("Arial Black", 10), command=affichage, bg='#6e706e')
bouton1.pack()

#bouton de fermeture de la frise
bouton2 = tk.Button(window, text='Fermer', font=(('Arial Black'), 10), command=window.destroy, bg='#94060f')
bouton2.place(x=window_x-60, y=0)

#bouton données
bouton3 = tk.Button(frame, text='Documents patient', font=(('Arial Black'), 10), bg='#6e706e', command=disp_data)
bouton3.pack()

window.mainloop()

