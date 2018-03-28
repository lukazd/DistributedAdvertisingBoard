import os
import re
import node_ip

from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString
from iota.adapter import HttpAdapter
from iota.adapter.sandbox import SandboxAdapter
from iota.adapter.wrappers import RoutingWrapper
from urlparse import urlparse

IOTA_REMOTE_NODE = "https://field.carriota.com:443"
SEED = os.environ['IOTA_SEED']

api = Iota(
    IOTA_REMOTE_NODE,
    seed = SEED
)

def get_balance(address):
    return api.get_balances(addresses)['balances'][0]

def create_and_send_transactions(dest_address, amount, message):
    transaction = ProposedTransaction(
            address = Address(dest_address),
            value = amount,
            tag = None,
            message = TryteString.from_string(message)
    )

    pt = api.prepare_transfer(transfers = [transaction], change_address = None)
    api.send_trytes(pt['trytes'], depth = 100)

def is_address_spent(address):
    return api.were_addresses_spent_from(addresses = [address])['states'][0]

def is_address_valid(address):
    return re.search("[9A-Z]{81}", address) is not None

create_and_send_transactions('VEYONVNFFAQPKYMMOJZJ9JLQNBVGQMMLSDNTWZQYCYYNNJIBOKJHHGCIKKNEVEAXQO9MJXEQLFPQCIEAW', 164, 'The number of the beast')
