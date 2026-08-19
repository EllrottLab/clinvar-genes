import unittest
from unittest.mock import patch

from scripts.clinvar_genes import lookup


class ClinVarScriptTest(unittest.TestCase):
    @patch("scripts.clinvar_genes.get")
    def test_lookup_returns_classification_or_error(self, get):
        get.return_value = {"esearchresult": {"idlist": []}}
        self.assertEqual(lookup("UNKNOWN"), {"gene": "UNKNOWN", "error": "no ClinVar result"})

        get.side_effect = [
            {"esearchresult": {"idlist": ["123"]}},
            {
                "result": {
                    "123": {
                        "genes": [{"symbol": "TP53", "geneid": "7157"}],
                        "germline_classification": {"description": "Pathogenic"},
                    }
                }
            },
        ]
        self.assertEqual(
            lookup("TP53"),
            {
                "gene": "TP53",
                "gene_id": "7157",
                "clinvar_id": "123",
                "germline_classification": {"description": "Pathogenic"},
            },
        )


if __name__ == "__main__":
    unittest.main()
