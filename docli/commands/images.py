# -*- coding: utf-8 -*-

import click
from urls import IMAGES
from base_request import DigitalOcean, print_table, CONTEXT_SETTINGS


@click.group()
def images_group():
	"""
	images command group
	"""
	pass


def validate(dic):
	return True


def invoke_list(token, proxy, url):
	method = 'GET'
	url = url
	result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
	return result


def run_command(token, proxy, record, url, tablefmt):
	page = 1
	has_page = True
	while has_page:
		if '?' in url:
			new_url = url + '&page=%d' % (page)
		else:
			new_url = url + '?page=%d' % (page)
		result = invoke_list(token, proxy, new_url)
		if result['has_error']:
			has_page = False
			click.echo()
			click.echo('Error: %s' %(result['error_message']))
		else:
			headers = ['Fields', 'Values']
			for dic in result['images']:
				table = [['Id', dic['id']], ['Name', dic['name']], ['Distribution', dic['distribution']], 
				['Slug', dic['slug']], ['Public', dic['public']], ['Created at', dic['created_at']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)
			total = 'Total images: %d' % (result['meta']['total'])
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


def image_by_id_slug(token, proxy, record, url, tablefmt):
	result = invoke_list(token, proxy, url)
	if result['has_error']:
		has_page = False
		click.echo()
		click.echo('Error: %s' %(result['error_message']))
	else:
		headers = ['Fields', 'Values']
		table = [['Id', result['image']['id']], ['Name', result['image']['name']], ['Distribution', result['image']['distribution']], 
				['Slug', result['image']['slug']], ['Public', result['image']['public']], ['Created at', result['image']['created_at']]]
		data = {'headers': headers, 'table_data': table}
		print_table(tablefmt, data, record)


@images_group.command(context_settings=CONTEXT_SETTINGS)
@click.option('--getlist', '-l', is_flag=True, help='get list of all images')
@click.option('--distribution', '-d', is_flag=True, help='get list of only distribution images')
@click.option('--application', '-a', is_flag=True, help='get list of only application images')
@click.option('--private', '-P', is_flag=True, help='get list of only users private images')
@click.option('--id', '-I', type=int, help='get image details using image id')
@click.option('--slug', '-S', type=str, help='get image details using image slug')
@click.option('--action', '-A', type=int, help='all actions that have been executed on an image')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def images(ctx, getlist, distribution, application, private, id, slug, action, token, tablefmt, proxy):
	"""
	Images in DigitalOcean may refer to one of a few different kinds of objects.
	"""

	if (not ctx.params['getlist'] and not ctx.params['distribution'] 
		and not ctx.params['application'] and not ctx.params['private'] 
		and not ctx.params['id'] and not ctx.params['slug'] and not ctx.params['action']):
		return click.echo(ctx.get_help())

	if validate(ctx.params):
		if getlist:
			url = IMAGES
			record = 'list images'
			return run_command(token, proxy, record, url, tablefmt)

		if distribution:
			url = IMAGES + '?type=distribution'
			record = 'list distribution images'
			return run_command(token, proxy, record, url, tablefmt)

		if application:
			url = IMAGES + '?type=application'
			record = 'list application images'
			return run_command(token, proxy, record, url, tablefmt)

		if private:
			url = IMAGES + '?private=true'
			record = 'list private images'
			return run_command(token, proxy, record, url, tablefmt)

		if id:
			url = IMAGES + str(id)
			record = 'image by id'
			return image_by_id_slug(token, proxy, record, url, tablefmt)

		if slug:
			url = IMAGES + slug
			record = 'image by slug'
			return image_by_id_slug(token, proxy, record, url, tablefmt)

		if action:
			page = 1
			has_page = True
			while has_page:
				url = IMAGES + str(action) + '/actions?page=%d' % (page)
				result = invoke_list(token, proxy, url)
				if result['has_error']:
					has_page = False
					click.echo()
					click.echo('Error: %s' %(result['error_message']))
				else:
					headers = ['Fields', 'Values']
					for dic in result['actions']:
						table = ['Id', dic['id'], ['Status', dic['status']], ['Type', dic['type']], 
								['Started at', dic['started_at']], ['Completed at', dic['completed_at']], 
								['Resource Type', dic['resource_type']], ['Resource id', dic['resource_id']], 
								['Region', dic['region']]]
						data = {'headers': headers, 'table_data': table}
						print_table(tablefmt, data, record)
					total = 'Total actions: %d' % (result['meta']['total'])
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