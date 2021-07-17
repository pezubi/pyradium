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

import xml.dom.minidom
import pygments
from pybeamer.xmlhooks.XMLHookRegistry import InnerTextHook, XMLHookRegistry

@XMLHookRegistry.register_hook
class CodeHook(InnerTextHook):
	_TAG_NAME = "code"

	@classmethod
	def handle_text(cls, text, rendered_presentation, node):
		lexer = pygments.lexers.get_lexer_by_name(node.getAttribute("lang"))
		highlighted_code = pygments.highlight(text, lexer, pygments.formatters.HtmlFormatter(cssclass = "code_highlight"))

		replacement_node = xml.dom.minidom.parseString(highlighted_code).firstChild
		rendered_presentation.copy_template_file("base/pygments.css", "pygments.css")
		rendered_presentation.add_css("pygments.css")

		return replacement_node
