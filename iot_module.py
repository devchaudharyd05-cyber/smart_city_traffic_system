# iot_module.py
# Simulates IoT traffic sensors placed at major Delhi NCR junctions

import random

def get_traffic_data():

    traffic_data = {

        "Connaught Place": random.randint(20,80),

        "AIIMS Ring Road": random.randint(20,80),

        "Noida Sector 62": random.randint(20,80),

        "Gurgaon Cyber City": random.randint(20,80)

    }

    return traffic_data