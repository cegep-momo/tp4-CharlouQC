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
        Retourne tous les attributs de l’objet sur une ou plusieurs lignes
        """
        return (f"Date/Heure: {self.dateHeureMesure}\n"
                f"Valeurs: {', '.join(map(str, self.dataMesure))}")
                
    def heure_actuelle() -> str:
        """
        Génère la date/heure actuelle 
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")