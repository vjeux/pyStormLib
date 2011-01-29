
# Python StormLib Wrapper
# by Vjeux <vjeuxx@gmail.com> http://blog.vjeux.com/
# http://github.com/vjeux/pyStormLib

# StormLib API Documentation
# http://www.zezula.net/en/mpq/Stormlib.html

from ctypes import cdll, Structure, byref, c_char, c_char_p, c_int, c_buffer
import os, glob, sys

storm = cdll.LoadLibrary(os.path.dirname(__file__) + '/libStorm.so')

# Wrapper around storm to check for errors
class StormWrapper(type):
	def __getattr__(self, attr):
		return lambda *arguments: Storm.__call(name=attr, func=getattr(storm, attr), *arguments)

	def __call(*arguments, **keywords):
		# In order to debug: uncomment to print every call
		#print keywords['name'], arguments[1:],
		
		# Call the function
		func = keywords['func']
		ret = func(*arguments[1:])

		# In order to debug: uncomment to print every call
		#print ret

		# Handle errors
		code = storm.GetLastError()
		if ret != 0 and code not in (0, 106, 107): # "No more files" and "End of file" are not real errors
			message = '%s\nCall: %s %s %s' % (MPQErrors.get(code, 'Error #%i' % code), keywords['name'], arguments[1:], ret)
			raise Exception(message)

		return ret

# MetaClass trick to be able to handle Storm.<function path>() with __getattr__
class Storm:
	__metaclass__ = StormWrapper

MPQErrors = {
	10000: "ERROR_AVI_FILE No MPQ file, but AVI file.",
	10001: "ERROR_UNKNOWN_FILE_KEY Returned by SFileReadFile when can't find file key",
	10002: "ERROR_CHECKSUM_ERROR Returned by SFileReadFile when sector CRC doesn't match",
	10003: "ERROR_INTERNAL_FILE The given operation is not allowed on internal file",
	10004: "ERROR_BASE_FILE_MISSING The file is present as incremental patch file, but base file is missing",

	2: "ERROR_FILE_NOT_FOUND",
	1: "ERROR_ACCESS_DENIED",
	9: "ERROR_INVALID_HANDLE",
	12: "ERROR_NOT_ENOUGH_MEMORY",
	105: "ERROR_BAD_FORMAT",
	106: "ERROR_NO_MORE_FILES",
	107: "ERROR_HANDLE_EOF",
	95: "ERROR_NOT_SUPPORTED",
	22: "ERROR_INVALID_PARAMETER",
	28: "ERROR_DISK_FULL",
	17: "ERROR_ALREADY_EXISTS",
	108: "ERROR_CAN_NOT_COMPLETE",
	109: "ERROR_FILE_CORRUPT",
	10: "ERROR_INSUFFICIENT_BUFFER"
}

class MPQFileData(Structure):
	_fields_ = [
		('filename', c_char * 1024),
		('plainpath', c_char_p),
		('hashindex', c_int, 32),
		('blockindex', c_int, 32),
		('filesize', c_int, 32),
		('fileflags', c_int, 32),
		('compsize', c_int, 32),
		('filetimelo', c_int, 32),
		('filetimehi', c_int, 32),
		('locale', c_int, 32)
	]

	mpq = None
	def __init__(self, mpq):
		self.mpq = mpq

	@property
	def path(self):
		"""Return a path with / instead of \ """
		return self.filename.replace('\\', '/')

	@property
	def basename(self):
		return os.path.basename(self.path)
	
	@property
	def dirname(self):
		return os.path.dirname(self.path)

	def extract(self, target=None):
		return self.mpq.extract(self.filename, target)

	def read(self):
		return self.mpq.read(self.filename)

	def __repr__(self):
		return self.filename

	def __str__(self):
		return self.filename
	
	def __hash__(self):
		return hash(self.filename)
	
	def __eq__(self, other):
		return self.filename == other.filename

	def __ne__(self, other):
		return self.filename != other.filename

class MPQ():
	mpq = c_int()

	def __init__(self, filename):
		"""Open the MPQ Archive"""

		if not os.path.exists(filename):
			raise "ERROR_FILE_NOT_FOUND %s" % filename
		Storm.SFileOpenArchive(filename, 0, 0x0100, byref(self.mpq))
	
	def close(self):
		"""Close the MPQ Archive"""
		Storm.SFileCloseArchive(self.mpq)

	def list(self, *arguments):
		"""List all the files matching the mask"""

		ret = set([])

		if len(arguments) == 0:
			arguments = ['*']

		for mask in arguments:
			# Initial Find
			file = MPQFileData(self)
			find = Storm.SFileFindFirstFile(self.mpq, mask, byref(file), None)
			if not find:
				return

			yield file
			ret.add(file)

			# Go through the results
			file = MPQFileData(self)
			while Storm.SFileFindNextFile(find, byref(file)):
				if file not in ret:
					yield file
					ret.add(file)
				file = MPQFileData(self)

	def extract(self, mpq_path, local_path=None):
		"""Extract the file"""

		# Handle arguments
		if isinstance(mpq_path, MPQFileData):
			mpq_path = mpq_path.filename
		if local_path is None:
			local_path = mpq_path
		
		# Create the directories
		local_path = local_path.replace('\\', '/')
		try:
			os.makedirs(os.path.dirname(local_path))
		except Exception:
			pass

		# Extract!
		Storm.SFileExtractFile(self.mpq, mpq_path, local_path, 1)

		# Allow chaining
		return self

	def has(self, path):
		"""Does the MPQ have the file?"""

		# Handle argument
		if isinstance(path, MPQFileData):
			path = path.filename

		try:
			Storm.SFileHasFile(self.mpq, path)
			return True
		except:
			return False
	
	def read(self, path):
		"""Return the file content"""

		# Handle argument
		if isinstance(path, MPQFileData):
			path = path.filename

		# Open the file
		file = c_int()
		Storm.SFileOpenFileEx(self.mpq, path, 1, byref(file))

		# Get the Size
		high = c_int()
		low = Storm.SFileGetFileSize(file, byref(high))
		size = high.value * pow(2, 32) + low

		# Read the File
		data = c_buffer(size)
		read = c_int()
		Storm.SFileReadFile(file, data, size, byref(read), None)

		# Close and Return
		Storm.SFileCloseFile(file)
		return data.raw

	def patch(self, path, prefix=''):
		"""Add MPQ as patches"""

		# Handle arguments
		path_list = sorted(glob.glob(path)) if isinstance(path, str) else path

		# Add the Patchs
		for path in path_list:
			Storm.SFileOpenPatchArchive(self.mpq, path, prefix, 0)

		# Allow chaining
		return self
