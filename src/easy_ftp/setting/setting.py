from easy_ftp.util import CaseClass
from pathlib import Path
import yaml
import getpass
import os
from cryptography.fernet import Fernet
from easy_ftp.executor import SFTPExecutor

KEYWORD_SFTP = 'sftp'
KEYWORD_FTP = 'ftp'
DEFAULT_SFTP_PORT = 22
DEFAULT_FTP_PORT = 21
DEFAULT_CONFIG_NAME = 'easy-ftp.yml'
DEFAULT_KEY_NAME = '.easy-ftp.key'


class Setting(CaseClass):
    """
    Manages all settings.
    """

    def __init__(self, config_path=None, encrypt_key_path=None, host=None, protocol=None, port=None, user=None, encrypted_password=None, decrypted_password=None):
        # set default encrypt key path
        if encrypt_key_path is None:
            encrypt_key_path = str(Path.home() / DEFAULT_KEY_NAME)

        CaseClass.__init__(self, config_path=config_path, encrypt_key_path=encrypt_key_path, host=host, protocol=protocol,
                           port=port, user=user, encrypted_password=encrypted_password, decrypted_password=decrypted_password)

    def load_config(self):
        config = yaml.load(open(self.config_path).read())
        assert isinstance(config, dict), 'Format error: %s' % self.config_path
        assert 'host' in config, 'Missing required entry `host`: %s' % self.config_path
        assert 'user' in config, 'Missing required entry `user`: %s' % self.config_path
        protocol = str(config.get('protocol')) or KEYWORD_SFTP
        port = config.get('port')
        if port is None:
            if protocol == KEYWORD_SFTP:
                port = DEFAULT_SFTP_PORT
            elif protocol == KEYWORD_FTP:
                port = DEFAULT_FTP_PORT
            else:
                assert False, 'Unknown protocol: %s: %s' % (protocol, self.config_path)

        return self.copy(host=config['host'], protocol=config['protocol'], port=port, user=config['user'], encrypted_password=config.get('pass'))

    def decrypt_password(self):
        if self.decrypted_password is not None:
            return self

        decrypted = ''
        if self.encrypted_password is None or self.encrypt_key_path is None or not Path(self.encrypt_key_path).exists():
            if self.encrypt_key_path is not None:
                print('[WARN] Could not find the encryption key: %s' % self.encrypt_key_path)
            decrypted = getpass.getpass()
        else:
            with Path(self.encrypt_key_path).open('rb') as input:
                decrypted = Fernet(input.read()).decrypt(self.encrypted_password.encode())
        return self.copy(decrypted_password=decrypted)

    def lookup_config(self):
        if self.config_path is not None:
            return self

        d = Path.cwd()
        path = ''
        while True:
            path = d / DEFAULT_CONFIG_NAME
            if path.exists():
                break
            nd = d.parent
            if d == nd:
                assert False, 'Counld not find the configuration file.'
            d = nd

        return self.copy(config_path=str(path))

    def encrypt_password(self):
        assert self.encrypt_key_path is not None

        s = getpass.getpass()
        path = Path(self.encrypt_key_path)
        key = b''
        if path.exists():
            with Path(self.encrypt_key_path).open('rb') as input:
                key = input.read()
        else:
            # create key file
            os.umask(0o377)
            with path.open('wb') as output:
                key = Fernet.generate_key()
                output.write(key)
            print('[INFO] Created the encryption key: %s' % self.encrypt_key_path)

        encrypted = Fernet(key).encrypt(s.encode())

        print('[INFO] Encrypted your password. Copy and paste the following to your configuration file.')
        print('\npass: %s\n' % encrypted.decode())
        return self

    def get_executor(self):
        if self.protocol == 'sftp':
            return SFTPExecutor(self.host, self.port, self.user, self.decrypted_password)
        assert False, 'Unknown protocol: %s' % self.protocol

    def __str__(self):
        s = self.copy(decrypted_password='******')
        return CaseClass.__str__(s)
