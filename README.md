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

Successful lookups are written to `results.out.tsv` as tab-separated input
gene symbol, NCBI Gene ID, and `germline_classification.description`:

```text
TP53	7157	Pathogenic
```

Every successful input gene also writes its complete, unmodified ESummary
record to the NDJSON file. Genes without a result and other per-gene failures
produce an error record instead of stopping the run.
See [the script documentation](scripts/README.clinvar_genes.md) for the full
input and output formats.

## Querying results with jq

Because each successful NDJSON line contains the full ClinVar record, `jq` can
extract fields not included in the TSV output. This example prints the ClinVar
accession, title, and review status while skipping error records:

```sh
jq -r 'select(has("error") | not) | [.accession_version, .title, .germline_classification.review_status] | @tsv' results.ndjson
```

To inspect the complete first successful record:

```sh
jq -n 'first(inputs | select(has("error") | not))' results.ndjson
```

## Tests

```sh
.venv/bin/python -m unittest discover -v
```

The suite includes a mocked script test and a live ClinVar integration test;
the full suite therefore requires internet access. See
[the test documentation](tests/README.test_clinvar.md) for test coverage, the
API flow, and response schemas.
