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
import hashlib
import os
from shutil import copy

def test_file_encrypted_decrypted(tmpdir, custom_outfile_extension, input_file, input_file_hash, private_key_name, public_key_name, password, sample_file):
    private_key_location = str(tmpdir.join(private_key_name))
    public_key_location = str(tmpdir.join(public_key_name))

    copy(input_file, str(tmpdir))
    input_temp_file = str(tmpdir.join(sample_file))
    custom_encrypted_temp_file = str(tmpdir.join(sample_file + custom_outfile_extension))
    encrypted_temp_file = str(tmpdir.join(sample_file + '.crypt'))

    with open(input_temp_file, 'rb') as in_file:
        input_temp_file_hash = hashlib.sha256(in_file.read()).hexdigest()

    gen_keys.generate_key_pair(private_key_location, public_key_location, password)

#just encrypt file
    encrypt.encrypt_file(input_temp_file, public_key_location)

    assert os.path.isfile(input_temp_file)
    os.remove(encrypted_temp_file)

#custom outfile
    encrypt.encrypt_file(input_temp_file, public_key_location, outfile_extension=custom_outfile_extension)

    with open(custom_encrypted_temp_file, 'rb') as in_file:
        custom_encrypted_temp_file_hash = hashlib.sha256(in_file.read()).hexdigest()

    assert custom_encrypted_temp_file_hash != input_file_hash
    assert os.path.isfile(input_temp_file)
    os.remove(custom_encrypted_temp_file)

#encrypt and remove input file
    encrypt.encrypt_file(input_temp_file, public_key_location, remove_input_file=True)

    assert not os.path.isfile(input_temp_file)

    with open(encrypted_temp_file, 'rb') as in_file:
        encrypted_temp_file_hash = hashlib.sha256(in_file.read()).hexdigest()

    assert input_temp_file_hash == input_file_hash
    assert encrypted_temp_file != input_file_hash

#decrypt file
    decrypt.decrypt_file(encrypted_temp_file, private_key_location, password)

    with open(input_temp_file, 'rb') as in_file:
        decrypted_temp_file_hash = hashlib.sha256(in_file.read()).hexdigest()

    assert decrypted_temp_file_hash == input_file_hash
