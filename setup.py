from setuptools import setup, find_packages

SRC_DIR = 'src'


def get_version():
    import sys

    sys.path[:0] = [SRC_DIR]
    return __import__('easy_ftp').__version__


setup(
    name='easy-ftp',
    python_requires='>=3.6.0',
    version=get_version(),
    description='Super Simple FTP/SFTP Client',
    author='mogproject',
    author_email='mogproj@gmail.com',
    url='https://github.com/mogproject/easy-ftp',
    install_requires=[
        'click',
        'pyyaml',
        'paramiko',
        'cryptography',
    ],
    tests_require=[
    ],
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR),
    include_package_data=True,
    test_suite='test',
    entry_points="""
    [console_scripts]
    easy-ftp = easy_ftp.easy_ftp:main
    """,
)
