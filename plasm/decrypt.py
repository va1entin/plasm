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

from nacl import encoding, public, pwhash, secret, utils

import argparse
import logging
import os
import re
import sys
import getpass

usedEncoder = encoding.RawEncoder

kdf = pwhash.argon2i.kdf
ops = pwhash.argon2i.OPSLIMIT_SENSITIVE

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


def decryptFilesInDir(directory, privateKeyLocation, password, fileExtension=".crypt"):
    loadedPrivateKey = decryptKey(privateKeyLocation, password)

    for file in os.listdir(directory):
        if file.endswith(fileExtension):
            try:
                file = os.path.join(os.path.abspath(directory), file)
                fileExtensionRegex = fileExtension + '$'
                outfile = re.sub(fileExtensionRegex, '', file)

                with open(file, 'rb') as in_file:
                    data = in_file.read()
                    box = public.SealedBox(loadedPrivateKey)
                    decrypted = box.decrypt(data)

                    with open(outfile, 'wb') as out_file:
                        out_file.write(decrypted)

                        logging.info("Decrypted {0} to {1}".format(file, outfile))
            except:
                logging.critical("Failed to decrypt {0}".format(file))

def decryptFile(file, privateKeyLocation, password, fileExtension=".crypt"):
    loadedPrivateKey = decryptKey(privateKeyLocation, password)

    if file.endswith(fileExtension):
        file = os.path.abspath(file)
        fileExtensionRegex = fileExtension + '$'
        outfile = re.sub(fileExtensionRegex, '', file)

        with open(file, 'rb') as in_file:
            data = in_file.read()

        box = public.SealedBox(loadedPrivateKey)
        decrypted = box.decrypt(data)

        with open(outfile, 'wb') as out_file:
            out_file.write(decrypted)

        logging.info("Decrypted {0} to {1}".format(file, outfile))
