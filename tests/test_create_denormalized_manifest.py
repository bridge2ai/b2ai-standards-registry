"""Tests for building and uploading the denormalized Manifest table."""

import unittest
from typing import cast
from unittest.mock import patch, sentinel

import pandas as pd

from scripts import create_denormalized_manifest as manifest_module


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
        self.assertEqual(df.loc[0, "organization_link"], "[Org One](/Explore/Organization/OrganizationDetailsPage?id=B2AI_ORG:1)")
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
        self.assertEqual(
            df.loc[0, "datasets_link"],
            "[2 datasets](/Explore/Organization/OrganizationDetailsPage?id=B2AI_ORG:1#DataSets)",
        )
        self.assertEqual(df.loc[1, "standards_and_tools"], [])


class UploadDenormalizedManifestTests(unittest.TestCase):
    """Verify denormalized Manifest upload orchestration."""

    @patch.object(manifest_module, "clear_populate_snapshot_table")
    @patch.object(manifest_module, "get_column_definitions")
    @patch.object(manifest_module, "build_denormalized_df")
    @patch.object(manifest_module, "build_lookup_dicts")
    @patch.object(manifest_module, "initialize_synapse")
    def test_upload_denormalized_manifest_uses_supplied_syn_and_table_id(
        self,
        mock_initialize_synapse,
        mock_build_lookup_dicts,
        mock_build_denormalized_df,
        mock_get_column_definitions,
        mock_clear_populate_snapshot_table,
    ):
        """upload_denormalized_manifest should reuse a provided Synapse client and explicit table ID."""
        df = pd.DataFrame([{"id": "B2AI_MANIFEST:1"}])
        mock_build_lookup_dicts.return_value = {"Organization": {}}
        mock_build_denormalized_df.return_value = df
        mock_get_column_definitions.return_value = [sentinel.column]

        returned_df = manifest_module.upload_denormalized_manifest(
            syn=sentinel.synapse,
            table_id="syn123",
        )

        self.assertIs(returned_df, df)
        mock_initialize_synapse.assert_not_called()
        mock_clear_populate_snapshot_table.assert_called_once_with(
            sentinel.synapse,
            "Manifest",
            [sentinel.column],
            df,
            "syn123",
        )


if __name__ == "__main__":
    unittest.main()
