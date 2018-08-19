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

from shutil import copytree
from PIL import Image

def test_dir_decrypted(tmpdir, privateKeyName, publicKeyName, password, sampleFile, sampleFileBW, inputDir):
    privateKeyLocation = str(tmpdir.join(privateKeyName))
    publicKeyLocation = str(tmpdir.join(publicKeyName))

    tempDir = str(tmpdir.join('imgs'))

    copytree(inputDir, tempDir)

    genKeys.generateKeyPair(privateKeyLocation, publicKeyLocation, password)

    inputTempFile = os.path.join(tempDir, sampleFile)
    inputTempFileBW = os.path.join(tempDir, sampleFileBW)

    encrypt.encrypt(inputTempFile, publicKeyLocation)
    encrypt.encrypt(inputTempFileBW, publicKeyLocation)

    encryptedTempFile = str(tmpdir.join(tempDir, sampleFile, '.crypt'))
    encryptedTempFileBW = str(tmpdir.join(tempDir, sampleFileBW, '.crypt'))

    os.remove(inputTempFile)
    os.remove(inputTempFileBW)
    assert not os.path.isfile(inputTempFile)
    assert not os.path.isfile(inputTempFileBW)

    decrypt.decryptFilesInDir(tempDir, privateKeyLocation, password)

    assert Image.open(inputTempFile)
    assert Image.open(inputTempFileBW)
