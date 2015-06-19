# -*- coding: utf-8 -*-

import click
from urls import DOMAIN_LIST
from base_request import DigitalOcean, print_table, CONTEXT_SETTINGS


@click.group()
def domain_group():
	"""
	domain command group
	"""
	pass


def validate(dic, option_list):
	"""
	domain command option validation
	"""
	for key in dic.viewkeys():
		if key in option_list:
			for option in option_list:
				if option != key:
					if dic[option] and dic[key]:
						raise click.UsageError('Invalid option combination --%s \
							cannot be used with --%s' % (option, key))

	if dic['getlist'] and dic['name']:
		raise click.UsageError('Invalid option combination --getlist cannot be \
			used with --name')

	if dic['getlist'] and dic['ip']:
		raise click.UsageError('Invalid option combination --getlist cannot be \
			used with --ip')

	if dic['name'] and dic['detail']:
		raise click.UsageError('Invalid option combination --name or -n cannot be \
			used with --detail')

	if dic['ip'] and dic['detail']:
		raise click.UsageError('Invalid option combination --ip or -i cannot be \
			used with --detail')

	if dic['name'] and dic['delete']:
		raise click.UsageError('Invalid option combination --name or -n cannot be \
			used with --delete')

	if dic['ip'] and dic['delete']:
		raise click.UsageError('Invalid option combination --ip or -i cannot be \
			used with --delete')

	if dic['create'] and dic['ip'] and not dic['name']:
		raise click.UsageError('--name or -n domain name missing')

	if dic['create'] and dic['name'] and not dic['ip']:
		raise click.UsageError('--ip or -i domain ip missing')

	if dic['name'] and not dic['create']:
		raise click.UsageError('--create or -c domain create option missing')

	if dic['ip'] and not dic['create']:
		raise click.UsageError('--create or -c domain create option missing')

	return True


@domain_group.command(context_settings=CONTEXT_SETTINGS)
@click.option('--getlist', '-l', is_flag=True, help='list all actions', is_eager=True)
@click.option('--create', '-c', is_flag=True, help='create new domain', is_eager=True)
@click.option('--name', '-n', type=str, help='domain name entry', metavar='<example.com>')
@click.option('--ip', '-i', type=str, help='ip address for domain', metavar='<1.2.3.4>')
@click.option('--detail', '-d', type=str, help='get details of existing domain name', metavar='<example.com>')
@click.option('--delete', '-r', type=str, help='delete existing domain name', metavar='<example.com>')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def domain(ctx, token, tablefmt, proxy, getlist, create, name, ip, detail, delete):
	"""
	Domains that you are managing through the DigitalOcean DNS interface.
	"""
	if (not ctx.params['getlist'] and not ctx.params['create'] 
		and not ctx.params['name'] and not ctx.params['ip'] 
		and not ctx.params['detail'] and not ctx.params['delete']):
		return click.echo(ctx.get_help())

	option_list = ['getlist', 'create', 'detail', 'delete']

	if validate(ctx.params, option_list):
		if getlist:
			method = 'GET'
			url = DOMAIN_LIST
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'domain'
				headers = ['Domain Name']
				table = []
				for domain in result['domains']:
					table.append([domain['name']])
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)

		if create:
			method = 'POST'
			url = DOMAIN_LIST
			params = {'name': name, 'ip_address': ip}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				click.echo()
				click.echo("Domain Created ", name)
				click.echo()

		if detail:
			method = 'GET'
			url = DOMAIN_LIST + detail
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				click.echo()
				click.echo("name: %s" %(result['domain']['name']))
				click.echo("ttl: %s" %(result['domain']['ttl']))
				click.echo("zone file: %s" %(result['domain']['zone_file']))

		if delete:
			method = 'DELETE'
			url = DOMAIN_LIST + delete
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				click.echo()
				click.echo("Domain %s deleted" %(delete))