#!/usr/bin/python

from distutils.core import setup

setup (name='gitselect',
       version='1.0.0',
       author='Marc Zinnschlag',
       author_email='marc@zpages.de',
       license = 'GPLv3+',
       description='quick selection of a file from a git repository',
       classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'OSI Approved :: GNU General Public License (GPL)',
            'Topic :: Software Development :: Version Control'
       ],

       scripts=['gitselect']
       )
