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

from setuptools import setup

setup(name='plasm',
      version='20180830',
      description='PyNaCl AbStraction Module',
      url='https://gitlab.com/va1entin/plasm',
      author='va1entin',
      author_email='gitlab@valentinsblog.com',
      license='GPL',
      packages=['plasm'],
      install_requires=[
          'pynacl',
      ],
      scripts=[
          'plasm/decrypt.py',
          'plasm/encrypt.py',
          'plasm/genKeys.py',
      ],
      zip_safe=True)
