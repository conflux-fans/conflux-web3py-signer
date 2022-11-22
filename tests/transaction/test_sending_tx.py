import json
from web3 import Web3
from web3.middleware.signing import construct_sign_and_send_raw_middleware
from eth_account.signers.local import LocalAccount

def test_sending_transactions(w3: Web3, account: LocalAccount):
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
    w3.eth.default_account = account.address
    tx_hash = w3.eth.send_transaction({
        "to": "0x0000000000000000000000000000000000000000",
        "value": 100
    })
    w3.eth.wait_for_transaction_receipt(tx_hash)

def test_interacting_with_contract(w3: Web3, account: LocalAccount):
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
    w3.eth.default_account = account.address
    with open("tests/metadata/ERC20.json") as f:
        metadata = json.load(f)
    erc20_factory = w3.eth.contract(abi=metadata["abi"], bytecode=metadata["bytecode"])
    deploy_hash = erc20_factory.constructor(name="Coin", symbol="C", initialSupply=10**18).transact()
    contract_address = w3.eth.wait_for_transaction_receipt(deploy_hash)["contractAddress"]
    erc20_contract = erc20_factory(contract_address)
    
    random_account = w3.eth.account.create()
    
    transfer_hash = erc20_contract.functions.transfer(random_account.address, 100).transact()
    transfer_receipt = w3.eth.wait_for_transaction_receipt(transfer_hash)
    
    assert erc20_contract.caller().balanceOf(random_account.address) == erc20_contract.functions.balanceOf(random_account.address).call() == 100
    
    from_block = transfer_receipt["blockNumber"]
    # erc20_contract.events.Transfer.processReceipt(transfer_receipt)
    processed_logs = erc20_contract.events.Transfer.getLogs(
        fromBlock=from_block
    )
    assert processed_logs
