import json
from textwrap import dedent


class TestAddBootaction:
	def test_no_args(self, host):
		result = host.run('stack add bootaction')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "action" argument is required
			{action} [args=string] [kernel=string] [os=string] [ramdisk=string] [type=string]
		''')

	def test_multiple_args(self, host):
		result = host.run('stack add bootaction test foo')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "action" argument must be unique
			{action} [args=string] [kernel=string] [os=string] [ramdisk=string] [type=string]
		''')

	def test_no_type(self, host):
		result = host.run('stack add bootaction test')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "type" parameter is required
			{action} [args=string] [kernel=string] [os=string] [ramdisk=string] [type=string]
		''')

	def test_invalid_type(self, host):
		result = host.run('stack add bootaction test type=foo')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "type" parameter must be "os" or "install"
			{action} [args=string] [kernel=string] [os=string] [ramdisk=string] [type=string]
		''')

	def test_no_kernel(self, host):
		result = host.run('stack add bootaction test type=os')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "kernel" parameter is required
			{action} [args=string] [kernel=string] [os=string] [ramdisk=string] [type=string]
		''')

	def test_existing(self, host):
		result = host.run('stack add bootaction memtest type=os kernel="kernel memtest"')
		assert result.rc == 255
		assert result.stderr == 'error - action "memtest" exists\n'

	def test_default_os(self, host, host_os):
		# Add an install bootaction that will get the default os
		result = host.run('stack add bootaction test type=install kernel=""')
		assert result.rc == 0

		# Make sure the action got added
		result = host.run('stack list bootaction test output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [
			{
				'args': None,
				'bootaction': 'test',
				'kernel': None,
				'os': host_os,
				'ramdisk': None,
				'type': 'install'
			}
		]

	def test_with_os(self, host):
		# Add an os bootaction with a specified os
		result = host.run('stack add bootaction test type=os os=ubuntu kernel=""')
		assert result.rc == 0

		# Make sure the action got added
		result = host.run('stack list bootaction test output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [
			{
				'args': None,
				'bootaction': 'test',
				'kernel': None,
				'os': 'ubuntu',
				'ramdisk': None,
				'type': 'os'
			}
		]

	def test_os_is_null(self, host):
		# Add an os bootaction with a null os
		result = host.run('stack add bootaction test type=os kernel=""')
		assert result.rc == 0

		# Make sure the action got added
		result = host.run('stack list bootaction test output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [
			{
				'args': None,
				'bootaction': 'test',
				'kernel': None,
				'os': None,
				'ramdisk': None,
				'type': 'os'
			}
		]

	def test_existing_bootname(self, host):
		# Add an os bootaction with an existing bootname
		result = host.run('stack add bootaction memtest type=os os=ubuntu kernel=""')
		assert result.rc == 0

		# Make sure the action got added
		result = host.run('stack list bootaction memtest output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [
			{
				'args': None,
				'bootaction': 'memtest',
				'kernel': 'kernel memtest',
				'os': None,
				'ramdisk': None,
				'type': 'os'
			},
			{
				'args': None,
				'bootaction': 'memtest',
				'kernel': None,
				'os': 'ubuntu',
				'ramdisk': None,
				'type': 'os'
			}
		]
