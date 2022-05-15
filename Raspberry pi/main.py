import tkinter as tk
from tkinter import ttk
from SteppingMotor import *
from Thermometer import *
from UltrasonicRanging import *
from AzureCloud import *
from Database import *
import logging
import json

logging.basicConfig(filename='control.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


# Classe qui s'occupe du UI et de tout le programme
class MainWindow(object):
    # Initialiser
    def __init__(self):
        logging.info("start")
        self.thermometer = Thermometer()
        self.steppingMotor = SteppingMotor()
        self.ultrasonicRanging = UltrasonicRanging()
        self.azureCloud = AzureCloud()
        self.database = Database()
        
        self.mode = "auto"

        self.root = tk.Tk()
        self.root.title('''Contrôle d'une serre''')

        canvas = tk.Canvas(self.root, width=500, height=300)
        canvas.grid(columnspan=6, rowspan=9)

        # Mise en place des variables
        self.temp = tk.StringVar()
        self.distance = tk.StringVar()
        self.direction = tk.StringVar()
        self.speed = tk.StringVar()
        self.current_percentage = tk.StringVar()

        # Mise en place du texte
        self.label_title = tk.Label(self.root, text="Contrôle d’une porte d’aération d’une serre").grid(columnspan=7,
                                                                                                        row=0, column=0)
        self.label_temp = tk.Label(self.root, text="Température ambiante :").grid(columnspan=2, row=1, column=0)
        self.label_var_temp = tk.Label(self.root, textvariable=self.temp).grid(row=1, column=2)
        self.label_dist = tk.Label(self.root, text="Distance d’ouverture de la porte :").grid(columnspan=2, row=2,
                                                                                              column=0)
        self.label_var_dist = tk.Label(self.root, textvariable=self.distance).grid(row=2, column=2)
        self.label_control = tk.Label(self.root, text="Contrôle :").grid(row=3, column=0)
        self.label_percentage = tk.Label(self.root, text="%").grid(row=4, column=3)
        self.label_status = tk.Label(self.root, text="Statut du Moteur :", ).grid(columnspan=2, row=6, column=0)
        self.labe_dir = tk.Label(self.root, text="Direction :").grid(row=7, column=0)
        self.label_var_dir = tk.Label(self.root, textvariable=self.direction).grid(row=7, column=1)
        self.label_speed = tk.Label(self.root, text="Vitesse :").grid(row=7, column=3)
        self.label_var_speed = tk.Label(self.root, textvariable=self.speed).grid(row=7, column=4)

        # Mise en place des buttons
        self.btn_auto = tk.Button(self.root, text="Automatique", command=self.pass_to_auto).grid(row=3, column=1)
        self.btn_manual = tk.Button(self.root, text="Manuelle", command=self.pass_to_manual).grid(row=4, column=1)
        self.btn_open = tk.Button(self.root, text="Ouvrir la porte", command=self.fully_open).grid(row=5, column=0)
        self.btn_close = tk.Button(self.root, text="Fermer la porte", command=self.fully_close).grid(row=5, column=1)
        self.btn_log = tk.Button(self.root, text="Afficher les logs", command=self.show_logs).grid(columnspan=7, row=8,
                                                                                                   column=0)

        # Mise en place de l'input
        self.percentage_input = tk.StringVar()
        self.entry_manual = tk.Entry(self.root, textvariable=self.percentage_input).grid(row=4, column=2)

        # Mise en place de la progress bar
        frame = tk.LabelFrame(self.root)
        frame.grid(row=4, column=5)
        self.label_progress = tk.Label(frame, text="Pourcentage d’ouverture\n de la porte :").grid(row=3, column=5)
        self.showing_bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.showing_bar.grid(row=6, column=5)
        self.label_var_progress_bar = tk.Label(frame, textvariable=self.current_percentage).grid(row=5, column=5)

        self.root.after(50, self.show_temp)
        self.root.after(50, self.show_distance)
        self.root.after(50, self.run)
        self.root.after(6000, self.send_message)
        self.root.mainloop()

    # S'occupe du déroulement dépendament du mode
    def run(self):
        if (self.mode == "auto"):
            self.pass_to_auto()
        elif (self.mode == "manual"):
            self.pass_to_manual()
        elif (self.mode == "open"):
            self.fully_open()
        elif (self.mode == "close"):
            self.fully_close()

        self.show_door_percentage()
        self.root.after(35, self.run)

    # Mode automatique où la distance change par rapport à la température
    def pass_to_auto(self):
        self.mode = "auto"
        logging.info("click bouton automatique")

        temp = int(self.temp.get()[:2])

        if ((temp) <= 20):
            self.fully_close()
        elif ((temp) >= 35):
            self.fully_open()
        elif (20 < int(temp) < 35):
            dist = int(7 + 7 * 0.067 * (temp - 20))
            self.open_to()

    # Mode manuel où la orte ouvre selon un pourcentage donné
    def pass_to_manual(self):
        self.mode = "manual"
        logging.info("click bouton manuelle")
        if (self.percentage_input.get() and int(self.percentage_input.get())):
            self.open_to()

    # Ouvrir la porte à 100%
    def fully_open(self):
        self.mode = "open"
        logging.info("click bouton ouvrir la porte")
        current_dist = int(self.distance.get()[:2])
        dist = 14

        if (current_dist < int(dist)):
            self.steppingMotor.move(0, 7)
        elif (current_dist > int(dist)):
            self.steppingMotor.move(1, 7)

    # Fermer la porte complétement
    def fully_close(self):
        self.mode = "close"
        logging.info("click bouton fermer la porte")
        current_dist = int(self.distance.get()[:2])
        dist = 7

        if (current_dist < int(dist)):
            self.steppingMotor.move(0, 7)
        elif (current_dist > int(dist)):
            self.steppingMotor.move(1, 7)

    # Ouvrir à une certaine distance la porte selon le mode
    def open_to(self):
        current_dist = int(self.distance.get()[:2])
        if (self.mode == "auto"):
            dist = int(7 + 7 * 0.067 * (int(self.temp.get()[:2]) - 20))
        if (self.mode == "manual"):
            dist = 7 + (int(self.percentage_input.get()) / 100) * 7

        if (current_dist < int(dist)):
            self.steppingMotor.move(0, 7)
            self.direction.set("Gauche")
            self.speed.set("2 tours / minute")
            logging.info("Le moteur va à gauche à une vitesse de 2 tours / minute")
        elif (current_dist > int(dist)):
            self.steppingMotor.move(1, 7)
            self.direction.set("Droite")
            self.speed.set("2 tours / minute")
            logging.info("Le moteur va à droite à une vitesse de 2 tours / minute")
        else:
            self.direction.set("Aucune")
            self.speed.set("0 tours / minute")
            logging.info("Le moteur ne bouge pas")

    # Nouvelle fenêtre qui affiche les logs
    def show_logs(self):
        logging.info("click bouton afficher les logs")
        file = open('control.log', mode='r')
        text = file.readlines()
        file.close()

        newWindow = tk.Toplevel(self.root)
        newWindow.title("Logs")
        newWindow.geometry("300x500")
        tk.Label(newWindow, text=text[:-50]).grid(row=0, column=0)

    # Affiche le pourcentage d'ouverture de la porte
    def show_door_percentage(self):
        percentage = ((int(self.distance.get()[:2]) - 7) / 7) * 100
        self.showing_bar['value'] = percentage
        if percentage > 100 :
            percentage = 100
        if percentage < 0 :
            percentage = 0
            
        self.current_percentage.set(str(int(percentage)) + " %")

    # Affiche la température
    def show_temp(self):
        self.thermometer.read_temp()
        self.temp.set(str("%.f" % self.thermometer.tempC) + " °C")
        logging.info("Température actuelle : " + str(self.temp.get()) + " °C")
        self.root.after(35, self.show_temp)

    # Affiche la distance
    def show_distance(self):
        self.ultrasonicRanging.read_distance()
        self.distance.set(str("%.f" % self.ultrasonicRanging.distance) + " cm")
        logging.info("distance actuelle : " + str(self.distance.get()) + " cm")
        self.root.after(50, self.show_distance)

    # Arreter le programme
    def destroy(self):
        logging.info("Destroy")
        self.thermometer.destroy()
    
    # Envoyer un message a Azure et l'ajouter dans la BD
    def send_message(self):
        if (self.mode == "manual" and int(self.percentage_input.get())):
            manual_value = str(self.percentage_input.get())
        else:
            manual_value = ""
             
        msg = {
          "temp": str(self.temp.get()).replace(" °C",""),
          "pourcentageOpeningDoor": str(self.current_percentage.get()).replace(" %",""),
          "control": self.mode,
          "pourcentageManual": manual_value
          }
        self.database.add(str(self.temp.get()), str(self.current_percentage.get()),self.mode, manual_value)
        self.azureCloud.send(json.dumps(msg))
        self.root.after(6000, self.send_message)


if __name__ == '__main__':
    try:
        MainWindow()
    except KeyboardInterrupt:  # ctrl-c
        MainWindow().destroy()

