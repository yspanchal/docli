# -*- coding: utf-8 -*-

import click
from urls import DROPLETS
from base_request import DigitalOcean, print_table, CONTEXT_SETTINGS


@click.group()
def droplet_group():
	"""
	droplet command group
	"""
	pass


def validate(dic):
	return True


def invoke_list(token, proxy, url):
	method = 'GET'
	url = url
	result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
	return result


@droplet_group.command(context_settings=CONTEXT_SETTINGS)
@click.option('--create', '-c', is_flag=True, help='create new droplet')
@click.option('--getlist', '-l', is_flag=True, help='get list of all droplets')
@click.option('--retrieve', '-R', type=int, help='retrieve an existing Droplet by id', metavar='<3812352>')
@click.option('--kernel', '-k', type=int, help='List all available kernels for a droplet', metavar='<3812352>')
@click.option('--name', '-n', type=str, help='The human-readable string used when displaying the Droplet name.', metavar='<example.com>')
@click.option('--region', '-r', type=str, help='The region that you wish to deploy in.', metavar='<nyc1>')
@click.option('--size', '-s', type=str, help='The size that you wish to select for this Droplet.', metavar='<1gb>')
@click.option('--image', '-i', type=str, help='The image ID of a public or private image.', metavar='<ubuntu-14-04-x64>')
@click.option('--sshkeys', '-S', type=str, help='Comma seperated IDs of the SSH keys to embed in the Droplet', nargs=10, metavar='<home, office>')
@click.option('--backup', '-b', help='A boolean indicating whether automated backups should be enabled.', default=False)
@click.option('--ipv6', '-I', help='A boolean indicating whether IPv6 is enabled.', default=False)
@click.option('--private_networking', '-P', help='A boolean indicating whether private networking is enabled.', default=False)
@click.option('--user_data', '-u', type=str, help='A string of the desired User Data for the Droplet.')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def droplet(ctx, create, getlist, retrieve, kernel, name, region, size, image, sshkeys, backup, ipv6, private_networking, user_data, token, tablefmt, proxy):
	"""
	A Droplet is a DigitalOcean virtual machine. you can list, create, or delete Droplets.
	"""
	if (not ctx.params['create'] and not ctx.params['getlist'] and not ctx.params['retrieve'] and not ctx.params['kernel'] and not ctx.params['name'] and not ctx.params['region'] and not ctx.params['size'] and not ctx.params['image'] and not ctx.params['sshkeys'] and not ctx.params['backup'] and not ctx.params['ipv6'] and not ctx.params['private_networking'] and not ctx.params['user_data']):
		return click.echo(ctx.get_help())

	if validate(ctx.params):
		if create:
			method = 'POST'
			url = DROPLETS
			params = {'name': name, 'region': region, 'size': size, 'image': image, 'ssh_keys': sshkeys, 'backups': backup, 'ipv6': ipv6, 'private_networking': private_networking, 'user_data': user_data}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'droplet create'
				click.echo()
				click.echo("Creating Your Droplet ", name)
				click.echo()
				headers = ['Fields', 'Values']
				table = [['Id', result['droplet']['id']], ['Name', result['droplet']['name']], ['Memory', result['droplet']['memory']], ['Vcpus', result['droplet']['vcpus']], ['Disk', result['droplet']['disk']], ['Locked', result['droplet']['locked']], ['Status', result['droplet']['status']], ['Kernal Id', result['droplet']['kernel']['id']], ['Kernel Name', result['droplet']['kernel']['name']], ['Kernel Version', result['droplet']['kernel']['version']], ['Created At', result['droplet']['created_at']], ['Features', result['droplet']['features']], ['Backup Id', result['droplet']['backup_ids']], ['SnapShot Id', result['droplet']['snapshot_ids']], ['Network', result['droplet']['networks']], ['Region', result['droplet']['region']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)

		if getlist:
			page = 1
			has_page = True
			while has_page:
				url = DROPLETS + '?page=%d' % (page)
				result = invoke_list(token, proxy, url)
				if result['has_error']:
					click.echo()
					click.echo('Error: %s' %(result['error_message']))
				else:
					record = 'droplet list'
					headers = ['Fields', 'Values']
					for dic in result['droplets']:
						droplet_id = dic['id']
						name = dic['name']
						memory = dic['memory']
						created_at = dic['created_at']
						if dic['networks']['v4']:
							network_v4 = dic['networks']['v4'][0]['ip_address']
						else:
							network_v4 = None

						if dic['networks']['v6']:
							network_v6 = dic['networks']['v6'][0]['ip_address']
						else:
							network_v6 = None

						table = [['Id', droplet_id], ['Name', name], ['Memory', memory], ['Created At', created_at], ['Network V4', network_v4], ['Network V6', network_v6]]
						data = {'headers': headers, 'table_data': table}
						print_table(tablefmt, data, record)
					total = 'Total droplets: %d' % (result['meta']['total'])
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

		if retrieve:
			method = 'GET'
			url = DROPLETS + str(retrieve)
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'retrieve droplet'
				headers = ['Fields', 'Values']
				droplet_id = result['droplet']['id']
				name = result['droplet']['name']
				memory = result['droplet']['memory']
				vcpus = result['droplet']['vcpus']
				disk = result['droplet']['disk']
				locked = result['droplet']['locked']
				status = result['droplet']['status']
				kernel_id = result['droplet']['kernel']['id']
				kernel_name = result['droplet']['kernel']['name']
				kernel_version = result['droplet']['kernel']['version']
				created_at = result['droplet']['created_at']
				features = result['droplet']['features']
				backup_ids = result['droplet']['backup_ids']
				snapshot_ids = result['droplet']['snapshot_ids']
				if result['droplet']['networks']['v4']:
					network_v4 = result['droplet']['networks']['v4'][0]['ip_address']
				else:
					network_v4 = None

				if result['droplet']['networks']['v6']:
					network_v6 = result['droplet']['networks']['v6'][0]['ip_address']
				else:
					network_v6 = None
				region = result['droplet']['region']['name']
				available = result['droplet']['region']['available']
				table = [['Id', droplet_id],['Name', name],['Memory', memory],['Vcpus', vcpus],['Disk', disk],['Locked', locked],['Status', status],['Kernel Id', kernel_id],['Kernel Name', kernel_name],['Kernel Version', kernel_version],['Created At', created_at],['Features', features],['Backup Id', backup_ids],['SnapShot Id', snapshot_ids],['Network V4', network_v4],['Network V6', network_v6],['Region', region],['Available', available]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)

		if kernel:
			page = 1
			has_page = True
			while has_page:
				url = DROPLETS + str(kernel) + '/kernels?page=%d' % (page)
				result = invoke_list(token, proxy, url)
				if result['has_error']:
					click.echo()
					click.echo('Error: %s' %(result['error_message']))
				else:
					record = "droplet kernel"
					headers = ['Kernel Id', 'Kernel Name', 'Kernel Version']
					table = []
					for dic in result['kernels']:
						table_list = [dic['id'], dic['name'], dic['version']]
						table.append(table_list)
					data = {'headers': headers, 'table_data': table}
					print_table(tablefmt, data, record)
					total = 'Total kernels: %d' % (result['meta']['total'])
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