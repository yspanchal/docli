# -*- coding: utf-8 -*-

import click
from urls import IMAGES
from base_request import DigitalOcean, print_table, CONTEXT_SETTINGS


@click.group()
def image_actions_group():
	"""
	image actions command group
	"""
	pass


def validate(dic, option_list):
	"""
	image actions command validation
	"""
	for key in dic.viewkeys():
		if key in option_list:
			for option in option_list:
				if option != key:
					if dic[option] and dic[key]:
						raise click.UsageError('Invalid option combination --%s \
							cannot be used with --%s' % (option, key))

	if (dic['transfer'] and not dic['region']) or (dic['region'] and not dic['transfer']):
		raise click.UsageError('--transfer option requires --region')

	if (dic['action'] and not dic['action_id']) or (dic['action_id'] and not dic['action']):
		raise click.UsageError('--action option requires --action-id')

	return True


def run_command(token, proxy, image_id, params, record):
	"""
	run command and process result
	"""
	method = 'POST'
	url = IMAGES + str(image_id) + '/actions'
	result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
	if result['has_error']:
		click.echo()
		click.echo('Error: %s' %(result['error_message']))
	else:
		headers = ['Fields', 'Values']
		table = [['Id', result['action']['id']], ['Status', result['action']['status']], 
		['Type', result['action']['type']], ['Started at', result['action']['started_at']], 
		['Completed at', result['action']['completed_at']], 
		['Resource Id', result['action']['resource_id']], 
		['Resource Type', result['action']['resource_type']], 
		['Region', result['action']['region']]]
		data = {'headers': headers, 'table_data': table}
		cmd = 'Command: docli image-actions -a %d -i %d' % (image_id, result['action']['id'])
		print_table(tablefmt, data, record)
		click.echo()
		click.echo('To get status update of above action execute following command.')
		click.echo(cmd)


@image_actions_group.command(name='image-actions', context_settings=CONTEXT_SETTINGS)
@click.option('--transfer', '-T', type=int, help='transfer given image id to region', metavar='<3812352>')
@click.option('--region', '-r', type=click.Choice(['nyc1', 'nyc2', 'nyc3', 'ams1', 'ams2', 'ams3', 'sfo1', 'sgp1', 'lon1', 'fra1']), help='transfer image to given region',  metavar='<nyc1>')
@click.option('--convert', '-c', type=int, help='convert given image id', metavar='<3812352>')
@click.option('--action', '-a', type=int, help='get action details for given image id', metavar='<3812352>')
@click.option('--action-id', '-i', type=int, help='get action details from given action id', metavar='<3812352>')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def image_actions(ctx, transfer, region, convert, action, action_id, token, tablefmt, proxy):
	"""
	Image actions are commands that can be given to a DigitalOcean image.
	"""
	if (not ctx.params['transfer'] and not ctx.params['region'] 
		and not ctx.params['convert'] and not ctx.params['action'] 
		and not ctx.params['action_id']):
		return click.echo(ctx.get_help())

	option_list = ['transfer','convert','action']

	if validate(ctx.params, option_list):
		if transfer:
			params = {"type":"transfer","region":region}
			record = 'image transfer'
			return run_command(token, proxy, transfer, params, record)

		if convert:
			params = {"type":"convert"}
			record = 'image convert'
			return run_command(token, proxy, convert, params, record)

		if action:
			method = 'GET'
			url = IMAGES + str(action) + '/' + str(action_id)
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'image action'
				headers = ['Fields', 'Values']
				dic = result['action']
				table = [['Id', dic['id']], ['Status', dic['status']], 
				['Type', click.style(dic['type'], fg='blue')], 
				['Started at', dic['started_at']], 
				['Completed at', dic['completed_at']], 
				['Resource id', dic['resource_id']], 
				['Resource type', dic['resource_type']], 
				['Region', dic['region']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)