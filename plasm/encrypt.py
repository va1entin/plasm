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
from plasm import common

import logging
import os

#logging.basicConfig(filename='/var/log/plasm.log',level=logging.INFO)


def read_public_key(public_key_location):
    public_key = common.read_file(public_key_location)
    return public.PublicKey(public_key, encoder=common.used_encoder)

def sealed_box(public_key, data):
    box = public.SealedBox(public_key)
    return box.encrypt(data)

def remove_file(input_file):
    logging.info(f'Deleting source file {input_file}')
    os.remove(input_file)

def encrypt_file(input_file, public_key_location='/etc/plasm/public.key', outfile_extension=common.file_extension, remove_input_file=common.remove_input_file):
    outfile = input_file + outfile_extension
    data = common.read_file(input_file)
    public_key = read_public_key(public_key_location)
    encrypted = sealed_box(public_key, data)
    outfile = common.write_file(outfile, encrypted)
    logging.info(f'Successfully encrypted {input_file} to {outfile}')
    if remove_input_file:
        remove_file(input_file)
    return outfile

def encrypt_files_in_dir(directory, public_key_location, outfile_extension=common.file_extension, remove_input_file=common.remove_input_file):
    for file in os.listdir(directory):
        try:
            file_path = os.path.join(directory, file)
            encrypt_file(file_path, public_key_location, outfile_extension=outfile_extension, remove_input_file=remove_input_file)
        except:
            logging.critical(f"Failed to encrypt {file}")
