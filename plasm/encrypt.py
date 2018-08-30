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

from nacl import encoding, public

import argparse
import logging
import os
import re
import sys

usedEncoder = encoding.RawEncoder

#logging.basicConfig(filename='/var/log/plasm.log',level=logging.INFO)


def readPublicKey(publicKeyLocation):
    with open(publicKeyLocation, 'rb') as key_file:
            publicKey = key_file.read()
    return public.PublicKey(publicKey, encoder=usedEncoder)

def readFile(infile, outfileExtension):
    outfile = re.sub(r'(\.[a-zA-Z0-9]*$)', r'\1.{}'.format(outfileExtension), infile)
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

def encrypt(inputFile, publicKeyLocation='/etc/plasm/public.key', outfileExtension="crypt", removeInputFile=False):
    data, outfile = readFile(inputFile, outfileExtension)
    publicKey = readPublicKey(publicKeyLocation)
    encrypted = sealedBox(publicKey, data)
    outfile = writeFile(outfile, encrypted)
    logging.debug('Successfully encrypted {0} to {1}'.format(inputFile, outfile))
    if removeInputFile:
        removeFile(inputFile)
    return outfile

def encryptFilesInDir(directory, publicKeyLocation, outfileExtension="crypt", removeInputFile=False):
    for file in os.listdir(directory):
        try:
            filePath = os.path.join(directory, file)
            encrypt(filePath, publicKeyLocation, outfileExtension=outfileExtension, removeInputFile=removeInputFile)
        except:
            logging.critical("Failed to encrypt {0}".format(file))
