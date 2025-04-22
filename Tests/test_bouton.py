import unittest
from gpiozero import Device
from gpiozero.pins.mock import MockFactory

import platine_test 

Device.pin_factory = MockFactory()

class TestBouton(unittest.TestCase):
    def setUp(self):     
        self.platine = platine_test.PlatineTest(20)
    
    def test_bouton_systeme_presse(self):
        # 1. Simule l'appui
        self.platine.bouton_systeme.pin.drive_low()
        self.assertTrue(self.platine.bouton_systeme.is_pressed)
        
        # 2. Simule le relâchement
        self.platine.bouton_systeme.pin.drive_high()
        self.assertFalse(self.platine.bouton_systeme.is_pressed)

if __name__ == "__main__":
    unittest.main()