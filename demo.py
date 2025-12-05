#!/usr/bin/env python3
"""
Complete demonstration of Schema Analyzer Package
Uses realistic schemas and demonstrates all features
"""

from schema_analyzer import SchemaAnalyzer, SizeCalculator, StatisticsCalculator
from sample_schemas import SCHEMAS, DOCUMENT_COUNTS


def demo_basic_usage():
    """Demonstrate basic usage"""
    print("\n" + "="*80)
    print("DEMO 1: BASIC SCHEMA ANALYSIS")
    print("="*80)
    
    analyzer = SchemaAnalyzer("multi_tenant_platform")
    
    # Load multiple schemas
    for collection_name, schema in SCHEMAS.items():
        analyzer.load_schema(collection_name, schema)
        doc_count = DOCUMENT_COUNTS.get(collection_name, 10000)
        analyzer.add_documents(collection_name, doc_count)
    
    print(f"\nDatabase: {analyzer.database.name}")
    print(f"Collections loaded: {len(analyzer.list_collections())}")
    
    for col_name in analyzer.list_collections():
        col = analyzer.get_collection(col_name)
        doc_count = DOCUMENT_COUNTS.get(col_name, 0)
        print(f"\n  ✓ {col_name}")
        print(f"    - Fields: {len(col.fields)}")
        print(f"    - Documents: {doc_count:,}")
    
    return analyzer


def demo_size_analysis(analyzer):
    """Demonstrate size calculation"""
    print("\n" + "="*80)
    print("DEMO 2: DATABASE SIZE ANALYSIS")
    print("="*80)
    
    SizeCalculator.print_size_report(analyzer.get_database())


def demo_sharding_analysis(analyzer):
    """Demonstrate sharding analysis"""
    print("\n" + "="*80)
    print("DEMO 3: SHARDING ANALYSIS - PRODUCTS BY CATEGORY")
    print("="*80)
    
    products_col = analyzer.get_collection("products")
    
    # Define category distribution
    def category_generator(i):
        categories = [
            "Electronics", "Books", "Clothing", "Home & Garden",
            "Sports", "Toys", "Beauty", "Automotive"
        ]
        # Create slightly skewed distribution
        if i % 100 < 30:
            return categories[0]  # Electronics gets more
        else:
            return categories[i % len(categories)]
    
    stats = StatisticsCalculator.analyze_sharding(
        products_col,
        "category",
        key_value_generator=category_generator,
        sample_size=DOCUMENT_COUNTS["products"]
    )
    
    StatisticsCalculator.print_sharding_report(stats)


def demo_compare_strategies(analyzer):
    """Compare multiple sharding strategies"""
    print("\n" + "="*80)
    print("DEMO 4: COMPARING SHARDING STRATEGIES - SOCIAL POSTS")
    print("="*80)
    
    posts_col = analyzer.get_collection("social_posts")
    
    # User distribution (zipf-like, some users post more)
    def user_generator(i):
        # Simulate Zipfian distribution where few users generate most posts
        num_users = 10000
        return f"user_{int(i ** 0.9) % num_users}"
    
    results = StatisticsCalculator.compare_sharding_strategies(
        posts_col,
        ["user_id", "_id"],
        key_generators={
            "user_id": user_generator
        }
    )
    
    StatisticsCalculator.print_comparison_report(results)


def demo_sensor_data(analyzer):
    """Analyze sensor data collection"""
    print("\n" + "="*80)
    print("DEMO 5: SENSOR DATA SHARDING BY LOCATION")
    print("="*80)
    
    sensor_col = analyzer.get_collection("sensor_data")
    
    # Different locations worldwide
    locations = ["ASIA", "EUROPE", "AMERICAS", "AFRICA", "OCEANIA"]
    
    def location_generator(i):
        return locations[i % len(locations)]
    
    stats = StatisticsCalculator.analyze_sharding(
        sensor_col,
        "location_id",
        key_value_generator=location_generator,
        sample_size=DOCUMENT_COUNTS["sensor_data"]
    )
    
    StatisticsCalculator.print_sharding_report(stats)


def demo_export_config(analyzer):
    """Export configuration"""
    print("\n" + "="*80)
    print("DEMO 6: EXPORT CONFIGURATION")
    print("="*80)
    
    import json
    
    config = {
        "database": {
            "name": analyzer.database.name,
            "collections": []
        }
    }
    
    for col_name in analyzer.list_collections():
        col = analyzer.get_collection(col_name)
        col_config = {
            "name": col_name,
            "document_count": DOCUMENT_COUNTS.get(col_name, 0),
            "fields": {
                fname: fobj.type 
                for fname, fobj in col.fields.items()
            }
        }
        config["database"]["collections"].append(col_config)
    
    # Save to file
    with open("database_configuration.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✓ Configuration exported to: database_configuration.json")
    print("\nSample configuration:")
    print(json.dumps(config, indent=2)[:500] + "...")


def main():
    """Run all demos"""
    print("\n" + "="*80)
    print("SCHEMA ANALYZER PACKAGE - COMPLETE DEMONSTRATION")
    print("="*80)

    
    try:
        # Run all demos
        analyzer = demo_basic_usage()
        demo_size_analysis(analyzer)
        demo_sharding_analysis(analyzer)
        #demo_compare_strategies(analyzer)
        #demo_sensor_data(analyzer)
        #demo_export_config(analyzer)
        
        print("\n" + "="*80)
        print("✓ ALL DEMOS COMPLETED SUCCESSFULLY")
        print("="*80)

        
    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
