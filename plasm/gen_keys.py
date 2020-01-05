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

from nacl import encoding, public, pwhash, secret, utils
from plasm import common

import datetime
import logging
import os


kdf = pwhash.argon2id.kdf
salt = utils.random(pwhash.argon2id.SALTBYTES)
ops = pwhash.argon2id.OPSLIMIT_SENSITIVE

#logging.basicConfig(filename='/var/log/plasm.log',level=logging.INFO)


def encrypt_key(memlimit, key, password):

    derivated_password = kdf(secret.SecretBox.KEY_SIZE, password, salt, opslimit=ops, memlimit=memlimit)

    secretBox = secret.SecretBox(derivated_password)
    encrypted_private_key = secretBox.encrypt(key)
    return encrypted_private_key

def write_private_key(outfile, salt, encrypted_key, memlimit):
    with open(outfile, 'wb') as out_file:
        out_file.write(salt)
        out_file.write(encrypted_key)
        out_file.write(str(memlimit).encode())

def backup_key_files(private_key_location, public_key_location):
    now = datetime.datetime.now()
    now = now.strftime("_%Y-%m-%d_%H-%M-%S")
    backup_private_key_location = os.path.join(private_key_location + now)
    backup_public_key_location = os.path.join(public_key_location + now)

    if os.path.isfile(private_key_location):
        os.rename(private_key_location, backup_private_key_location)
        logging.info(f"Existing private key {private_key_location} was backuped to {backup_private_key_location}")

    if os.path.isfile(public_key_location):
        os.rename(public_key_location, backup_public_key_location)
        logging.info(f"Existing public key {public_key_location} was backuped to {backup_public_key_location}")

def generate_key_pair(private_key_location, public_key_location, password, memlimit=common.memlimit):
    backup_key_files(private_key_location, public_key_location)

    private_key = public.PrivateKey.generate()

    encoded_private_key = private_key.encode(encoder=common.used_encoder)
    encoded_public_key = private_key.public_key.encode(encoder=common.used_encoder)

    password = common.ensure_is_bytes(password)
    encrypted_private_key = encrypt_key(memlimit, encoded_private_key, password)

    write_private_key(private_key_location, salt, encrypted_private_key, memlimit)
    common.write_file(public_key_location, encoded_public_key)

    logging.info(f'IMPORTANT: Backup the newly generated private key at {private_key_location} immediately. If you lose it, you will not be able to decrypt your files.')
