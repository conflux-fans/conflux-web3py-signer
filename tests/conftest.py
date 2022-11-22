import os
import pytest
from typing import Union
import conflux_web3py_signer
from web3 import Web3
from eth_account.signers.local import LocalAccount
from eth_account import Account


@pytest.fixture(scope="session")
def url() -> str:
    r = os.environ.get("BRIDGE_URL")
    if not r:
        raise ValueError("Environment BRIDGE_URL is not set")
    return r

@pytest.fixture(scope="session")
def secret() -> Union[str, None]:
    return os.environ.get("SECRET")

@pytest.fixture
def w3(url: str) -> Web3:
    return Web3(Web3.HTTPProvider(url))

@pytest.fixture
def account(secret: str) -> LocalAccount:
    if secret is None:
        return Account.create()
    return Account.from_key(secret)

def test_connection(w3: Web3):
    assert w3.is_connected()
