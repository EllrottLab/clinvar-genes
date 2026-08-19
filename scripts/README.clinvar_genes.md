# ClinVar gene lookup

`clinvar_genes.py` reads newline-delimited gene symbols, retrieves one matching
ClinVar record per gene, and writes one NDJSON record per nonblank input line.
Successful lines contain the complete ESummary record returned by ClinVar.

## Usage

Python 3.12 or newer is required. From the project root:

```sh
scripts/clinvar_genes.py tests/fixtures/gene_list.txt results.ndjson > results.out.tsv
```

The two positional arguments are:

1. `input`: a text file containing one gene symbol per line.
2. `output`: the NDJSON file to create or overwrite.

For each gene, the script searches ClinVar with `<gene>[gene]`, requests the
first matching record, and reads its `germline_classification.description`.

## Standard output

Successful lookups print these fields, in order and separated by tabs:

1. Input gene symbol
2. NCBI Gene ID
3. `germline_classification.description`

```text
TP53	7157	Pathogenic
```

The usage example redirects this stream to `results.out.tsv`. Failed lookups
are not printed to standard output; their error records still appear in the
NDJSON file.

## NDJSON output

Each line is an independent JSON object. On success, it is the complete object
at `result[clinvar_id]` in the ESummary response. The surrounding response
envelope (`header`, `result`, and `uids`) is not written, but no fields inside
the selected ClinVar record are selected, renamed, or discarded. See
[the test documentation](../tests/README.test_clinvar.md#esummary) for the
response structure and fields used for standard output.

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
