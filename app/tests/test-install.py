import os
import stat
import unittest

class TestInstall(unittest.TestCase):

    def test_TS27_instalacion_ficheros_en_maquina(self):
        self.assertTrue(os.path.exists("/etc/systemd/system/hermesd.service"))
        self.assertTrue(os.path.exists("/etc/systemd/system/hermesd-dashboard.service"))
        self.assertTrue(os.path.exists("/etc/hermesd/service.conf"))
        self.assertTrue(os.path.exists("/hermesd/hermes.py"))
        self.assertTrue(os.path.exists("/hermesd/service.py"))
        self.assertTrue(os.path.exists("/hermesd/dashboard.py"))
        self.assertTrue(os.path.exists("/hermesd/hermes.csv"))
    
    def test_TS33_permisos_ficheros(self):
        self.assertEqual(stat.S_IMODE(os.lstat("/etc/systemd/system/hermesd.service").st_mode), 0o777)
        self.assertEqual(stat.S_IMODE(os.lstat("/etc/systemd/system/hermesd-dashboard.service").st_mode), 0o777)
        self.assertEqual(stat.S_IMODE(os.lstat("/etc/hermesd/service.conf").st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(os.lstat("/hermesd/hermes.csv").st_mode), 0o400)
    
    def test_TS34_permisos_scripts(self):
        self.assertEqual(stat.S_IMODE(os.lstat("/hermesd/hermes.py").st_mode), 0o100)
        self.assertEqual(stat.S_IMODE(os.lstat("/hermesd/service.py").st_mode), 0o100)
        self.assertEqual(stat.S_IMODE(os.lstat("/hermesd/dashboard.py").st_mode), 0o100)
