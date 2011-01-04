[pyStormLib](http://blog.vjeux.com/) - python wrapper for StormLib
================================

This is a really basic Python Wrapper for [Zezula StormLib](http://www.zezula.net/en/mpq/stormlib.html) that manages MPQ files. Feel free to fork it to add more features.

API
---
* **MPQ**(path): Open a MPQ

* **list**(mask='*'): List of all the files matching the mask

* **read**(path): Content of the file

* **has**(path): Does the MPQ have the file?

* **extract**(mpq_path, local_path=mpq_path): Extract a file.
    * mpq_path can be a file returned by **list**



Example
-------
	from storm import MPQ

	mpq = MPQ('wow-update-13316.MPQ')

	print '[list] List TXT and ANIM files'
	print list(mpq.list('*.txt')) + list(mpq.list('*.anim'))

	print '[extract] Extracting all the enUS DBC'
	for file in mpq.list('enUS*.dbc'):
		print file
		mpq.extract(file, 'extract/' + str(file))

	print '[read] Reading a few TXT'
	for file in mpq.list('en*.txt'):
		print file
		print mpq.read(file)
