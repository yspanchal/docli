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


@droplet_group.command(context_settings=CONTEXT_SETTINGS)
@click.option('--create', '-c', is_flag=True, help='create new droplet')
@click.option('--name', '-n', type=str, help='The human-readable string used when displaying the Droplet name.', metavar='<example.com>')
@click.option('--region', '-r', type=str, help='The region that you wish to deploy in.', metavar='<nyc1>')
@click.option('--size', '-s', type=str, help='The size that you wish to select for this Droplet.', metavar='<1gb>')
@click.option('--image', '-i', type=str, help='The image ID of a public or private image.', metavar='<ubuntu-14-04-x64>')
@click.option('--sshkeys', '-S', type=str, help='Comma seperated IDs of the SSH keys to embed in the Droplet', nargs=-1, metavar='<home, office>')
@click.option('--backup', '-b', help='A boolean indicating whether automated backups should be enabled.', default=False)
@click.option('--ipv6', '-I', help='A boolean indicating whether IPv6 is enabled.', default=False)
@click.option('--private_networking', '-P', help='A boolean indicating whether private networking is enabled.', default=False)
@click.option('--user_data', '-u', type=str, help='A string of the desired User Data for the Droplet.')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def droplet(ceate, token, tablefmt, proxy):
	"""
	A Droplet is a DigitalOcean virtual machine. you can list, create, or delete Droplets.
	"""
	if not ctx.params['create'] and not ctx.params['name'] and ctx.params['region'] and not ctx.params['size'] and not ctx.params['image'] and not ctx.params['sshkeys'] and not ctx.params['backup'] and not ctx.params['ipv6'] and not ctx.params['private_networking'] and not ctx.params['user_data']:
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