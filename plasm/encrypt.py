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

from nacl import encoding, public

import logging
import os

usedEncoder = encoding.RawEncoder

#logging.basicConfig(filename='/var/log/plasm.log',level=logging.INFO)


def readPublicKey(publicKeyLocation):
    with open(publicKeyLocation, 'rb') as key_file:
            publicKey = key_file.read()
    return public.PublicKey(publicKey, encoder=usedEncoder)

def readFile(infile, outfileExtension):
    outfile = infile + outfileExtension
    with open(infile, 'rb') as in_file:
        data = in_file.read()
    return data, outfile

def writeFile(outfile, data):
    with open(outfile, 'wb') as out_file:
        out_file.write(data)
    return outfile

def sealedBox(publicKey, data):
    box = public.SealedBox(publicKey)
    return box.encrypt(data)

def removeFile(inputFile):
    logging.debug('Deleting source file {0}'.format(inputFile))
    os.remove(inputFile)

def encryptFile(inputFile, publicKeyLocation='/etc/plasm/public.key', outfileExtension=".crypt", removeInputFile=False):
    data, outfile = readFile(inputFile, outfileExtension)
    publicKey = readPublicKey(publicKeyLocation)
    encrypted = sealedBox(publicKey, data)
    outfile = writeFile(outfile, encrypted)
    logging.debug('Successfully encrypted {0} to {1}'.format(inputFile, outfile))
    if removeInputFile:
        removeFile(inputFile)
    return outfile

def encryptFilesInDir(directory, publicKeyLocation, outfileExtension=".crypt", removeInputFile=False):
    for file in os.listdir(directory):
        try:
            filePath = os.path.join(directory, file)
            encryptFile(filePath, publicKeyLocation, outfileExtension=outfileExtension, removeInputFile=removeInputFile)
        except:
            logging.critical("Failed to encrypt {0}".format(file))
