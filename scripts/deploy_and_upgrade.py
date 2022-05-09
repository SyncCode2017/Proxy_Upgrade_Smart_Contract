from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    network,
    Pink_Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    Pink_BoxV2,
)


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Pink_Box.deploy({"from": account})
    print(box.retrieve())

    # setting up proxy admin to be this contract. You can set it up to be multi-sig
    proxy_admin = ProxyAdmin.deploy({"from": account})

    # proxy admin dont have constructor but initializer function
    # initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade to v2!")

    # proxy allow us to call all the functions in Pink_Box.sol with proxy
    # proxy delegates all our calls to box eventhough we are using proxy.address
    proxy_box = Contract.from_abi("Pink_Box", proxy.address, Pink_Box.abi)
    proxy_box.store(1, {"from": account, "gas_limit": 1000000})
    print(proxy_box.retrieve())

    # Now to upgrade our Pink_Box.sol to Pink_BoxV2.sol
    box_v2 = Pink_BoxV2.deploy({"from": account, "gas_limit": 1000000})
    upgrade_transaction = upgrade(
        account, proxy, box_v2, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)
    print("Proxy has been upgraded!")
    proxy_box = Contract.from_abi("Pink_BoxV2", proxy.address, Pink_BoxV2.abi)
    proxy_box.increment({"from": account, "gas_limit": 1000000})
    print(proxy_box.retrieve())
