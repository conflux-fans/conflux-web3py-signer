import conflux_web3py_signer
from eth_account import Account as EthAccount
from cfx_account import Account as CfxAccount
from web3 import Web3

def test_account_hack_result(w3: Web3):
    assert EthAccount is CfxAccount
    assert isinstance(w3.eth.account, CfxAccount)
