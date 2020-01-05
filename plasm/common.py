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

from nacl import encoding, pwhash, secret

# Plasm settings
remove_input_file = False
file_extension=".crypt"

# PyNaCl settings
used_encoder = encoding.RawEncoder
memlimit = pwhash.argon2id.MEMLIMIT_SENSITIVE
#ops = pwhash.argon2id.OPSLIMIT_SENSITIVE

def ensure_is_bytes(input_str):
    if not isinstance(input_str, bytes):
        return input_str.encode()
    else:
        return input_str

def read_file(infile):
    with open(infile, 'rb') as in_file:
        data = in_file.read()
    return data

def write_file(outfile, data):
    with open(outfile, 'wb') as out_file:
        out_file.write(data)
    return outfile
