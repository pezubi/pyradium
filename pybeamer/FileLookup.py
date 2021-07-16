#	pybeamer - HTML presentation/slide show generator
#	Copyright (C) 2015-2021 Johannes Bauer
#
#	This file is part of pybeamer.
#
#	pybeamer is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pybeamer is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pybeamer; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import os
from .Exceptions import FailedToLookupFileException

class FileLookup():
	def __init__(self, paths):
		self._paths = tuple(paths)

	def lookup(self, filename):
		for dirname in self._paths:
			path = dirname + "/" + filename
			if os.path.isfile(path):
				return path
		if len(self._paths) == 0:
			raise FailedToLookupFileException("No such file: %s (no directories given to look up)" % (filename))
		else:
			raise FailedToLookupFileException("No such file: %s (looked in %s)" % (filename, ", ".join(self._paths)))

	def __iter__(self):
		yield from self._paths