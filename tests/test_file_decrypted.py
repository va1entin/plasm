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
import os

from shutil import copy
from PIL import Image

def test_file_decrypted(tmpdir, privateKeyName, publicKeyName, password, sampleFile, inputFile):
    privateKeyLocation = str(tmpdir.join(privateKeyName))
    publicKeyLocation = str(tmpdir.join(publicKeyName))

    copy(inputFile, str(tmpdir))
    inputTempFile = str(tmpdir.join(sampleFile))

    genKeys.generateKeyPair(privateKeyLocation, publicKeyLocation, password)

    encrypt.encrypt(inputTempFile, publicKeyLocation)

    encryptedTempFile = str(tmpdir.join(sampleFile + '.crypt'))

    os.remove(inputTempFile)
    assert not os.path.isfile(inputTempFile)

    decrypt.decryptFile(encryptedTempFile, privateKeyLocation, password)

    assert Image.open(inputTempFile)
