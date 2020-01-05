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

from shutil import copytree

def test_dir_encrypted_decrypted(tmpdir, private_key_name, public_key_name, password, sample_file, sample_file_bw, input_dir, input_file_hash, input_file_bw_hash):
#set key locations, temp paths and copy img files
    private_key_location = str(tmpdir.join(private_key_name))
    public_key_location = str(tmpdir.join(public_key_name))

    temp_dir = str(tmpdir.join('imgs'))

    copytree(input_dir, temp_dir)

    input_temp_file = os.path.join(temp_dir, sample_file)
    input_temp_file_bw = os.path.join(temp_dir, sample_file_bw)
    encrypted_temp_file_foo = input_temp_file + '.foobar'
    encrypted_temp_file_bw_foo = input_temp_file_bw + '.foobar'
    encrypted_femp_file = input_temp_file + '.crypt'
    encrypted_femp_file_bw = input_temp_file_bw + '.crypt'

#generate keys
    gen_keys.generate_key_pair(private_key_location, public_key_location, password)

#encrypt files with .foobar
    encrypt.encrypt_files_in_dir(temp_dir, public_key_location, outfile_extension=".foobar", remove_input_file=False)

    assert os.path.isfile(encrypted_temp_file_foo)
    assert os.path.isfile(encrypted_temp_file_bw_foo)

#encrypt files with .crypt
    encrypt.encrypt_files_in_dir(temp_dir, public_key_location, remove_input_file=True)

    assert os.path.isfile(encrypted_femp_file)
    assert os.path.isfile(encrypted_femp_file_bw)

#decrypt files with .crypt
    decrypt.decrypt_files_in_dir(temp_dir, private_key_location, password)

#compare decrypted files hashes
    with open(input_temp_file, 'rb') as in_file:
        decrypted_temp_file_hash = hashlib.sha256(in_file.read()).hexdigest()
    with open(input_temp_file_bw, 'rb') as in_file:
        decrypted_temp_file_bw_hash = hashlib.sha256(in_file.read()).hexdigest()

    assert decrypted_temp_file_hash == input_file_hash
    assert decrypted_temp_file_bw_hash == input_file_bw_hash
