# clinvar-genes

Look up germline clinical-significance classifications for a newline-delimited
list of gene symbols using NCBI ClinVar.

## Requirements

- Python 3.12 or newer
- Internet access to NCBI E-utilities

The project uses only the Python standard library.

## Usage

```sh
python3.12 -m venv .venv
.venv/bin/python scripts/clinvar_genes.py tests/fixtures/gene_list.txt results.ndjson > results.out.tsv
```

Successful lookups are written to standard output as tab-separated gene
symbol, NCBI Gene ID, and germline classification:

```text
TP53	7157	Pathogenic
```

Every input gene also produces an NDJSON record. Genes without a result and
other per-gene failures produce an error record instead of stopping the run.
See [the script documentation](scripts/README.clinvar_genes.md) for the full
input and output formats.

## Tests

```sh
.venv/bin/python -m unittest discover -v
```

The suite includes a live ClinVar integration test and therefore requires
internet access. See [the test documentation](tests/README.test_clinvar.md) for
the API flow and response schemas.
