import datetime

class Mesure:
    
    def __init__(self, dateHeureMesure: str, dataMesure: list):
        """
        Constructeur de la classe Mesure.
        """
        self.dateHeureMesure = dateHeureMesure
        self.dataMesure = dataMesure
        
    
    def __repr__(self) -> str:
        
        return f"Mesure(dateHeureDescription='{self.dateHeureMesure}', dataMesure={self.dataMesure})"
    
    def afficherMesure(self) -> str:
        """
        Affiche l'angle formaté
        """
        angle = self.dataMesure[1]  # Récupère l'angle
        return (f"Date/Heure: {self.dateHeureMesure}\n"
                f"Angle: {angle:.1f}°")  
                
    def heure_actuelle():
        """
        Génère la date/heure actuelle 
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")