# -*- coding: utf-8 -*-

import click
from urls import REGIONS, SIZES
from base_request import DigitalOcean, print_table, CONTEXT_SETTINGS


@click.group()
def region_size_group():
	"""
	region and size command group
	"""
	pass


def validate(dic, option_list):
	"""
	region and size command validation
	"""
	for key in dic.viewkeys():
		if key in option_list:
			for option in option_list:
				if option != key:
					if dic[option] and dic[key]:
						raise click.UsageError('Invalid option combination --%s \
							cannot be used with --%s' % (option, key))

	return True

@region_size_group.command(name='info', context_settings=CONTEXT_SETTINGS)
@click.option('--region', '-r', is_flag=True, help='get list of available regions')
@click.option('--size', '-s', is_flag=True, help='get list of available droplet sizes')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def region_size(ctx, region, size, token, tablefmt, proxy):
	"""
	Get list of regions and droplet sizes available with Digital Ocean
	"""
	if (not ctx.params['region'] and not ctx.params['size']):
		return click.echo(ctx.get_help())

	option_list = ['region', 'size']

	if validate(ctx.params, option_list):
		if region:
			method = 'GET'
			url = REGIONS
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'region list'
				for dic in result['regions']:
					headers = ['Fields', 'Values']
					table = [['Name', dic['name']], ['Slug', dic['slug']], ['Available', dic['available']]]
					data = {'headers': headers, 'table_data': table}
					print_table(tablefmt, data, record)
				total = 'Total regions: %d' % (result['meta']['total'])
				click.echo(total)

		if size:
			method = 'GET'
			url = SIZES
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'size list'
				for dic in result['sizes']:
					headers = ['Fields', 'Values']
					table = [['Slug', dic['slug']], ['Memory', dic['memory']], ['VCPUS', dic['vcpus']], 
					['Disk', dic['disk']], ['Transfer', dic['transfer']], ['Price Monthly', dic['price_monthly']], 
					['Price Hourly', dic['price_hourly']], ['Available', dic['available']]]
					data = {'headers': headers, 'table_data': table}
					print_table(tablefmt, data, record)
				total = 'Total sizes: %d' % (result['meta']['total'])
				click.echo(total)