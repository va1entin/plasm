#!/usr/bin/env python
# Copyright 2018 Valentin Heidelberger
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

import logging
import os
import re

usedEncoder = encoding.RawEncoder

kdf = pwhash.argon2id.kdf
ops = pwhash.argon2id.OPSLIMIT_SENSITIVE

#logging.basicConfig(filename='/var/log/plasm.log',level=logging.INFO)


def decryptKey(privateKey, password):
    with open(privateKey, 'rb') as in_file:
        salt = in_file.read(16)
        in_file.seek(16)
        encrypted = in_file.read(72)
        in_file.seek(88)
        mem = int(in_file.read())

    key = kdf(secret.SecretBox.KEY_SIZE, password, salt, opslimit=ops, memlimit=mem)
    box = secret.SecretBox(key)
    loadedPrivateKey = box.decrypt(encrypted)
    loadedPrivateKey = public.PrivateKey(loadedPrivateKey, encoder=usedEncoder)

    return loadedPrivateKey

def decryptFilesInDir(directory, privateKeyLocation, password, infileExtension=".crypt"):
    loadedPrivateKey = decryptKey(privateKeyLocation, password)

    for file in os.listdir(directory):
        if file.endswith(infileExtension):
            try:
                file = os.path.join(os.path.abspath(directory), file)
                infileExtensionRegex = infileExtension + '$'
                outfile = re.sub(infileExtensionRegex, '', file)

                with open(file, 'rb') as in_file:
                    data = in_file.read()
                    box = public.SealedBox(loadedPrivateKey)
                    decrypted = box.decrypt(data)

                    with open(outfile, 'wb') as out_file:
                        out_file.write(decrypted)

                        logging.info("Decrypted {0} to {1}".format(file, outfile))
            except:
                logging.critical("Failed to decrypt {0}".format(file))

def decryptFile(file, privateKeyLocation, password, infileExtension=".crypt"):
    loadedPrivateKey = decryptKey(privateKeyLocation, password)

    if file.endswith(infileExtension):
        file = os.path.abspath(file)
        infileExtensionRegex = infileExtension + '$'
        outfile = re.sub(infileExtensionRegex, '', file)

        with open(file, 'rb') as in_file:
            data = in_file.read()

        box = public.SealedBox(loadedPrivateKey)
        decrypted = box.decrypt(data)

        with open(outfile, 'wb') as out_file:
            out_file.write(decrypted)

        logging.info("Decrypted {0} to {1}".format(file, outfile))
