import json
from textwrap import dedent


class TestRemoveAccess:
	def test_no_args(self, host):
		result = host.run('stack remove access')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "command" parameter is required
			{command=string} {group=string}
		''')

	def test_no_command(self, host):
		result = host.run('stack remove access group=apache')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "command" parameter is required
			{command=string} {group=string}
		''')

	def test_no_group(self, host):
		result = host.run('stack remove access command="*"')
		assert result.rc == 255
		assert result.stderr == dedent('''\
			error - "group" parameter is required
			{command=string} {group=string}
		''')

	def test_invalid_group(self, host):
		result = host.run('stack remove access command="*" group=test')
		assert result.rc == 255
		assert result.stderr == 'error - cannot find group test\n'

	def test_group_name(self, host):
		# Remove the default apache group access
		result = host.run('stack remove access command="*" group=apache')
		assert result.rc == 0

		# Confirm it is gone
		result = host.run('stack list access output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [
			{
				'command': '*',
				'group': 'root'
			},
			{
				'command': 'list*',
				'group': 'wheel'
			},
			{
				'command': 'list *',
				'group': 'nobody'
			}
		]

	def test_group_id(self, host):
		# Get the apache group id
		gid = host.group('apache').gid

		# Remove the default apache group access
		result = host.run(f'stack remove access command="*" group={gid}')
		assert result.rc == 0

		# Confirm it is gone
		result = host.run('stack list access output-format=json')
		assert result.rc == 0
		assert json.loads(result.stdout) == [
			{
				'command': '*',
				'group': 'root'
			},
			{
				'command': 'list*',
				'group': 'wheel'
			},
			{
				'command': 'list *',
				'group': 'nobody'
			}
		]
