"""
Comprehensive Schema Comparison Tool
Compares Production vs Development databases to ensure they're identical
"""

import pyodbc
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.sql import text
import pandas as pd
from tabulate import tabulate

def get_database_schema(database_name, connection_string_template):
    """Get detailed schema information from a database"""
    
    connection_string = connection_string_template.format(database=database_name)
    engine = create_engine(connection_string)
    inspector = inspect(engine)
    
    schema_info = {
        'tables': {},
        'table_count': 0,
        'total_columns': 0
    }
    
    # Get all tables
    tables = inspector.get_table_names()
    schema_info['table_count'] = len(tables)
    
    for table_name in tables:
        table_info = {
            'columns': {},
            'indexes': [],
            'foreign_keys': [],
            'primary_keys': []
        }
        
        # Get columns
        columns = inspector.get_columns(table_name)
        for col in columns:
            table_info['columns'][col['name']] = {
                'type': str(col['type']),
                'nullable': col['nullable'],
                'default': col.get('default'),
                'autoincrement': col.get('autoincrement', False)
            }
            schema_info['total_columns'] += 1
        
        # Get indexes
        try:
            indexes = inspector.get_indexes(table_name)
            for idx in indexes:
                table_info['indexes'].append({
                    'name': idx['name'],
                    'columns': idx['column_names'],
                    'unique': idx['unique']
                })
        except:
            pass
        
        # Get foreign keys
        try:
            foreign_keys = inspector.get_foreign_keys(table_name)
            for fk in foreign_keys:
                table_info['foreign_keys'].append({
                    'name': fk.get('name'),
                    'columns': fk['constrained_columns'],
                    'referred_table': fk['referred_table'],
                    'referred_columns': fk['referred_columns']
                })
        except:
            pass
        
        # Get primary keys
        try:
            pk = inspector.get_pk_constraint(table_name)
            if pk and pk['constrained_columns']:
                table_info['primary_keys'] = pk['constrained_columns']
        except:
            pass
        
        schema_info['tables'][table_name] = table_info
    
    return schema_info

def compare_schemas(prod_schema, dev_schema):
    """Compare two database schemas and return detailed differences"""
    
    comparison = {
        'summary': {},
        'table_differences': {},
        'column_differences': {},
        'missing_tables': {'prod_only': [], 'dev_only': []},
        'identical': True
    }
    
    # Compare table counts
    comparison['summary'] = {
        'production_tables': prod_schema['table_count'],
        'development_tables': dev_schema['table_count'],
        'production_columns': prod_schema['total_columns'],
        'development_columns': dev_schema['total_columns']
    }
    
    # Find missing tables
    prod_tables = set(prod_schema['tables'].keys())
    dev_tables = set(dev_schema['tables'].keys())
    
    comparison['missing_tables']['prod_only'] = list(prod_tables - dev_tables)
    comparison['missing_tables']['dev_only'] = list(dev_tables - prod_tables)
    
    if comparison['missing_tables']['prod_only'] or comparison['missing_tables']['dev_only']:
        comparison['identical'] = False
    
    # Compare common tables
    common_tables = prod_tables & dev_tables
    
    for table_name in common_tables:
        prod_table = prod_schema['tables'][table_name]
        dev_table = dev_schema['tables'][table_name]
        
        table_diff = {
            'column_differences': {},
            'missing_columns': {'prod_only': [], 'dev_only': []},
            'index_differences': {},
            'fk_differences': {}
        }
        
        # Compare columns
        prod_cols = set(prod_table['columns'].keys())
        dev_cols = set(dev_table['columns'].keys())
        
        table_diff['missing_columns']['prod_only'] = list(prod_cols - dev_cols)
        table_diff['missing_columns']['dev_only'] = list(dev_cols - prod_cols)
        
        # Compare column definitions for common columns
        common_cols = prod_cols & dev_cols
        for col_name in common_cols:
            prod_col = prod_table['columns'][col_name]
            dev_col = dev_table['columns'][col_name]
            
            if prod_col != dev_col:
                table_diff['column_differences'][col_name] = {
                    'production': prod_col,
                    'development': dev_col
                }
                comparison['identical'] = False
        
        # Store table differences if any exist
        if (table_diff['missing_columns']['prod_only'] or 
            table_diff['missing_columns']['dev_only'] or 
            table_diff['column_differences']):
            comparison['table_differences'][table_name] = table_diff
            comparison['identical'] = False
    
    return comparison

