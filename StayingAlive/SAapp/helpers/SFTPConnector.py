import os

import paramiko
from base64 import decodebytes

keydata = b"""AAAAC3NzaC1lZDI1NTE5AAAAIBXPxzSczLFKF/k0MrNfVAGJXrRcm74WydJti3cWo0Oj"""
key = paramiko.Ed25519Key(data=decodebytes(keydata))

class SFTPConnector:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.get_host_keys().add('[sandbox.bulme.at]:22', 'ssh-rsa', key)
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy)

        file = open("SAapp/helpers/config.txt")
        line = file.readline()
        self.data = line.split(",")
        file.close()

        self._hostname = self.data[0]
        self._port = self.data[1]
        self._username = self.data[2]
        self._password = self.data[3]
        self._serverlocation = self.data[4]

    def connect_to_server(self):
        try:
            self.client.connect(self._hostname, self._port, self._username, self._password)
            return self.client.open_sftp()
            
        except Exception as e:
            return e
    
    def upload_video(self, file_to_upload):
        file_only = file_to_upload.split("/")
        file_location_on_server = self._serverlocation + file_only[-1]
        
        sftp = self.connect_to_server()
        try:
            sftp.put(file_to_upload, file_location_on_server)
            sftp.close()
            return file_location_on_server

        except Exception as e:
            sftp.close()
            return e

    def get_video(self, path):
        sftp = self.connect_to_server()
        try:
            file_name = path.split('/')[-1]
            sftp.get(path, f"SAapp\\media\\{file_name}")
            sftp.close()
            return
        except Exception as e:
            sftp.close()
            raise Exception("Exercise not found")
            return e
