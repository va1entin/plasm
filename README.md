# PynacL AbStraction Module

Plasm is a simple [PyNaCl](https://github.com/pyca/pynacl) abstraction module to easily integrate file encryption into python projects. It makes key generation and file encryption/decryption very simple.
If you are willing to dive deeper or want to customize more than what plasm allows to, feel free to check out [PyNaCl's documentation](https://pynacl.readthedocs.io/) and use it directly.

## Usage
### Non-interactive

Generating keys:
```python
import plasm

plasm.genKeys.generateKeyPair()
```

Encrypting a file:
```python
import plasm

plasm.encrypt.encrypt(myFile)
```

Decrypting a file:
```python
import plasm

plasm.decrypt.decrypt(myFile)
```

Decrypting all files ending with ".crypt" in a directory:
```python
import plasm

plasm.decrypt.decryptFilesInDir(tempDir, privateKeyLocation, password)
```

### Interactive

Generating keys:
```
genKeys.py -h
usage: genKeys.py [-h] [--memlimit int] [--directory /etc/plasm]

optional arguments:
  -h, --help            show this help message and exit
  --memlimit int        Maximum amount of memory in bytes to use for key
                        encryption, minimum 8192
  --directory /etc/plasm
                        Directory to write keys to
```

Encrypting a file:
```
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
```

Decrypting a file/dir:
```
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
```
