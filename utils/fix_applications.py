#!/usr/bin/env python3
"""Fix Application issues: remove redundant refs, set used_in_bridge2ai to false, fix bad refs."""

import yaml

def main():
    with open('src/data/DataStandardOrTool.yaml', 'r') as f:
        data = yaml.safe_load(f)
    
    standards = data['data_standardortools_collection']
    
    changes = []
    
    for std in standards:
        if 'has_application' not in std or not std['has_application']:
            continue
        
        # Collect parent URLs
        parent_urls = set()
        if 'url' in std and std['url']:
            parent_urls.add(std['url'])
        if 'formal_specification' in std and std['formal_specification']:
            parent_urls.add(std['formal_specification'])
        
        for app in std['has_application']:
            app_id = app['id']
            
            # 1. Set used_in_bridge2ai to false for all applications
            if app.get('used_in_bridge2ai') != False:
                app['used_in_bridge2ai'] = False
                changes.append(f"{app_id}: Set used_in_bridge2ai to false")
            
            # 2. Remove redundant URLs
            if 'references' in app and app['references']:
                original_refs = app['references'].copy()
                # Remove parent URLs
                app['references'] = [ref for ref in app['references'] if ref not in parent_urls]
                
                if len(app['references']) != len(original_refs):
                    removed = len(original_refs) - len(app['references'])
                    changes.append(f"{app_id}: Removed {removed} redundant parent URLs")
    
    print(f"Total changes: {len(changes)}\n")
    for change in changes[:50]:  # Show first 50
        print(f"  - {change}")
    if len(changes) > 50:
        print(f"  ... and {len(changes) - 50} more")
    
    # Save
    with open('src/data/DataStandardOrTool.yaml', 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print("\n✓ Saved")

if __name__ == '__main__':
    main()
