#!/usr/bin/env python3
"""
Analyze DataStandardOrTool.yaml to find entries with short purpose_detail text.
"""

import re
from pathlib import Path

def count_sentences(text):
    """Count sentences in text. A sentence ends with . ! or ?"""
    if not text:
        return 0
    # Split on sentence endings followed by space or end of string
    sentences = re.split(r'[.!?]+(?:\s|$)', text.strip())
    # Filter out empty strings
    sentences = [s for s in sentences if s.strip()]
    return len(sentences)

def analyze_purpose_details(yaml_file):
    """Analyze purpose_detail fields in the YAML file."""
    with open(yaml_file, 'r') as f:
        lines = f.readlines()
    
    short_entries = []
    current_entry = None
    in_purpose_detail = False
    purpose_text = []
    
    for i, line in enumerate(lines):
        # Start of a new entry
        if line.startswith('- id: B2AI_STANDARD:'):
            # Process previous entry if it exists
            if current_entry and purpose_text:
                full_text = ' '.join(purpose_text)
                sentence_count = count_sentences(full_text)
                if sentence_count <= 2:
                    short_entries.append({
                        'id': current_entry['id'],
                        'name': current_entry['name'],
                        'sentence_count': sentence_count,
                        'text_length': len(full_text),
                        'preview': full_text[:100] + '...' if len(full_text) > 100 else full_text
                    })
            
            # Start new entry
            current_entry = {'id': line.split('id:')[1].strip(), 'name': 'Unknown'}
            in_purpose_detail = False
            purpose_text = []
            
        # Get the standard name
        elif current_entry and line.strip().startswith('name:') and not in_purpose_detail:
            current_entry['name'] = line.split('name:', 1)[1].strip()
        
        # Start of purpose_detail
        elif line.strip().startswith('purpose_detail:'):
            in_purpose_detail = True
            # Get text on same line if exists
            rest = line.split('purpose_detail:', 1)[1].strip()
            if rest:
                purpose_text.append(rest)
                
        # Continue collecting purpose_detail text
        elif in_purpose_detail:
            # End if we hit another top-level key (not indented)
            if line and line[0] not in [' ', '-', '\n']:
                in_purpose_detail = False
            # End if we hit another field at same indentation level
            elif re.match(r'\s{2}[a-z_]+:', line):
                in_purpose_detail = False
            # Continue collecting text
            elif line.strip():
                purpose_text.append(line.strip())
    
    # Handle last entry
    if current_entry and purpose_text:
        full_text = ' '.join(purpose_text)
        sentence_count = count_sentences(full_text)
        if sentence_count <= 2:
            short_entries.append({
                'id': current_entry['id'],
                'name': current_entry['name'],
                'sentence_count': sentence_count,
                'text_length': len(full_text),
                'preview': full_text[:100] + '...' if len(full_text) > 100 else full_text
            })
    
    # Sort by character count (length), smallest to largest
    short_entries.sort(key=lambda x: x['text_length'])
    
    return short_entries

def generate_markdown_table(entries):
    """Generate a Markdown table of the results."""
    md = "# Purpose Detail Analysis for DataStandardOrTool\n\n"
    
    md += f"## Summary\n\n"
    md += f"- **Total entries with short purpose_detail** (≤2 sentences): {len(entries)}\n"
    
    # Count by sentence count
    zero_sent = len([e for e in entries if e['sentence_count'] == 0])
    one_sent = len([e for e in entries if e['sentence_count'] == 1])
    two_sent = len([e for e in entries if e['sentence_count'] == 2])
    
    md += f"- **Zero sentences**: {zero_sent}\n"
    md += f"- **One sentence**: {one_sent}\n"
    md += f"- **Two sentences**: {two_sent}\n\n"
    
    md += "## Entries with Short purpose_detail (≤2 sentences)\n\n"
    md += "| Standard ID | Standard Name | Characters |\n"
    md += "|-------------|---------------|------------|\n"
    
    for entry in entries:
        name_display = entry['name'][:60] + '...' if len(entry['name']) > 60 else entry['name']
        md += f"| {entry['id']} | {name_display} | {entry['text_length']} |\n"
    
    md += f"\n**Count: {len(entries)} entries**\n"
    
    return md

if __name__ == '__main__':
    yaml_file = Path(__file__).parent / 'src' / 'data' / 'DataStandardOrTool.yaml'
    
    entries = analyze_purpose_details(yaml_file)
    
    markdown = generate_markdown_table(entries)
    
    print(markdown)
