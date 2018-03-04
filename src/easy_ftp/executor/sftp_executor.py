import sys
import paramiko


class SFTPExecutor():
    def __init__(self, host, port, username, password):
        assert host is not None
        assert port is not None
        assert username is not None
        assert password is not None

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print('[INFO] Connecting to %s@%s:%s...' % (username, host, port))
        ssh.connect(host, port, username, password)
        sftp = ssh.open_sftp()

        self.host = host
        self.ssh = ssh
        self.sftp = sftp

    def listdir(self, path):
        print('[INFO] Listing remote directory: %s' % path)
        return sorted(self.sftp.listdir_attr(path), key=lambda a: a.filename)

    def get(self, remote_path, local_path):
        print('[INFO] Downloading: %s:%s -> %s' % (self.host, remote_path, local_path))
        self.sftp.get(remote_path, local_path, self.__print_progress)
        print()

    def put(self, local_path, remote_path):
        print('[INFO] Uploading: %s -> %s:%s' % (local_path, self.host, remote_path))
        self.sftp.put(local_path, remote_path, self.__print_progress, confirm=True)
        print()

    @staticmethod
    def __print_progress(transferred_bytes, total_bytes):
        sys.stdout.write('\r[INFO] Transferring... [%d / %d] (%d%%)' %
                         (transferred_bytes, total_bytes, transferred_bytes * 100 // total_bytes))

    def close(self):
        self.sftp.close()
        self.ssh.close()
