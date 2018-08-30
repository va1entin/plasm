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

from nacl import public
import os
import re
import glob

def test_key_creation_existing_keys(tmpdir, privateKeyName, publicKeyName, password, inputFile, usedEncoder):
    privateKeyLocation = str(tmpdir.join(privateKeyName))
    publicKeyLocation = str(tmpdir.join(publicKeyName))

    genKeys.generateKeyPair(privateKeyLocation, publicKeyLocation, password)

    genKeys.generateKeyPair(privateKeyLocation, publicKeyLocation, password)

    backupPrivateKeyLocation = privateKeyLocation + '_[0-9][0-9][0-9][0-9]-[0-2][0-9]-[0-3][0-9]_[0-2][0-9]-[0-5][0-9]-[0-5][0-9]'
    backupPublicKeyLocation = publicKeyLocation + '_[0-9][0-9][0-9][0-9]-[0-2][0-9]-[0-3][0-9]_[0-2][0-9]-[0-5][0-9]-[0-5][0-9]'
    backupPrivateKeyLocation = glob.glob(backupPrivateKeyLocation)[0]
    backupPublicKeyLocation = glob.glob(backupPublicKeyLocation)[0]

    loadedPrivateKey = decrypt.decryptKey(privateKeyLocation, password)
    loadedPublicKey = encrypt.readPublicKey(publicKeyLocation)

    assert isinstance(loadedPublicKey, public.PublicKey)

    assert isinstance(loadedPrivateKey, public.PrivateKey)
    assert isinstance(loadedPrivateKey.public_key, public.PublicKey)

    assert len(loadedPublicKey.encode(usedEncoder)) == 32
    assert len(loadedPrivateKey.encode(usedEncoder)) == 32


    loadedPrivateKey = decrypt.decryptKey(backupPrivateKeyLocation, password)
    loadedPublicKey = encrypt.readPublicKey(backupPublicKeyLocation)

    assert isinstance(loadedPublicKey, public.PublicKey)

    assert isinstance(loadedPrivateKey, public.PrivateKey)
    assert isinstance(loadedPrivateKey.public_key, public.PublicKey)

    assert len(loadedPublicKey.encode(usedEncoder)) == 32
    assert len(loadedPrivateKey.encode(usedEncoder)) == 32
