import os
import socket
import unittest

class TestRemove(unittest.TestCase):

    def test_TS28_desinstalacion_ficheros_en_maquina(self):
        self.assertFalse(os.path.exists("/etc/systemd/system/hermesd.service"))
        self.assertFalse(os.path.exists("/etc/systemd/system/hermesd-dashboard.service"))
        self.assertFalse(os.path.exists("/etc/hermesd/"))
        self.assertFalse(os.path.exists("/hermesd/"))

    def test_TS30_dashboard_deshabilitado(self):
        ip = '127.0.0.1'
        port = 8020

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1) 
            s.connect((ip, port))
            connected = True
        except:
            connected = False
        finally:
            s.close()

        self.assertFalse(connected)