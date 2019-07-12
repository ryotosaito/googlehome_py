from base64 import b64encode
from gtts import gTTS
from io import BytesIO
from pychromecast import get_chromecasts
import socket

def is_ip_addr(str):
    try:
        socket.inet_aton(str)
        return True
    except socket.error:
        try:
            socket.inet_pton(socket.AF_INET6, str)
            return True
        except socket.error:
            return False

class GoogleHome():
    devices = []

    def __init__(self, ip_or_name):
        if len(self.devices) == 0:
            self.get_devices()
        if is_ip_addr(ip_or_name):
            ip = ip_or_name
            filtered_devices = list(filter(lambda x: x.host == ip, devices))
        else:
            name = ip_or_name
            filtered_devices = list(filter(lambda x: x.device.friendly_name == name, devices))
        if len(devices) == 0:
            raise RuntimeError("Device named " + ip_or_name + " not found")
        self.dev = devices[0]

    @classmethod
    def get_devices(cls):
        cls.devices = get_chromecasts()

    def read_message(self, msg, lang):
        fp = BytesIO()
        gTTS(msg, lang=lang).write_to_fp(fp)
        fp.seek(0)
        mc = self.dev.media_controller
        mc.play_media('data:audio/mp3;base64,' + b64encode(fp.read()).decode('UTF-8'), 'audio/mp3')

