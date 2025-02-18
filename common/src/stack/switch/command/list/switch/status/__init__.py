# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

from stack.argument_processors.host import HostArgProcessor
from stack.argument_processors.switch import SwitchArgProcessor
import stack.commands
from stack.exception import CommandError
import stack.util

class command(HostArgProcessor, SwitchArgProcessor, stack.commands.list.command):
	pass

class Command(command):
	"""
	List Port, Speed, State of the switch  and Mac, VLAN, Hostname, and interface
	about each port on the switch.

	<arg optional='1' type='string' name='switch' repeat='1'>
	Zero, one or more switch names. If no switch names are supplies, info about
	all the known switches is listed.
	</arg>

	<example cmd='list switch status switch-0-0'>
	List status info for switch-0-0.
	</example>

	<example cmd='list switch status'>
	List status info for all known switches/
	</example>
	"""
	def run(self, params, args):

		_switches = self.getSwitchNames(args)
		self.beginOutput()
		for switch in self.call('list.host.interface', _switches):

			switch_name = switch['host']
			model = self.getHostAttr(switch_name, 'component.model')
			self.runImplementation(model, [switch])

		self.endOutput(header=['switch', 'port',  'speed', 'state', 'mac', 'vlan', 'host', 'interface'])
