import struct
import json
import os

# ==============================================================================
# CONFIGURAÇÃO MANUAL DEFINITIVA
# ==============================================================================
# Esta é a única seção que você precisa editar.
# Para cada arquivo, definimos seu endereço de carga e uma lista de tabelas.
#
# - load_address: O endereço de carga do overlay, obtido do y9.bin.
# - tables: Uma lista de tabelas de texto dentro do arquivo.
#   - id: Um nome único para o script (ex: "script_1", "item_names").
#   - offset: Onde a tabela de ponteiros começa no arquivo (em hexadecimal).
#   - count: O número TOTAL de ponteiros na tabela (incluindo os inválidos).
#
OVERLAY_DATA = {
    "overlay_0000.bin": {"load_address": 0x0222C380, "encoding": "shift_jis", "tables": []},
    "overlay_0001.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_1", "offset": 0x033C, "count": 3076}]},
    "overlay_0002.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_2", "offset": 0x0254, "count": 1671}]},
    "overlay_0003.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_3", "offset": 0x01AC, "count": 1357}]},
    "overlay_0004.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_4", "offset": 0x03B4, "count": 1538}]},
    "overlay_0005.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_5", "offset": 0x03A4, "count": 1433}]},
    "overlay_0006.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_6", "offset": 0x0080, "count": 1153}]},
    "overlay_0007.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_7", "offset": 0x03AC, "count": 1123}]},
    "overlay_0008.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_8", "offset": 0x0084, "count": 1093}]},
    "overlay_0009.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_9", "offset": 0x03C0, "count": 1053}]},
    "overlay_0010.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_10", "offset": 0x03A8, "count": 1258}]},
    "overlay_0011.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_11", "offset": 0x03B4, "count": 832}]},
    "overlay_0012.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_12", "offset": 0x03B8, "count": 904}]},
    "overlay_0013.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_13", "offset": 0x0198, "count": 1614}]},
    "overlay_0014.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_14", "offset": 0x0404, "count": 3677}]},
    "overlay_0015.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_15", "offset": 0x0400, "count": 2890}]},
    "overlay_0016.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_16", "offset": 0x040C, "count": 2043}]},
    "overlay_0017.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_17", "offset": 0x03F0, "count": 2191}]},
    "overlay_0018.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_18", "offset": 0x04B0, "count": 2693}]},
    "overlay_0019.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_19", "offset": 0x03F4, "count": 2906}]},
    "overlay_0020.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_20", "offset": 0x0410, "count": 2340}]},
    "overlay_0021.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_21", "offset": 0x03E0, "count": 2400}]},
    "overlay_0022.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_22", "offset": 0x03F4, "count": 1708}]},
    "overlay_0023.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_23", "offset": 0x03D8, "count": 3852}]},
    "overlay_0024.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_24", "offset": 0x0478, "count": 2684}]},
    "overlay_0025.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_25", "offset": 0x0474, "count": 1886}]},
    "overlay_0026.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_26", "offset": 0x03D4, "count": 4106}]},
    "overlay_0027.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_27", "offset": 0x03A8, "count": 1313}]},
    "overlay_0028.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_28", "offset": 0x03B8, "count": 2287}]},
    "overlay_0029.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_29", "offset": 0x03D0, "count": 1546}]},
    "overlay_0030.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_30", "offset": 0x03CC, "count": 1558}]},
    "overlay_0031.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_31", "offset": 0x0374, "count": 3359}]},
    "overlay_0032.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_32", "offset": 0x03C4, "count": 416}]},
    "overlay_0033.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_33", "offset": 0x03CC, "count": 4534}]},
    "overlay_0034.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "tables": [{"id": "script_34", "offset": 0x03E0, "count": 466}]},
}
# ==============================================================================

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def is_sjis_lead_byte(byte_val):
    return 0x81 <= byte_val <= 0x9F or 0xE0 <= byte_val <= 0xFC

