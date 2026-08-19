# ClinVar gene lookup

`clinvar_genes.py` reads newline-delimited gene symbols, retrieves one matching
ClinVar record per gene, and writes one NDJSON record per nonblank input line.

## Usage

Python 3.12 or newer is required. From the project root:

```sh
scripts/clinvar_genes.py tests/fixtures/gene_list.txt results.ndjson
```

The two positional arguments are:

1. `input`: a text file containing one gene symbol per line.
2. `output`: the NDJSON file to create or overwrite.

For each gene, the script searches ClinVar with `<gene>[gene]`, requests the
first matching record, and reads its `germline_classification.description`.

## Standard output

Successful lookups print the input gene symbol, NCBI Gene ID, and
classification, separated by tabs:

```text
TP53	7157	Pathogenic
```

Failed lookups are not printed to standard output.

## NDJSON output

Each line is an independent JSON object. A successful lookup has this shape:

```json
{"gene":"TP53","gene_id":"7157","clinvar_id":"123","germline_classification":{"description":"Pathogenic"}}
```

| Field | Description |
| --- | --- |
| `gene` | Input gene symbol. |
| `gene_id` | NCBI Gene ID from the matching ClinVar record. |
| `clinvar_id` | ClinVar record ID selected by ESearch. |
| `germline_classification.description` | ClinVar germline clinical significance. |

If no ClinVar record is found, the script writes an error record and continues:

```json
{"gene":"UNKNOWN","error":"no ClinVar result"}
```

Missing classifications, mismatched records, network failures, invalid API
responses, and other per-gene lookup failures are also written as error records.
They do not stop the remaining genes from being processed.

## Live-service behavior

The script uses NCBI's live ESearch and ESummary endpoints, so results can
change with ClinVar releases and internet access is required. Requests are
limited to fewer than three per second to comply with NCBI's unauthenticated
E-utilities rate limit. With two requests per successful gene, large input
files can take several minutes.
