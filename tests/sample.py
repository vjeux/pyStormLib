
import sys
sys.path.insert(0, '..')

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
