import sys
import click
from pathlib import Path
from easy_ftp.setting import Setting
from easy_ftp import _print_version, VERSION_HELP, _command_wrapper


@click.group()
@click.option('--version', is_flag=True, callback=_print_version, expose_value=False, is_eager=True, help=VERSION_HELP)
def main():
    """
    Super Simple FTP/SFTP Client

    Type `easy-ftp COMMAND --help` for more information.
    """


@main.command('ls')
@click.argument('remote_path', nargs=-1)
@click.option('--config', type=str, metavar='PATH', default=None, help='Use the specific configuration file.')
@click.option('--key', type=str, metavar='PATH', default=None, help='Use the specific encryption key.')
@click.option('--debug', flag_value=True, default=False, help="Print the stack trace of the Exception.")
def ftp_list(remote_path, config, key, debug):
    """
    Prints the list of files in the remote server.

    @param remote_path: list of paths to get information
    """
    _command_wrapper(_ftp_list_impl, debug, config, key, remote_path)


def _ftp_list_impl(config, key, remote_path):
    exec = Setting(config, key).lookup_config().load_config().decrypt_password().get_executor()
    if not remote_path:
        remote_path = ['.']
    for p in remote_path:
        for ls in exec.listdir(p):
            print(ls)
    exec.close()


@main.command('get')
@click.argument('remote_path', nargs=-1)
@click.option('--config', type=str, metavar='PATH', default=None, help='Use the specific configuration file.')
@click.option('--key', type=str, metavar='PATH', default=None, help='Use the specific encryption key.')
@click.option('--debug', flag_value=True, default=False, help="Print the stack trace of the Exception.")
def ftp_get(remote_path, config, key, debug):
    """
    Downloads remote files.

    @param remote_path: list of remote file paths to download.
    If the last argument is an existing local directory, it will be interpreted as the local destination.
    """
    _command_wrapper(_ftp_get_impl, debug, config, key, remote_path)


def _ftp_get_impl(config, key, remote_path):
    exec = Setting(config, key).lookup_config().load_config().decrypt_password().get_executor()

    # check if the local dir is specified
    local_dir = Path()
    if len(remote_path) > 1 and Path(remote_path[-1]).is_dir():
        local_dir = Path(remote_path[-1])
        remote_path = remote_path[:-1]

    for p in remote_path:
        exec.get(p, local_dir / Path(p).name)
    exec.close()


@main.command('put')
@click.argument('local_path', nargs=-1)
@click.option('--config', type=str, metavar='PATH', default=None, help='Use the specific configuration file.')
@click.option('--key', type=str, metavar='PATH', default=None, help='Use the specific encryption key.')
@click.option('--debug', flag_value=True, default=False, help="Print the stack trace of the Exception.")
def ftp_put(local_path, config, key, debug):
    """
    Uploads local files.

    @param local_path: list of local file paths to upload.
    If the last argument ends with '/', it will be interpreted as the remote destination.
    """
    _command_wrapper(_ftp_put_impl, debug, config, key, local_path)


def _ftp_put_impl(config, key, local_path):
    exec = Setting(config, key).lookup_config().load_config().decrypt_password().get_executor()

    # check if the remote dir is specified
    remote_dir = Path()
    if len(local_path) > 1 and local_path[-1].endswith('/'):
        remote_dir = Path(local_path[-1])
        local_path = local_path[:-1]

    for p in local_path:
        exec.put(p, str(remote_dir / Path(p).name))
    exec.close()


@main.command('encrypt')
@click.option('--key', type=str, metavar='PATH', default=None, help='Use the specific encryption key.')
@click.option('--debug', flag_value=True, default=False, help="Print the stack trace of the Exception.")
def encrypt(key, debug):
    """
    Encrypts a password.

    A key file will be generated if it does not exist. You will be prompted for a password.
    """
    _command_wrapper(lambda key: Setting(encrypt_key_path=key).encrypt_password(), debug, key)
