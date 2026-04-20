import os
import re
import argparse
from pathlib import Path
from collections import defaultdict, Counter

import pandas as pd
from tqdm import tqdm


DEFAULT_INPUT_DIR = "TestData"
DEFAULT_REF_FFN = "matched_from_pse_all.ffn"
DEFAULT_OUTPUT_DIR = "output_csv"
FINAL_OUTPUT_NAME = "ALL_RESULT.csv"


def clean_gene_name(name):
    return re.sub(r"\.peg\.\d+.*$", "", str(name), flags=re.IGNORECASE)


def format_cluster_name(name):
    return re.sub(r"([A-Za-z]+)(\d+)$", r"\1 \2", name)


def map_base(x):
    if x in ["A", "a"]:
        return "2"
    elif x in ["T", "t"]:
        return "3"
    elif x in ["C", "c"]:
        return "4"
    elif x in ["G", "g"]:
        return "5"
    else:
        return x


def parse_ref_header(header):
    header = header[1:].strip()
    pipe_idx = header.find("|")
    triple_space_idx = header.find("   ")

    if pipe_idx != -1 and triple_space_idx != -1 and triple_space_idx > pipe_idx:
        return header[pipe_idx + 1:triple_space_idx].strip()
    if pipe_idx != -1:
        return header[pipe_idx + 1:].strip()
    return header


def parse_input_header(header):
    header = header[1:].strip()
    pipe_idx = header.find("|")
    if pipe_idx != -1 and pipe_idx + 1 < len(header):
        return header[pipe_idx + 1:].strip()
    return header


def parse_fasta_to_dict(filepath, ref_mode=False):
    seq_dict = {}
    current_name = None
    seq_parts = []

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for raw_line in f:
            line = raw_line.strip()

            if not line:
                continue

            if line.startswith(">"):
                if current_name is not None:
                    seq_dict[current_name] = "".join(seq_parts)

                if ref_mode:
                    current_name = parse_ref_header(line)
                else:
                    current_name = parse_input_header(line)

                seq_parts = []
            else:
                seq_parts.append(line)

    if current_name is not None:
        seq_dict[current_name] = "".join(seq_parts)

    return seq_dict


def convert_triplets(ref_seq, target_seq):
    if not ref_seq or not target_seq:
        return "PP"

    if len(target_seq) % 3 != 0:
        return "PP"

    result = []
    target_idx = 0

    for ch in ref_seq:
        if ch == "-":
            result.extend(["0", "0", "0"])
        else:
            if target_idx + 3 > len(target_seq):
                return "PP"
            result.extend([
                target_seq[target_idx],
                target_seq[target_idx + 1],
                target_seq[target_idx + 2]
            ])
            target_idx += 3

    if target_idx != len(target_seq):
        return "PP"

    return result


def select_representative_genes(converted, valid_genes):
    grouped = defaultdict(list)

    for gene in valid_genes:
        grouped[clean_gene_name(gene)].append(gene)

    selected_genes = {}

    for cleaned_name, genes in grouped.items():
        if len(genes) == 1:
            selected_genes[cleaned_name] = genes[0]

        elif len(genes) == 2:
            selected_genes[cleaned_name] = genes[0]

        else:
            seq_list = []
            gene_seq_pairs = []

            for g in genes:
                seq = converted.get(g)
                if seq == "PP":
                    continue
                seq_tuple = tuple(seq)
                seq_list.append(seq_tuple)
                gene_seq_pairs.append((g, seq_tuple))

            if not seq_list:
                continue

            most_common_seq, _ = Counter(seq_list).most_common(1)[0]

            for g, seq_tuple in gene_seq_pairs:
                if seq_tuple == most_common_seq:
                    selected_genes[cleaned_name] = g
                    break

    return selected_genes


def process_one_file(input_path, ref_dict):
    target_dict = parse_fasta_to_dict(input_path, ref_mode=False)

    if not target_dict:
        return None

    common_keys = [k for k in target_dict if k in ref_dict]
    if not common_keys:
        return None

    converted = {}
    for gene in common_keys:
        converted[gene] = convert_triplets(
            target_dict.get(gene, ""),
            ref_dict.get(gene, "")
        )

    valid_genes = [g for g in converted if converted[g] != "PP"]
    if not valid_genes:
        return None

    selected_genes = select_representative_genes(converted, valid_genes)
    if not selected_genes:
        return None

    representative_genes = list(selected_genes.values())

    lengths = [len(converted[g]) for g in representative_genes if isinstance(converted[g], list)]
    if not lengths:
        return None

    listx_len = min(lengths)

    safe_selected_genes = {}
    for cleaned_name, original_gene in selected_genes.items():
        seq = converted.get(original_gene)
        if isinstance(seq, list) and len(seq) >= listx_len:
            safe_selected_genes[cleaned_name] = original_gene

    if not safe_selected_genes:
        return None

    representative_genes = list(safe_selected_genes.values())
    listx_len = min(len(converted[g]) for g in representative_genes)

    output_data = {}
    base_name = Path(input_path).stem
    base_name_fixed = format_cluster_name(base_name)

    for j in range(listx_len):
        try:
            list4 = [converted[g][j] for g in representative_genes]
        except IndexError:
            continue

        if "0" not in list4 and len(set(list4)) > 2:
            col_name = f"{base_name_fixed}_{j}"
            output_data[col_name] = {
                cleaned_name: map_base(converted[original_gene][j])
                for cleaned_name, original_gene in safe_selected_genes.items()
            }

    df = pd.DataFrame(output_data)

    if not df.empty:
        df = df.reindex(list(safe_selected_genes.keys()))

    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", default=DEFAULT_INPUT_DIR)
    parser.add_argument("--ref_ffn", default=DEFAULT_REF_FFN)
    parser.add_argument("--output_dir", default=DEFAULT_OUTPUT_DIR)

    args = parser.parse_args()

    INPUT_DIR = args.input_dir
    REF_FFN = args.ref_ffn
    OUTPUT_DIR = args.output_dir

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(REF_FFN):
        print("Reference file missing")
        return

    if not os.path.isdir(INPUT_DIR):
        print("Input folder missing")
        return

    ref_dict = parse_fasta_to_dict(REF_FFN, ref_mode=True)

    file_list = []
    for root, _, files in os.walk(INPUT_DIR):
        for f in files:
            file_list.append(os.path.join(root, f))

    all_dfs = []

    for input_path in tqdm(file_list):
        try:
            df = process_one_file(input_path, ref_dict)
            if df is not None and not df.empty:
                all_dfs.append(df)
        except Exception as e:
            print(f"[ERROR] {input_path}: {e}")

    if all_dfs:
        final_df = pd.concat(all_dfs, axis=1)
        final_df = final_df.fillna(0)

        output_path = os.path.join(OUTPUT_DIR, FINAL_OUTPUT_NAME)
        final_df.to_csv(output_path, encoding="utf-8-sig")

        print(f"[DONE] Merged file saved: {output_path}")
    else:
        print("[WARNING] No data to merge")


if __name__ == "__main__":
    main()