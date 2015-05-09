
# -*- coding: utf-8 -*-

import os
import logging
import requests
import ConfigParser

import click
from tabulate import tabulate


class DigitalOcean(object):
	"""
	Basic api requests class for docli
	"""
	
	api_url = "https://api.digitalocean.com/v2/"

	@classmethod
	def do_request(self, method, url, token=None, params=None, headers=None, proxy=None):

		auth_token = token

		if not auth_token:
			config = ConfigParser.ConfigParser()
			config.read(os.path.expanduser('~/.do.cfg'))
			auth_token = config.get('docli', 'auth_token') or os.getenv('do_auth_token')

		if not auth_token:
			data = {'has_error':True, 'error_message':'Authentication token not provided.'}
			return data

		if headers:
			headers.update({'Authorization': 'Bearer ' + auth_token})
		else:
			headers = {'Authorization': 'Bearer ' + auth_token}

		if proxy:
			proxy = proxy.split(',')

		request_method = {'GET':requests.get, 'POST': requests.post, 'PUT': requests.put, 'DELETE': requests.delete}

		request_url = self.api_url + url

		req = request_method[method]

		res = req(request_url, headers=headers, params=params,  proxies=proxy)

		if res.status_code == 204:
			data = {'has_error':False, 'error_message':''}
			return data

		try:
			data = res.json()
			data.update({'has_error':False, 'error_message':''})
		except ValueError as e:
			msg = "Cannot read response, %s" %(e.message)
			data = {'has_error':True, 'error_message':msg}

		if not res.ok:
			msg = data['message']
			data.update({'has_error':True, 'error_message':msg})

		return data


def print_table(data_dict={}, tablefmt='fancy_grid'):

	"""
	returns colored table output
	"""
	headers = []
	table = []

	if not data_dict:
		return click.echo('Invalid data !!!')

	if data_dict['headers']:
		headers = data_dict['headers']

		if not isinstance(headers, list):
			return click.echo('Invalid headers !!!')

		headers = [click.style(str(each_element), bold=True, fg='red') for each_element in headers]

	if data_dict['table_data']:
		table_data = data_dict['table_data']

		if not all(isinstance(each_list, list) for each_list in table_data):
			return click.echo("Invlaid table data !!!")

		table = [[click.style(str(each_element), fg='green') for each_element in each_list] for each_list in table_data]

	return click.echo(tabulate(table, headers, tablefmt="fancy_grid"))