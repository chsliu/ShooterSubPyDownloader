from distutils.core import setup
import py2exe

dll_excludes=['w9xpopen.exe']
setup(console=[	'ShooterSubPyDownloader.py',
				'ShooterSubAll.py',
		])


