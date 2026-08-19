#!/usr/bin/env python3
import argparse
import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def get(endpoint, **params):
    time.sleep(0.34)  # NCBI permits at most three requests/second without an API key.
    params.update(db="clinvar", retmode="json", tool="clinvar-genes")
    with urlopen(f"{EUTILS}/{endpoint}.fcgi?{urlencode(params)}", timeout=30) as response:
        return json.load(response)


def lookup(gene):
    ids = get("esearch", term=f"{gene}[gene]", retmax=1)["esearchresult"]["idlist"]
    if not ids:
        return {"gene": gene, "error": "no ClinVar result"}

    clinvar_id = ids[0]
    record = get("esummary", id=clinvar_id)["result"][clinvar_id]
    matching_gene = next((item for item in record["genes"] if item["symbol"] == gene), None)
    if not matching_gene:
        return {"gene": gene, "error": "gene missing from ClinVar result"}

    description = record["germline_classification"]["description"]
    if not description:
        return {"gene": gene, "gene_id": matching_gene["geneid"], "error": "no germline classification"}

    return record


def main():
    parser = argparse.ArgumentParser(description="Write ClinVar classifications as NDJSON.")
    parser.add_argument("input", type=Path, help="newline-delimited gene symbols")
    parser.add_argument("output", type=Path, help="output NDJSON file")
    args = parser.parse_args()

    with args.output.open("w") as output:
        for gene in filter(None, map(str.strip, args.input.read_text().splitlines())):
            try:
                result = lookup(gene)
            except Exception as error:
                result = {"gene": gene, "error": str(error)}
            output.write(json.dumps(result) + "\n")
            if "error" not in result:
                gene_id = next(item["geneid"] for item in result["genes"] if item["symbol"] == gene)
                print(gene, gene_id, result["germline_classification"]["description"], sep="\t")


if __name__ == "__main__":
    main()
