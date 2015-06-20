# -*- coding: utf-8 -*-

import click
from urls import DROPLETS
from base_request import DigitalOcean, print_table, CONTEXT_SETTINGS


@click.group()
def droplet_actions_group():
	"""
	droplet actions command group
	"""
	pass


def validate(dic, option_list):
	"""
	droplet actions command validation
	"""
	for key in dic.viewkeys():
		if key in option_list:
			for option in option_list:
				if option != key:
					if dic[option] and dic[key]:
						raise click.UsageError('Invalid option combination --%s \
							cannot be used with --%s' % (option, key))

	if (dic['restore'] and not dic['backup_id']) \
		or (dic['backup_id'] and not dic['restore']):
		raise click.UsageError('--restore option requires --backup-id')

	if (dic['resize'] and not dic['size']) or (dic['size'] and not dic['resize']):
		raise click.UsageError('--resize option requires --size')

	if (dic['rebuild'] and not dic['image']) or (dic['image'] and not dic['rebuild']):
		raise click.UsageError('--rebuild option requires --image')

	if (dic['rename'] and not dic['name']) or (dic['name'] and not dic['rename']):
		raise click.UsageError('--rename option requires --name')

	if (dic['change_kernel'] and not dic['kernel']) \
		or (dic['kernel'] and not dic['change_kernel']):
		raise click.UsageError('--change-kernel option requires --kernel')

	if (dic['snapshot'] and not dic['sname']) \
		or (dic['sname'] and not dic['snapshot']):
		raise click.UsageError('--snapshot option requires --sname')

	return True


def run_command(droplet_id, params, record, token, proxy, tablefmt):
	"""
	run command and process result
	"""
	method = 'POST'
	url = DROPLETS + str(droplet_id) + '/actions'
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
		print_table(tablefmt, data, record)
		click.echo()
		click.echo('To get status update of above action execute following command.')
		click.echo('Command: docli action -i %d' % droplet_id)


