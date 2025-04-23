from view.LCD import LCD
import time

class Vue:
    def __init__(self):
        self.lcd = LCD(addr=0x27, bl=1)
        
    def afficher_message(self, ligne1="", ligne2="", delai=0):
        """Affiche un message sur l'écran LCD"""
        self.lcd.clear()
        self.lcd.write(0, 0, ligne1[:16])  # Limite à 16 caractères
        self.lcd.write(0, 1, ligne2[:16])
        if delai > 0:
            time.sleep(delai)
            
    def afficher_mesure(self, angle):
        """Affiche l'angle du servo avec formatage"""
        self.afficher_message(
            ligne1="Angle servo:",
            ligne2=f"{angle*180:.1f}°"  # Conversion 0-1 -> 0-180°
        )
    
    def nettoyer(self):
        self.lcd.clear()