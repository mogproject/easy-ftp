import sys
import click
from easy_ftp.setting import Setting
from easy_ftp import _print_version, VERSION_HELP, _command_wrapper


@click.group()
@click.option('--version', is_flag=True, callback=_print_version, expose_value=False, is_eager=True, help=VERSION_HELP)
def main():
    """
    Main function
    """


@main.command('ls')
@click.option('--config', type=str, metavar='PATH', default=None, help='Use the specific configuration file.')
@click.option('--key', type=str, metavar='PATH', default=None, help='Use the specific encryption key.')
@click.option('--debug', flag_value=True, default=False, help="Print the stack trace of the Exception.")
def ftp_list(config, key, debug):
    _command_wrapper(_ftp_list_impl, debug, config, key)


def _ftp_list_impl(config, key):
    print(Setting(config, key).lookup_config().load_config().decrypt_password())


@main.command('get')
def ftp_get():
    pass


@main.command('put')
def ftp_put():
    pass


@main.command('encrypt')
@click.option('--key', type=str, metavar='PATH', default=None, help='Use the specific encryption key.')
@click.option('--debug', flag_value=True, default=False, help="Print the stack trace of the Exception.")
def encrypt(key, debug):
    _command_wrapper(lambda key: Setting(encrypt_key_path=key).encrypt_password(), debug, key)
