# @SI_Copyright@
# Copyright (c) 2006 - 2017 StackIQ Inc.
# All rights reserved. stacki(r) v4.0 stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @SI_Copyright@
#
# @Copyright@
# Copyright (c) 2000 - 2010 The Regents of the University of California
# All rights reserved. Rocks(r) v5.4 www.rocksclusters.org
# https://github.com/Teradata/stacki/blob/master/LICENSE-ROCKS.txt
# @Copyright@

import stack.file
import stack.commands


class Command(stack.commands.sync.command):
	"""
	For each system configuration file controlled by Stack, first
	rebuild the configuration file by extracting data from the
	database, then restart the relevant services.

	<example cmd='sync config'>
	Rebuild all configuration files and restart relevant services.
	</example>
	"""

	def run(self, params, args):

		self.notify('Sync Config\n')

		self.runPlugins()