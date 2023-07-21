import random, json
from threading import current_thread
import paho.mqtt.client as paho
from concurrent.futures import ThreadPoolExecutor

from django.utils import timezone
from django.utils.timezone import datetime, make_aware, get_current_timezone
from datasimulate.cloud_constants import create_publish_format
from publish_data.models import CloudPublishData
from datasimulate.models import APDevice
from datatransform.models import PublishData
from celery import shared_task

# Create your views here.

def get_publish_data(device_data:APDevice):
    data = sorted(PublishData.objects.all(), key=lambda x: random.random())[:1]
    publish_data = create_publish_format(data[0].msg_type, device_data.mac_address, int(device_data.client_topic.split("/")[-1]),data[0].data)
    paho.Client.connected_flag = False
    paho.Client.bad_connection_flag = False
    publisher = paho.Client("PUBLISHER")
    print(current_thread().name, data[0].msg_type)
    publisher.connect(device_data.broker_ip,device_data.port)
    publisher.publish("airpro/dev/to/cloud",json.dumps(publish_data)) 
    data = {
        "msg_type":data[0].msg_type,
        "mac_address":device_data.mac_address,
        "device_id":publish_data['device_id'],
        "data":publish_data
    }
    CloudPublishData.objects.create(**data)   


@shared_task(name="publish_data")
def publish_data():
    with ThreadPoolExecutor(max_workers=20, thread_name_prefix="publish_data") as exe:
        _ = [exe.submit(get_publish_data, data) for data in APDevice.objects.all()]


def delete_tmp_data():
    yesterday = timezone.now() - timezone.timedelta(1)
    end_of_day = make_aware(datetime.combine(yesterday, datetime.max.time()),get_current_timezone())
    CloudPublishData.objects.filter(updated_time__lte=end_of_day).delete()
