import time
import smbus2 as smbus

class LCD:
    def __init__(self, addr=0x27, bl=1):
        """Initialise l'écran LCD avec l'adresse I2C et l'état du rétroéclairage."""
        self.LCD_ADDR = addr
        self.BLEN = bl
        self.BUS = smbus.SMBus(1)
        self.init_lcd()

    def write_word(self, addr, data):
        """Écrit un octet sur le bus I2C."""
        temp = data
        if self.BLEN == 1:
            temp |= 0x08
        else:
            temp &= 0xF7
        self.BUS.write_byte(addr, temp)

    def send_command(self, comm):
        """Envoie une commande à l'écran LCD."""
        # Partie haute
        buf = comm & 0xF0
        buf |= 0x04  # RS = 0, RW = 0, EN = 1
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB  # EN = 0
        self.write_word(self.LCD_ADDR, buf)

        # Partie basse
        buf = (comm & 0x0F) << 4
        buf |= 0x04  # RS = 0, RW = 0, EN = 1
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB  # EN = 0
        self.write_word(self.LCD_ADDR, buf)

    def send_data(self, data):
        """Envoie des données (caractères) à l'écran LCD."""
        # Partie haute
        buf = data & 0xF0
        buf |= 0x05  # RS = 1, RW = 0, EN = 1
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB  # EN = 0
        self.write_word(self.LCD_ADDR, buf)

        # Partie basse
        buf = (data & 0x0F) << 4
        buf |= 0x05  # RS = 1, RW = 0, EN = 1
        self.write_word(self.LCD_ADDR, buf)
        time.sleep(0.002)
        buf &= 0xFB  # EN = 0
        self.write_word(self.LCD_ADDR, buf)

    def init_lcd(self):
        """Initialise l'écran LCD."""
        try:
            self.send_command(0x33)  # Init mode 8 bits
            time.sleep(0.005)
            self.send_command(0x32)  # Passage en mode 4 bits
            time.sleep(0.005)
            self.send_command(0x28)  # 2 lignes, 5x7 caractères
            time.sleep(0.005)
            self.send_command(0x0C)  # Affichage activé, curseur désactivé
            time.sleep(0.005)
            self.clear()  # Nettoyage de l'écran
            self.BUS.write_byte(self.LCD_ADDR, 0x08)
        except Exception as e:
            print(f"Erreur lors de l'initialisation de l'écran LCD : {e}")

    def clear(self):
        """Efface l'écran LCD."""
        self.send_command(0x01)

    def openlight(self):
        """Allume le rétroéclairage de l'écran LCD."""
        self.BUS.write_byte(self.LCD_ADDR, 0x08)

    def write(self, x, y, text):
        """Écrit du texte sur l'écran LCD à la position (x, y)."""
        if x < 0:
            x = 0
        if x > 15:
            x = 15
        if y < 0:
            y = 0
        if y > 1:
            y = 1

        # Déplacement du curseur
        addr = 0x80 + 0x40 * y + x
        self.send_command(addr)

        for char in text:
            self.send_data(ord(char))


if __name__ == '__main__':
    lcd = LCD(0x27, 1)  # Création de l'objet LCD
    lcd.write(4, 0, 'Hello')
    lcd.write(7, 1, 'World !')
