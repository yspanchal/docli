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


def validate(dic, option_list):
	"""
	ssh key command validation
	"""
	for key in dic.viewkeys():
		if key in option_list:
			for option in option_list:
				if option != key:
					if dic[option] and dic[key]:
						raise click.UsageError('Invalid option combination --%s \
							cannot be used with --%s' % (option, key))

	if (dic['create'] and not dic['name'] and not dic['key'])\
	or (dic['name'] and not dic['create'] and not dic['key'])\
	or (dic['key'] and not dic['create'] and not dic['name']):
		raise click.UsageError('Missing option, --create requires --name and \
			--key option')

	if (dic['update'] and not dic['name'] or not dic['key']):
		raise click.UsageError('Missing option, --update requires --name or \
			--key option')

	return True


def invoke_list(token, proxy, page=1):
	"""
	invoke actual request
	"""
	method = 'GET'
	url = KEYS
	result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
	return result


@ssh_keys_group.command(name='ssh-key', context_settings=CONTEXT_SETTINGS)
@click.option('--getlist', '-l', is_flag=True, help='list all ssh keys')
@click.option('--create', '-c', is_flag=True, help='add new ssh key')
@click.option('--name', '-n', type=str, help='name of ssh key', metavar='<My SSH Key>')
@click.option('--key', '-k', type=str, help='public ssh keys string', metavar='<ssh-rsa xxx... >')
@click.option('--retrieve', '-r', type=int, help='retrieve ssh key from id', metavar='<512190>')
@click.option('--update', '-u', type=int, help='update ssh key from id', metavar='<512190>')
@click.option('--delete', '-d', type=int, help='delete ssh key from id', metavar='<512190>')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def ssh_keys(ctx, getlist, create, name, key, retrieve, update, delete, token, 
			tablefmt, proxy):
	"""
	DigitalOcean allows you to add SSH public keys to the interface 
	so that you can embed your public key into a Droplet at the time of creation.
	"""
	if (not ctx.params['getlist'] and not ctx.params['create'] and not ctx.params['name'] 
		and not ctx.params['key'] and not ctx.params['retrieve'] and not ctx.params['update'] 
		and not ctx.params['delete']):
		return click.echo(ctx.get_help())

	option_list = ['getlist', 'create', 'retrieve', 'update', 'delete']

	if validate(ctx.params, option_list):
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
					record = 'ssh key list'
					headers = ['Fields', 'Values']
					for dic in result['ssh_keys']:
						click.echo("-----------------------------------------")
						click.echo("Id: %d" % (dic['id']))
						click.echo("Finger Print: %s" % (dic['fingerprint']))
						click.echo("Public Key: %s" % (dic['public_key']))
						click.echo("Name: %s" % (dic['name']))
						click.echo("-----------------------------------------")
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
				record = 'ssh key create'
				dic = result['ssh_key']
				click.echo("-----------------------------------------")
				click.echo("Id: %d" % (dic['id']))
				click.echo("Finger Print: %s" % (dic['fingerprint']))
				click.echo("Public Key: %s" % (dic['public_key']))
				click.echo("Name: %s" % (dic['name']))
				click.echo("-----------------------------------------")

		if retrieve:
			method = 'GET'
			url = KEYS + str(retrieve)
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				dic = result['ssh_key']
				record = 'ssh key retrieve'
				click.echo("-----------------------------------------")
				click.echo("Id: %d" % (dic['id']))
				click.echo("Finger Print: %s" % (dic['fingerprint']))
				click.echo("Public Key: %s" % (dic['public_key']))
				click.echo("Name: %s" % (dic['name']))
				click.echo("-----------------------------------------")

		if update:
			method = 'PUT'
			url = KEYS + str(update)
			params = {}
			if name:
				params.update({'name':name})
			if key:
				params.update({'public_key':key})

			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'ssh key update'
				dic = result['ssh_key']
				click.echo("-----------------------------------------")
				click.echo("Id: %d" % (dic['id']))
				click.echo("Finger Print: %s" % (dic['fingerprint']))
				click.echo("Public Key: %s" % (dic['public_key']))
				click.echo("Name: %s" % (dic['name']))
				click.echo("-----------------------------------------")

		if delete:
			method = 'DELETE'
			url = KEYS + str(delete)
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				msg = "ssh key id %d deleted." % delete
				click.echo()
				click.echo(msg)