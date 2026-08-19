import json
import unittest
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def get(endpoint, **params):
    params.update(db="clinvar", retmode="json", tool="clinvar-genes-test")
    with urlopen(f"{EUTILS}/{endpoint}.fcgi?{urlencode(params)}", timeout=30) as response:
        return json.load(response)


class ClinVarTest(unittest.TestCase):
    def test_gene_has_clinical_significance(self):
        genes = (Path(__file__).parent / "fixtures/gene_list.txt").read_text().splitlines()
        gene = genes[0]

        search = get("esearch", term=f"{gene}[gene]", retmax=1)
        clinvar_id = search["esearchresult"]["idlist"][0]
        record = get("esummary", id=clinvar_id)["result"][clinvar_id]

        self.assertIn(gene, {item["symbol"] for item in record["genes"]})
        self.assertTrue(record["germline_classification"]["description"])


if __name__ == "__main__":
    unittest.main()
