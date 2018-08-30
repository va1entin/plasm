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

from shutil import copytree

def test_dir_encrypted_decrypted(tmpdir, privateKeyName, publicKeyName, password, sampleFile, sampleFileBW, inputDir, inputFileHash, inputFileBWHash):
    privateKeyLocation = str(tmpdir.join(privateKeyName))
    publicKeyLocation = str(tmpdir.join(publicKeyName))

    tempDir = str(tmpdir.join('imgs'))

    copytree(inputDir, tempDir)

    genKeys.generateKeyPair(privateKeyLocation, publicKeyLocation, password)

    inputTempFile = os.path.join(tempDir, sampleFile)
    inputTempFileBW = os.path.join(tempDir, sampleFileBW)

    with open(inputTempFile, 'rb') as in_file:
        inputTempFileHash = hashlib.sha256(in_file.read()).hexdigest()

    with open(inputTempFileBW, 'rb') as in_file:
        inputTempFileBWHash = hashlib.sha256(in_file.read()).hexdigest()

    encrypt.encryptFilesInDir(tempDir, publicKeyLocation)

    encryptedTempFile = inputTempFile + '.crypt'
    encryptedTempFileBW = inputTempFileBW + '.crypt'

    assert os.path.isfile(encryptedTempFile)
    assert os.path.isfile(encryptedTempFileBW)

    os.remove(inputTempFile)
    os.remove(inputTempFileBW)
    assert not os.path.isfile(inputTempFile)
    assert not os.path.isfile(inputTempFileBW)

    decrypt.decryptFilesInDir(tempDir, privateKeyLocation, password)

    with open(inputTempFile, 'rb') as in_file:
        decryptedTempFileHash = hashlib.sha256(in_file.read()).hexdigest()
    with open(inputTempFileBW, 'rb') as in_file:
        decryptedTempFileBWHash = hashlib.sha256(in_file.read()).hexdigest()

    assert decryptedTempFileHash == inputFileHash
    assert decryptedTempFileBWHash == inputFileBWHash
