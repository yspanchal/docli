# -*- coding: utf-8 -*-

import click
from urls import DOMAIN_LIST
from base_request import DigitalOcean, print_table, CONTEXT_SETTINGS


@click.group()
def record_group():
	"""
	record command group
	"""
	pass


def validate(dic):

	return True

@record_group.command(context_settings=CONTEXT_SETTINGS)
@click.option('--getlist', '-l', type=str, help='list all domain records', metavar='<example.com>')
@click.option('--create', '-c', type=str, help='create new domain record', metavar='<example.com>')
@click.option('--delete', '-r', type=str, help='delete existing domain record', metavar='<example.com>')
@click.option('--update', '-u', type=str, help='update existing domain record', metavar='<example.com>')
@click.option('--type', '-y', type=str, help='The record type (A, MX, CNAME, etc)', metavar='<type>')
@click.option('--name', '-n', type=str, help='The host name, alias, or service being defined by the record', metavar='<name>')
@click.option('--data', '-w', type=str, help='Variable data depending on record type', metavar='<data>')
@click.option('--priority', '-x', type=int, help='The priority of the host', default='null', metavar='<priority>')
@click.option('--port', '-P', type=int, help='The port that the service is accessible on', default='null', metavar='<port>')
@click.option('--weight', '-g', type=int, help='The weight of records with the same priority', default='null', metavar='<weight>'))
@click.option('--recordid', '-i', type=str, help='The record id to be updated', metavar='<3352896>')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def record(ctx, token, tablefmt, proxy, getlist, create, recordid, delete, update, type, name, data, priority, port, weight):
	"""
	Individual DNS records configured for a domain.
	"""
	if not ctx.params['getlist'] and not ctx.params['create'] and not ctx.params['delete'] and not ctx.params['update']:
		click.echo(ctx.get_help())

	if validate(ctx.params):
		if getlist:
			method = 'GET'
			url = DOMAIN_LIST + getlist + '/records'
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'action'
				headers = ['Fields', 'Values']
				for dic in result['domain_records']:
					table = [['Id', dic['id']], ['Type', dic['type']], ['Name', dic['name']], ['Data', dic['data']], ['Priority', dic['priority']], ['Port', dic['port']], ['Weight', dic['weight']]]
					data = {'headers': headers, 'table_data': table}
					print_table(tablefmt, data, record)
				total = 'Total results: %d' % (result['meta']['total'])
				click.echo()
				click.echo(total)

		if create:
			method = 'POST'
			url = DOMAIN_LIST + create + '/records'
			params = {'type': type, 'name': name, 'data': data, 'priority': priority, 'port': port, 'weight': weight}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				click.echo()
				click.echo("Domain record added for ", create)
				click.echo()
				headers = ['Fields', 'Values']
				table = [['Id', result['domain_record']['id']], ['Type', result['domain_record']['type']], ['Name', result['domain_record']['name']], ['Data', result['domain_record']['data']], ['Priority', result['domain_record']['priority']], ['Port', result['domain_record']['port']], ['Weight', result['domain_record']['weight']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)

		if update:
			method = 'PUT'
			url = DOMAIN_LIST + update + '/records/' + recordid
			params = {}
			if name:
				params.update({'name': name})

			if type:
				params.update({'type': type})

			if data:
				params.update({'data': data})

			if priority:
				params.update({'priority': priority})

			if port:
				params.update({'port': port})

			if weight:
				params.update({'weight': weight})

			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				click.echo()
				click.echo("Domain record updated for ", update)
				click.echo()
				headers = ['Fields', 'Values']
				table = [['Id', result['domain_record']['id']], ['Type', result['domain_record']['type']], ['Name', result['domain_record']['name']], ['Data', result['domain_record']['data']], ['Priority', result['domain_record']['priority']], ['Port', result['domain_record']['port']], ['Weight', result['domain_record']['weight']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)

		if delete:
			method = 'DELETE'
			url = DOMAIN_LIST + delete + '/records/' + recordid
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				click.echo()
				click.echo("Domain %s record id %s deleted" %(delete, recordid))