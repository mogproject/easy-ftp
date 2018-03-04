import os
import sys

__version__ = '0.0.1'


#
# Constants
#
VERSION_HELP = "Show program's version number and exit."


#
# Utility Functions
#
__program_name = os.path.basename(sys.argv[0])


def _print_version(ctx, param, value):
    import click
    if not value or ctx.resilient_parsing:
        return
    click.echo('%s %s' % (__program_name, __version__))
    ctx.exit()


def _command_wrapper(main_impl, debug, *args):
    try:
        main_impl(*args)
    except Exception as e:
        # raise errors when debugging
        if debug:
            raise e

        # print errors
        print('%s: %s' % (e.__class__.__name__, e))
