# -*- coding: utf-8 -*-

import click
from urls import KEYS
from base_request import DigitalOcean, print_table, CONTEXT_SETTINGS


@click.group()
def ssh_keys_group():
	"""
	ssh keys command group
	"""
	pass


def validate(dic):
	return True


def invoke_list(token, proxy, page=1):
	method = 'GET'
	url = KEYS
	result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
	return result


@ssh_keys_group.command(name='ssh-key', context_settings=CONTEXT_SETTINGS)
@click.option('--getlist', '-l', is_flag=True, help='list all ssh keys')
@click.option('--create', '-c', is_flag=True, help='add new ssh key')
@click.option('--name', '-n', type=str, help='name of ssh key', metavar='<My SSH Key>')
@click.option('--key', '-k', type=str, help='public ssh keys string', metavar='<ssh-rsa xxx... >')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def ssh_keys(ctx, getlist, create, name, key, token, tablefmt, proxy):
	"""
	DigitalOcean allows you to add SSH public keys to the interface 
	so that you can embed your public key into a Droplet at the time of creation.
	"""
	if (not ctx.params['getlist'] and not ctx.params['create'] and not ctx.params['name'] 
		and not ctx.params['key']):
		return click.echo(ctx.get_help())

	if validate(ctx.params):
		if getlist:
			page = 1
			has_page = True
			while has_page:
				url = KEYS
				result = invoke_list(token, proxy, page)
				if result['has_error']:
					has_page = False
					click.echo()
					click.echo('Error: %s' %(result['error_message']))
				else:
					headers = ['Fields', 'Values']
					for dic in result['ssh_keys']:
						table = [['Id', dic['id']], ['Finger Print', dic['fingerprint']], ['Public Key', dic['public_key']], 
						['Name', dic['name']]]
						data = {'headers': headers, 'table_data': table}
						print_table(tablefmt, data, record)
					total = 'Total ssh keys: %d' % (result['meta']['total'])
					click.echo(total)
					if result['links'].has_key('pages'):
						if result['links']['pages'].has_key('next'):
							page += 1
							value = click.prompt('Do you want to continue ?', type=str, default='n')
							if value.lower() != 'y':
								has_page = False
						else:
							has_page = False
					else:
						has_page = False

		if create:
			method = 'POST'
			url = KEYS
			params = {'name':name, 'public_key':key}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				headers = ['Fields', 'Values']
				table = [['Id', result['ssh_key']['id']], ['Finger Print', result['ssh_key']['fingerprint']], ['Public Key', result['ssh_key']['public_key']], ['Name', result['ssh_key']['name']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)