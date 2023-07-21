from typing import List, Dict
from datetime import datetime

class Cloud:
    CONNECT_DEVICE_URL = 'http://122.170.105.253:8080/api/devices/'
    NETWORK_ID = "1b01ac37-c873-4b97-9b6b-5f018de9fc4e"
    ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwNjYwODU5LCJpYXQiOjE2ODkxMjQ4NTksImp0aSI6ImM3N2M0YzgxMTY5ZDQ2MTc4YTAzYTNjOTBjZDRhODI0IiwidXNlcl9pZCI6M30.qOo8BUfu-XKcTQEB6dlz04QFyTwmxGruVfnX6SlJbrA'
    ADD_DEVICE_URL = 'http://122.170.105.253:8080/device/'
    HEADERS = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    DEVICE_DATA = {'type':6,'alpn':2.5}


def create_publish_format(msg_type: int, mac_add: str, device_id: str,data: List) -> Dict:
    
    timestamp = int(round(datetime.now().timestamp()))
    return {
        "type": msg_type,
        "flag": "REQ",
        "ver": 1,
        "timestamp": timestamp,
        "macaddr": mac_add,
        "device_id": device_id,
        "data": data
    }