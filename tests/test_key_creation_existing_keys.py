#!/usr/bin/env python
# Copyright 2018-2020 Valentin Heidelberger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from plasm import gen_keys
from plasm import encrypt
from plasm import decrypt

from nacl import public
import os
import re
import glob

def test_key_creation_existing_keys(tmpdir, private_key_name, public_key_name, password, used_encoder):
    private_key_location = str(tmpdir.join(private_key_name))
    public_key_location = str(tmpdir.join(public_key_name))

    gen_keys.generate_key_pair(private_key_location, public_key_location, password)

    gen_keys.generate_key_pair(private_key_location, public_key_location, password)

    backup_private_key_location = private_key_location + '_[0-9][0-9][0-9][0-9]-[0-2][0-9]-[0-3][0-9]_[0-2][0-9]-[0-5][0-9]-[0-5][0-9]'
    backup_public_key_location = public_key_location + '_[0-9][0-9][0-9][0-9]-[0-2][0-9]-[0-3][0-9]_[0-2][0-9]-[0-5][0-9]-[0-5][0-9]'
    backup_private_key_location = glob.glob(backup_private_key_location)[0]
    backup_public_key_location = glob.glob(backup_public_key_location)[0]

    loaded_private_key = decrypt.decrypt_key(private_key_location, password)
    loaded_public_key = encrypt.read_public_key(public_key_location)

    assert isinstance(loaded_public_key, public.PublicKey)

    assert isinstance(loaded_private_key, public.PrivateKey)
    assert isinstance(loaded_private_key.public_key, public.PublicKey)

    assert len(loaded_public_key.encode(used_encoder)) == 32
    assert len(loaded_private_key.encode(used_encoder)) == 32


    loaded_private_key = decrypt.decrypt_key(backup_private_key_location, password)
    loaded_public_key = encrypt.read_public_key(backup_public_key_location)

    assert isinstance(loaded_public_key, public.PublicKey)

    assert isinstance(loaded_private_key, public.PrivateKey)
    assert isinstance(loaded_private_key.public_key, public.PublicKey)

    assert len(loaded_public_key.encode(used_encoder)) == 32
    assert len(loaded_private_key.encode(used_encoder)) == 32
