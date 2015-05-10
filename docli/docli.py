# -*- coding: utf-8 -*-

import click
from commands.account import account_group

docli = click.CommandCollection(sources=[account_group])

if __name__ == '__main__':
	docli()