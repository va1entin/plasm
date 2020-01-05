#!/usr/bin/env python
# Copyright 2020 Valentin Heidelberger
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

from plasm import common
from plasm import decrypt
from plasm import encrypt
from plasm import gen_keys

import argparse
import getpass
import logging

def setup_parser():
    parser = argparse.ArgumentParser()

    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('-g', '--gen_keys', action='store_true', help='Generate key pair')
    modes.add_argument('-d', '--decrypt', action='store_true', help='Decrypt file')
    modes.add_argument('-e', '--encrypt', action='store_true', help='Encrypt file')

    # Required in at least one mode
    parser.add_argument('--input_file', help='File to encrypt/decrypt')

    # Optional
    parser.add_argument('--private_key_location', help='Location to read/write private key from/to', default='/etc/plasm/private.key')
    parser.add_argument('--public_key_location', help='Location to read/write public key from/to', default='/etc/plasm/public.key')
    parser.add_argument('--pwd_file', help='File to read password from')
    parser.add_argument('--memlimit', type=int, help='Memlimit to use for key generation', default=common.memlimit)
    parser.add_argument('--remove_input_file', action='store_true', help='Whether to remove input file after encryption', default=common.remove_input_file)

    args = parser.parse_args()
    return parser, args

def args_valid(parser, args):
    if args.encrypt and not args.input_file:
        parser.error("Encrypt requires --public_key_location and --input_file")

    if args.decrypt and not args.input_file:
        parser.error("Decrypt requires --private_key_location and --input_file")
    else:
        args.password = get_password(args)

def get_password(args):
    if args.pwd_file:
        logging.info(f"Reading password from {args.pwd_file}")
        common.read_file(args.pwd_file)
    else:
        logging.info("No --pwd_file specified, getting password interactively")
        password = getpass.getpass(prompt="Password for private key: ")
    return password

def main(args):
    if args.gen_keys:
        logging.info("Generating key pair...")
        gen_keys.generate_key_pair(args.private_key_location, args.public_key_location, args.password, memlimit=args.memlimit)
        logging.info(f"Successfully generated key pair at {args.private_key_location} and {args.public_key_location}")
    elif args.decrypt:
        logging.info("Decrypting file...")
        decrypt.decrypt_file(args.input_file, args.private_key_location, args.password)
        logging.info(f"Successfully decrypted file {args.input_file}")
    elif args.encrypt:
        logging.info("Encrypting file...")
        encrypt.encrypt_file(args.input_file, args.public_key_location, removeInputFile=args.remove_input_file)
        logging.info(f"Successfully encrypted file {args.input_file}")

if __name__ == '__main__':
    parser, args = setup_parser()
    args_valid(parser, args)
    main(args)
