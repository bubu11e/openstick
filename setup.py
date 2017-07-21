#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#    Copyright 2017 Julien Girard 
#
#    Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3 ;
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://http://www.gnu.org/licenses/gpl-3.0.html
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

from setuptools import setup, find_packages
# Thanks Sam & Max : http://sametmax.com/creer-un-setup-py-et-mettre-sa-bibliotheque-python-en-ligne-sur-pypi/

setup(
    name='openstick',
    version="1.1.2",
    packages=find_packages(),
    author="Julien GIRARD",
    author_email="julien.girard.ju@gmail.com",
    description="Because sometimes you don't need a full stack",
    long_description="Because sometimes you don't need a full stack",
    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,
    install_requires=['names'],
    url='https://github.com/julien-girard/openstick',
    entry_points={
        'console_scripts': [
            'openstick = openstick.openstick:launch',
            'openstick_ls = openstick.openstick:list'
            ]
    },
    scripts=[],

    license="GPL3",
)
