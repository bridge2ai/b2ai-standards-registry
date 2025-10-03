#!/usr/bin/env python3
"""Shared ID linking functionality for B2AI documentation pages.

This module provides functions to convert B2AI IDs in text to appropriate markdown links
across different resource types (substrates, topics, standards, use cases, datasets).
"""
from __future__ import annotations
import re
import unicodedata
from pathlib import Path
from typing import Dict
import yaml


def slugify(value: str) -> str:
    """Convert a string to a URL-friendly slug."""
    value = unicodedata.normalize('NFKD', value).encode(
        'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^a-zA-Z0-9]+', '-', value).strip('-').lower()
    return value or 'default'


def load_all_b2ai_data() -> Dict[str, Dict]:
    """Load all B2AI data files and create ID-to-info mappings."""
    repo_root = Path(__file__).resolve().parent.parent
    data_mappings = {}

    # Data files and their keys
    data_files = {
        'DataStandardOrTool.yaml': 'data_standardortools_collection',
        'DataSet.yaml': 'data_collection',
        'DataSubstrate.yaml': 'data_substrates_collection',
        'DataTopic.yaml': 'data_topics_collection',
        'UseCase.yaml': 'use_cases'
    }

    for filename, key in data_files.items():
        file_path = repo_root / 'src' / 'data' / filename
        if file_path.exists():
            with open(file_path, 'r') as f:
                data = yaml.safe_load(f)
                items = data.get(key, [])
                for item in items:
                    if 'id' in item:
                        data_mappings[item['id']] = item

    return data_mappings


def convert_ids_to_links(text: str, all_data: Dict[str, Dict] | None = None, relative_path_prefix: str = "..") -> str:
    """Convert B2AI IDs in text to appropriate markdown links.

    Args:
        text: Text containing B2AI IDs to convert
        all_data: Dictionary mapping B2AI IDs to their data. If None, will load automatically.
        relative_path_prefix: Path prefix for relative links (e.g., ".." for going up one directory)

    Returns:
        Text with B2AI IDs converted to markdown links
    """
    if not text:
        return text

    if all_data is None:
        all_data = load_all_b2ai_data()

    # Pattern to match B2AI IDs
    id_pattern = r'(B2AI_(?:STANDARD|DATA|SUBSTRATE|TOPIC|USECASE):\d+)'

    def replace_id(match):
        id_str = match.group(1)

        if id_str.startswith('B2AI_STANDARD:'):
            # Link to Standards Explorer
            return f"[{id_str}](https://b2ai.standards.synapse.org/Explore/Standard/DetailsPage?id={id_str})"

        elif id_str.startswith('B2AI_USECASE:'):
            # Link to use case page
            if id_str in all_data:
                name = all_data[id_str].get('name', id_str)
                slug = slugify(name)
                return f"[{id_str}]({relative_path_prefix}/usecases/{slug}.markdown)"
            return id_str

        elif id_str.startswith('B2AI_SUBSTRATE:'):
            # Link to substrate page with name in parentheses
            if id_str in all_data:
                name = all_data[id_str].get('name', id_str)
                slug = slugify(name)
                return f"[{id_str}]({relative_path_prefix}/substrates/{slug}.markdown) ({name})"
            return id_str

        elif id_str.startswith('B2AI_TOPIC:'):
            # Link to topic page with name in parentheses
            if id_str in all_data:
                name = all_data[id_str].get('name', id_str)
                # Topics use the exact name with spaces removed but capitalization preserved
                # Remove spaces but keep capitalization
                slug = name.replace(' ', '')
                return f"[{id_str}]({relative_path_prefix}/topics/{slug}.markdown) ({name})"
            return id_str

        elif id_str.startswith('B2AI_DATA:'):
            # For now, just return the ID as-is since we don't have individual dataset pages
            return id_str

        return id_str

    return re.sub(id_pattern, replace_id, text)


def convert_substrate_links(substrate_list: list, all_data: Dict[str, Dict], relative_path_prefix: str = "..") -> list:
    """Convert a list of substrate references to markdown links.

    Args:
        substrate_list: List of substrate IDs or strings
        all_data: Dictionary mapping B2AI IDs to their data
        relative_path_prefix: Path prefix for relative links

    Returns:
        List of converted markdown links
    """
    converted = []
    for substrate in substrate_list:
        substrate_str = str(substrate)
        if substrate_str in all_data:
            name = all_data[substrate_str].get('name', substrate_str)
            slug = slugify(name)
            converted.append(
                f"[{substrate_str}]({relative_path_prefix}/substrates/{slug}.markdown) ({name})")
        else:
            # Try to convert any embedded IDs in the string
            converted.append(convert_ids_to_links(
                substrate_str, all_data, relative_path_prefix))
    return converted


def convert_topic_links(topic_list: list, all_data: Dict[str, Dict], relative_path_prefix: str = "..") -> list:
    """Convert a list of topic references to markdown links.

    Args:
        topic_list: List of topic IDs or strings
        all_data: Dictionary mapping B2AI IDs to their data
        relative_path_prefix: Path prefix for relative links

    Returns:
        List of converted markdown links
    """
    converted = []
    for topic in topic_list:
        topic_str = str(topic)
        if topic_str in all_data:
            name = all_data[topic_str].get('name', topic_str)
            # Topics use the exact name with spaces removed but capitalization preserved
            slug = name.replace(' ', '')
            converted.append(
                f"[{topic_str}]({relative_path_prefix}/topics/{slug}.markdown) ({name})")
        else:
            # Try to convert any embedded IDs in the string
            converted.append(convert_ids_to_links(
                topic_str, all_data, relative_path_prefix))
    return converted


def convert_anatomy_links(anatomy_list: list) -> list:
    """Convert a list of anatomy terms (UBERON, CLO, etc.) to OBO Library PURL links.

    Args:
        anatomy_list: List of anatomy term IDs (e.g., UBERON:0000468, CLO:0000031)

    Returns:
        List of markdown links to OBO Library
    """
    converted = []
    for anatomy in anatomy_list:
        anatomy_str = str(anatomy)
        # Convert UBERON:0000468 to UBERON_0000468 for OBO PURL
        if ':' in anatomy_str:
            obo_id = anatomy_str.replace(':', '_')
            obo_url = f"http://purl.obolibrary.org/obo/{obo_id}"
            converted.append(f"[{anatomy_str}]({obo_url})")
        else:
            converted.append(anatomy_str)
    return converted

