# ClinVar tests

Run both tests from the project root:

```sh
.venv/bin/python -m unittest discover -v
```

`test_clinvar_script.py` mocks NCBI responses and verifies that the lookup
preserves the complete ESummary record, or returns a non-fatal error record
when no result exists.

## Live integration test

`test_clinvar.py` verifies that a gene from `fixtures/gene_list.txt` has a
ClinVar record with a germline clinical-significance classification.

The test reads the fixture, selects its first gene, and makes two live requests
to the NCBI E-utilities API:

1. `esearch.fcgi` searches ClinVar for `<gene>[gene]` and returns one ClinVar ID.
2. `esummary.fcgi` retrieves that record. The test confirms that the requested
   gene appears in `genes` and that `germline_classification.description` is
   non-empty.

Run only the integration test with:

```sh
.venv/bin/python -m unittest tests.test_clinvar -v
```

This is an integration test: it requires internet access and depends on live
ClinVar data. Record IDs and classifications may change between ClinVar
releases.

## Response payloads

Both endpoints return JSON. The schemas below show the fields consumed by the
test; NCBI may include additional fields.

### ESearch

```json
{
  "header": {
    "type": "string",
    "version": "string"
  },
  "esearchresult": {
    "count": "string containing an integer",
    "retmax": "string containing an integer",
    "retstart": "string containing an integer",
    "idlist": ["ClinVar ID as a string"],
    "translationset": [],
    "translationstack": [],
    "querytranslation": "string"
  }
}
```

The test uses `esearchresult.idlist[0]` as the ID for the summary request.

### ESummary

```json
{
  "header": {
    "type": "string",
    "version": "string"
  },
  "result": {
    "uids": ["ClinVar ID"],
    "<ClinVar ID>": {
      "uid": "string",
      "accession": "string",
      "accession_version": "string",
      "title": "string",
      "genes": [
        {
          "symbol": "string",
          "geneid": "string",
          "strand": "string",
          "source": "string"
        }
      ],
      "germline_classification": {
        "description": "string",
        "last_evaluated": "string",
        "review_status": "string",
        "fda_recognized_database": "string",
        "trait_set": [
          {
            "trait_name": "string",
            "trait_xrefs": [
              {
                "db_source": "string",
                "db_id": "string"
              }
            ]
          }
        ]
      }
    }
  }
}
```

The `<ClinVar ID>` property is dynamic and matches the ID listed in `uids`.
Clinical significance is the non-empty value at
`result[clinvar_id].germline_classification.description`, for example
`"Pathogenic"`, `"Likely pathogenic"`, or `"Uncertain significance"`.
The script writes the complete `result[clinvar_id]` object as one NDJSON line;
the outer ESummary response envelope is not included.
