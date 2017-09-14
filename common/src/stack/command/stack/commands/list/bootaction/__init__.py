# @SI_Copyright@
# Copyright (c) 2006 - 2017 StackIQ Inc.
# All rights reserved. stacki(r) v4.0 stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @SI_Copyright@

import stack.commands


class Command(stack.commands.list.command):
	"""
	Lists the available PXE OS Install targets.
	"""

	def run(self, params, args):

		(req_type, req_os) = self.fillParams([
			('type', None),
			('os', None)])

		self.beginOutput()

		for (b_action, b_type, b_os, b_kernel, b_ramdisk, b_args) in self.db.select(
				"""
				bn.name, bn.type, o.name, ba.kernel, ba.ramdisk, ba.args from 
				bootactions ba 
				inner join bootnames bn on ba.bootname = bn.id 
				left join oses o on ba.os = o.id
				"""):

			if req_type == '':
				if b_type is not None:
					continue
			elif req_type and req_type != b_type:
				continue

			if req_os == '':
				if b_os is not None:
					continue
			elif req_os and req_os != b_os:
				continue

			if args and b_action not in args:
				continue
			
			self.addOutput(b_action, (b_type, b_os, b_kernel, b_ramdisk, b_args))

		self.endOutput(header=[ 'bootaction', 'type', 'os', 'kernel', 'ramdisk', 'args'])
