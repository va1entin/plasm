# PynacL AbStraction Module

Plasm is a simple [PyNaCl](https://github.com/pyca/pynacl) abstraction module to easily integrate file encryption into python projects. It makes key generation and file encryption/decryption very simple.
Plasm uses the sealedBox construct. The sealedBox uses key pairs of public and private keys. This allows encrypt using only a public key. That way the private key required for decryption can be stored in a safe place away from the machine that does the encryption. The private key is also encrypted itself using a password. This password is specified during the creation of the key pair. During decryption of a file encrypted with the public key, the private key is first decrypted using the password specified before it's creation and then used to decrypt the file.

If you are willing to dive deeper or want to customize more than what plasm allows to, feel free to check out [PyNaCl's documentation](https://pynacl.readthedocs.io/) and use it directly.

## Usage

### Generating keys:
```python
from plasm import genKeys

genKeys.generateKeyPair(privateKeyLocation, publicKeyLocation, password)
```

### Encrypting a file
* removeInputFile is optional and False by default.

```python
from plasm import encrypt

encrypt.encrypt(myFile, publicKeyLocation, removeInputFile=True)
```

### Encrypting all files in a directory:
* outfileExtension is optional and set to ".crypt" by default
* removeInputFile is optional and False by default.

```python
from plasm import encrypt

encrypt.encryptFilesInDir(directory, publicKeyLocation, outfileExtension=".crypt", removeInputFile=False):
```

### Decrypting a file:
```python
from plasm import decrypt

decrypt.decryptFile(encryptedFile, privateKeyLocation, password)
```

### Decrypting all files with a certain extension in a directory:
* infileExtension is optional and set to ".crypt" by default

```python
from plasm import decrypt

decrypt.decryptFilesInDir(directory, privateKeyLocation, password, infileExtension=".crypt"):
```

## Testing
plasm offers a test suite based on pytest.
To run all tests, move to the root directory of plasm and run pytest:

```
pytest
```

If you want a coverage report, use this command:

```
pytest --cov=plasm/ --cov-report term-missing -s tests
```
