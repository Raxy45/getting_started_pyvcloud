import time
from pyvcloud.vcd.vm import VM
from pyvcloud.vcd.vapp import VApp
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.exceptions import EntityNotFoundException, MultipleRecordsException
from pyvcloud.vcd.client import BasicLoginCredentials, Client
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class VCD_Utils():
    def __init__(self, vcloud_host_name, vcloud_org_name,
                 vcloud_org_vdc_name,
                 vcloud_user_name, vcloud_user_pwd):
        try:
            self.client = ""
            self.vdc = ""
            self.org = ""

            self.client = Client(vcloud_host_name,
                                 verify_ssl_certs=False,
                                 log_requests=False,
                                 log_headers=False,
                                 log_bodies=False)

            self.client.set_credentials(BasicLoginCredentials(vcloud_user_name,
                                                              vcloud_org_name,
                                                              vcloud_user_pwd))
            self.org_resource = self.client.get_org()
            self.org = Org(self.client, resource=self.org_resource)
            self.vdc_resource = self.org.get_vdc(name=vcloud_org_vdc_name)
            self.vdc = VDC(self.client, resource=self.vdc_resource)
        except Exception as err:
            print(f"Error encountered in login(), Error: {err}")

    # Helper Methods
    def get_vapp(self, vapp_name):
        try:
            vapp_resource = self.vdc.get_vapp(vapp_name)
            vapp = VApp(self.client, resource=vapp_resource)
            return vapp
        except Exception as exc:
            print(f"Error encountered in get_vapp(), Error: {exc}")
            return False

    def get_vm(self, vapp_name):
        try:
            vapp = self.get_vapp(vapp_name)
            vm_resource = vapp.get_all_vms()[0]
            vm = VM(self.client, resource=vm_resource)
            return vm
        except Exception as exc:
            print(f"Error encountered in get_vm(), Error {exc}")
            return False

    def does_vapp_exist(self, vApp_name):
        try:
            self.vdc.reload()
            vApp = self.vdc.get_vapp(vApp_name)
            return True
        except EntityNotFoundException:
            return False
        except Exception as err:
            print(
                f"Error encountered in does_vapp_exist method(), Error : {err}")
            return False

    # C: CREATE
    def create_new_vApp(self, vapp_name, template, network='default_network_name',
                        catalog_name='default_catalog_name', storage_profile=None):
        try:
            vapp = self.vdc.instantiate_vapp(vapp_name, catalog=catalog_name, template=template,
                                             description=vapp_name, deploy=False, power_on=False)
            print(f"Instantiating vapp {vapp_name}....")
            print(
                f"Checking if the vapp {vapp_name} is successfully created or not......")
            time.sleep(30)
            if(self.does_vapp_exist(vapp_name)):
                print(f"Successfully created vApp: {vapp_name}")
                return True
            else:
                print(f"Couldn't create the vapp {vapp_name}")
                return False
        except Exception as err:
            print(f'Error encountered in create_new_vApp(), Error: {err}')
            return False

    # R : READ
    def get_vapp_ip_address(self, vapp_name):
        try:
            if(self.does_vapp_exist(vapp_name)):
                vapp = self.get_vapp(vapp_name)
                vm = self.get_vm(vapp_name)
                vm_dict = vm.general_setting_detail()
                vm_name = vm_dict.get('Name')
                return vapp.get_primary_ip(vm_name)
            else:
                return None
        except Exception as err:
            print(f"Error encountered in get_vapp_ip_address(), Error: {err}")
            return None

    # U: Update
    def update_vapp_cpu(self, vapp_name, virtual_cpus, cores_per_socket):
        try:
            vm = self.get_vm(vapp_name)
            print(f"Updating the cpu of vapp {vapp_name}...")
            task = vm.modify_cpu(virtual_cpus, cores_per_socket)
            print(f"Successfully updated the cpu of the vapp {vapp_name}")
            return True
        except Exception as err:
            print(f"Error encountered in update_vapp_cpu(), Error: {err}")
            return False

    # D : Delete
    def delete_vapp(self, vapp_name):
        try:
            print(f"Deleting the vApp {vapp_name}...")
            self.vdc.delete_vapp(vapp_name, force=True)
            print(f"Checking if the vApp {vapp_name} is deleted or not.....")
            time.sleep(30)
            if(self.does_vapp_exist(vapp_name)):
                print(f"Couldn't delete the vapp {vapp_name}")
                return False
            else:
                print(f"Successfully deleted the vApp with name {vapp_name}")
                return True
        except EntityNotFoundException:
            print(f"The vApp with the name {vapp_name} doesn't exist!")
            return True
        except MultipleRecordsException:
            print(f"More than one vApp with the name {vapp_name} exist")
            return False
        except Exception as err:
            print(f"Error encountered in delete_vapp() method, Error : {err}")
            return False

    def logout(self):
        print("ENTERING logout.....")
        self.client.logout()
        print("Successfully logged out")
