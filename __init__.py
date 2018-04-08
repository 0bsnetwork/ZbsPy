# Copyright (C) 2017 PyWaves Developers
#
# This file is part of PyWaves.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoinlib, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

from __future__ import absolute_import, division, print_function, unicode_literals

DEFAULT_TX_FEE = 100000
DEFAULT_ASSET_FEE = 100000000
DEFAULT_MATCHER_FEE = 300000
DEFAULT_LEASE_FEE = 100000
DEFAULT_ALIAS_FEE = 100000
VALID_TIMEFRAMES = (5, 15, 30, 60, 240, 1440)
MAX_WDF_REQUEST = 100

import requests

from .address import *
from .asset import *
from .order import *

OFFLINE = False
NODE = 'https://nodes.wavesnodes.com'

ADDRESS_VERSION = 1
ADDRESS_CHECKSUM_LENGTH = 4
ADDRESS_HASH_LENGTH = 20
ADDRESS_LENGTH = 1 + 1 + ADDRESS_CHECKSUM_LENGTH + ADDRESS_HASH_LENGTH

CHAIN = 'mainnet'
CHAIN_ID = 'W'
MATCHER = 'https://nodes.wavesnodes.com'
MATCHER_PUBLICKEY = ''

DATAFEED = 'http://marketdata.wavesplatform.com'

logging.getLogger("requests").setLevel(logging.WARNING)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def setOffline():
    global OFFLINE
    OFFLINE = True

def setOnline():
    global OFFLINE
    OFFLINE = False

def setChain(chain = CHAIN):
    global CHAIN, CHAIN_ID

    if chain.lower()=='mainnet' or chain.lower()=='w':
        CHAIN = 'mainnet'
        CHAIN_ID = 'W'
    elif chain.lower()=='hacknet' or chain.lower()=='u':
        CHAIN = 'hacknet'
        CHAIN_ID = 'U'
    else:
        CHAIN = 'testnet'
        CHAIN_ID = 'T'

def setNode(node = NODE, chain = CHAIN):
    global NODE, CHAIN, CHAIN_ID
    NODE = node
    setChain(chain)

def setMatcher(node = MATCHER):
    global MATCHER, MATCHER_PUBLICKEY
    try:
        MATCHER_PUBLICKEY = wrapper('/matcher', host = node)
        MATCHER = node
        logging.info('Setting matcher %s %s' % (MATCHER, MATCHER_PUBLICKEY))
    except:
        MATCHER_PUBLICKEY = ''

def setDatafeed(wdf = DATAFEED):
    global DATAFEED
    DATAFEED = wdf
    logging.info('Setting datafeed %s ' % (DATAFEED))

def wrapper(api, postData='', host='', headers=''):
    global OFFLINE
    if OFFLINE:
        offlineTx = {}
        offlineTx['api-type'] = 'POST' if postData else 'GET'
        offlineTx['api-endpoint'] = api
        offlineTx['api-data'] = postData
        return offlineTx
    if not host:
        host = NODE
    if postData:
        req = requests.post('%s%s' % (host, api), data=postData, headers={'content-type': 'application/json'}).json()
    else:
        req = requests.get('%s%s' % (host, api), headers=headers).json()
    return req

def height():
    return wrapper('/blocks/height')['height']

def lastblock():
    return wrapper('/blocks/last')

def block(n):
    return wrapper('/blocks/at/%d' % n)

def tx(id):
    return wrapper('/transactions/info/%s' % id)

def getOrderBook(assetPair):
    orderBook = assetPair.orderbook()
    try:
        bids = orderBook['bids']
        asks = orderBook['asks']
    except:
        bids = ''
        asks = ''
    return bids, asks

def symbols():
    return wrapper('/api/symbols', host=DATAFEED)

def markets():
    return wrapper('/api/markets', host=DATAFEED)

def validateAddress(address):
    addr = crypto.bytes2str(base58.b58decode(address))
    if addr[0] != chr(ADDRESS_VERSION):
        logging.error("Wrong address version")
    elif addr[1] != CHAIN_ID:
        logging.error("Wrong chain id")
    elif len(addr) != ADDRESS_LENGTH:
        logging.error("Wrong address length")
    elif addr[-ADDRESS_CHECKSUM_LENGTH:] != crypto.hashChain(crypto.str2bytes(addr[:-ADDRESS_CHECKSUM_LENGTH]))[:ADDRESS_CHECKSUM_LENGTH]:
        logging.error("Wrong address checksum")
    else:
        return True
    return False

WAVES = Asset('')


