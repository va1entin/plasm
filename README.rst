PynacL AbStraction Module
=========================

Plasm is a simple `PyNaCl <https://github.com/pyca/pynacl>`__
abstraction module to easily integrate file encryption into python
projects. It makes key generation and file encryption/decryption very
simple. Plasm uses the sealedBox construct. The sealedBox uses key pairs
of public and private keys. This allows encrypt using only a public key.
That way the private key required for decryption can be stored in a safe
place away from the machine that does the encryption. The private key is
also encrypted itself using a password. This password is specified
during the creation of the key pair. During decryption of a file
encrypted with the public key, the private key is first decrypted using
the password specified before it’s creation and then used to decrypt the
file.

If you are willing to dive deeper or want to customize more than what
plasm allows to, feel free to check out `PyNaCl’s
documentation <https://pynacl.readthedocs.io/>`__ and use it directly.

Usage
-----

Non-interactive
~~~~~~~~~~~~~~~

Generating keys:
^^^^^^^^^^^^^^^^

.. code:: python

    from plasm import genKeys

    genKeys.generateKeyPair(privateKeyLocation, publicKeyLocation, password)

Encrypting a file
^^^^^^^^^^^^^^^^^

-  removeInputFile is optional and False by default.

.. code:: python

    from plasm import encrypt

    encrypt.encrypt(myFile, publicKeyLocation, removeInputFile=True)

Decrypting a file:
^^^^^^^^^^^^^^^^^^

.. code:: python

    from plasm import decrypt

    decrypt.decryptFile(encryptedFile, privateKeyLocation, password)

Decrypting all files ending with “.crypt” in a directory:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from plasm import decrypt

    decrypt.decryptFilesInDir(dir, privateKeyLocation, password)

Interactive
~~~~~~~~~~~

Generating keys:

::

    genKeys.py -h
    usage: genKeys.py [-h] [--memlimit int] [--directory /etc/plasm]

    optional arguments:
      -h, --help            show this help message and exit
      --memlimit int        Maximum amount of memory in bytes to use for key
                            encryption, minimum 8192
      --directory /etc/plasm
                            Directory to write keys to

Encrypting a file:

::

    usage: encrypt.py [-h] --key /path/to/public.key [--directory /path/to/files]
                      [--file /path/to/file] [--removeInputFile]

    optional arguments:
      -h, --help            show this help message and exit
      --key /path/to/public.key
                            Public key to use
      --directory /path/to/files
                            Encrypt all files in this directory
      --file /path/to/file  Encrypt only the specified file
      --removeInputFile     Remove input file(s) after encryption

Decrypting a file/dir:

::

    usage: decrypt.py [-h] --key /path/to/private.key [--dir /path/to/files.crypt]
                      [--file /path/to/file.crypt]

    optional arguments:
      -h, --help            show this help message and exit
      --key /path/to/private.key
                            Private key to use
      --dir /path/to/files.crypt
                            Decrypt all files ending with .crypt in this directory
      --file /path/to/file.crypt
                            Decrypt only the specified file
