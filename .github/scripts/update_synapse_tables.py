import sys
from scripts.analyze_and_update_synapse_tables import analyze_and_update

if __name__ == "__main__":
    analyze_and_update(sys.argv[1:])
