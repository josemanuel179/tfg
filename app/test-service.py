import unittest
import service

class TestService(unittest.TestCase):
	
    def test_analize_services_empty(self):
        result = service.analize_services('','')
        self.assertEqual(result, 'OK')
    
    def test_analize_services_I(self):
        result = service.analize_services('1.13.1-11.el8','1.13.1-20.el8')
        self.assertEqual(result, 'UPDATE')
    
    def test_analize_services_II(self):
        result = service.analize_services('1.13.1-11.el8','1.13.2-11.el8')
        self.assertEqual(result, 'UPDATE')
    
    def test_analize_services_III(self):
        result = service.analize_services('1.13.1-11.el8','1.14.1-11.el8')
        self.assertEqual(result, 'UPDATE')
    
    def test_analize_services_IV(self):
        result = service.analize_services('1.13.1-11.el8','2.14.1-11.el8')
        self.assertEqual(result, 'OK')

    def test_analize_services_V(self):
        result = service.analize_services('1:0.9.3-25.el','1:0.9.3-25.el')
        self.assertEqual(result, 'OK')

    def test_analize_services_VI(self):
        result = service.analize_services('1:0.9.3-25.el','1:0.9.3-26.el')
        self.assertEqual(result, 'UPDATE')

    def test_analize_services_VII(self):
        result = service.analize_services('1:0.9.3-25.el','1:0.9.4-15.el')
        self.assertEqual(result, 'UPDATE')

    def test_analize_services_VIII(self):
        result = service.analize_services('1:0.9.3-25.el','1:0.9.4-26.el')
        self.assertEqual(result, 'UPDATE')

    def test_analize_services_IX(self):
        result = service.analize_services('1:0.9.3-25.el','1:1.0.3-26.el')
        self.assertEqual(result, 'OK')

    def test_analize_services_X(self):
        result = service.analize_services('3.6.8-38.module_el8.5.0+895+a459eca8','3.6.9-8.module_el8.5.0+895+a459eca8')
        self.assertEqual(result, 'UPDATE')

    def test_analize_services_XI(self):
        result = service.analize_services('3.6.8-38.module_el8.5.0+895+a459eca8','4.0.1-3.module_el8.5.0+895+a459eca8')
        self.assertEqual(result, 'OK')
    
    def test_analize_services_XII(self):
        result = service.analize_services('0.115-13.el8_5.1','0.115-20.el8_5.1')
        self.assertEqual(result, 'UPDATE')

    def test_analize_services_XIII(self):
        result = service.analize_services('2.4-4.el8','2.5-4.el8')
        self.assertEqual(result, 'UPDATE')
    
    def test_analize_services_XIV(self):
        result = service.analize_services('2.4-4.el8','2.5-10.el8')
        self.assertEqual(result, 'UPDATE')
    
    def test_analize_services_XV(self):
        result = service.analize_services('2.4-4.el8','3.1-1.el8')
        self.assertEqual(result, 'OK')

    def test_analize_services_XVI(self):
        result = service.analize_services('2022a-1.el8', '2022a-2.el8')
        self.assertEqual(result, 'OK')