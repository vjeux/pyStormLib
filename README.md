[pyStormLib](http://blog.vjeux.com/) - python wrapper for StormLib
================================

This is a really basic Python Wrapper for [Zezula StormLib](http://www.zezula.net/en/mpq/stormlib.html) that manages MPQ files. Feel free to fork it to add more features.

API
---
* **MPQ**(path): Open a MPQ

* **list**(mask='*'): Return a list of all the files matching the mask

* **extract**(mpq_path, local_path=mpq_path): Extract a file.
    * mpq_path can be a file returned by **list**



Example
-------
Extract all the files of a MPQ in the 'extract' folder.

    from storm import MPQ
    
    mpq = MPQ('wow-update-13316.MPQ')
    for file in mpq.list():
        print file
        mpq.extract(file, 'extract/' + str(file))
