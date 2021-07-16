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

import sys
import argparse
from .MultiCommand import MultiCommand
from .ActionRender import ActionRender
from .ActionServe import ActionServe
from .ActionAcroSort import ActionAcroSort
from .Enums import PresentationMode

def _geometry(text):
	text = text.split("x", maxsplit = 1)
	if len(text) != 2:
		raise argparse.ArgumentTypeError("Not a valid geometry: %s" % (text))
	return (int(text[0]), int(text[1]))

def main():
	mc = MultiCommand()

	def genparser(parser):
		parser.add_argument("--image-max-dimension", metavar = "pixels", type = int, default = 1000, help = "When rendering imaages, specifies the maximum dimension they're downsized to. The lower this value, the smaller the output files and the lower the quality. Defaults to %(default)d pixels.")
		parser.add_argument("-I", "--include-dir", metavar = "path", action = "append", default = [ ], help = "Specifies an additional include directory in which, for example, images are located which are referenced from the presentation. Can be issued multiple times.")
		parser.add_argument("--template-dir", metavar = "path", action = "append", default = [ ], help = "Specifies an additional template directories in which template style files are located. Can be issued multiple times.")
		parser.add_argument("-t", "--template-style", metavar = "name", default = "default", help = "Template style to use. Defaults to %(default)s.")
		parser.add_argument("-g", "--geometry", metavar = "width x height", type = _geometry, default = "1280x720", help = "Slide geometry, in pixels. Defaults to %(default)s.")
		parser.add_argument("-r", "--remove-pauses", action = "store_true", help = "Ignore all pause directives and just render the final slides.")
		parser.add_argument("-i", "--index-filename", metavar = "filename", default = "index.html", help = "Gives the name of the presentation index file. Defaults to %(default)s. Useful if you want to render multiple presentations in one subdirectory.")
		parser.add_argument("-m", "--presentation-mode", metavar = "{%s}" % (",".join(enumitem.value for enumitem in PresentationMode)), type = PresentationMode, default = "interactive", help = "Generate this type of presentation. Can be one of %(choices)s, defaults to %(default)s.")
		parser.add_argument("-f", "--force", action = "store_true", help = "Overwrite files in destination directory if they already exist.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increase verbosity. Can be specified more than once.")
		parser.add_argument("infile", help = "Input XML file of the slide show.")
		parser.add_argument("outdir", help = "Output directory the presentation is put into.")
	mc.register("render", "Render a slide show", genparser, action = ActionRender)

	def genparser(parser):
		parser.add_argument("-b", "--bind-addr", metavar = "addr", type = str, default = "127.0.0.1", help = "Address to bind to. Defaults to %(default)s.")
		parser.add_argument("-p", "--port", metavar = "port", type = int, default = 8123, help = "Port to serve directory under. Defaults to %(default)s.")
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("dirname", help = "Directory that should be served.")
	mc.register("serve", "Serve a slide show as HTTP", genparser, action = ActionServe)

	def genparser(parser):
		parser.add_argument("-v", "--verbose", action = "count", default = 0, help = "Increases verbosity. Can be specified multiple times to increase.")
		parser.add_argument("acrofile", help = "Acronym database JSON file.")
	mc.register("acrosort", "Sort an acryonym database", genparser, action = ActionAcroSort)

	return mc.run(sys.argv[1:])

if __name__ == "__main__":
	main()
