#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    # For insecure platform warnings
    'pyopenssl>=0.13',
    'ndg-httpsclient>=0.4.0',
    'pyasn1>=0.1.7',

    'lxml>=3.4.4',
    'requests>=2.7.0',
    'futures>=3.0.3',
    'docopt>=0.6.2',
]

setup(
    name='chat-parser',
    version='0.0.1',
    description="Parses messages for special content.",
    author="Erick Yellott",
    author_email='erick.yellott@gmail.com',
    url='https://github.com/yellottyellott/chat-parser',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'chatparse = chat_parser.main:main',
        ]
    },
)
