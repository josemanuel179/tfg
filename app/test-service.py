import unittest
import service
import ipaddress

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
    
    def test_analize_services_XVII(self):
        result = service.analize_services('4.3.91-3.28.1', '4.3.100-150300.3.42.1')
        self.assertEqual(result, 'UPDATE')
    
    def test_analize_services_XVIII(self):
        result = service.analize_services('3.2-9.24.2', '4.1-150300.16.9.1')
        self.assertEqual(result, 'OK')
    
    def test_analize_services_XX(self):
        result = service.analize_services('20.10.9_ce-156.1','20.10.12_ce-159.1')
        self.assertEqual(result, 'OK')

    def test_analize_services_XXI(self):
        result = service.analize_services('2.20-2.1','2.26-150300.4.3.1')
        self.assertEqual(result, 'UPDATE')
    
    def test_analize_services_XXII(self):
        result = service.analize_services('0.6.65-2.1','0.6.68-150300.4.5.1')
        self.assertEqual(result, 'UPDATE')
    
    def test_analize_services_XXIII(self):
        result = service.analize_services('1.2-1.30','1.2-3.3.1')
        self.assertEqual(result, 'UPDATE')
    
    def test_get_ips_I(self):
        result = service.get_ip_range('')
        self.assertEqual(result, [''])
    
    def test_get_ips_II(self):
        result = service.get_ip_range('192.168.56.110')
        self.assertEqual(result, ['192.168.56.110'])
    
    def test_get_ips_III(self):
        result = service.get_ip_range('63.45.12.34')
        self.assertEqual(result, ['63.45.12.34'])
    
    def test_get_ips_IV(self):
        result = service.get_ip_range('192.168.56.110-192.168.56.114')
        self.assertEqual(result, ['192.168.56.110','192.168.56.111','192.168.56.112','192.168.56.113','192.168.56.114'])
    
    def test_get_ips_V(self):
        result = service.get_ip_range('63.45.12.30 - 63.45.12.34')
        self.assertEqual(result, ['63.45.12.30','63.45.12.31','63.45.12.32','63.45.12.33','63.45.12.34'])
    
    def test_get_ips_VI(self):
        result = service.get_ip_range('192.0.2.0/29')
        self.assertEqual(result, ['192.0.2.1','192.0.2.2','192.0.2.3','192.0.2.4','192.0.2.5','192.0.2.6'])
    
    def test_get_ips_VII(self):
        result = service.get_ip_range('192.168.56.0/30')
        self.assertEqual(result, ['192.168.56.1','192.168.56.2'])
