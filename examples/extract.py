
import sys
sys.path.insert(0, '..')

from storm import MPQ

mpq = MPQ('wow-update-13316.MPQ')
for file in mpq.list():
	print file
	mpq.extract(file, 'extract/' + str(file))
