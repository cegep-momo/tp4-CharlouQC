from time import time, sleep
from model import platine
from view import vue
from model import mesure

class Controleur:
    def __init__(self):
        self.modele = platine.Platine()
        self.vue = vue.Vue()
        self.en_fonction = False

    def demarrer_systeme(self):
        self.en_fonction = True
        self.vue.afficher_message("Systeme demarre", "En attente...")

        # Délais distincts
        servo_delai = 0.01
        lcd_delai = 5

        derniere_update_servo = time()
        derniere_update_lcd = time()

        while self.en_fonction:
            temps_actuel = time()

            # Mise à jour du servo
            if temps_actuel - derniere_update_servo >= servo_delai:
                angle = self.modele.lire_potentiometre()
                self.modele.controler_servo(angle)
                derniere_update_servo = temps_actuel

            # Mise à jour du LCD
            if temps_actuel - derniere_update_lcd >= lcd_delai:
                self.vue.afficher_mesure(angle)
                derniere_update_lcd = temps_actuel

            # Vérification des boutons
            if self.modele.bouton_mesure.is_pressed:
                self._traiter_mesure()

            if self.modele.bouton_systeme.is_pressed:
                self.arreter_systeme()

            sleep(0.001)

    def _traiter_mesure(self):
        self.vue.afficher_message("Capture en cours", "...")
        self.modele.capturer_mesure()
        sleep(5)
        self.modele.sauvegarder_mesure()
        self.vue.afficher_message("Angle sauvegarde!", "", 2)

    def arreter_systeme(self):
        self.en_fonction = False
        self.vue.afficher_message("Systeme arrete", "Au revoir!", 2)
        self.vue.nettoyer()
        self.modele.nettoyer()

    def executer(self):
     try:
          while True:
            if self.modele.bouton_systeme.is_pressed:
                # Attend que le bouton soit relâché avant de continuer
                while self.modele.bouton_systeme.is_pressed:
                    sleep(0.01)
                self.demarrer_systeme()
            sleep(0.00001)
     except KeyboardInterrupt:
        self.arreter_systeme()

