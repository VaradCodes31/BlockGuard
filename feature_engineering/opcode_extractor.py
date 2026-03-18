# feature_engineering/opcode_extractor.py

def build_opcode_map():
    opcode_map = {}

    # -------------------------------
    # Arithmetic
    # -------------------------------
    opcode_map.update({
        "00": "STOP",
        "01": "ADD",
        "02": "MUL",
        "03": "SUB",
        "04": "DIV",
        "05": "SDIV",
        "06": "MOD",
        "07": "SMOD",
        "08": "ADDMOD",
        "09": "MULMOD",
        "0a": "EXP",
        "0b": "SIGNEXTEND",
    })

    # -------------------------------
    # Comparison & Bitwise
    # -------------------------------
    opcode_map.update({
        "10": "LT",
        "11": "GT",
        "12": "SLT",
        "13": "SGT",
        "14": "EQ",
        "15": "ISZERO",
        "16": "AND",
        "17": "OR",
        "18": "XOR",
        "19": "NOT",
        "1a": "BYTE",
        "1b": "SHL",
        "1c": "SHR",
        "1d": "SAR",
    })

    # -------------------------------
    # SHA3
    # -------------------------------
    opcode_map["20"] = "SHA3"

    # -------------------------------
    # Environmental Information
    # -------------------------------
    opcode_map.update({
        "30": "ADDRESS",
        "31": "BALANCE",
        "32": "ORIGIN",
        "33": "CALLER",
        "34": "CALLVALUE",
        "35": "CALLDATALOAD",
        "36": "CALLDATASIZE",
        "37": "CALLDATACOPY",
        "38": "CODESIZE",
        "39": "CODECOPY",
        "3a": "GASPRICE",
        "3b": "EXTCODESIZE",
        "3c": "EXTCODECOPY",
        "3d": "RETURNDATASIZE",
        "3e": "RETURNDATACOPY",
        "3f": "EXTCODEHASH",
    })

    # -------------------------------
    # Block Information
    # -------------------------------
    opcode_map.update({
        "40": "BLOCKHASH",
        "41": "COINBASE",
        "42": "TIMESTAMP",
        "43": "NUMBER",
        "44": "DIFFICULTY",
        "45": "GASLIMIT",
        "46": "CHAINID",
        "47": "SELFBALANCE",
        "48": "BASEFEE",
    })

    # -------------------------------
    # Stack / Memory / Storage
    # -------------------------------
    opcode_map.update({
        "50": "POP",
        "51": "MLOAD",
        "52": "MSTORE",
        "53": "MSTORE8",
        "54": "SLOAD",
        "55": "SSTORE",
        "56": "JUMP",
        "57": "JUMPI",
        "58": "PC",
        "59": "MSIZE",
        "5a": "GAS",
        "5b": "JUMPDEST",
    })

    # -------------------------------
    # PUSH (0x60 - 0x7f)
    # -------------------------------
    for i in range(0x60, 0x80):
        opcode_map[f"{i:02x}"] = f"PUSH{i - 0x5f}"

    # -------------------------------
    # DUP (0x80 - 0x8f)
    # -------------------------------
    for i in range(0x80, 0x90):
        opcode_map[f"{i:02x}"] = f"DUP{i - 0x7f}"

    # -------------------------------
    # SWAP (0x90 - 0x9f)
    # -------------------------------
    for i in range(0x90, 0xa0):
        opcode_map[f"{i:02x}"] = f"SWAP{i - 0x8f}"

    # -------------------------------
    # LOG (0xa0 - 0xa4)
    # -------------------------------
    for i in range(0xa0, 0xa5):
        opcode_map[f"{i:02x}"] = f"LOG{i - 0xa0}"

    # -------------------------------
    # System Operations
    # -------------------------------
    opcode_map.update({
        "f0": "CREATE",
        "f1": "CALL",
        "f2": "CALLCODE",
        "f3": "RETURN",
        "f4": "DELEGATECALL",
        "f5": "CREATE2",
        "fa": "STATICCALL",
        "fd": "REVERT",
        "fe": "INVALID",
        "ff": "SELFDESTRUCT",
    })

    return opcode_map


# Build once
opcode_map = build_opcode_map()


# -------------------------------
# Main Function
# -------------------------------
def bytecode_to_opcodes(bytecode):

    # 🔥 Clean input
    bytecode = bytecode.replace("0x", "").strip().lower()

    opcodes = []
    i = 0
    length = len(bytecode)

    while i < length:

        # Safety check
        if i + 2 > length:
            break

        opcode = bytecode[i:i+2]

        if opcode in opcode_map:
            op_name = opcode_map[opcode]
            opcodes.append(op_name)

            # 🔥 HANDLE PUSH CORRECTLY
            if op_name.startswith("PUSH"):
                push_size = int(op_name[4:])
                i += 2 + (push_size * 2)  # skip data bytes
            else:
                i += 2
        else:
            opcodes.append("UNKNOWN")
            i += 2

    return opcodes