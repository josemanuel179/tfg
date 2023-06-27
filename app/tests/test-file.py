import os
import csv
import datetime
import unittest

class TestFile(unittest.TestCase):

    def test_TS31_comprobacion_creacion_fichero_datos_tras_reinicio(self):
        actual_time = datetime.datetime.now()
        self.assertTrue(os.path.exists("/hermesd/" + actual_time.strftime("%Y%m%d") + '_hermes.csv'))

    def test_TS32_comprobacion_fichero_original_tras_reinicio(self):
        path = "/hermesd/hermes.csv"

        with open(path, 'r', newline= "") as file:
            reader = csv.reader(file)
            lines = sum(1 for _ in reader)

        self.assertEqual(lines, 1)