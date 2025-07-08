import struct
import json
import os
import re
import shutil
import glob

# ==============================================================================
# CONFIGURAÇÃO MANUAL DEFINITIVA
# ==============================================================================
OVERLAY_DATA = {
    "overlay_0001.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x20},
    "overlay_0002.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x40},
    "overlay_0003.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x60},
    "overlay_0004.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x80, "forced_start_offset": 0x1D24},
    "overlay_0005.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0xA0, "forced_start_offset": 0x1B58},
    "overlay_0006.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0xC0, "forced_start_offset": 0x1344},
    "overlay_0007.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0xE0, "forced_start_offset": 0x16AC},
    "overlay_0008.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x100, "forced_start_offset": 0x11F4},
    "overlay_0009.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x120, "forced_start_offset": 0x16A8},
    "overlay_0010.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x140, "forced_start_offset": 0x1924},
    "overlay_0011.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x160, "forced_start_offset": 0x1140},
    "overlay_0012.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x180, "forced_start_offset": 0x13C0},
    "overlay_0013.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x1A0},
    "overlay_0014.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x1C0},
    "overlay_0015.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x1E0},
    "overlay_0016.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x200},
    "overlay_0017.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x220},
    "overlay_0018.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x240},
    "overlay_0019.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x260},
    "overlay_0020.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x280},
    "overlay_0021.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x2A0},
    "overlay_0022.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x2C0},
    "overlay_0023.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x2E0, "forced_start_offset": 0x4020},
    "overlay_0024.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x300},
    "overlay_0025.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x320},
    "overlay_0026.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x340},
    "overlay_0027.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x360},
    "overlay_0028.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x380},
    "overlay_0029.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x3A0},
    "overlay_0030.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x3C0},
    "overlay_0031.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x3E0},
    "overlay_0032.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x400},
    "overlay_0033.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x420},
    "overlay_0034.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x440},
    "overlay_0035.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x460},
    "overlay_0036.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x480},
    "overlay_0037.bin": {"load_address": 0x0227C3C0, "encoding": "shift_jis", "y9_offset": 0x4A0}
}

INPUT_DIR = "input"
TRANSLATED_DIR = "translated"
REPACKED_DIR = "repacked"
Y9_DIR = "y9"

