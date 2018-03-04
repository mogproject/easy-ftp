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

        self.ssh = ssh
        self.sftp = sftp

    def listdir(self, path='.'):
        print('[INFO] Listing remote directory: %s' % path)
        return sorted(self.sftp.listdir_attr(path), key=lambda a: a.filename)

    def close(self):
        self.sftp.close()
        self.ssh.close()
