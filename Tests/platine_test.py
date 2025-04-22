from gpiozero import Button

class PlatineTest:
    """Version simplifiée pour les tests"""
    def __init__(self, pin_bouton):     
        self.bouton_systeme = Button(pin_bouton)  
        self.systeme_actif = False