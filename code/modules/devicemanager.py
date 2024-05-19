from modules.device import Device

class DeviceManager:
    def __init__(self):
        self.devices = {}
        self.device_list = []
        self.linked_ids = dict()

    def create_device(self,bluetooth_id,wifi_id,lte_id):
        device: Device
        for device in self.device_list:
            # Get the Bluetooth ID once and check it
            bluetooth_id_device = getattr(device, 'bluetooth_id', None)
            flag = bluetooth_id_device is not None and bluetooth_id_device == bluetooth_id

            # Get the WiFi ID once and check it
            wifi_id_device = getattr(device, 'wifi_id', None)
            flag1 = wifi_id_device is not None and wifi_id_device == wifi_id

            # Get the LTE ID once and check it
            lte_id_device = getattr(device, 'lte_id', None)
            flag2 = lte_id_device is not None and lte_id_device == lte_id
                
            if flag==1 or flag1==1 or flag2==1:
                self.update_device(device,bluetooth_id,wifi_id,lte_id)  
                return
                
        new_device = Device(bluetooth_id,wifi_id,lte_id)
        self.device_list.append(new_device)

    def update_device(self,device: Device,bluetooth_id,wifi_id,lte_id):
        
        if bluetooth_id is not None and device.bluetooth_id!=bluetooth_id:
            self.linked_ids[device.bluetooth_id]=bluetooth_id
            device.bluetooth_id = bluetooth_id
            
        if wifi_id is not None and device.wifi_id!=wifi_id:
            self.linked_ids[device.wifi_id]=wifi_id
            device.wifi_id = wifi_id
            
        if lte_id is not None and device.lte_id!=lte_id:
            self.linked_ids[device.lte_id]=lte_id
            device.lte_id = lte_id
        
        
        
    def linking_id(self,protocol,old_id,new_id):
        # print("link device")
        device: Device
        for device in self.device_list:
            if protocol=='Bluetooth':
                if getattr(device,'bluetooth_id') == old_id:
                    device.bluetooth_id = new_id
                    if old_id in self.linked_ids:
                        self.linked_ids[old_id]=new_id
            if protocol=='WiFi':
                if getattr(device,'wifi_id') == old_id:
                    
                    device.wifi_id=new_id
                    if old_id in self.linked_ids:
                        self.linked_ids[old_id]=new_id
            if protocol=='LTE':
                if getattr(device,'lte_id') == old_id:
                    device.lte_id=new_id
                    if old_id in self.linked_ids:
                        self.linked_ids[old_id]=new_id
                      
        # return self.linked_ids
