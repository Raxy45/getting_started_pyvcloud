from vcloud_util import VCD_Utils

vCloud_hostname = 'your_hostname.com'
org_name = 'your_orgname'
vCloud_vdc = 'your_VDC'
vCloud_username = 'Awesome_user'
vCloud_pwd = 'secret_pwd'

vcd_object = VCD_Utils(vCloud_hostname, org_name,
                       vCloud_vdc, vCloud_username, vCloud_pwd)

vapp_name = "Awesome_vApp"
vapp_template = 'Awesome_template'

print(vcd_object.create_new_vApp(vapp_name, vapp_template))
print(vcd_object.get_vapp_ip_address(vapp_name))
print(vcd_object.update_vapp_cpu(
    vapp_name, virtual_cpus=2, cores_per_socket=1))
print(vcd_object.delete_vapp(vapp_name))
vcd_object.logout()
