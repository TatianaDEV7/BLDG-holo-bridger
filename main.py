import pandas as pd
from web3 import Web3
from loguru import logger
import random
import time
from tqdm import tqdm
from moralis import evm_api
from config import *
from eth_abi import *
from eth_utils import *

holo_abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"target","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"adminCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint32","name":"fromChain","type":"uint32"},{"internalType":"address","name":"holographableContract","type":"address"},{"internalType":"address","name":"hToken","type":"address"},{"internalType":"address","name":"hTokenRecipient","type":"address"},{"internalType":"uint256","name":"hTokenValue","type":"uint256"},{"internalType":"bool","name":"doNotRevert","type":"bool"},{"internalType":"bytes","name":"bridgeInPayload","type":"bytes"}],"name":"bridgeInRequest","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint32","name":"toChain","type":"uint32"},{"internalType":"address","name":"holographableContract","type":"address"},{"internalType":"uint256","name":"gasLimit","type":"uint256"},{"internalType":"uint256","name":"gasPrice","type":"uint256"},{"internalType":"bytes","name":"bridgeOutPayload","type":"bytes"}],"name":"bridgeOutRequest","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"getAdmin","outputs":[{"internalType":"address","name":"adminAddress","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"toChain","type":"uint32"},{"internalType":"address","name":"holographableContract","type":"address"},{"internalType":"uint256","name":"gasLimit","type":"uint256"},{"internalType":"uint256","name":"gasPrice","type":"uint256"},{"internalType":"bytes","name":"bridgeOutPayload","type":"bytes"}],"name":"getBridgeOutRequestPayload","outputs":[{"internalType":"bytes","name":"samplePayload","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getFactory","outputs":[{"internalType":"address","name":"factory","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHolograph","outputs":[{"internalType":"address","name":"holograph","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getJobNonce","outputs":[{"internalType":"uint256","name":"jobNonce","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint32","name":"","type":"uint32"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"getMessageFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOperator","outputs":[{"internalType":"address","name":"operator","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRegistry","outputs":[{"internalType":"address","name":"registry","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"initPayload","type":"bytes"}],"name":"init","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"uint32","name":"toChain","type":"uint32"},{"internalType":"address","name":"holographableContract","type":"address"},{"internalType":"bytes","name":"bridgeOutPayload","type":"bytes"}],"name":"revertedBridgeOutRequest","outputs":[{"internalType":"string","name":"revertReason","type":"string"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"adminAddress","type":"address"}],"name":"setAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"factory","type":"address"}],"name":"setFactory","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"holograph","type":"address"}],"name":"setHolograph","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"}],"name":"setOperator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"registry","type":"address"}],"name":"setRegistry","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
lzEndpointABI = '[{"inputs":[{"internalType":"uint16","name":"_chainId","type":"uint16"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"version","type":"uint16"}],"name":"DefaultReceiveVersionSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"version","type":"uint16"}],"name":"DefaultSendVersionSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"version","type":"uint16"}],"name":"NewLibraryVersionAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"srcChainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"srcAddress","type":"bytes"},{"indexed":false,"internalType":"uint64","name":"nonce","type":"uint64"},{"indexed":false,"internalType":"address","name":"dstAddress","type":"address"}],"name":"PayloadCleared","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"srcChainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"srcAddress","type":"bytes"},{"indexed":false,"internalType":"address","name":"dstAddress","type":"address"},{"indexed":false,"internalType":"uint64","name":"nonce","type":"uint64"},{"indexed":false,"internalType":"bytes","name":"payload","type":"bytes"},{"indexed":false,"internalType":"bytes","name":"reason","type":"bytes"}],"name":"PayloadStored","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint16","name":"chainId","type":"uint16"},{"indexed":false,"internalType":"bytes","name":"srcAddress","type":"bytes"}],"name":"UaForceResumeReceive","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"ua","type":"address"},{"indexed":false,"internalType":"uint16","name":"version","type":"uint16"}],"name":"UaReceiveVersionSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"ua","type":"address"},{"indexed":false,"internalType":"uint16","name":"version","type":"uint16"}],"name":"UaSendVersionSet","type":"event"},{"inputs":[],"name":"BLOCK_VERSION","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DEFAULT_VERSION","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"chainId","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"defaultReceiveLibraryAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"defaultReceiveVersion","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"defaultSendLibrary","outputs":[{"internalType":"contract ILayerZeroMessagingLibrary","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"defaultSendVersion","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"address","name":"_userApplication","type":"address"},{"internalType":"bytes","name":"_payload","type":"bytes"},{"internalType":"bool","name":"_payInZRO","type":"bool"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"estimateFees","outputs":[{"internalType":"uint256","name":"nativeFee","type":"uint256"},{"internalType":"uint256","name":"zroFee","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"}],"name":"forceResumeReceive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getChainId","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"},{"internalType":"uint16","name":"_chainId","type":"uint16"},{"internalType":"address","name":"_userApplication","type":"address"},{"internalType":"uint256","name":"_configType","type":"uint256"}],"name":"getConfig","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"}],"name":"getInboundNonce","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"address","name":"_srcAddress","type":"address"}],"name":"getOutboundNonce","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_userApplication","type":"address"}],"name":"getReceiveLibraryAddress","outputs":[{"internalType":"address","name":"receiveLibraryAddress","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_userApplication","type":"address"}],"name":"getReceiveVersion","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_userApplication","type":"address"}],"name":"getSendLibraryAddress","outputs":[{"internalType":"address","name":"sendLibraryAddress","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_userApplication","type":"address"}],"name":"getSendVersion","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"}],"name":"hasStoredPayload","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"inboundNonce","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isReceivingPayload","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isSendingPayload","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"latestVersion","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"}],"name":"libraryLookup","outputs":[{"internalType":"contract ILayerZeroMessagingLibrary","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_newLayerZeroLibraryAddress","type":"address"}],"name":"newVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"address","name":"","type":"address"}],"name":"outboundNonce","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"address","name":"_dstAddress","type":"address"},{"internalType":"uint64","name":"_nonce","type":"uint64"},{"internalType":"uint256","name":"_gasLimit","type":"uint256"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"receivePayload","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_srcChainId","type":"uint16"},{"internalType":"bytes","name":"_srcAddress","type":"bytes"},{"internalType":"bytes","name":"_payload","type":"bytes"}],"name":"retryPayload","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_dstChainId","type":"uint16"},{"internalType":"bytes","name":"_destination","type":"bytes"},{"internalType":"bytes","name":"_payload","type":"bytes"},{"internalType":"address payable","name":"_refundAddress","type":"address"},{"internalType":"address","name":"_zroPaymentAddress","type":"address"},{"internalType":"bytes","name":"_adapterParams","type":"bytes"}],"name":"send","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_version","type":"uint16"},{"internalType":"uint16","name":"_chainId","type":"uint16"},{"internalType":"uint256","name":"_configType","type":"uint256"},{"internalType":"bytes","name":"_config","type":"bytes"}],"name":"setConfig","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_newDefaultReceiveVersion","type":"uint16"}],"name":"setDefaultReceiveVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_newDefaultSendVersion","type":"uint16"}],"name":"setDefaultSendVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_newVersion","type":"uint16"}],"name":"setReceiveVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_newVersion","type":"uint16"}],"name":"setSendVersion","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"","type":"uint16"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"storedPayload","outputs":[{"internalType":"uint64","name":"payloadLength","type":"uint64"},{"internalType":"address","name":"dstAddress","type":"address"},{"internalType":"bytes32","name":"payloadHash","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"uaConfigLookup","outputs":[{"internalType":"uint16","name":"sendVersion","type":"uint16"},{"internalType":"uint16","name":"receiveVersion","type":"uint16"},{"internalType":"address","name":"receiveLibraryAddress","type":"address"},{"internalType":"contract ILayerZeroMessagingLibrary","name":"sendLibrary","type":"address"}],"stateMutability":"view","type":"function"}]'

