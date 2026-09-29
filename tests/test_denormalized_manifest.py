"""Tests for building the denormalized Manifest table."""

import unittest
from typing import cast
from unittest.mock import patch

import pandas as pd

from scripts.publishing import denormalized_manifest as manifest_module


class BuildDenormalizedDfTests(unittest.TestCase):
    """Verify Manifest records are expanded and linked correctly."""

    @patch.object(manifest_module, "get_anatomy_label_cached", return_value="Retina")
    @patch.object(manifest_module, "load_json_to_dataframe")
    def test_build_denormalized_df_explodes_data_parts_and_builds_links(
        self,
        mock_load_json_to_dataframe,
        _mock_get_anatomy_label_cached,
    ):
        """build_denormalized_df should emit one row per data part and populate resolved markdown links."""
        mock_load_json_to_dataframe.return_value = pd.DataFrame([
            {
                "id": "B2AI_MANIFEST:1",
                "organization": "B2AI_ORG:1",
                "datasets": ["B2AI_DATA:1", "B2AI_DATA:2"],
                "data_parts": [
                    {
                        "data_part_name": "Imaging",
                        "data_part_description": "Image data",
                        "standards_and_tools": ["B2AI_STANDARD:1"],
                        "uses_data_substrates": ["B2AI_SUBSTRATE:1"],
                        "concerns_data_topics": ["B2AI_TOPIC:1"],
                        "anatomy": ["UBERON:0001"],
                    },
                    {
                        "data_part_name": "Metadata",
                        "data_part_description": "Metadata only",
                    },
                ],
            },
        ])
        lookups = {
            "Organization": {"B2AI_ORG:1": "Org One"},
            "DataStandardOrTool": {"B2AI_STANDARD:1": "FHIR"},
            "DataSubstrate": {"B2AI_SUBSTRATE:1": "Microscopy Image"},
            "DataTopic": {"B2AI_TOPIC:1": "Cell Morphology"},
            "topic_standard_counts": {"B2AI_TOPIC:1": 5},
        }

        df = manifest_module.build_denormalized_df(lookups)

        self.assertEqual(len(df), 2)
        self.assertEqual(df.loc[0, "organization"], "B2AI_ORG:1")
        self.assertEqual(df.loc[0, "standards_and_tools_links"], ["[FHIR](/Explore/Standard/DetailsPage?id=B2AI_STANDARD:1)"])
        self.assertEqual(
            df.loc[0, "uses_data_substrates_links"],
            ["[Microscopy Image](https://bridge2ai.github.io/b2ai-standards-registry/substrates/microscopy-image/)"],
        )
        topic_links = cast(list[str], df.loc[0, "concerns_data_topics_links"])
        self.assertTrue(topic_links[0].startswith("[Cell Morphology (5)](/Explore?qw0="))
        self.assertEqual(
            df.loc[0, "anatomy_links"],
            ["[Retina](http://purl.obolibrary.org/obo/UBERON_0001)"],
        )
        self.assertEqual(df.loc[0, "datasets"], ["B2AI_DATA:1", "B2AI_DATA:2"])
        self.assertEqual(df.loc[1, "standards_and_tools"], [])


class AnatomyLabelLookupTests(unittest.TestCase):
    """A failed label lookup is recorded; a term with no label isn't."""

    @patch.object(manifest_module, "get_ontology_label",
                  side_effect=manifest_module.requests.ConnectionError("down"))
    def test_network_failure_is_recorded(self, _mock_get_ontology_label):
        failures: list[str] = []
        label = manifest_module.get_anatomy_label_cached("UBERON:0001", {}, failures)
        self.assertIsNone(label)
        self.assertEqual(failures, ["UBERON:0001"])

    @patch.object(manifest_module, "get_ontology_label", return_value=None)
    def test_missing_label_is_not_a_failure(self, _mock_get_ontology_label):
        failures: list[str] = []
        self.assertIsNone(manifest_module.get_anatomy_label_cached("UBERON:0001", {}, failures))
        self.assertEqual(failures, [])


class GetOntologyLabelTests(unittest.TestCase):
    """get_ontology_label only raises when asked to, and never for a 404."""

    def response(self, status):
        response = manifest_module.requests.Response()
        response.status_code = status
        return response

    def test_server_error_raises_only_when_asked(self):
        with patch.object(manifest_module.requests, "get", return_value=self.response(503)):
            self.assertIsNone(manifest_module.get_ontology_label("UBERON:0001"))
            with self.assertRaises(manifest_module.requests.HTTPError):
                manifest_module.get_ontology_label("UBERON:0001", raise_on_error=True)

    def test_not_found_never_raises(self):
        with patch.object(manifest_module.requests, "get", return_value=self.response(404)):
            self.assertIsNone(manifest_module.get_ontology_label("UBERON:0001", raise_on_error=True))

    def test_connection_error_raises_only_when_asked(self):
        with patch.object(manifest_module.requests, "get", side_effect=manifest_module.requests.ConnectionError()):
            self.assertIsNone(manifest_module.get_ontology_label("UBERON:0001"))
            with self.assertRaises(manifest_module.requests.ConnectionError):
                manifest_module.get_ontology_label("UBERON:0001", raise_on_error=True)


if __name__ == "__main__":
    unittest.main()
