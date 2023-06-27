import unittest
import service
import paramiko

ip = '127.0.0.1'
user = 'root'
passw = 'root'

class TestService(unittest.TestCase):

    def test_TS03_comprobacion_maquina_UNIX_no_systemctl(self):
        self.assertEqual(service.check_machine_specs(os_check = 'Linux', systemctl_check = 1), False)
    
    def test_TS04_comprobacion_maquina_UNIX_systemctl(self):
        self.assertEqual(service.check_machine_specs(os_check = 'Linux', systemctl_check = 0), True)
    
    def test_TS05_comprobacion_no_maquina(self):
        self.assertEqual(service.check_machine_specs(os_check = '', systemctl_check = 0), False)

    def test_TS05_comprobacion_maquina_no_UNIX(self):
        self.assertEqual(service.check_machine_specs(os_check = 'Windows', systemctl_check = 0), False)
    
    def test_TS05_comprobacion_maquina_no_UNIX_2(self):
        self.assertEqual(service.check_machine_specs(os_check = 'Android', systemctl_check = 0), False)
    
    def test_TS06_comprobacion_maquina_UNIX(self):
        self.assertEqual(service.check_machine_specs(os_check = 'Linux', systemctl_check = 0), True)
    
    def test_TS06_comprobacion_maquina_UNIX(self):
        self.assertEqual(service.check_machine_specs(os_check = 'Darwin', systemctl_check = 0), True)

    def test_TS07_comprobacion_no_ping_no_ip(self):
        self.assertEqual(service.get_ping(''), False)

    def test_TS07_comprobacion_no_ping_ICMP(self):
        self.assertEqual(service.get_ping('10.0.0.1'), False)

    def test_TS08_comprobacion_ping_ICMP_maquina_local(self):
        self.assertEqual(service.get_ping(ip), True)
    
    def test_TS08_comprobacion_ping_ICMP_DNS_Google(self):
        self.assertEqual(service.get_ping('8.8.8.8'), True)
    
    def test_TS09_comprobacion_sistema_operativo_maquina_no_dentro_alcance_1(self):
        self.assertEqual(service.check_distro('ios'), False)
    
    def test_TS09_comprobacion_sistema_operativo_maquina_no_dentro_alcance_2(self):
        self.assertEqual(service.check_distro('windows'), False)
    
    def test_TS10_comprobacion_sistema_operativo_maquina_dentro_alcance_1(self):
        self.assertEqual(service.check_distro('debian'), True)
    
    def test_TS10_comprobacion_sistema_operativo_maquina_dentro_alcance_2(self):
        self.assertEqual(service.check_distro('fedora'), True)
    
    def test_TS11_comprobacion_error_puerto_1(self):
        self.assertEqual(service.check_port_connections(ip, port = '0'), False)
    
    def test_TS11_comprobacion_error_puerto_2(self):
        self.assertEqual(service.check_port_connections(ip, port = ''), False)
    
    def test_TS11_comprobacion_error_puerto_3(self):
        self.assertEqual(service.check_port_connections(ip, port = 'TCP-22'), False)

    def test_TS12_comprobacion_puerto_cerrado_SMB(self):
        self.assertEqual(service.check_port_connections(ip, port = 445), False)

    def test_TS13_comprobacion_puerto_abierto_HTTP(self):
        self.assertEqual(service.check_port_connections(ip, port = 80), True)

    def test_TS13_comprobacion_puerto_abierto_SSH(self):
        self.assertEqual(service.check_port_connections(ip, port = 22), True)

    def test_TS14_obtencion_servicio_preinstalado_SSH(self):
        service_name = 'openssh-server'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username=user, password=passw)
        
        distro = service.get_distro(client)
        commands = service.get_commands_distro(distro)
        services, _ = service.get_installed_services(client, commands)

        result = any([item[0] == service_name for item in services if item])
        
        self.assertTrue(result)
        client.close()
    
    def test_TS14_obtencion_servicio_preinstalado_TAR(self):
        service_name = 'tar'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username=user, password=passw)
        
        distro = service.get_distro(client)
        commands = service.get_commands_distro(distro)
        services, _ = service.get_installed_services(client, commands)

        result = any([item[0] == service_name for item in services if item])
        
        self.assertTrue(result)
        client.close()

    def test_TS15_obtencion_servicio_no_instalado_RSH(self):
        service_name = 'rsh'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username=user, password=passw)
        
        distro = service.get_distro(client)
        commands = service.get_commands_distro(distro)
        services, _ = service.get_installed_services(client, commands)

        result = any([item[0] == service_name for item in services if item])
        
        self.assertFalse(result)
        client.close()
     
    def test_TS15_obtencion_servicio_no_instalado_RLOGIN(self):
        service_name = 'rlogin'
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username=user, password=passw)
        
        distro = service.get_distro(client)
        commands = service.get_commands_distro(distro)
        services, _ = service.get_installed_services(client, commands)

        result = any([item[0] == service_name for item in services if item])
        
        self.assertFalse(result)
        client.close()

    def test_TS16_accion_servicios_vacio(self):
        self.assertEqual(service.analize_services('',''), 'OK')

    def test_TS17_accion_servicio_actualizado_tipo1(self):
        result = service.analize_services('1.13.1-11.el8','.13.1-11.el8')
        self.assertEqual(result, 'OK')
    
    def test_TS17_accion_servicio_actualizado_tipo2(self):
        result = service.analize_services('3.6.8-38.module_el8.5.0+895+a459eca8','6.8-38.module_el8.5.0+895+a459eca8')
        self.assertEqual(result, 'OK')

    def test_TS17_accion_servicio_actualizado_tipo3(self):
        result = service.analize_services('4.3.91-3.28.1', '4.3.91-3.28.1')
        self.assertEqual(result, 'OK')

    def test_TS17_accion_servicio_actualizado_tipo4(self):
        result = service.analize_services('2.4.37-40','2.4.37-40')
        self.assertEqual(result, 'OK')

    def test_TS18_accion_servicio_desactualizado_retrocompatible_beta_tipo1(self):
        result = service.analize_services('1.13.1-11.el8','1.13.1-29.el8')
        self.assertEqual(result, 'UPDATE')
    
    def test_TS18_accion_servicio_desactualizado_retrocompatible_beta_tipo2(self):
        result = service.analize_services('3.6.8-38.module_el8.5.0+895+a459eca8','3.6.8-50.module_el8.5.0+895+a459eca8')
        self.assertEqual(result, 'UPDATE')

    def test_TS18_accion_servicio_desactualizado_retrocompatible_beta_tipo3(self):
        result = service.analize_services('4.3.91-3.28.1', '4.3.91-4.2.1')
        self.assertEqual(result, 'UPDATE')

    def test_TS18_accion_servicio_desactualizado_retrocompatible_beta_tipo4(self):
        result = service.analize_services('2.4.37-40','2.4.37-63')
        self.assertEqual(result, 'UPDATE')

    def test_TS18_accion_servicio_desactualizado_retrocompatible_parche_tipo1(self):
        result = service.analize_services('1.13.1-11.el8','1.13.2-10.el8')
        self.assertEqual(result, 'UPDATE')
    
    def test_TS18_accion_servicio_desactualizado_retrocompatible_parche_tipo2(self):
        result = service.analize_services('3.6.3-38.module_el8.5.0+895+a459eca8','3.6.8-40.module_el8.5.0+895+a459eca8')
        self.assertEqual(result, 'UPDATE')

    def test_TS18_accion_servicio_desactualizado_retrocompatible_parche_tipo3(self):
        result = service.analize_services('4.3.91-3.28.1', '4.3.96-3.28.1')
        self.assertEqual(result, 'UPDATE')

    def test_TS18_accion_servicio_desactualizado_retrocompatible_parche_tipo4(self):
        result = service.analize_services('2.4.37-40','2.4.40-0')
        self.assertEqual(result, 'UPDATE')
    
    def test_TS18_accion_servicio_desactualizado_retrocompatible_minor_tipo1(self):
        result = service.analize_services('1.13.1-11.el8','1.14.2-10.el8')
        self.assertEqual(result, 'UPDATE')
    
    def test_TS18_accion_servicio_desactualizado_retrocompatible_minor_tipo2(self):
        result = service.analize_services('3.6.8-38.module_el8.5.0+895+a459eca8','3.7.2-12.module_el8.5.0+895+a459eca8')
        self.assertEqual(result, 'UPDATE')

    def test_TS18_accion_servicio_desactualizado_retrocompatible_minor_tipo3(self):
        result = service.analize_services('4.3.91-3.28.1', '4.4.10-1.20.0')
        self.assertEqual(result, 'UPDATE')

    def test_TS18_accion_servicio_desactualizado_retrocompatible_minor_tipo4(self):
        result = service.analize_services('2.4.37-40','2.7.3-13')
        self.assertEqual(result, 'UPDATE')

    def test_TS19_accion_servicio_desactualizado_no_retrocompatible_tipo1(self):
        result = service.analize_services('1.13.1-11.el8','2.14.1-11.el8')
        self.assertEqual(result, 'OK')
    
    def test_TS19_accion_servicio_desactualizado_no_retrocompatible_tipo2(self):
        result = service.analize_services('3.6.8-38.module_el8.5.0+895+a459eca8','6.8-38.module_el8.5.0+895+a459eca8')
        self.assertEqual(result, 'OK')

    def test_TS19_accion_servicio_desactualizado_no_retrocompatible_tipo3(self):
        result = service.analize_services('4.3.91-3.28.1', '5.3.91-3.28.1')
        self.assertEqual(result, 'OK')

    def test_TS19_accion_servicio_desactualizado_no_retrocompatible_tipo4(self):
        result = service.analize_services('2.4.37-40','4.2.0-4')
        self.assertEqual(result, 'OK')    

    def test_TS20_obtencion_comandos_necesarios_sin_sistema_operativo(self):
        self.assertEqual(service.get_commands_distro(''), None)

    def test_TS20_obtencion_comandos_necesarios_por_sistema_operativo_no_dentro_alcance_WINDOWS(self):
        self.assertEqual(service.get_commands_distro('windows'), None)
    
    def test_TS20_obtencion_comandos_necesarios_por_sistema_operativo_no_dentro_alcance_ARCH(self):
        self.assertEqual(service.get_commands_distro('arch'), None)

    def test_TS21_obtencion_comandos_necesarios_por_sistema_operativo_DEBIAN(self):
        debian_commands = ['debian', 'apt list --installed', 'apt list --upgradeable', 'apt install -y ']
        self.assertEqual(service.get_commands_distro('debian'), debian_commands)
    
    def test_TS21_obtencion_comandos_necesarios_por_sistema_operativo_SUSE(self):
        suse_commands = ['opensuse', 'zypper pa --installed-only', 'zypper list-updates', 'zypper up -y ']
        self.assertEqual(service.get_commands_distro('suse'), suse_commands)
    
    def test_TS22_obtencion_maquina_sin_IP(self):
        result = service.get_ip_range('')
        self.assertEqual(result, [])
    
    def test_TS22_obtencion_maquina_erronea_1(self):
        result = service.get_ip_range('d.2111.332.1')
        self.assertEqual(result, [])
    
    def test_TS22_obtencion_maquina_erronea_2(self):
        result = service.get_ip_range('122.121.12')
        self.assertEqual(result, [])
    
    def test_TS23_obtencion_maquina_IP_1(self):
        result = service.get_ip_range('127.0.0.1')
        self.assertEqual(result, ['127.0.0.1'])
    
    def test_TS23_obtencion_maquina_IP_2(self):
        result = service.get_ip_range('192.168.56.110')
        self.assertEqual(result, ['192.168.56.110'])

    def test_TS24_obtencion_maquina_IP_lista_IPs_tipo1(self):
        result = service.get_ip_range('192.168.56.1,192.168.56.2,192.168.56.3')
        self.assertEqual(result, ['192.168.56.1','192.168.56.2','192.168.56.3'])
    
    def test_TS24_obtencion_maquina_lista_IPs_tipo2(self):
        result = service.get_ip_range('192.0.2.1 ,192.0.2.2, 192.0.2.3')
        self.assertEqual(result, ['192.0.2.1','192.0.2.2','192.0.2.3'])

    def test_TS25_obtencion_maquina_rango_IPs_tipo1(self):
        result = service.get_ip_range('192.168.56.110-192.168.56.114')
        self.assertEqual(result, ['192.168.56.110','192.168.56.111','192.168.56.112','192.168.56.113','192.168.56.114'])
    
    def test_TS25_obtencion_maquina_rango_IPs_tipo2(self):
        result = service.get_ip_range('63.45.12.30 - 63.45.12.34')
        self.assertEqual(result, ['63.45.12.30','63.45.12.31','63.45.12.32','63.45.12.33','63.45.12.34'])
    
    def test_TS25_obtencion_maquina_rango_IPs_tipo3(self):
        result = service.get_ip_range('63.45.12.30 -63.45.12.34')
        self.assertEqual(result, ['63.45.12.30','63.45.12.31','63.45.12.32','63.45.12.33','63.45.12.34'])
    
    def test_TS26_obtencion_maquina_red_tipo1(self):
        result = service.get_ip_range('192.0.2.0/29')
        self.assertEqual(result, ['192.0.2.1','192.0.2.2','192.0.2.3','192.0.2.4','192.0.2.5','192.0.2.6'])
    
    def test_TS26_obtencion_maquina_red_tipo2(self):
        result = service.get_ip_range('192.168.56.0 / 30')
        self.assertEqual(result, ['192.168.56.1','192.168.56.2'])
    
    def test_TS26_obtencion_maquina_red_tipo2(self):
        result = service.get_ip_range('192.168.56.0 /30')
        self.assertEqual(result, ['192.168.56.1','192.168.56.2'])