"""Cypher magic"""
__version__ = '0.0.2'

from .cypher import CypherMagic

def load_ipython_extension(ipython):
    ipython.register_magics(CypherMagic)