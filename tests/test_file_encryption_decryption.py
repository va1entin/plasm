#!/usr/bin/env python
# This file is part of Plasm.
#
# Plasm is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from plasm import genKeys
from plasm import encrypt
from plasm import decrypt
import hashlib
import os

from shutil import copy

def test_file_encrypted_decrypted(tmpdir, privateKeyName, publicKeyName, password, sampleFile, inputFile, inputFileHash):
    privateKeyLocation = str(tmpdir.join(privateKeyName))
    publicKeyLocation = str(tmpdir.join(publicKeyName))

    copy(inputFile, str(tmpdir))
    inputTempFile = str(tmpdir.join(sampleFile))
    customOutfileExtension = '.foobar'
    customEncryptedTempFile = str(tmpdir.join(sampleFile + customOutfileExtension))
    encryptedTempFile = str(tmpdir.join(sampleFile + '.crypt'))

    with open(inputTempFile, 'rb') as in_file:
        inputTempFileHash = hashlib.sha256(in_file.read()).hexdigest()

    genKeys.generateKeyPair(privateKeyLocation, publicKeyLocation, password)

#just encrypt file
    encrypt.encrypt(inputTempFile, publicKeyLocation)

    assert os.path.isfile(inputTempFile)
    os.remove(encryptedTempFile)

#custom outfile
    encrypt.encrypt(inputTempFile, publicKeyLocation, outfileExtension=customOutfileExtension)

    with open(customEncryptedTempFile, 'rb') as in_file:
        customEncryptedTempFileHash = hashlib.sha256(in_file.read()).hexdigest()

    assert customEncryptedTempFileHash != inputFileHash
    assert os.path.isfile(inputTempFile)
    os.remove(customEncryptedTempFile)

#encrypt and remove input file
    encrypt.encrypt(inputTempFile, publicKeyLocation, removeInputFile=True)

    assert not os.path.isfile(inputTempFile)

    with open(encryptedTempFile, 'rb') as in_file:
        encryptedTempFileHash = hashlib.sha256(in_file.read()).hexdigest()

    assert inputTempFileHash == inputFileHash
    assert encryptedTempFile != inputFileHash

#decrypt file
    decrypt.decryptFile(encryptedTempFile, privateKeyLocation, password)

    with open(inputTempFile, 'rb') as in_file:
        decryptedTempFileHash = hashlib.sha256(in_file.read()).hexdigest()

    assert decryptedTempFileHash == inputFileHash
