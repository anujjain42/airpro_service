import random
import string
import requests
from concurrent.futures import ThreadPoolExecutor
from generate_mac import generate_mac
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.template.response import TemplateResponse
from datasimulate.cloud_constants import Cloud
from .models import APDevice
# Register your models here.

def generate_serial_number(length):
    serial_number = 'AIRDUM_'+''.join(random.choices(string.digits + string.ascii_uppercase, k=length))
    return serial_number

def connect_cloud(sn, self, request):
    mac = generate_mac.total_random()
    obj = APDevice.objects.create(serial_number=sn, alias=sn, mac_address=mac)
    data = {'serial_number':sn, 'alias':sn, 'network':Cloud.NETWORK_ID}
    r = requests.post(Cloud.ADD_DEVICE_URL, json=data, headers=Cloud.HEADERS)
    data = {**Cloud.DEVICE_DATA,'serial_number':sn, 'mac_address':mac}
    r = requests.post(Cloud.CONNECT_DEVICE_URL, json=data)
    data_json = r.json()
    obj.client_topic = data_json['client_topic']
    obj.server_topic = data_json['server_topic']
    obj.broker_ip = data_json['broker_ip']
    obj.port = data_json['port']
    obj.save()
    print(r.json())
    self.message_user(request, f"Created **{obj.serial_number}** serial number on cloud",messages.SUCCESS)
    return redirect(reverse('admin:datasimulate_apdevice_changelist'))

@admin.register(APDevice)
class APDeviceAdmin(admin.ModelAdmin):
    change_list_template = 'custom_change_form.html'    
    
    def create_dummy_data(self, request):
        if request.method == 'POST':
            num_entries = int(request.POST.get('serial_number', 0))
            with ThreadPoolExecutor(max_workers=20, thread_name_prefix="create_dummy_data") as exe:
                _ = [exe.submit(connect_cloud, generate_serial_number(9), self, request) for _ in range(num_entries)]
            self.message_user(request, f"Created {num_entries} dummy data entries.",messages.SUCCESS)
            return redirect(reverse('admin:datasimulate_apdevice_changelist'))

        context = self.admin_site.each_context(request)
        return TemplateResponse(request, 'admin/create_dummy_data.html', context)
    
    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST' and request.POST.get('action') == 'create_dummy_data':
            return self.create_dummy_data(request)
        return super().changelist_view(request, extra_context=extra_context)

    list_display = ['__str__', 'client_topic', 'server_topic',  'broker_ip', ]
    
