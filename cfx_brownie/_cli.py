import conflux_web3py_signer.hook_brownie
from brownie._cli.__main__ import main as brownie_main
import pkg_resources

__version__ = pkg_resources.get_distribution("conflux-web3py-signer").version

def main():
    print(f"conflux-web3py-signer v{__version__} - transaction signer for Conflux RPC Bridge integrated with Brownie\n")
    brownie_main()
