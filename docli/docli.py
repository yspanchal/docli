# -*- coding: utf-8 -*-

import click
from commands.account import account_group
from commands.actions import actions_group
from commands.domain import domain_group
from commands.records import record_group
from commands.base_request import CONTEXT_SETTINGS

import os

sources_list = [account_group, actions_group, domain_group, record_group]

def config_file(file):
	"""
	create configuration file
	"""
	value = click.prompt('Enter digital ocean access token', type=str)
	f = open(file, 'w')
	f.write('[docli]\nauth_token='+value)
	f.close()
	click.echo()
	click.echo("configuration completed.")


@click.command(cls=click.CommandCollection, sources=sources_list, context_settings=CONTEXT_SETTINGS, invoke_without_command=True, no_args_is_help=True)
@click.option('-c', '--configure', is_flag=True, help='configure digital ocean access token')
def docli(configure):
	"""
	'docli' is Digital Ocean command line interfaces

	# To configure docli

	>>> docli --configure

	or

	# To get list available commands

	>>> docli --help
	"""
	if configure:
		file = os.path.expanduser('~/.do.cfg')
		if not os.path.isfile(file):
			config_file(file)
		else:
			value = click.prompt('Do you want to reconfigure docli [y/n] ?', type=str, default='n')
			if value.lower() == 'y':
				config_file(file)
			else:
				click.echo()
				click.echo('done..!!!')


if __name__ == '__main__':
	docli()