@droplet_actions_group.command(name='droplet-actions', context_settings=CONTEXT_SETTINGS)
@click.option('--disable-backups', '-d', type=int, help='Disable backups for given droplet id', metavar='<3812352>')
@click.option('--reboot', '-r', type=int, help='Reboot droplet for given droplet id', metavar='<3812352>')
@click.option('--power-cycle', '-P', type=int, help='Power cycle droplet for given droplet id', metavar='<3812352>')
@click.option('--shutdown', '-s', type=int, help='Shutdown droplet for given droplet id', metavar='<3812352>')
@click.option('--power-off', '-O', type=int, help='Power Off droplet for given droplet id', metavar='<3812352>')
@click.option('--power-on', '-o', type=int, help='Power On droplet for given droplet id', metavar='<3812352>')
@click.option('--password-reset', '-w', type=int, help='Password Reset droplet for given droplet id', metavar='<3812352>')
@click.option('--ipv6', '-v', type=int, help='Enable ipv6 for given droplet id', metavar='<3812352>')
@click.option('--private-networking', '-n', type=int, help='Enable private networking for given droplet id', metavar='<3812352>')
@click.option('--upgrade', '-u', type=int, help='Upgrade droplet for given droplet id', metavar='<3812352>')
@click.option('--restore', '-R', type=int, help='Restore droplet from backup for given droplet id', metavar='<3812352>')
@click.option('--backup-id', '-b', type=int, help='Restore droplet from given backup id', metavar='<1214392>')
@click.option('--resize', '-z', type=int, help='Resize droplet for given droplet id', metavar='<3812352>')
@click.option('--size', '-S', type=click.Choice(['512mb', '1gb', '2gb', '4gb', '8gb', '16gb', '32gb', '48gb', '64gb']), help='Resize droplet from given size', metavar='<1214392>')
@click.option('--rebuild', '-B', type=int, help='Rebuild droplet from image for given droplet id', metavar='<3812352>')
@click.option('--image', '-i', type=str, help='Rebuild droplet from given image id or slug', metavar='<1214392 or ubuntu-14-04-x64>')
@click.option('--rename', '-m', type=int, help='Rename droplet for given droplet id', metavar='<3812352>')
@click.option('--name', '-N', type=str, help='Rename droplet from given name', metavar='<example-server>')
@click.option('--change-kernel', '-c', type=int, help='Change droplet kernel for given droplet id', metavar='<3812352>')
@click.option('--kernel', '-k', type=int, help='Change droplet kernel from given kernel id', metavar='<199>')
@click.option('--snapshot', '-a', type=int, help='Create snapshot of droplet for given droplet id', metavar='<3812352>')
@click.option('--sname', '-A', type=str, help='Snapshot name for given droplet', metavar='<example-server>')
@click.option('--token', '-t', type=str, help='digital ocean authentication token', metavar='<token>')
@click.option('--tablefmt', '-f', type=click.Choice(['fancy_grid', 'simple', 'plain', 'grid', 'pipe', 'orgtbl', 'psql', 'rst', 'mediawiki', 'html', 'latex', 'latex_booktabs', 'tsv']), help='output table format', default='fancy_grid', metavar='<format>')
@click.option('--proxy', '-p', help='proxy url to be used for this call', metavar='<http://ip:port>')
@click.pass_context
def droplet_actions(ctx, disable_backups, reboot, power_cycle, shutdown, power_off,
					power_on, password_reset, ipv6, private_networking, upgrade,
					restore, backup_id, resize, size, rebuild, image, rename, name,
					change_kernel, kernel, snapshot, sname, token, tablefmt, proxy):
	"""
	Droplet actions are tasks that can be executed on a Droplet.
	These can be things like rebooting, resizing, snapshotting, etc.
	"""

	if (not ctx.params['disable_backups'] and not ctx.params['reboot'] 
		and not ctx.params['power_cycle'] and not ctx.params['shutdown'] 
		and not ctx.params['power_off'] and not ctx.params['power_on'] 
		and not ctx.params['password_reset'] and not ctx.params['ipv6'] 
		and not ctx.params['private_networking'] and not ctx.params['upgrade'] 
		and not ctx.params['restore'] and not ctx.params['backup_id'] 
		and not ctx.params['resize'] and not ctx.params['size'] 
		and not ctx.params['rebuild'] and not ctx.params['image'] 
		and not ctx.params['rename'] and not ctx.params['name'] 
		and not ctx.params['change_kernel'] and not ctx.params['kernel'] 
		and not ctx.params['snapshot'] and not ctx.params['sname']):
		return click.echo(ctx.get_help())

	option_list = ['disable_backups', 'reboot', 'power_cycle', 'shutdown', 'power_off',
	 'power_on', 'password_reset', 'ipv6', 'private_networking', 'upgrade', 'restore', 
	 'resize', 'rebuild', 'rename', 'change_kernel', 'snapshot']

	if validate(ctx.params, option_list):
		if disable_backups:
			params = {'type':'disable_backups'}
			record = 'droplet disable backups'
			return run_command(disable_backups, params, record, token, proxy, tablefmt)

		if reboot:
			params = {'type':'reboot'}
			record = 'droplet reboot'
			return run_command(reboot, params, record, token, proxy, tablefmt)
	
		if power_cycle:
			params = {'type':'power_cycle'}
			record = 'droplet power_cycle'
			return run_command(power_cycle, params, record, token, proxy, tablefmt)

		if shutdown:
			params = {'type':'shutdown'}
			record = 'droplet shutdown'
			return run_command(shutdown, params, record, token, proxy, tablefmt)

		if power_off:
			params = {'type':'power_off'}
			record = 'droplet power_off'
			return run_command(power_off, params, record, token, proxy, tablefmt)

		if power_on:
			params = {'type':'power_on'}
			record = 'droplet power_on'
			return run_command(power_on, params, record, token, proxy, tablefmt)

		if password_reset:
			params = {'type':'password_reset'}
			record = 'droplet password_reset'
			return run_command(password_reset, params, record, token, proxy, tablefmt)

		if ipv6:
			params = {'type':'enable_ipv6'}
			record = 'droplet ipv6'
			return run_command(ipv6, params, record, token, proxy, tablefmt)

		if private_networking:
			params = {'type':'enable_private_networking'}
			record = 'droplet private_networking'
			return run_command(private_networking, params, record, token, proxy, tablefmt)

		if upgrade:
			params = {'type':'upgrade'}
			record = 'droplet upgrade'
			return run_command(upgrade, params, record, token, proxy, tablefmt)

		if restore:
			params = {'type':'restore', 'image':backup_id}
			record = 'droplet restore'
			return run_command(restore, params, record, token, proxy, tablefmt)

		if resize:
			params = {'type':'resize', 'size':size}
			record = 'droplet resize'
			return run_command(resize, params, record, token, proxy, tablefmt)

		if rebuild:
			params = {'type':'rebuild', 'image':image}
			record = 'droplet rebuild'
			return run_command(rebuild, params, record, token, proxy, tablefmt)

		if rename:
			params = {'type':'rename', 'name':name}
			record = 'droplet rename'
			return run_command(rename, params, record, token, proxy, tablefmt)

		if change_kernel:
			params = {'type':'change_kernel', 'kernel':kernel}
			record = 'droplet change_kernel'
			return run_command(change_kernel, params, record, token, proxy, tablefmt)

		if snapshot:
			params = {'type':'snapshot', 'name':sname}
			record = 'droplet snapshot'
			return run_command(snapshot, params, record, token, proxy, tablefmt)