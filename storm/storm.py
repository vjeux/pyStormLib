
# Python StormLib Wrapper
# by Vjeux <vjeuxx@gmail.com> http://blog.vjeux.com/

# API Documentation
# http://www.zezula.net/en/mpq/stormlib.html

from ctypes import *
import os, re

storm = cdll.LoadLibrary(re.sub('/[^/]+$', '', __file__) + '/libStorm.so')

class MPQFileData(Structure):
	_fields_ = [
		('filename', c_char * 1024),
		('plainname', c_char_p),
		('hashindex', c_int, 32),
		('blockindex', c_int, 32),
		('filesize', c_int, 32),
		('fileflags', c_int, 32),
		('compsize', c_int, 32),
		('filetimelo', c_int, 32),
		('filetimehi', c_int, 32),
		('locale', c_int, 32)
	]

	def __repr__(self):
		return self.filename

	def __str__(self):
		return self.filename

class MPQ():
	mpq_handle = c_int()

	def __init__(self, filename):
		storm.SFileOpenArchive(filename, 0, 0, byref(self.mpq_handle))
	
	def close(self):
		storm.SFileCloseArchive(self.mpq_handle)

	def list(self, mask='*'):
		ret = []

		file_desc = MPQFileData()
		hFind = storm.SFileFindFirstFile(self.mpq_handle, mask, byref(file_desc), None)
		ret.append(file_desc)

		file_desc = MPQFileData()
		while storm.SFileFindNextFile(hFind, byref(file_desc)):
			ret.append(file_desc)
			file_desc = MPQFileData()

		return ret

	def extract(self, mpq_path, local_path=None):
		if isinstance(mpq_path, MPQFileData):
			mpq_path = mpq_path.filename

		if local_path is None:
			local_path = mpq_path
		local_path = local_path.replace('\\', '/')

		try:
			os.makedirs(re.sub('/[^/]+$', '', local_path))
		except Exception:
			pass
		
		storm.SFileExtractFile(self.mpq_handle, mpq_path, local_path)
