[pyStormLib](http://blog.vjeux.com/) - python wrapper for StormLib
================================

This is a really basic Python Wrapper for [Zezula StormLib](http://www.zezula.net/en/mpq/stormlib.html) that manages MPQ files.

API
---
* **MPQ**(path): Open a MPQ
* **list**(mask='*'): Return a list of all the files matching the mask
* **extract**(mpq_path, local_path=mpq_path): Extract a file.
    * mpq_path can be a file returned by **list**



Example
-------
    mpq = MPQ('wow-update-13316.MPQ')
    for file in mpq.list():
        print file
        mpq.extract(file, 'extract/' + str(file))
