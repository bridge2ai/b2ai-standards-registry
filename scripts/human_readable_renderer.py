#!/usr/bin/env python3
"""
Human-readable HTML renderer for D4D YAML data
Creates natural, document-like HTML without raw JSON structures
"""

import os
import yaml
from datetime import datetime
from jinja2 import Template, Environment
from pathlib import Path
from bs4 import BeautifulSoup

class HumanReadableRenderer:
    """Renders D4D data in a human-readable HTML format"""

    def __init__(self):
        self.d4d_sections = {
            "Motivation": {
                "title": "Motivation",
                "description": "Why was the dataset created?",
                "icon": "🎯"
            },
            "Composition": {
                "title": "Composition",
                "description": "What do the instances represent?",
                "icon": "📊"
            },
            "Collection": {
                "title": "Collection Process",
                "description": "How was the data acquired?",
                "icon": "🔍"
            },
            "Preprocessing": {
                "title": "Preprocessing/Cleaning/Labeling",
                "description": "Was any preprocessing/cleaning/labeling done?",
                "icon": "🔧"
            },
            "Uses": {
                "title": "Uses",
                "description": "What (other) tasks could the dataset be used for?",
                "icon": "🚀"
            },
            "Distribution": {
                "title": "Distribution",
                "description": "How will the dataset be distributed?",
                "icon": "📤"
            },
            "Maintenance": {
                "title": "Maintenance",
                "description": "How will the dataset be maintained?",
                "icon": "🔄"
            },
            "Human": {
                "title": "Human Subjects",
                "description": "Does the dataset relate to people?",
                "icon": "👥"
            }
        }

    def categorize_data(self, data):
        """Organize data into D4D sections with intelligent categorization"""
        sections = {section: [] for section in self.d4d_sections.keys()}

        def get_section_for_key(key):
            """Determine which D4D section a key belongs to"""
            key_lower = key.lower()

            # Motivation keywords
            if any(word in key_lower for word in ['purpose', 'goal', 'objective', 'motivation', 'funding', 'funder', 'grantor', 'grant']):
                return "Motivation"

            # Composition keywords
            elif any(word in key_lower for word in ['instance', 'count', 'participant', 'sample', 'subpopulation', 'distribution', 'demographics']):
                return "Composition"

            # Collection keywords
            elif any(word in key_lower for word in ['collection', 'acquisition', 'methodology', 'procedure', 'protocol', 'creator', 'issued']):
                return "Collection"

            # Uses keywords
            elif any(word in key_lower for word in ['use', 'purpose', 'task', 'application', 'machine learning', 'artificial intelligence']):
                return "Uses"

            # Distribution keywords
            elif any(word in key_lower for word in ['license', 'access', 'download', 'doi', 'url', 'availability', 'bytes']):
                return "Distribution"

            # Maintenance keywords
            elif any(word in key_lower for word in ['version', 'maintenance', 'update', 'support']):
                return "Maintenance"

            # Human subjects keywords
            elif any(word in key_lower for word in ['human', 'participant', 'consent', 'ethics', 'privacy', 'identifier']):
                return "Human"

            else:
                return "Collection"  # Default section

        def process_item(key, value, parent_context=""):
            """Process a data item and add to appropriate section"""
            section = get_section_for_key(key)

            # Create a structured data item
            item = {
                'key': key,
                'value': value,
                'context': parent_context,
                'type': type(value).__name__
            }

            sections[section].append(item)

        # Process the data structure
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "DatasetCollection" and isinstance(value, dict) and "resources" in value:
                    # Special handling for DatasetCollection resources
                    for resource in value.get("resources", []):
                        if isinstance(resource, dict):
                            for res_key, res_value in resource.items():
                                process_item(res_key, res_value, "Dataset Resource")
                else:
                    process_item(key, value)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                process_item(f"Item {i+1}", item)

        # Remove empty sections
        return {k: v for k, v in sections.items() if v}

    def format_value(self, value, context=""):
        """Format a value for human-readable display"""
        if isinstance(value, dict):
            return self._format_dict(value)
        elif isinstance(value, list):
            return self._format_list(value)
        elif isinstance(value, str):
            return self._format_string(value)
        elif isinstance(value, (int, float)):
            return self._format_number(value)
        elif isinstance(value, bool):
            return "Yes" if value else "No"
        else:
            return str(value)

    def _format_dict(self, d):
        """Format dictionary as nested definition list"""
        if not d:
            return "<em>No information provided</em>"

        items = []
        for key, value in d.items():
            formatted_key = self._humanize_key(key)
            formatted_value = self.format_value(value)
            items.append(f"<dt>{formatted_key}</dt><dd>{formatted_value}</dd>")

        return f"<dl class='nested-dict'>{''.join(items)}</dl>"

    def _format_list(self, lst):
        """Format list as bulleted or numbered list"""
        if not lst:
            return "<em>No items</em>"

        # Determine if this should be an ordered or unordered list
        is_ordered = all(isinstance(item, dict) and len(item) > 3 for item in lst) if lst else False

        list_tag = "ol" if is_ordered else "ul"
        items = []

        for item in lst:
            formatted_item = self.format_value(item)
            items.append(f"<li>{formatted_item}</li>")

        return f"<{list_tag} class='formatted-list'>{''.join(items)}</{list_tag}>"

    def _format_string(self, s):
        """Format string with proper emphasis and links"""
        if not s:
            return "<em>Not specified</em>"

        # Handle URLs
        if s.startswith(('http://', 'https://', 'doi:')):
            if s.startswith('doi:'):
                url = f"https://doi.org/{s[4:]}"
                return f'<a href="{url}" target="_blank">{s}</a>'
            else:
                return f'<a href="{s}" target="_blank">{s}</a>'

        # Handle long descriptions
        if len(s) > 200:
            return f'<div class="long-description">{s}</div>'

        return s

    def _format_number(self, n):
        """Format numbers with appropriate units and separators"""
        if isinstance(n, int) and n > 1000:
            # Add thousand separators for large numbers
            return f"{n:,}"
        return str(n)

    def _humanize_key(self, key):
        """Convert key names to human-readable labels"""
        # Convert snake_case and camelCase to Title Case
        key = key.replace('_', ' ').replace('-', ' ')

        # Handle common abbreviations and terms
        replacements = {
            'id': 'ID',
            'url': 'URL',
            'uri': 'URI',
            'doi': 'DOI',
            'api': 'API',
            'ai': 'AI',
            'ml': 'ML',
            'nih': 'NIH',
            'irb': 'IRB',
            'phi': 'PHI',
            'pii': 'PII'
        }

        words = key.split()
        for i, word in enumerate(words):
            if word.lower() in replacements:
                words[i] = replacements[word.lower()]
            else:
                words[i] = word.capitalize()

        return ' '.join(words)

    def render_to_html(self, data, title):
        """Render data to human-readable HTML"""

        categorized_data = self.categorize_data(data)

        # HTML template for human-readable display
        template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Datasheet for Dataset</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #fafafa;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .header h1 {
            margin: 0 0 0.5rem 0;
            font-size: 2rem;
            font-weight: 300;
        }

        .header .subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
            margin: 0;
        }

        .section {
            background: white;
            margin-bottom: 2rem;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .section-header {
            background: #f8f9fa;
            padding: 1.5rem;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .section-icon {
            font-size: 1.5rem;
        }

        .section-title {
            margin: 0;
            color: #2c3e50;
            font-size: 1.25rem;
            font-weight: 600;
        }

        .section-description {
            margin: 0.25rem 0 0 0;
            color: #6c757d;
            font-size: 0.9rem;
        }

        .section-content {
            padding: 1.5rem;
        }

        .data-item {
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #f1f3f4;
        }

        .data-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
        }

        .item-label {
            font-weight: 600;
            color: #495057;
            margin-bottom: 0.5rem;
            display: block;
        }

        .item-context {
            font-size: 0.8rem;
            color: #6c757d;
            margin-bottom: 0.25rem;
            font-style: italic;
        }

        .nested-dict {
            margin: 0.5rem 0;
            background: #f8f9fa;
            border-radius: 6px;
            padding: 1rem;
        }

        .nested-dict dt {
            font-weight: 600;
            color: #495057;
            margin-top: 0.75rem;
        }

        .nested-dict dt:first-child {
            margin-top: 0;
        }

        .nested-dict dd {
            margin: 0.25rem 0 0.5rem 1rem;
            color: #6c757d;
        }

        .formatted-list {
            margin: 0.5rem 0;
            padding-left: 1.5rem;
        }

        .formatted-list li {
            margin-bottom: 0.5rem;
        }

        .long-description {
            background: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0 6px 6px 0;
            line-height: 1.7;
        }

        a {
            color: #007bff;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .timestamp {
            text-align: center;
            color: #6c757d;
            font-size: 0.85rem;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e9ecef;
        }

        @media (max-width: 768px) {
            body {
                padding: 1rem;
            }

            .header {
                padding: 1.5rem;
            }

            .header h1 {
                font-size: 1.5rem;
            }

            .section-content {
                padding: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>{{ title }}</h1>
        <p class="subtitle">Datasheet for Dataset - Human Readable Format</p>
    </div>

    {% if categorized_data %}
        {% for section_name, items in categorized_data.items() %}
            {% if items %}
            <div class="section">
                <div class="section-header">
                    <span class="section-icon">{{ sections[section_name].icon }}</span>
                    <div>
                        <h2 class="section-title">{{ sections[section_name].title }}</h2>
                        <p class="section-description">{{ sections[section_name].description }}</p>
                    </div>
                </div>
                <div class="section-content">
                    {% for item in items %}
                    <div class="data-item">
                        {% if item.context %}
                        <div class="item-context">{{ item.context }}</div>
                        {% endif %}
                        <label class="item-label">{{ humanize_key(item.key) }}</label>
                        <div class="item-value">{{ format_value(item.value)|safe }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
        {% endfor %}
    {% else %}
        <div class="section">
            <div class="section-content">
                <p><em>No data available to display.</em></p>
            </div>
        </div>
    {% endif %}

    <div class="timestamp">
        Generated on {{ timestamp }} using Bridge2AI Data Sheets Schema
    </div>
</body>
</html>
"""

        # Create Jinja2 environment with custom functions
        env = Environment()
        env.globals['humanize_key'] = self._humanize_key
        env.globals['format_value'] = self.format_value

        template = env.from_string(template_str)

        return template.render(
            title=title,
            categorized_data=categorized_data,
            sections=self.d4d_sections,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

def process_yaml_file(file_path, output_dir, org_id, separate_css):
    """Process a YAML file and generate human-readable HTML"""

    renderer = HumanReadableRenderer()

    # Read and parse YAML
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        data = yaml.safe_load(f)

    if not data:
        print(f"No data found in {file_path}")
        return False

    # Generate output filename
    base_name = Path(file_path).stem
    output_path = os.path.join(output_dir, f"{org_id}_d4d.html")

    # Generate HTML
    html_content = renderer.render_to_html(data, base_name)

    # Extract CSS, conditionally remove CSS from HTML content
    css_path, html = extract_css(output_dir, output_path, html_content, separate_css)

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated human-readable HTML: {output_path}")
    print(f"Generated CSS: {css_path}")
    return True

def extract_css(output_dir, output_path, html_content, separate_css):
    """Extract CSS styling from D4D HTML"""

    soup = BeautifulSoup(html_content, 'html.parser')

    extracted_css = []

    for css_tag in soup.find_all("style", recursive=True):
        extracted_css.append(css_tag.string)
        if separate_css:
            css_tag.extract()
            html_content = soup.prettify(formatter="html")

    css_path = os.path.join(output_dir, f"{Path(output_path).stem}.css")

    with open(css_path, 'w', encoding='utf-8') as c:
        c.write("\n".join(extracted_css))

    return css_path, html_content

def main():
    """Process all YAML files and generate human-readable HTML versions"""

    input_dir = "src/data/sheets"
    output_dir = "project/data/sheets"
    separate_css = True

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Process text files
    text_org_map = {
        "D4D_-_AI-READI_FAIRHub_v3.yaml": "B2AI_ORG_114",
        "D4D_-_CM4AI_Dataverse_v3.yaml": "B2AI_ORG_116",
        "D4D_-_VOICE_PhysioNet_v3.yaml": "B2AI_ORG_117"
    }

    processed_count = 0

    for txt_file, org_id in text_org_map.items():
        txt_path = os.path.join(input_dir, txt_file)
        if os.path.exists(txt_path):
            if process_yaml_file(txt_path, output_dir, org_id, separate_css):
                processed_count += 1
        else:
            print(f"File not found: {txt_path}")

    print(f"\nProcessed {processed_count} files.")
    print(f"Human-readable HTML files saved in: {output_dir}")

if __name__ == "__main__":
    main()
