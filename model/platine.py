import time
import json
import board
import busio
from gpiozero import Button, AngularServo
from model import mesure
from view import Adafruit_ADS1X15

class Platine:
    def __init__(
        self,
        servo_pin: int = 25,
        min_angle: float = 0,
        max_angle: float = 180,
        min_pulse_width: float = 0.0005,
        max_pulse_width: float = 0.0025,
        initial_angle: float = 0,
    ):
        """Initialise les composants matériels."""
        # Boutons de contrôle et de mesure (GPIO20, GPIO18)
        self.bouton_systeme = Button(20)
        self.bouton_mesure = Button(18)

        # Initialisation I2C et ADC ADS7830 (adresse 0x4B détectée)
        i2c = busio.I2C(board.SCL, board.SDA)
        self.adc = Adafruit_ADS1X15.ADS7830(i2c, address=0x4B)
        self.CHANNEL_POT = 0

        # Configuration du servomoteur
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.servo = AngularServo(
        servo_pin,
        min_angle=self.min_angle,
        max_angle=self.max_angle,
        min_pulse_width=min_pulse_width,
        max_pulse_width=max_pulse_width,
        initial_angle=initial_angle, 
        )

        # État interne
        self.systeme_actif = False
        self.derniere_mesure = None
        self.mesure = mesure.Mesure

    def lire_potentiometre(self) -> float:
        """Lit et renvoie une valeur normalisée (0–1) du potentiomètre."""
        raw = self.adc.read(self.CHANNEL_POT)      
        if raw > 255:
            raw >>= 8
        return max(0.0, min(1.0, raw / 255.0))

    def controler_servo(self, angle_normalise: float):
        """Positionne le servomoteur selon une valeur normalisée (0–1)."""
        # Mappe 0–1 à min_angle–max_angle
        angle = angle_normalise * (self.max_angle - self.min_angle) + self.min_angle
        self.servo.angle = angle

    def capturer_mesure(self):
     """Crée un objet Mesure avec la valeur et l'angle"""
     val = self.lire_potentiometre()
     angle = val * (self.max_angle - self.min_angle) + self.min_angle
     self.derniere_mesure = self.mesure(
        dateHeureMesure=self.mesure.heure_actuelle(),
        dataMesure=[val, angle]  # Stocke les deux valeurs
    )
     return self.derniere_mesure

    def sauvegarder_mesure(self, fichier: str = "mesures.json"):
     """Sauvegarde la dernière mesure au format JSON dans un tableau."""
     if self.derniere_mesure:
        try:
            # Convertit la valeur normalisée en angle
            angle = self.derniere_mesure.dataMesure[0] * (self.max_angle - self.min_angle) + self.min_angle
            
            data = {
                "date": self.derniere_mesure.dateHeureMesure,
                "angle": f"{round(angle, 1)}°"  
            }
            
            try:
                with open(fichier, "r") as f:
                    mesures = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                mesures = []
                
            mesures.append(data)
            
            with open(fichier, "w") as f:
                json.dump(mesures, f, indent=4, ensure_ascii=False)  
                
        except Exception as e:
            print(f"Erreur sauvegarde : {e}")

    def nettoyer(self):
        """Libère les ressources du servomoteur."""
        try:
            self.servo.close()
        except Exception:
            pass
