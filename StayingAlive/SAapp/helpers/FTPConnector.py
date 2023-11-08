import paramiko

class FTPConnector:
    def __init__(self, hostname, port, username, password):
        self.client = paramiko.SSHClient()
        self.client.load_host_keys()
        self.client.set_missing_host_key_policy(paramiko.RejectPolicy)

        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password


    def connect_to_server(self):
        try:
            self.client.connect(self._hostname, self._port, self._username, self._password)
            return self.client.open_sftp()
            
        except Exception as e:
            return e
    
    def generate_path_for_video(self):
        file_location_on_server = "/StayingAlive/test.mp4"
        return file_location_on_server
    

    def upload_video(self, file_to_upload):
        file_location_on_server = self.generate_path_for_video()

        sftp = self.connect_to_server()
        try:
            sftp.put(file_to_upload, file_location_on_server)
            sftp.close()

        except Exception as e:
            sftp.close()
            return e
        

upload_current_video = FTPConnector(hostname="schueler.bulme.at", port="22", username="florentin.aldrian", password="ThBlum3Cod3")
upload_current_video.upload_video(file_to_upload="/test.mp4")