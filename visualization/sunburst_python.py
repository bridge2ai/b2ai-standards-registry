import pandas as pd
import json
import plotly.graph_objects as go
from itertools import permutations
from collections import defaultdict

def load_and_process_data(csv_file):
    """Load CSV and process topic arrays into hierarchical structure"""

    # Read CSV
    df = pd.read_csv(csv_file)

    # Parse topic arrays from JSON strings
    topic_arrays = []
    for topic_str in df['topic']:
        try:
            topics = json.loads(topic_str)
            if len(topics) > 0:
                topic_arrays.append(topics)
        except:
            continue

    print(f"Loaded {len(topic_arrays)} topic arrays")

    # Generate all permutations for each topic array
    all_paths = []
    for topics in topic_arrays:
        # Generate all possible orderings (permutations) of the topics
        for perm in permutations(topics):
            all_paths.append(list(perm))

    print(f"Generated {len(all_paths)} total paths")

    return all_paths

def build_sunburst_data(paths, max_depth=6):
    """Build hierarchical data structure for sunburst plot"""

    # Track all unique nodes and their counts
    node_counts = defaultdict(int)

    ids = ["root"]
    labels = ["All Topics"]
    parents = [""]
    values = [0]  # Will be set later

    # Track all unique node IDs to avoid duplicates
    processed_nodes = {"root"}

    # Process each path
    for path in paths:
        current_path_ids = ["root"]

        for level in range(min(len(path), max_depth)):
            topic = path[level]

            # Create hierarchical ID
            if level == 0:
                node_id = topic
                parent_id = "root"
            else:
                # Create unique path-based ID
                path_so_far = path[:level+1]
                node_id = " → ".join(path_so_far)
                parent_id = " → ".join(path_so_far[:-1])

            # Count this node
            node_counts[node_id] += 1

            # Add to data structure if not already present
            if node_id not in processed_nodes:
                ids.append(node_id)
                labels.append(f"{topic}")
                parents.append(parent_id)
                values.append(0)  # Will be updated below
                processed_nodes.add(node_id)

    # Update values with counts
    for i, node_id in enumerate(ids):
        if node_id == "root":
            values[i] = len(paths)
        else:
            values[i] = node_counts[node_id]

    return ids, labels, parents, values

def create_sunburst_plot(csv_file, max_depth=6):
    """Create and display sunburst plot"""

    # Load and process data
    paths = load_and_process_data(csv_file)

    # Build sunburst data
    ids, labels, parents, values = build_sunburst_data(paths, max_depth)

    print(f"Created sunburst with {len(ids)} nodes")

    # Create the plot
    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        values=values,
        branchvalues="total",
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percentParent} of parent<extra></extra>',
        maxdepth=max_depth + 1,
        insidetextorientation='radial',
        textfont=dict(size=12),
    ))

    fig.update_layout(
        title={
            'text': f"Topic Co-occurrence Patterns (All Permutations)",
            'x': 0.5,
            'font': {'size': 20}
        },
        font_size=12,
        width=1000,
        height=800,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    return fig

def create_standalone_html(csv_file, output_file="sunburst_plot.html", max_depth=6):
    """Create a standalone HTML file with the plot"""

    # Generate the plot
    fig = create_sunburst_plot(csv_file, max_depth)

    # Create HTML with embedded plot
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Topic Sunburst Plot</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }}

        #plotDiv {{
            width: 100%;
            height: 800px;
            margin: 0 auto;
        }}

        .info {{
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .stat-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }}

        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Topic Co-occurrence Analysis</h1>
        <div id="plotDiv"></div>

        <div class="info">
            <h3>About This Visualization</h3>
            <p>This sunburst plot shows all possible hierarchical relationships between topics in your dataset.
            Each topic array generates all possible permutations, creating multiple paths through the data.</p>

            <div class="stats" id="stats">
                <!-- Stats will be populated by JavaScript -->
            </div>
        </div>
    </div>

    <script>
        // Plot data will be inserted here
        var plotData = {fig.to_json()};

        // Create the plot
        Plotly.newPlot('plotDiv', plotData.data, plotData.layout, {{
            responsive: true,
            displayModeBar: true,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d'],
            displaylogo: false
        }});

        // Add statistics
        const data = plotData.data[0];
        const stats = [
            {{label: "Total Nodes", value: data.ids.length}},
            {{label: "Max Depth", value: {max_depth}}},
            {{label: "Root Value", value: data.values[0]}},
            {{label: "Unique Topics", value: new Set(data.labels.map(l => l.split('<br>')[0])).size - 1}}
        ];

        const statsDiv = document.getElementById('stats');
        stats.forEach(stat => {{
            const card = document.createElement('div');
            card.className = 'stat-card';
            card.innerHTML = `
                <div class="stat-number">${{stat.value}}</div>
                <div class="stat-label">${{stat.label}}</div>
            `;
            statsDiv.appendChild(card);
        }});
    </script>
</body>
</html>"""

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Standalone HTML created: {output_file}")
    return html_content

def export_for_react(csv_file, output_file="sunburst_data.json", max_depth=6):
    """Export data in format suitable for React/TypeScript"""

    fig = create_sunburst_plot(csv_file, max_depth)

    # Extract data in clean format
    data = fig.data[0]

    react_config = {
        "data": [{
            "type": "sunburst",
            "ids": data.ids,
            "labels": data.labels,
            "parents": data.parents,
            "values": data.values,
            "branchvalues": "total",
            "hovertemplate": '<b>%{label}</b><br>Count: %{value}<br>%{percentParent} of parent<extra></extra>',
            "maxdepth": max_depth + 1,
            "insidetextorientation": 'radial'
        }],
        "layout": {
            "title": {
                "text": "Topic Co-occurrence Patterns",
                "x": 0.5,
                "font": {"size": 20}
            },
            "font": {"size": 12},
            "paper_bgcolor": "white"
        },
        "config": {
            "responsive": True,
            "displayModeBar": True,
            "displaylogo": False
        }
    }

    with open(output_file, 'w') as f:
        json.dump(react_config, f, indent=2)

    print(f"React/TypeScript data exported to {output_file}")
    return react_config

# Main execution
if __name__ == "__main__":
    csv_file = 'topics.csv'

    # Create standalone HTML (best for immediate viewing)
    create_standalone_html(csv_file, "sunburst_plot.html", max_depth=6)

    # Also create the standard Plotly figure
    fig = create_sunburst_plot(csv_file, max_depth=6)
    fig.show()

    # Export for React integration
    export_for_react(csv_file, "sunburst_data.json", max_depth=6)

    print("\nFiles created:")
    print("1. sunburst_plot.html - Standalone HTML with embedded plot")
    print("2. sunburst_data.json - Data for React/TypeScript integration")
    print("3. Interactive plot displayed in browser (if available)")
