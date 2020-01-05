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

from nacl import encoding, public, pwhash, secret
from plasm import common

import logging
import os
import re

kdf = pwhash.argon2id.kdf
ops = pwhash.argon2id.OPSLIMIT_SENSITIVE

#logging.basicConfig(filename='/var/log/plasm.log',level=logging.INFO)


def decrypt_key(private_key, password):
    with open(private_key, 'rb') as in_file:
        salt = in_file.read(16)
        in_file.seek(16)
        encrypted = in_file.read(72)
        in_file.seek(88)
        mem = int(in_file.read())

    password = common.ensure_is_bytes(password)
    key = kdf(secret.SecretBox.KEY_SIZE, password, salt, opslimit=ops, memlimit=mem)
    box = secret.SecretBox(key)
    loaded_private_key = box.decrypt(encrypted)
    loaded_private_key = public.PrivateKey(loaded_private_key, encoder=common.used_encoder)

    return loaded_private_key

def decrypt_files_in_dir(directory, private_key_location, password, infile_extension=common.file_extension):
    loaded_private_key = decrypt_key(private_key_location, password)

    for file in os.listdir(directory):
        if file.endswith(infile_extension):
            try:
                file = os.path.join(os.path.abspath(directory), file)
                decrypt_file(file, private_key_location, password, infile_extension, loaded_private_key)
            except:
                logging.critical(f"Failed to decrypt {file}")

def decrypt_file(file, private_key_location, password, infile_extension=common.file_extension, loaded_private_key=None):
    if not loaded_private_key:
        loaded_private_key = decrypt_key(private_key_location, password)

    if file.endswith(infile_extension):
        file = os.path.abspath(file)
        infile_extension_regex = infile_extension + '$'
        outfile = re.sub(infile_extension_regex, '', file)

        data = common.read_file(file)

        box = public.SealedBox(loaded_private_key)
        decrypted = box.decrypt(data)

        common.write_file(outfile, decrypted)
        logging.info(f"Decrypted {file} to {outfile}")
