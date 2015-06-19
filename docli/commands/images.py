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


def validate(dic, option_list):
	"""
	images command validation
	"""
	for key in dic.viewkeys():
		if key in option_list:
			for option in option_list:
				if option != key:
					if dic[option] and dic[key]:
						raise click.UsageError('Invalid option combination --%s \
							cannot be used with --%s' % (option, key))

	if (dic['update'] and not dic['name']) or (dic['name'] and not dic['update']):
		raise click.UsageError('--update option requires --name')

	return True


def invoke_list(token, proxy, url):
	"""
	invoke actual request
	"""
	method = 'GET'
	url = url
	result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
	return result


def run_command(token, proxy, record, url, tablefmt):
	"""
	run request and process result
	"""
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
	"""
	get images by id or slug
	"""
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
@click.option('--id', '-I', type=int, help='get image details using image id', metavar='<3812352>')
@click.option('--slug', '-S', type=str, help='get image details using image slug', metavar='<my-image>')
@click.option('--action', '-A', type=int, help='all actions that have been executed on an image', metavar='<3812352>')
@click.option('--update', '-u', type=int, help='update image name for given image id', metavar='<3812352>')
@click.option('--name', '-n', type=str, help='image name to be updated', metavar='<my-fancy-image>')
@click.option('--delete', '-D', type=int, help='delete image for given image id', metavar='<3812352>')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def images(ctx, getlist, distribution, application, private, id, slug, action, update, delete, name, token, tablefmt, proxy):
	"""
	Images in DigitalOcean may refer to one of a few different kinds of objects.
	"""

	if (not ctx.params['getlist'] and not ctx.params['distribution'] 
		and not ctx.params['application'] and not ctx.params['private'] 
		and not ctx.params['id'] and not ctx.params['slug'] and not ctx.params['action'] 
		and not ctx.params['update'] and not ctx.params['name'] and not ctx.params['delete']):
		return click.echo(ctx.get_help())

	option_list = ['getlist', 'distribution', 'application', 'private', 'id', 'slug', 'action', 'update', 'delete']

	if validate(ctx.params, option_list):
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

		if update:
			method = 'PUT'
			url = IMAGES + str(update)
			params = {"name":name}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				has_page = False
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'image update'
				headers = ['Fields', 'Values']
				table = [['Id', result['image']['id']], ['Name', result['image']['name']], 
						['Distribution', result['image']['distribution']], ['Slug', result['image']['slug']], 
						['Public', result['image']['public']], ['Regions', result['image']['regions']], 
						['Created at', result['image']['created_at']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)

		if delete:
			method = 'DELETE'
			url = IMAGES + str(delete)
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				has_page = False
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				click.echo()
				click.echo("Image id %d deleted" % (delete))