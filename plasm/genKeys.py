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
import datetime
import getpass
import logging
import os
import sys

usedEncoder = encoding.RawEncoder

kdf = pwhash.argon2i.kdf
salt = utils.random(pwhash.argon2i.SALTBYTES)
ops = pwhash.argon2i.OPSLIMIT_SENSITIVE

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
    now = now.strftime("_%Y-%m-%d_%H_%M_%S")
    backupPrivateKeyLocation = os.path.join(privateKeyLocation + now)
    backupPublicKeyLocation = os.path.join(publicKeyLocation + now)

    if os.path.isfile(privateKeyLocation):
        os.rename(privateKeyLocation, backupPrivateKeyLocation)
        logging.info("Existing private key {0} was backuped to {1}".format(privateKeyLocation, backupPrivateKeyLocation))

    if os.path.isfile(publicKeyLocation):
        os.rename(publicKeyLocation, backupPublicKeyLocation)
        logging.info("Existing public key {0} was backuped to {1}".format(publicKeyLocation, backupPublicKeyLocation))

def generateKeyPair(privateKeyLocation, publicKeyLocation, password, memlimit=pwhash.argon2i.MEMLIMIT_SENSITIVE):
    backupKeyFiles(privateKeyLocation, publicKeyLocation)

    privateKey = public.PrivateKey.generate()

    encodedPrivateKey = privateKey.encode(encoder=usedEncoder)
    encodedPublicKey = privateKey.public_key.encode(encoder=usedEncoder)

    encryptedPrivateKey = encryptKey(memlimit, encodedPrivateKey, password)

    writePrivateKey(privateKeyLocation, salt, encryptedPrivateKey, memlimit)
    writePublicKey(publicKeyLocation, encodedPublicKey)

    logging.info('IMPORTANT: Backup the newly generated private key at {0} immediately. If you lose it, you will not be able to decrypt your files.'.format(privateKeyLocation))

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--memlimit", type=int, metavar="int", help="Maximum amount of memory in bytes to use for key encryption, minimum 8192", default=pwhash.argon2i.MEMLIMIT_SENSITIVE)
    parser.add_argument("--directory", metavar="/etc/plasm", help="Directory to write keys to", default=os.getcwd())
    args = parser.parse_args()

    if args.directory:
        try:
            if os.path.exists(args.directory):
                logging.info("Using specified directory {0} as output directory".format(args.directory))
        except:
            raise Error("Specified output directory {0} does not exist".format(args.directory))
    else:
        logging.info("No output directory specified. Using current directory {0} as output directory.".format(args.directory))

    publicKeyLocation = os.path.join(args.directory, 'public.key')
    privateKeyLocation = os.path.join(args.directory, 'private.key')

    args.password = getpass.getpass()

    generateKeyPair(privateKeyLocation, publicKeyLocation, args.password, args.memlimit)

if __name__ == "__main__":
    getArgs()
