import uuid
from azure.iot.device import IoTHubDeviceClient
from azure.iot.device import Message

class AzureCloud(object):
    def __init__(self):
        self.Conn_str = '''HostName=ObjetsConnectesHub.azure-devices.net;DeviceId=collect_info_tp2;SharedAccessKey=xFhtCxSHHW5DPoblCd0y1TTFJ9PXao4iL57QyCl4XbA='''
        self.Device_client = IoTHubDeviceClient.create_from_connection_string(self.Conn_str)

    def send(self, message):
        try:
            # Connect the client.
            self.Device_client.connect()

            # Send recurring telemetry
            print("J'envoit un message " + message)
            msg = Message(message)
            msg.message_id = uuid.uuid4()
            msg.correlation_id = 'correlation-1234'
            msg.content_encoding = 'utf-8'
            msg.content_type = 'application/json'
            self.Device_client.send_message(msg)

        except KeyboardInterrupt:
            print("User initiated exit")
        except Exception:
            print("Unexpected exception!")
            raise

