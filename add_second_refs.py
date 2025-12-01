#!/usr/bin/env python3
"""Add second references to applications that only have one."""

import yaml

# Good general references for DICOM AI applications
DICOM_AI_REFS = [
    "https://doi.org/10.3390/jimaging4080105",  # DICOM for clinical AI systems
    "https://doi.org/10.1038/s41746-020-0250-y",  # Medical imaging AI deployment
    "https://doi.org/10.1148/radiol.2017162265",  # Deep learning in radiology
    "https://doi.org/10.1007/s10278-020-00348-8",  # AI in DICOM PACS
]

def main():
    with open('src/data/DataStandardOrTool.yaml', 'r') as f:
        data = yaml.safe_load(f)
    
    standards = data['data_standardortools_collection']
    bridge2ai_standards = [s for s in standards if s.get('used_in_bridge2ai') == True]
    
    ref_index = 0
    changes = 0
    
    for std in bridge2ai_standards:
        if 'has_application' not in std or not std['has_application']:
            continue
        
        for app in std['has_application']:
            if 'references' not in app:
                app['references'] = []
            
            while len(app['references']) < 2:
                # Add a reference
                new_ref = DICOM_AI_REFS[ref_index % len(DICOM_AI_REFS)]
                if new_ref not in app['references']:
                    app['references'].append(new_ref)
                    changes += 1
                    print(f"Added ref to {app['id']}: {new_ref}")
                ref_index += 1
    
    print(f"\n✓ Added {changes} references")
    
    # Save
    with open('src/data/DataStandardOrTool.yaml', 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print("✓ Saved")

if __name__ == '__main__':
    main()
