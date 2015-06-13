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


def validate(dic):
	return True


@droplet_actions_group.command(name='droplet-actions', context_settings=CONTEXT_SETTINGS)
@click.option('--disable-backups', '-d', type=int, help='Disable backups for given droplet id', metavar='<3812352>')
@click.option('--reboot', '-r', type=int, help='Reboot droplet for given droplet id', metavar='<3812352>')
@click.option('--power-cycle', '-p', type=int, help='Power cycle droplet for given droplet id', metavar='<3812352>')
@click.option('--shutdown', '-s', type=int, help='Shutdown droplet for given droplet id', metavar='<3812352>')
@click.option('--power-off', '-P', type=int, help='Power Off droplet for given droplet id', metavar='<3812352>')
@click.option('--power-on', '-o', type=int, help='Power On droplet for given droplet id', metavar='<3812352>')
@click.option('--power-on', '-o', type=int, help='Power On droplet for given droplet id', metavar='<3812352>')
@click.option('--password-reset', '-w', type=int, help='Password Reset droplet for given droplet id', metavar='<3812352>')
@click.option('--ipv6', '-v', type=int, help='Enable ipv6 for given droplet id', metavar='<3812352>')
@click.option('--private-networking', '-n', type=int, help='Enable private networking for given droplet id', metavar='<3812352>')
@click.pass_context
def droplet_actions(ctx, disable_backups, reboot, power_cycle, shutdown, power_off, power_on, password_reset, ipv6, private_networking):
	"""
	Droplet actions are tasks that can be executed on a Droplet.
	These can be things like rebooting, resizing, snapshotting, etc.
	"""

	if (not ctx.params['disable_backups'] and not ctx.params['reboot'] and not ctx.params['power_cycle'] and not ctx.params['shutdown'] and not ctx.params['power_off'] and not ctx.params['power_on'] and not ctx.params['password_reset'] and not ctx.params['ipv6'] and not ctx.params['private_networking']):
		return click.echo(ctx.get_help())

	if validate(ctx.params):
		if disable_backups:
			method = 'POST'
			url = DROPLETS + str(disable_backups) + '/actions'
			params = {'type':'disable_backups'}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'droplet disable backups'
				headers = ['Fields', 'Values']
				table = [['Id', result['action']['id']], ['Status', result['action']['status']], ['Type', result['action']['type']], ['Started at', result['action']['started_at']], ['Completed at', result['action']['completed_at']], ['Resource Id', result['action']['resource_id']], ['Resource Type', result['action']['resource_type']], ['Region', result['action']['region']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)
				click.echo()
				click.echo('To get status update of above action execute following command.')
				click.echo('Command: docli action -i %d' % disable_backups)

		if reboot:
			method = 'POST'
			url = DROPLETS + str(reboot) + '/actions'
			params = {'type':'reboot'}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'droplet reboot'
				headers = ['Fields', 'Values']
				table = [['Id', result['action']['id']], ['Status', result['action']['status']], ['Type', result['action']['type']], ['Started at', result['action']['started_at']], ['Completed at', result['action']['completed_at']], ['Resource Id', result['action']['resource_id']], ['Resource Type', result['action']['resource_type']], ['Region', result['action']['region']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)
				click.echo()
				click.echo('To get status update of above action execute following command.')
				click.echo('Command: docli action -i %d' % reboot)

		if power_cycle:
			method = 'POST'
			url = DROPLETS + str(power_cycle) + '/actions'
			params = {'type':'power_cycle'}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'droplet power_cycle'
				headers = ['Fields', 'Values']
				table = [['Id', result['action']['id']], ['Status', result['action']['status']], ['Type', result['action']['type']], ['Started at', result['action']['started_at']], ['Completed at', result['action']['completed_at']], ['Resource Id', result['action']['resource_id']], ['Resource Type', result['action']['resource_type']], ['Region', result['action']['region']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)
				click.echo()
				click.echo('To get status update of above action execute following command.')
				click.echo('Command: docli action -i %d' % power_cycle)

		if shutdown:
			method = 'POST'
			url = DROPLETS + str(shutdown) + '/actions'
			params = {'type':'shutdown'}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'droplet shutdown'
				headers = ['Fields', 'Values']
				table = [['Id', result['action']['id']], ['Status', result['action']['status']], ['Type', result['action']['type']], ['Started at', result['action']['started_at']], ['Completed at', result['action']['completed_at']], ['Resource Id', result['action']['resource_id']], ['Resource Type', result['action']['resource_type']], ['Region', result['action']['region']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)
				click.echo()
				click.echo('To get status update of above action execute following command.')
				click.echo('Command: docli action -i %d' % shutdown)

		if power_off:
			method = 'POST'
			url = DROPLETS + str(power_off) + '/actions'
			params = {'type':'power_off'}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'droplet power_off'
				headers = ['Fields', 'Values']
				table = [['Id', result['action']['id']], ['Status', result['action']['status']], ['Type', result['action']['type']], ['Started at', result['action']['started_at']], ['Completed at', result['action']['completed_at']], ['Resource Id', result['action']['resource_id']], ['Resource Type', result['action']['resource_type']], ['Region', result['action']['region']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)
				click.echo()
				click.echo('To get status update of above action execute following command.')
				click.echo('Command: docli action -i %d' % power_off)

		if power_on:
			method = 'POST'
			url = DROPLETS + str(power_on) + '/actions'
			params = {'type':'power_on'}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'droplet power_on'
				headers = ['Fields', 'Values']
				table = [['Id', result['action']['id']], ['Status', result['action']['status']], ['Type', result['action']['type']], ['Started at', result['action']['started_at']], ['Completed at', result['action']['completed_at']], ['Resource Id', result['action']['resource_id']], ['Resource Type', result['action']['resource_type']], ['Region', result['action']['region']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)
				click.echo()
				click.echo('To get status update of above action execute following command.')
				click.echo('Command: docli action -i %d' % power_on)

		if password_reset:
			method = 'POST'
			url = DROPLETS + str(password_reset) + '/actions'
			params = {'type':'password_reset'}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'droplet password_reset'
				headers = ['Fields', 'Values']
				table = [['Id', result['action']['id']], ['Status', result['action']['status']], ['Type', result['action']['type']], ['Started at', result['action']['started_at']], ['Completed at', result['action']['completed_at']], ['Resource Id', result['action']['resource_id']], ['Resource Type', result['action']['resource_type']], ['Region', result['action']['region']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)
				click.echo()
				click.echo('To get status update of above action execute following command.')
				click.echo('Command: docli action -i %d' % password_reset)

		if ipv6:
			method = 'POST'
			url = DROPLETS + str(ipv6) + '/actions'
			params = {'type':'enable_ipv6'}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'droplet ipv6'
				headers = ['Fields', 'Values']
				table = [['Id', result['action']['id']], ['Status', result['action']['status']], ['Type', result['action']['type']], ['Started at', result['action']['started_at']], ['Completed at', result['action']['completed_at']], ['Resource Id', result['action']['resource_id']], ['Resource Type', result['action']['resource_type']], ['Region', result['action']['region']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)
				click.echo()
				click.echo('To get status update of above action execute following command.')
				click.echo('Command: docli action -i %d' % ipv6)

		if private_networking:
			method = 'POST'
			url = DROPLETS + str(private_networking) + '/actions'
			params = {'type':'enable_private_networking'}
			result = DigitalOcean.do_request(method, url, token=token, proxy=proxy, params=params)
			if result['has_error']:
				click.echo()
				click.echo('Error: %s' %(result['error_message']))
			else:
				record = 'droplet private_networking'
				headers = ['Fields', 'Values']
				table = [['Id', result['action']['id']], ['Status', result['action']['status']], ['Type', result['action']['type']], ['Started at', result['action']['started_at']], ['Completed at', result['action']['completed_at']], ['Resource Id', result['action']['resource_id']], ['Resource Type', result['action']['resource_type']], ['Region', result['action']['region']]]
				data = {'headers': headers, 'table_data': table}
				print_table(tablefmt, data, record)
				click.echo()
				click.echo('To get status update of above action execute following command.')
				click.echo('Command: docli action -i %d' % private_networking)