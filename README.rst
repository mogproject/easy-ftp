========
Easy FTP
========

Super Simple FTP/SFTP Client.

.. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
   :target: http://choosealicense.com/licenses/apache-2.0/
   :alt: License

--------
Features
--------

**Easy FTP** automates the log-in process of FTP / SFTP with project-wise configurations.

**Easy FTP** best fits with you if you:

* need to regularly access to FTP/SFTP servers with the password authentication
* have several projects that require different IDs/passwords

------------
Dependencies
------------

* Python >= 3.6
* click
* pyyaml
* paramiko
* cryptography

------------
Installation
------------

1. Clone this repository
~~~~~~~~~~~~~~~~~~~~~~~~

::

    git clone git@github.com:mogproject/easy-ftp.git

or

::

    git clone https://github.com/mogproject/easy-ftp.git

2. Install module by ``pip``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    cd easy-ftp
    pip install .

``pip`` command may require ``sudo`` depending on your environment.

Make sure that ``easy-ftp`` command is installed on your operating system. (If you are using ``pyenv``, don't forget to run ``pyenv rehash``.)

::

    easy-ftp --version

3. Encrypt your password(s)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For the sake of security, **Easy FTP** avoids handling raw passwords. You must obtain encrypted passwords by the following command, or you will be prompted for the password each time.

::

    easy-ftp encrypt

Example output::

    password:    # Type your password here.
    [INFO] Created the encryption key: <KEY_PATH>
    [INFO] Encrypted your password. Copy and paste the following to your configuration file.

    pass: gAAAAABanBsDN0SeG7wCAGhpCn20Kbhj48aWTSayRL71cZ8iZ9Agso3kl_owVws5uUhgFV7pZTuYPENVDhXMnmjQCm3ZqbcrTA==

**Easy FTP** generates a randomized key file, whose default path is ``~/.easy-ftp.key``. You may specify the key path with ``--key`` option.

Remember encrypted passwords are **recoverable** with the key file. Protect the key file accordingly at your own risk.

4. Write your configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, you will be writing ``easy-ftp.yml`` in your project directory.

Example ``easy-ftp.yml``::

    host: ftp.example.com
    protocol: sftp
    port: 22
    user: exampleuser
    pass: gAAAAABanBsDN0SeG7wCAGhpCn20Kbhj48aWTSayRL71cZ8iZ9Agso3kl_owVws5uUhgFV7pZTuYPENVDhXMnmjQCm3ZqbcrTA==

+----------+----------+---------+----------------------------------------+
| Keyword  | Required | Default | Description                            |
+==========+==========+=========+========================================+
| host     | Yes      | --      | FTP/SFTP server to connect to          |
+----------+----------+---------+----------------------------------------+
| protocol | No       | sftp    | ``sftp`` or ``ftp``                    |
+----------+----------+---------+----------------------------------------+
| port     | No       | 22/21   | Port number to connect to              |
+----------+----------+---------+----------------------------------------+
| user     | Yes      | --      | User name to authenticate              |
+----------+----------+---------+----------------------------------------+
| pass     | No       | --      | Encrypted password to authenticate     |
+----------+----------+---------+----------------------------------------+

-----------
Lookup Path
-----------

Similar to `Vagrant <https://docs.vagrantup.com/v2/vagrantfile/>`_, when you run any ``easy-ftp`` command, Easy FTP climbs up the directory tree looking for the first ``easy-ftp.yml`` it can find, starting first in the current directory.
So if you run ``easy-ftp`` in ``/home/mogproject/projects/foo``, it will search the following paths in order for a ``easy-ftp.yml``, until it finds one:

::

    /home/mogproject/projects/foo/easy-ftp.yml
    /home/mogproject/projects/easy-ftp.yml
    /home/mogproject/easy-ftp.yml
    /home/easy-ftp.yml
    /easy-ftp.yml

This feature lets you run ``easy-ftp`` from any directory in your project.

-----------------
Command Reference
-----------------

Run ``easy-ftp --help`` and ``easy-ftp <COMMAND> --help`` for the details.

* ``easy-ftp ls``

Prints the list of files in the remote server.

* ``easy-ftp get``

Downloads remote files.

* ``easy-ftp put``

Uploads local files.

-------
Upgrade
-------

::

    pip install --upgrade .

--------------
Uninstallation
--------------

::

    pip uninstall easy-ftp

* Remove your key file (default: ``~/.easy-ftp.key``) and configuration files

