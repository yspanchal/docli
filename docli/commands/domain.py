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


def validate_list(ctx, param, value):
	if value:
		if ctx.params.has_key('create'):
			if ctx.params['create']:
				raise click.UsageError('Invalid option combination %s & %s' %(param.name, 'create'))
	return value


def validate_create(ctx, param, value):
	# print ctx.params
	if value:
		if ctx.params.has_key('getlist'):
			if ctx.params['getlist']:
				raise click.UsageError('Invalid option combination %s & %s' %(param.name, 'create'))
	return value


@domain_group.command(context_settings=CONTEXT_SETTINGS)
@click.option('--create', '-c', help='create new sdomain', is_eager=True, callback=validate_create)
@click.option('--getlist', '-l', is_flag=True, help='list all actions', is_eager=True, callback=validate_list)
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def domain(ctx, token, tablefmt, proxy, getlist, create):
	"""
	Domains that you are managing through the DigitalOcean DNS interface.
	"""
	if getlist:
		method = 'GET'
		url = DOMAIN_LIST
		result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
		if result['has_error']:
			click.echo()
			click.echo(result['error_message'])
		else:
			record = 'domain'
			headers = ['Domain Name']
			table = []
			for domain in result['domains']:
				table.append([domain['name']])
			data = {'headers': headers, 'table_data': table}
			print_table(tablefmt, data, record)

	if create:
		print "create"