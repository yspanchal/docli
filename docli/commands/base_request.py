
# -*- coding: utf-8 -*-

import os
import logging
import requests
import ConfigParser


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