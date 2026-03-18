import os
import subprocess
import pandas as pd

DATASET_PATH = "../data/raw/smartbugs-curated/dataset"
OUTPUT_FILE = "../data/processed/smartbugs_bytecode.csv"

records = []

# Absolute path for Docker volume mount
BASE_PATH = os.path.abspath("../data/raw/smartbugs-curated")


def compile_contract(relative_path):
    """
    Compile a Solidity contract using Docker solc
    """

    try:
        command = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{BASE_PATH}:/contracts",
            "ethereum/solc:0.4.24",
            "--bin",
            f"/contracts/dataset/{relative_path}"
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        output = result.stdout.split("\n")

        for i, line in enumerate(output):

            if line.strip() == "Binary:":
                return output[i + 1].strip()

    except Exception:
        pass

    return None


for vuln_type in os.listdir(DATASET_PATH):

    folder = os.path.join(DATASET_PATH, vuln_type)

    if not os.path.isdir(folder):
        continue

    print("Processing:", vuln_type)

    for file in os.listdir(folder):

        if file.endswith(".sol"):

            relative_path = f"{vuln_type}/{file}"

            bytecode = compile_contract(relative_path)

            if bytecode:

                records.append({
                    "contract_file": file,
                    "bytecode": bytecode,
                    "vuln_type": vuln_type
                })


df = pd.DataFrame(records)

df.to_csv(OUTPUT_FILE, index=False)

print("\nSaved SmartBugs bytecode dataset:", len(df))
print("Saved to:", OUTPUT_FILE)