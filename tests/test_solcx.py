import solcx
import re
import pprint

with open('sample1.sol', 'r') as f:
    source = f.read()

# Default
version_to_install = "0.8.0"

# Find pragma
match = re.search(r"pragma solidity [^0-9]*([0-9]+\.[0-9]+\.[0-9]+)", source)
if match:
    version_to_install = match.group(1)

print("Found solc version:", version_to_install)

try:
    solcx.install_solc(version_to_install)
    solcx.set_solc_version(version_to_install)
    compiled = solcx.compile_source(source)
    print("Compiled successfully!")
    for contract_id, contract_interface in compiled.items():
        print(f"Contract: {contract_id}")
        bin_runtime = contract_interface.get('bin-runtime')
        if bin_runtime:
            print("Successfully extracted bin-runtime:")
            print(bin_runtime[:100] + "...")
except Exception as e:
    print("Error:", e)
