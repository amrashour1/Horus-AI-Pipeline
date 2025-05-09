#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
u0633u0643u0631u064au0628u062a u0644u0627u062eu062au0628u0627u0631 u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a
"""

import sys
import os
import logging

# u0625u0636u0627u0641u0629 u0645u062cu0644u062f u0627u0644u0645u0634u0631u0648u0639 u0625u0644u0649 u0645u0633u0627u0631 u0627u0644u0628u062du062b
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# u0625u0639u062fu0627u062f u0627u0644u062au0633u062cu064au0644
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# u0627u0633u062au064au0631u0627u062f u0645u062fu064au0631 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a
try:
    from db_manager import DatabaseManager
    from db_config import DB_CONFIG
except ImportError as e:
    print(f"u062eu0637u0623 u0641u064a u0627u0633u062au064au0631u0627u062f u0627u0644u0648u062du062fu0627u062a: {e}")
    sys.exit(1)

def main():
    """u0627u0644u062fu0627u0644u0629 u0627u0644u0631u0626u064au0633u064au0629 u0644u0627u062eu062au0628u0627u0631 u0627u0644u0627u062au0635u0627u0644"""
    print("\n=== u0627u062eu062au0628u0627u0631 u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0628u064au0627u0646u0627u062a MySQL ===\n")
    
    # u0639u0631u0636 u0625u0639u062fu0627u062fu0627u062a u0627u0644u0627u062au0635u0627u0644 (u0628u062fu0648u0646 u0643u0644u0645u0629 u0627u0644u0645u0631u0648u0631)
    db_config_safe = DB_CONFIG.copy()
    if 'password' in db_config_safe:
        db_config_safe['password'] = '********'  # u0625u062eu0641u0627u0621 u0643u0644u0645u0629 u0627u0644u0645u0631u0648u0631 u0644u0644u0623u0645u0627u0646
    
    print("u0625u0639u062fu0627u062fu0627u062a u0627u0644u0627u062au0635u0627u0644:")
    for key, value in db_config_safe.items():
        print(f"  {key}: {value}")
    print()
    
    try:
        # u0625u0646u0634u0627u0621 u0645u062fu064au0631 u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a
        db_manager = DatabaseManager()
        
        # u0627u062eu062au0628u0627u0631 u0627u0644u0627u062au0635u0627u0644
        print("u062cu0627u0631u064d u0627u062eu062au0628u0627u0631 u0627u0644u0627u062au0635u0627u0644...")
        if db_manager.test_connection():
            print("\u2705 u062au0645 u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a u0628u0646u062cu0627u062d!")
            
            # u0627u062eu062au0628u0627u0631 u0627u0644u0627u0633u062au0639u0644u0627u0645 u0627u0644u0628u0633u064au0637
            print("\nu062cu0627u0631u064d u0627u062eu062au0628u0627u0631 u0627u0633u062au0639u0644u0627u0645 u0628u0633u064au0637...")
            result = db_manager.execute_query("SELECT VERSION() as version")
            if result and len(result) > 0:
                print(f"\u2705 u0625u0635u062fu0627u0631 MySQL: {result[0]['version']}")
            else:
                print("\u274c u0641u0634u0644 u0627u0644u0627u0633u062au0639u0644u0627u0645 u0627u0644u0628u0633u064au0637")
        else:
            print("\u274c u0641u0634u0644 u0627u0644u0627u062au0635u0627u0644 u0628u0642u0627u0639u062fu0629 u0627u0644u0628u064au0627u0646u0627u062a!")
            print("u062au0623u0643u062f u0645u0646 u062au0634u063au064au0644 u062eu0627u062fu0645 MySQL u0648u0635u062du0629 u0628u064au0627u0646u0627u062a u0627u0644u0627u062au0635u0627u0644 u0641u064a u0645u0644u0641 db_config.py")
    
    except Exception as e:
        print(f"\u274c u062du062fu062b u062eu0637u0623 u063au064au0631 u0645u062au0648u0642u0639: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    print("\n=== u0627u0646u062au0647u0649 u0627u0644u0627u062eu062au0628u0627u0631 ===\n")
    sys.exit(0 if success else 1)
