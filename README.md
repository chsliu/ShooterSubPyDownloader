ShooterSubPyDownloader
======================

This is a shooter.cn subtitle download tool using Python.

Couple of interesting features are made from magic282 original version.

- works on directories and files.
- detects whether the subtitle is in english or chinese, and change the extension name accordingly. eng for english, zh for chinese.
- converts gb or big5 encodings to utf8 encoding while saving the file.
- ignore.txt file is used to skip unwanted files to speed up the whole download process.
- automatically overwrite or remove old subtitles if new one is downloaded. ***Use with caution***


setup.bat
---------

Generate win32 executable.


sub-dir.bat [dir]
-----------------

Download subtitles for the whole directory recursively. All video files without a chinese subtitle will be tried, even if an english one is already present. An ignore.txt will be generated with a list of filenames when files are older than 7 days and no chinese subtitles downloaded, and these listed files will be ignored on the next run.


sub-file.bat [file]
-------------------

Download subtitle for a single file.

