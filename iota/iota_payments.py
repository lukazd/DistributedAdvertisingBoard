import os

from iota import Iota, ProposedTransaction, ProposedBundle, Address, Tag, TryteString
from iota.adapter import HttpAdapter
from iota.adapter.wrappers import RoutingWrapper

IOTA_LOCAL_NODE = "http://localhost:14265"
IOTA_REMOTE_NODE = "https://nodes.thetangle.org:443"
SEED = os.environ['IOTA_SEED']

# Remote node for all operations except POW
api = Iota(
    RoutingWrapper(IOTA_REMOTE_NODE).add_route('attachToTangle', IOTA_LOCAL_NODE),
    seed = SEED)

def get_balance(addresses):
        return api.get_balances(addresses)['balances']

def create_and_send_transactions(source_address, dest_address, amount, message):
        transaction = ProposedTransaction(
                address = Address(dest_address),
                value = amount,
                tag = None,
                message = TryteString.from_string(message)
        )

        pt = api.prepare_transfer(transfers = [transaction], change_address = None)
        api.send_trytes(pt['trytes'], depth = 100)

def check_spent_address(address):
    # TODO: Check for outbound transactions
    api.find_transactions([addresses])

source_address = "HXCGVJHWCFRXLXJUSTZRJACTGDNCHRSAKFKWEJIDJLZGYJG9ATUZWUOIXTZPAGWVIXHISLZNQJMPJNQID9JPOMOUKD"
source_address, source_checksum = source_address[:-9], source_address[-9:]

dest_address = "VEYONVNFFAQPKYMMOJZJ9JLQNBVGQMMLSDNTWZQYCYYNNJIBOKJHHGCIKKNEVEAXQO9MJXEQLFPQCIEAWDODLCPROX"
dest_address, dest_checksum = dest_address[:-9], dest_address[-9:]

print(get_balance([dest_address]))
create_and_send_transactions(source_address, dest_address, 500, "Here is 500 iota.")
