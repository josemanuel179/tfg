import socket
import unittest

class TestDashbooard(unittest.TestCase):
    
    def test_TS29_instanciacion_dashboard(self):
        ip = '127.0.0.1'
        port = 8020

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(90) 
            s.connect((ip, port))
            connected = True
        except:
            connected = False
        finally:
            s.close()

        self.assertTrue(connected)