def is_sjis_trail_byte(byte_val):
    return 0x40 <= byte_val <= 0x7E or 0x80 <= byte_val <= 0xFC

# Substitua o trecho abaixo da função extract_script por esta versão:
def extract_script(f, base_config, table_config, filename):
    file_size = f.seek(0, 2)
    script_data = []
    offset_map = {}  # string_offset → lista de ids

    for i in range(table_config['count']):
        pointer_offset = table_config['offset'] + (i * 4)
        f.seek(pointer_offset)
        pointer_bytes = f.read(4)
        if len(pointer_bytes) < 4:
            break

        pointer_value = struct.unpack('<I', pointer_bytes)[0]
        string_offset = pointer_value - base_config['load_address']

        entry = {
            "id": i,
            "pointer_offset": hex(pointer_offset),
            "original_pointer_value": pointer_value,
            "string_offset": string_offset,
            "text": ""
        }

        if pointer_value == 0 or string_offset < 0 or string_offset >= file_size:
            entry["text"] = "INVALID_POINTER"
            script_data.append(entry)
            continue

        f.seek(string_offset)
        output_text = ""
        while True:
            char_byte = f.read(1)
            if not char_byte:
                break
            byte_val = char_byte[0]

            if byte_val == 0x00:
                output_text += "<00>"
                while True:
                    current_pos = f.tell()
                    if current_pos >= file_size:
                        break
                    padding_byte = f.read(1)
                    if padding_byte == b'\x00':
                        output_text += "<00>"
                    else:
                        f.seek(current_pos)
                        break
                break
            elif byte_val == 0x0A:
                output_text += "\n"
            elif is_sjis_lead_byte(byte_val):
                next_byte_pos = f.tell()
                second_byte_peek = f.read(1)
                f.seek(next_byte_pos)

                if second_byte_peek and is_sjis_trail_byte(second_byte_peek[0]):
                    second_byte = f.read(1)
                    full_char_bytes = char_byte + second_byte
                    try:
                        output_text += full_char_bytes.decode(base_config["encoding"])
                    except UnicodeDecodeError:
                        output_text += f"{{{full_char_bytes.hex().upper()}}}"
                else:
                    output_text += f"{{{byte_val:02X}}}"
            else:
                output_text += f"{{{byte_val:02X}}}"

        entry["text"] = output_text

        # ❌ Patch direto no momento da extração
        if (table_config['id'] == "script_16" and filename == "overlay_0016.bin"
           and i == 247):
           entry["text"] = "理解……！<00><00>{64}<00>{E4}<00>{03}<00><00><00>"

        if string_offset not in offset_map:
            offset_map[string_offset] = []
        offset_map[string_offset].append(i)

        script_data.append(entry)

    for entry in script_data:
        if entry["text"] != "INVALID_POINTER":
            shared = offset_map.get(entry["string_offset"], [])
            shared = [i for i in shared if i != entry["id"]]
            if shared:
                entry["shared_with"] = shared

    return script_data

def main():
    print("Iniciando ferramenta de extração definitiva...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename, config in OVERLAY_DATA.items():
        if not config.get("tables"):
            continue

        print(f"\nProcessando arquivo: '{filename}'")
        input_path = os.path.join(INPUT_DIR, filename)

        try:
            with open(input_path, "rb") as f:
                for table_info in config['tables']:
                    output_path = os.path.join(OUTPUT_DIR, f"{filename.replace('.bin', '')}_{table_info['id']}.json")
                    script_content = extract_script(f, config, table_info, filename)

                    with open(output_path, "w", encoding="utf-8") as f_out:
                        json.dump(script_content, f_out, ensure_ascii=False, indent=2)
                    print(f"  -> Tabela '{table_info['id']}' salva com {len(script_content)} entradas.")
        except FileNotFoundError:
            print(f"  [ERRO] Arquivo '{input_path}' não encontrado.")
        except Exception as e:
            print(f"  [ERRO] Falha ao processar {filename}: {e}")

    print("\nExtração concluída.")

if __name__ == "__main__":
    main()