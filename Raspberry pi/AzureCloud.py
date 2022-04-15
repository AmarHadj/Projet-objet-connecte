# sudo python3 -m pip install --upgrade requests
# pip3 install azure-iot-device

import uuid
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message

class AzureCloud(object):
    def __init__(self):
        self.Conn_str = '''HostName=ObjetsConnectesHub.azure-devices.net;DeviceId=collect_info_tp2;SharedAccessKey=xFhtCxSHHW5DPoblCd0y1TTFJ9PXao4iL57QyCl4XbA='''
        self.Device_client = IoTHubDeviceClient.create_from_connection_string(self.Conn_str)
        
        try :
    # Connect the client.
            self.Device_client.connect()

            print('IoTHub Device Client Recurring Telemetry Sample')
            print('Press Ctrl+C to exit')
            try :
                # Connect the client.
                self.Device_client.connect()
            except KeyboardInterrupt:
                print('User initiated exit')
        except Exception:
            print('Unexpected exception!')
            raise
        finally:
            self.Device_client.shutdown()
            
    def send(self, message):
        
        msg = Message(message)
        msg.message_id = uuid.uuid4()
        msg.correlation_id = 'correlation-1234'
        #msg.custom_properties['tornado-warning'] = 'yes'
        msg.content_encoding = 'utf-8'
        msg.content_type = 'application/json'
        self.Device_client.send_message(msg)


    
# redue 'a la page 14