def main():
    print("Iniciando ferramenta de REPACK com REUTILIZAÇÃO de textos e shared_with...")
    os.makedirs(REPACKED_DIR, exist_ok=True)
    
    y9_input_path = os.path.join(Y9_DIR, "y9.bin")
    y9_output_path = os.path.join(REPACKED_DIR, "y9.bin")

    if not os.path.exists(y9_input_path):
        print(f"[ERRO] '{y9_input_path}' não encontrado. Este arquivo é essencial.")
        return

    with open(y9_input_path, "rb") as f:
        y9_data = bytearray(f.read())

    files_to_process = {}
    json_files = glob.glob(os.path.join(TRANSLATED_DIR, '*.json'))
    for json_path in json_files:
        try:
            base_name = os.path.basename(json_path).split('_')[0] + "_" + os.path.basename(json_path).split('_')[1]
            overlay_filename = f"{base_name}.bin"
            if overlay_filename not in files_to_process:
                files_to_process[overlay_filename] = []
            files_to_process[overlay_filename].append(json_path)
        except IndexError:
            print(f"[AVISO] Ignorando arquivo JSON com nome mal formatado: {json_path}")

    tag_regex = re.compile(r'(\{[0-9A-Fa-f]{2}\}|\n|<00>)')

    for filename, json_paths in files_to_process.items():
        print(f"\nRepackando '{filename}'...")
        original_path = os.path.join(INPUT_DIR, filename)

        if filename not in OVERLAY_DATA:
            print(f"  [AVISO] Nenhuma configuração encontrada para '{filename}'. Pulando.")
            continue

        config = OVERLAY_DATA[filename]

        with open(original_path, "rb") as f:
            original_overlay_data = bytearray(f.read())

        all_entries = []
        for json_path in json_paths:
            with open(json_path, 'r', encoding='utf-8') as f:
                all_entries.extend(json.load(f))

        # Determina o offset mínimo para truncar
        if "forced_start_offset" in config:
            min_string_offset = config["forced_start_offset"]
            print(f"  [Info] Início do bloco de texto forçado para 0x{min_string_offset:X}")
        else:
            min_string_offset = float('inf')
            for entry in all_entries:
                offset = entry['original_pointer_value'] - config['load_address']
                if 0 <= offset < min_string_offset:
                    min_string_offset = offset

            if min_string_offset == float('inf'):
                print("  [AVISO] Nenhum texto válido encontrado para este overlay. Copiando o arquivo original.")
                shutil.copy(original_path, os.path.join(REPACKED_DIR, filename))
                continue

        print(f"  [Info] Bloco de texto começa em 0x{min_string_offset:X}. Truncando o arquivo aqui.")
        repacked_data = original_overlay_data[:min_string_offset]
        eof_offset = len(repacked_data)

        # Mapas para controlar textos já escritos e offsets
        text_offset_map = {}  # texto codificado (bytes) → offset onde foi escrito
        id_to_offset_map = {} # id → offset usado para ponteiro

        # Cria um dicionário id → entry para facilitar acesso
        entries_by_id = {entry['id']: entry for entry in all_entries}

        # Para controlar quais ids já foram escritos/reaproveitados
        written_ids = set()

        for entry in all_entries:
            current_id = entry['id']
            if current_id in written_ids:
                # Já processado por shared_with
                continue

            # Codificar o texto
            parts = tag_regex.split(entry["text"])
            final_encoded_bytes = bytearray()
            for part in parts:
                if not part:
                    continue
                if part == '\n':
                    final_encoded_bytes.append(0x0A)
                elif part == '<00>':
                    final_encoded_bytes.append(0x00)
                elif part.startswith('{') and part.endswith('}'):
                    final_encoded_bytes.append(int(part.strip('{}'), 16))
                else:
                    final_encoded_bytes.extend(part.encode(config["encoding"], 'ignore'))

            text_key = bytes(final_encoded_bytes)

            shared_ids = entry.get("shared_with", [])

            if shared_ids:
                # Tem compartilhamento
                # Escreve o texto uma vez
                reused_offset = eof_offset
                repacked_data.extend(final_encoded_bytes)
                eof_offset += len(final_encoded_bytes)

                # Atualiza offset para o id atual e os compartilhados
                id_to_offset_map[current_id] = reused_offset
                written_ids.add(current_id)

                for sid in shared_ids:
                    id_to_offset_map[sid] = reused_offset
                    written_ids.add(sid)

                print(f"    Escrevendo texto compartilhado ID {current_id} e ids {shared_ids} no offset 0x{reused_offset:X}")

            else:
                # Não tem shared_with, escreve o texto diretamente
                reused_offset = eof_offset
                repacked_data.extend(final_encoded_bytes)
                eof_offset += len(final_encoded_bytes)
                id_to_offset_map[current_id] = reused_offset
                written_ids.add(current_id)
                print(f"    Escrevendo texto ID {current_id} no offset 0x{reused_offset:X}")

        # Agora escreve todos os ponteiros (inclusive reaproveitando offsets para shared_with)
        for entry in all_entries:
            id_ = entry['id']
            offset_to_write = int(entry['pointer_offset'], 16)
            if id_ not in id_to_offset_map:
                print(f"    [AVISO] ID {id_} sem offset calculado! Ignorando ponteiro.")
                continue

            new_pointer_val = config['load_address'] + id_to_offset_map[id_]
            packed_pointer = struct.pack('<I', new_pointer_val)
            repacked_data[offset_to_write:offset_to_write + 4] = packed_pointer

        # Salva arquivo reempacotado
        repacked_path = os.path.join(REPACKED_DIR, filename)
        with open(repacked_path, "wb") as f_out:
            f_out.write(repacked_data)

        # Atualiza tamanho no y9.bin
        new_size = len(repacked_data)
        size_offset = config['y9_offset'] + 0x08
        print(f"  -> Tamanho novo: {new_size} bytes. Atualizando y9.bin no offset 0x{size_offset:X}...")
        packed_size = struct.pack('<I', new_size)
        y9_data[size_offset:size_offset + 4] = packed_size

    # Salva y9.bin atualizado
    with open(y9_output_path, "wb") as f_out:
        f_out.write(y9_data)

    print("\nProcesso concluído. Arquivos finais estão na pasta 'repacked'.")

if __name__ == "__main__":
    main()