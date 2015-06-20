# -*- coding: utf-8 -*-

import click
from commands.account import account_group
from commands.actions import actions_group
from commands.domain import domain_group
from commands.records import record_group
from commands.droplet import droplet_group
from commands.droplet_actions import droplet_actions_group
from commands.images import images_group
from commands.image_actions import image_actions_group
from commands.ssh_keys import ssh_keys_group
from commands.region_size import region_size_group
from commands.base_request import CONTEXT_SETTINGS

import os

sources_list = [account_group, actions_group, domain_group, record_group, 
				droplet_group, droplet_actions_group, images_group, 
				image_actions_group, ssh_keys_group, region_size_group]

def config_file(file, reconfigure=False):
	"""
	create configuration file
	"""
	value = click.prompt('Enter digital ocean access token', type=str)
	f = open(file, 'w')
	f.write('[docli]\nauth_token='+value)
	f.close()
	if not reconfigure:
		bashrc = os.path.expanduser('~/.bashrc')
		bash_profile = os.path.expanduser('~/.bash_profile')
		profile = os.path.expanduser('~/.profile')
		if os.path.isfile(bashrc):
			bashrc_file = open(bashrc, 'a')
			bashrc_file.write('eval "$(_DOCLI_COMPLETE=source docli)"')
			bashrc_file.close()
			click.echo("apply changes by running 'source ~/.bashrc' without ''")
		elif os.path.isfile(bash_profile):
			bash_profile_file = open(bash_profile, 'a')
			bash_profile_file.write('eval "$(_DOCLI_COMPLETE=source docli)"')
			bash_profile_file.close()
			click.echo("apply changes by running 'source ~/.bash_profile' without ''")
		elif os.path.isfile(profile):
			profile_file = open(profile, 'a')
			profile_file.write('eval "$(_DOCLI_COMPLETE=source docli)"')
			profile_file.close()
			click.echo("apply changes by running 'source ~/.profile' without ''")
		else:
			msg = 'Add following line to your bashrc.\n eval "$(_DOCLI_COMPLETE=source docli)"'
			click.echo(msg)
	click.echo()
	click.echo("configuration completed.")


@click.command(cls=click.CommandCollection, sources=sources_list, context_settings=CONTEXT_SETTINGS, invoke_without_command=True, no_args_is_help=True)
@click.option('-c', '--configure', is_flag=True, help='configure digital ocean access token')
@click.version_option(version=1.0, message=('Digital Ocean command line interface. \n%(prog)s, version %(version)s, by Yogesh panchal, yspanchal@gmail.com'))
def docli(configure):
	"""
	'docli' is Digital Ocean command line interfaces

	# To configure docli
	>>> docli --configure

	# To get list available commands
	>>> docli --help

	# How to generate access token
	https://goo.gl/hPkQG7
	"""
	if configure:
		file = os.path.expanduser('~/.do.cfg')
		if not os.path.isfile(file):
			config_file(file)
		else:
			value = click.prompt('Do you want to reconfigure docli [y/n] ?', type=str, default='n')
			if value.lower() == 'y':
				reconfigure = True
				config_file(file, reconfigure)
			else:
				click.echo()
				click.echo('done..!!!')


if __name__ == '__main__':
	docli()