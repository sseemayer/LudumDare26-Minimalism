#!/usr/bin/env python2

from distutils.core import setup

try:
    import py2app
except ImportError:
    pass

NAME = 'The Migration'
VERSION = '0.1'

plist = dict(
    CFBundleIconFile=NAME,
    CFBundleName=NAME,
    CFBundleShortVersionString=VERSION,
    CFBundleGetInfoString=' '.join([NAME, VERSION]),
    CFBundleExecutable=NAME,
    CFBundleIdentifier='de.semicolonsoftware.themigration',
)

setup(
    name=NAME,
    version=VERSION,
    description='Guide a fish swarm across the sea',
    author='Stefan Seemayer',
    author_email='mail@semicolonsoftware.de',
    url='http://ludumdare.com/compo/author/semi',

    data_files=['./data'],
    app=[
        #dict(script="aliens_bootstrap.py", plist=plist),
        dict(script="the_migration.py", plist=plist),
    ],
    options={
        'py2app': {
            'includes': ['pygame', 'py2d', 'pyhiero', 'glyph']
        }
    }
)