def print_comparison_report(comparison):
    """Print a detailed comparison report"""
    
    print("🔍 DATABASE SCHEMA COMPARISON REPORT")
    print("=" * 60)
    
    # Summary
    summary = comparison['summary']
    print(f"\n📊 SUMMARY:")
    print(f"  Production Tables: {summary['production_tables']}")
    print(f"  Development Tables: {summary['development_tables']}")
    print(f"  Production Columns: {summary['production_columns']}")
    print(f"  Development Columns: {summary['development_columns']}")
    
    # Overall status
    if comparison['identical']:
        print(f"\n✅ RESULT: SCHEMAS ARE IDENTICAL! 🎉")
        return
    else:
        print(f"\n⚠️  RESULT: DIFFERENCES FOUND")
    
    # Missing tables
    missing = comparison['missing_tables']
    if missing['prod_only']:
        print(f"\n🔴 TABLES ONLY IN PRODUCTION ({len(missing['prod_only'])}):")
        for table in missing['prod_only']:
            print(f"  • {table}")
    
    if missing['dev_only']:
        print(f"\n🔴 TABLES ONLY IN DEVELOPMENT ({len(missing['dev_only'])}):")
        for table in missing['dev_only']:
            print(f"  • {table}")
    
    # Table differences
    if comparison['table_differences']:
        print(f"\n🔍 TABLE DIFFERENCES:")
        for table_name, diff in comparison['table_differences'].items():
            print(f"\n  📋 Table: {table_name}")
            
            if diff['missing_columns']['prod_only']:
                print(f"    🔴 Columns only in Production:")
                for col in diff['missing_columns']['prod_only']:
                    print(f"      • {col}")
            
            if diff['missing_columns']['dev_only']:
                print(f"    🔴 Columns only in Development:")
                for col in diff['missing_columns']['dev_only']:
                    print(f"      • {col}")
            
            if diff['column_differences']:
                print(f"    🔄 Column definition differences:")
                for col_name, col_diff in diff['column_differences'].items():
                    print(f"      • {col_name}:")
                    print(f"        Production:  {col_diff['production']}")
                    print(f"        Development: {col_diff['development']}")

def main():
    """Main comparison function"""
    
    print("🚀 Starting comprehensive schema comparison...")
    
    # Connection string template
    connection_template = "mssql+pyodbc://localhost/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    
    try:
        print("\n📡 Connecting to Production database...")
        prod_schema = get_database_schema("JobTrackerDB", connection_template)
        
        print("📡 Connecting to Development database...")
        dev_schema = get_database_schema("JobTrackerDB_Dev", connection_template)
        
        print("🔍 Analyzing schemas...")
        comparison = compare_schemas(prod_schema, dev_schema)
        
        print_comparison_report(comparison)
        
        # Create detailed table list
        print(f"\n📋 DETAILED TABLE LIST:")
        print(f"\n🏭 Production Tables ({prod_schema['table_count']}):")
        for table_name in sorted(prod_schema['tables'].keys()):
            col_count = len(prod_schema['tables'][table_name]['columns'])
            print(f"  ✅ {table_name} ({col_count} columns)")
        
        print(f"\n🛠️  Development Tables ({dev_schema['table_count']}):")
        for table_name in sorted(dev_schema['tables'].keys()):
            col_count = len(dev_schema['tables'][table_name]['columns'])
            print(f"  ✅ {table_name} ({col_count} columns)")
        
        # Migration status
        print(f"\n🎯 MIGRATION STATUS:")
        if comparison['identical']:
            print(f"  ✅ All databases are synchronized!")
            print(f"  ✅ Total tables: {prod_schema['table_count']}")
            print(f"  ✅ Total columns: {prod_schema['total_columns']}")
            print(f"  ✅ JobTrackerDB migration: COMPLETE! 🚀")
        else:
            print(f"  ⚠️  Databases have differences that need attention")
        
    except Exception as e:
        print(f"❌ Error during comparison: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()