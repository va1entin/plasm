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

from nacl import encoding, public, pwhash, secret, utils

import datetime
import logging
import os

usedEncoder = encoding.RawEncoder

kdf = pwhash.argon2id.kdf
salt = utils.random(pwhash.argon2id.SALTBYTES)
ops = pwhash.argon2id.OPSLIMIT_SENSITIVE

#logging.basicConfig(filename='/var/log/plasm.log',level=logging.INFO)

def encryptKey(memlimit, key, password):

    derivatedPassword = kdf(secret.SecretBox.KEY_SIZE, password, salt, opslimit=ops, memlimit=memlimit)

    secretBox = secret.SecretBox(derivatedPassword)
    encryptedPrivateKey = secretBox.encrypt(key)
    return encryptedPrivateKey

def writePrivateKey(outfile, salt, encryptedKey, memlimit):
    with open(outfile, 'wb') as out_file:
        out_file.write(salt)
        out_file.write(encryptedKey)
        out_file.write(str(memlimit).encode())

def writePublicKey(outfile, publicKey):
    with open(outfile, 'wb') as out_file:
        out_file.write(publicKey)

def backupKeyFiles(privateKeyLocation, publicKeyLocation):
    now = datetime.datetime.now()
    now = now.strftime("_%Y-%m-%d_%H-%M-%S")
    backupPrivateKeyLocation = os.path.join(privateKeyLocation + now)
    backupPublicKeyLocation = os.path.join(publicKeyLocation + now)

    if os.path.isfile(privateKeyLocation):
        os.rename(privateKeyLocation, backupPrivateKeyLocation)
        logging.info("Existing private key {0} was backuped to {1}".format(privateKeyLocation, backupPrivateKeyLocation))

    if os.path.isfile(publicKeyLocation):
        os.rename(publicKeyLocation, backupPublicKeyLocation)
        logging.info("Existing public key {0} was backuped to {1}".format(publicKeyLocation, backupPublicKeyLocation))

def generateKeyPair(privateKeyLocation, publicKeyLocation, password, memlimit=pwhash.argon2id.MEMLIMIT_SENSITIVE):
    backupKeyFiles(privateKeyLocation, publicKeyLocation)

    privateKey = public.PrivateKey.generate()

    encodedPrivateKey = privateKey.encode(encoder=usedEncoder)
    encodedPublicKey = privateKey.public_key.encode(encoder=usedEncoder)

    encryptedPrivateKey = encryptKey(memlimit, encodedPrivateKey, password)

    writePrivateKey(privateKeyLocation, salt, encryptedPrivateKey, memlimit)
    writePublicKey(publicKeyLocation, encodedPublicKey)

    logging.info('IMPORTANT: Backup the newly generated private key at {0} immediately. If you lose it, you will not be able to decrypt your files.'.format(privateKeyLocation))
