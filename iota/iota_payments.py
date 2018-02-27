import os
import re

from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString
from iota.adapter import HttpAdapter
from iota.adapter.wrappers import RoutingWrapper

IOTA_LOCAL_NODE = "http://localhost:14265"
IOTA_REMOTE_NODE = "https://nodes.thetangle.org:443"
SEED = os.environ['IOTA_SEED']

api = Iota(
    RoutingWrapper(IOTA_REMOTE_NODE).add_route('attachToTangle', IOTA_LOCAL_NODE),
    seed = SEED)

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
