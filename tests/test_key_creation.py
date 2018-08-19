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

def test_key_creation(tmpdir, privateKeyName, publicKeyName, password, inputFile, usedEncoder):
    privateKeyLocation = str(tmpdir.join(privateKeyName))
    publicKeyLocation = str(tmpdir.join(publicKeyName))

    genKeys.generateKeyPair(privateKeyLocation, publicKeyLocation, password)

    loadedPublicKey = encrypt.readPublicKey(publicKeyLocation)
    loadedPrivateKey = decrypt.decryptKey(privateKeyLocation, password)

    assert isinstance(loadedPublicKey, public.PublicKey)

    assert isinstance(loadedPrivateKey, public.PrivateKey)
    assert isinstance(loadedPrivateKey.public_key, public.PublicKey)

    assert len(loadedPublicKey.encode(usedEncoder)) == 32
    assert len(loadedPrivateKey.encode(usedEncoder)) == 32
