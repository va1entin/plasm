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

def readFile(infile):
    with open(infile, 'rb') as in_file:
        data = in_file.read()
        outfile = re.sub(r'(\.[a-zA-Z0-9]*$)', r'\1.crypt', infile)
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

def encrypt(inputFile, publicKeyLocation='/etc/plasm/public.key', removeInputFile=False):
    #try:
    data, outfile = readFile(inputFile)
    publicKey = readPublicKey(publicKeyLocation)
    encrypted = sealedBox(publicKey, data)
    outfile = writeFile(outfile, encrypted)
    logging.debug('Successfully encrypted {0} to {1}'.format(inputFile, outfile))
    if removeInputFile:
        removeFile(inputFile)
    return outfile
    #except:
    #    logging.error('Encryption of file {0} failed.'.format(inputFile))
    #    return None

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", metavar="/path/to/public.key", help="Public key to use", default='/etc/plasm/public.key', required=True)
    parser.add_argument("--directory", metavar="/path/to/files", help="Encrypt all files in this directory")
    parser.add_argument("--file", metavar="/path/to/file", help="Encrypt only the specified file")
    parser.add_argument("--removeInputFile", action='store_true', help="Remove input file(s) after encryption")
    args = parser.parse_args()

    if args.key:
        if not os.path.isfile(args.key):
            logging.critical('Public key does not exist: {0}'.format(args.key))
            sys.exit(1)

    encrypt(args.file, args.key, args.removeInputFile)

if __name__ == "__main__":
    getArgs()
