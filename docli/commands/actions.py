# -*- coding: utf-8 -*-

import click
from urls import ACTION_LIST
from base_request import DigitalOcean, print_table, CONTEXT_SETTINGS


@click.group()
def actions_group():
	"""
	action command group
	"""
	pass


def validate(dic, option_list):
	"""
	actions command option validation
	"""
	for key in dic.viewkeys():
		if key in option_list:
			for option in option_list:
				if option != key:
					if dic[option] and dic[key]:
						raise click.UsageError('Invalid option combination --%s \
							cannot be used with --%s' % (option, key))

	return True


def invoke_list(token, proxy, page=1):
	"""
	invoke actual request
	"""
	method = 'GET'
	url = ACTION_LIST + '?page=%d' % (page)
	result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
	return result


@actions_group.command(context_settings=CONTEXT_SETTINGS)
@click.option('--getlist', '-l', is_flag=True, help='list all actions')
@click.option('--getid', '-i', help='get specific actions by id', type=int, metavar='<action_id>')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def action(ctx, getlist, getid, token, proxy, tablefmt):
	"""
	Actions are records of events that have occurred on the resources
	"""
	if not getlist and not getid:
		return click.echo(ctx.get_help())

	option_list = ['getlist', 'getid']

	if validate(ctx.params, option_list):
		if getlist:
			page = 1
			has_page = True
			while has_page:
				result = invoke_list(token, proxy, page)
				if result['has_error']:
					click.echo()
					click.echo('Error: %s' %(result['error_message']))
					has_page = False
				else:
					record = 'action'
					headers = ['Fields', 'Values']
					for dic in result['actions']:
						table = [['Id', dic['id']], ['Status', dic['status']], 
						['Type', click.style(dic['type'], fg='blue')], 
						['Started at', dic['started_at']], 
						['Completed at', dic['completed_at']], 
						['Resource id', dic['resource_id']], 
						['Resource type', dic['resource_type']], 
						['Region', dic['region']['name']], 
						['Size', dic['region']['sizes'][0]]]
						data = {'headers': headers, 'table_data': table}
						print_table(tablefmt, data, record)
					total = 'Total results: %d' % (result['meta']['total'])
					click.echo()
					click.echo(total)
					if result['links']['pages'].has_key('next'):
						page += 1
						value = click.prompt('Do you want to continue ?', type=str, default='n')
						if value.lower() != 'y':
							has_page = False
					else:
						has_page = False

		if getid:
			method = 'GET'
			url = ACTION_LIST + str(getid)
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
				has_page = False
			else:
				record = 'action'
				headers = ['Fields', 'Values']
				dic = result['action']
				table = [['Id', dic['id']], ['Status', dic['status']], 
				['Type', click.style(dic['type'], fg='blue')], 
				['Started at', dic['started_at']], 
				['Completed at', dic['completed_at']], 
				['Resource id', dic['resource_id']], 
				['Resource type', dic['resource_type']], 
				['Region', dic['region']['name']], 
				['Size', dic['region']['sizes'][0]]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)