holograph_ids = {'polygon':4,
                'avax': 3,
                'bsc': 2}

Lz_ids= {'bsc':102,
        'avax':106,
        'polygon':109}

gas_holo = {'bsc':4500000000,
            'avax':37500000000,
            'polygon':400000000000}

wallets = []
results = []
class Bridger:
    def __init__(self, privatekey,chain,to,delay,api,mode=1):
        self.privatekey = privatekey
        self.chain = chain
        self.to = to
        self.w3 = ''
        self.scan = ''
        self.account = ''
        self.address = ''
        self.mode = mode
        self.delay = delay
        self.moralisapi = api
        self.HolographBridgeAddress = Web3.to_checksum_address('0xD85b5E176A30EdD1915D6728FaeBD25669b60d8b')
        self.LzEndAddress = Web3.to_checksum_address('0x3c2269811836af69497E5F486A85D7316753cf62')
        self.BLDGAddress = Web3.to_checksum_address('0x8C531f965C05Fab8135d951e2aD0ad75CF3405A2')

    def check_status_tx(self, tx_hash):

        logger.info(f'{self.address}:{self.chain} - waiting for confirmation transaction {self.scan}{self.w3.to_hex(tx_hash)}...')
        while True:
            try:
                status = self.w3.eth.get_transaction_receipt(tx_hash)
                status = status['status']
                if status in [0, 1]:
                    return status
                time.sleep(1)
            except Exception as error:
                time.sleep(1)

    def sleep_indicator(self,secs):
        for i in tqdm(range(secs), desc='wait', bar_format="{desc}: {n_fmt}s / {total_fmt}s {bar}", colour='green'):
            time.sleep(1)

    def check_nft(self):
        if self.mode == 0 and self.chain != 'opti':
            cc = {'avax':'avalanche',
                  'polygon':'polygon',
                  'bsc':'bsc'}
            api_key = self.moralisapi
            params = {
                "chain": cc[self.chain],
                "format": "decimal",
                "token_addresses": [
                    self.BLDGAddress
                ],
                "media_items": False,
                "address": self.address}
            try:
                result = evm_api.nft.get_wallet_nfts(api_key=api_key, params=params)
                id_ = int(result['result'][0]['token_id'])
                if id_:
                    logger.success(f'{self.address} - BLDG {id_} nft founded on {self.chain}...')
                    return id_
            except Exception as e:
                return False

        elif self.mode == 0 and self.chain == 'opti':
            contract_abi = [
                {
                    "constant": True,
                    "inputs": [{"name": "_owner", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "balance", "type": "uint256"}],
                    "payable": False,
                    "stateMutability": "view",
                    "type": "function"
                },
                {
                    "constant": True,
                    "inputs": [{"name": "_owner", "type": "address"}],
                    "name": "tokensOfOwner",
                    "outputs": [{"name": "tokenIds", "type": "uint256[]"}],
                    "payable": False,
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
            contract = self.w3.eth.contract(address=self.BLDGAddress, abi=contract_abi)
            bal = contract.functions.balanceOf(self.address).call()
            if bal:
                id_ = contract.functions.tokensOfOwner(self.address).call()[0]
                logger.success(f'{self.address} - BLDG {id_} nft founded on {self.chain}...')
                return id_
            else:
                return False


        elif self.mode == 1:
            for chain in ['avalanche', 'polygon', 'bsc']:

                    api_key = self.moralisapi
                    params = {
                        "chain": chain,
                        "format": "decimal",
                        "token_addresses": [
                            self.BLDGAddress
                        ],
                        "media_items": False,
                        "address": self.address}
                    try:
                        result = evm_api.nft.get_wallet_nfts(api_key=api_key, params=params)
                        id_ = int(result['result'][0]['token_id'])
                        if id_:
                            logger.success(f'{self.address} - BLDG {id_} nft founded on {chain}...')
                            if chain == 'avalanche': chain = 'avax'
                            return chain, id_

                    except Exception as e:
                        if 'list index out of range' in str(e):
                            continue

            logger.error(f'{self.address} - BLDG nft not in wallet...')
            return False


    def start(self):
        if self.mode == 0:
            self.w3 = Web3(Web3.HTTPProvider(info[self.chain][1]))
            self.scan = info[self.chain][0]
            self.account = self.w3.eth.account.from_key(self.privatekey)
            self.address = self.account.address
            data = self.check_nft()
            if data:
                nft_id = data
            else:
                return self.address,'BLDG nft not in wallet'

        elif self.mode == 1:
            self.w3 = Web3(Web3.HTTPProvider(info['bsc'][1]))
            self.address = self.w3.eth.account.from_key(self.privatekey).address
            data = self.check_nft()

            if data:
                chain,nft_id = data
                self.chain = chain
                self.w3 = Web3(Web3.HTTPProvider(info[self.chain][1]))
                self.scan = info[self.chain][0]
                self.account = self.w3.eth.account.from_key(self.privatekey)
                self.address = self.account.address
                if chain == self.to:
                    chains = ['avax', 'polygon', 'bsc']
                    chains.remove(self.to)
                    self.to = random.choice(chains)
            else:
                return self.address,'BLDG nft not in wallet'

        payload = to_hex(encode(['address', 'address', 'uint256'], [self.address, self.address, nft_id]))
        gas_price = gas_holo[self.to]
        gas_lim = random.randint(450000, 500000)

        holograph = self.w3.eth.contract(address=self.HolographBridgeAddress, abi=holo_abi)
        lzEndpoint = self.w3.eth.contract(address=self.LzEndAddress, abi=lzEndpointABI)

        lzFee = lzEndpoint.functions.estimateFees(Lz_ids[self.to],self.HolographBridgeAddress,'0x',False,'0x').call()[0]
        lzFee = int(lzFee * 2.5)
        to = holograph_ids[self.to]

        while True:
            logger.info(f'{self.address}:{self.chain} - trying to bridge... ')
            try:
                tx = holograph.functions.bridgeOutRequest(to, self.BLDGAddress, gas_lim, gas_price,payload).build_transaction({
                    'from': self.address,
                    'value': lzFee,
                    'gas': holograph.functions.bridgeOutRequest(to, self.BLDGAddress, gas_lim, gas_price,payload).estimate_gas({'from': self.address, 'value': lzFee,'nonce': self.w3.eth.get_transaction_count(self.address), }),
                    'gasPrice': self.w3.eth.gas_price,
                    'nonce': self.w3.eth.get_transaction_count(self.address),
                })
                sign = self.account.sign_transaction(tx)
                hash = self.w3.eth.send_raw_transaction(sign.rawTransaction)
                status = self.check_status_tx(hash)
                self.sleep_indicator(10)
                if status == 1:
                    logger.success(f'{self.address}:{self.chain} - successfully bridged BLDG {nft_id} to {self.to} : {self.scan}{self.w3.to_hex(hash)}...')
                    self.sleep_indicator(random.randint(self.delay[0],self.delay[1]))
                    return self.address, 'success'
            except Exception as e:
                error = str(e)
                if 'nonce too low' in error or 'already known' in error:
                    logger.success(f'{self.address}:{self.chain} - successfully bridged BLDG {nft_id} to {self.to}...')
                    self.sleep_indicator(random.randint(self.delay[0],self.delay[1]))
                    return self.address, 'success'
                logger.error(f'{self.address}:{self.chain} - error {e}')
                return self.address, 'error'


def main():
    logger.info(f'{" "*32}creator - https://t.me/iliocka{" "*32}')

    with open("keys.txt", "r") as f:
        keys = [row.strip() for row in f]
    for key in keys:
        holo = Bridger(key,chain,to,delay,api,mode)
        res = holo.start()
        wallets.append(res[0]), results.append(res[1])

    res = {'address': wallets, 'result': results}
    df = pd.DataFrame(res)
    df.to_csv('results.csv', index=False)
    logger.success('Bridging done...')
    print(f'\n{" " * 32}creator - https://t.me/iliocka{" " * 32}\n')
    print(f'\n{" " * 32}donate - EVM 0xFD6594D11b13C6b1756E328cc13aC26742dBa868{" " * 32}\n')
    print(f'\n{" " * 32}donate - trc20 TMmL915TX2CAPkh9SgF31U4Trr32NStRBp{" " * 32}\n')
    logger.success('...')

if __name__ == '__main__':
    main()