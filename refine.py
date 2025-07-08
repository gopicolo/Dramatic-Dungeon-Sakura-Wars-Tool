import json
import os
import glob

# --- Configuração das Pastas ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_JSON_DIR = os.path.join(SCRIPT_DIR, "output")
REFINED_JSON_DIR = os.path.join(SCRIPT_DIR, "refined_json")
# --------------------------------

def refine_json_file(input_path, output_path):
    """
    Lê um arquivo JSON, remove entradas inválidas, substitui tags,
    re-indexa os IDs e corrige o campo 'shared_with'.
    Também remove entradas cujo texto seja exatamente strings indesejadas.
    """
    try:
        print(f"  [INFO] Lendo '{input_path}'...")
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        refined_data = []
        id_map = {}  # id antigo → novo id
        old_id = 0
        new_id = 0

        # Strings que, se forem exatamente iguais ao texto, devem ser removidas
        EXACT_STRINGS_TO_REMOVE = [
            "{20}<00>", "{64}<00>", "{1E}<00>",
            "{32}<00>", "{1F}<00>", "{1D}<00>",
            "{1B}<00>", "{24}<00>", "{06}<00>",
            "{18}<00>", "{16}<00>", "{1A}<00>",
            "{10}<00>", "{22}<00>", "{21}<00>",
            "{4B}<00>",
            "{AA}{AA}{55}{D5}<00>",
            "{38}{DB}{27}{02}{03}<00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00>",
            "{24}{D8}{27}{02}{03}<00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00><00>"
        ]

        # 1. Filtra entradas inválidas e cria o id_map
        for entry in data:
            text = entry['text']

            # Pula texto inválido ou exato a ser removido
            if "INVALID_POINTER" in text or text in EXACT_STRINGS_TO_REMOVE:
                old_id += 1
                continue

            # Substitui tags comuns
            text = text.replace('{21}', '!').replace('{3F}', '?')
            entry['text'] = text

            id_map[entry['id']] = new_id
            entry['id'] = new_id
            refined_data.append(entry)

            old_id += 1
            new_id += 1

        # 2. Corrige os shared_with
        for entry in refined_data:
            if "shared_with" in entry:
                updated_shared = [
                    id_map[old_id]
                    for old_id in entry["shared_with"]
                    if old_id in id_map
                ]
                if updated_shared:
                    entry["shared_with"] = updated_shared
                else:
                    entry.pop("shared_with")

        # 3. Salva a saída
        with open(output_path, 'w', encoding='utf-8') as f_out:
            json.dump(refined_data, f_out, ensure_ascii=False, indent=2)

        print(f"  -> Sucesso! {len(refined_data)} entradas válidas refinadas e salvas em '{output_path}'")

    except FileNotFoundError:
        print(f"  [AVISO] Arquivo não encontrado, pulando: {input_path}")
    except Exception as e:
        print(f"  [ERRO] Ocorreu um erro ao processar {input_path}: {e}")

def main():
    """
    Função principal que encontra e processa todos os arquivos JSON.
    """
    print("Iniciando ferramenta de refinamento de arquivos JSON...")

    # Cria a pasta de saída se ela não existir
    os.makedirs(REFINED_JSON_DIR, exist_ok=True)

    # Encontra todos os arquivos .json na pasta de entrada
    json_files = glob.glob(os.path.join(INPUT_JSON_DIR, '*.json'))

    if not json_files:
        print(f"Nenhum arquivo .json encontrado na pasta '{INPUT_JSON_DIR}'. Execute o extrator primeiro.")
        return

    for json_path in json_files:
        filename = os.path.basename(json_path)
        print(f"\nRefinando '{filename}'...")

        output_path = os.path.join(REFINED_JSON_DIR, filename)
        refine_json_file(json_path, output_path)

    print("\nRefinamento de todos os arquivos concluído.")
    print(f"Os arquivos refinados estão na pasta '{REFINED_JSON_DIR}'.")

if __name__ == "__main__":
    main()
