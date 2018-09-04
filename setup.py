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

from setuptools import setup

setup(name='plasm',
      version='20180831',
      description='PyNaCl AbStraction Module',
      url='https://gitlab.com/va1entin/plasm',
      author='va1entin',
      author_email='gitlab@valentinsblog.com',
      license='Apache License 2.0',
      packages=['plasm'],
      install_requires=[
          'pynacl>=1.2.0',
      ],
      zip_safe=True)
