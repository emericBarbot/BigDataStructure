"""
Example usage and tests for the Schema Analyzer package
"""

import json
from schema_analyzer import SchemaAnalyzer, SizeCalculator, StatisticsCalculator


# Example 1: Simple User Collection
USER_SCHEMA = {
    "type": "object",
    "title": "User",
    "properties": {
        "_id": {"type": "string"},
        "username": {"type": "string", "minLength": 3, "maxLength": 50},
        "email": {"type": "string", "maxLength": 100},
        "age": {"type": "integer"},
        "is_active": {"type": "boolean"},
        "created_at": {"type": "string"},
    },
    "required": ["_id", "username", "email"]
}

# Example 2: Complex Product Collection with nested objects
PRODUCT_SCHEMA = {
    "type": "object",
    "title": "Product",
    "properties": {
        "_id": {"type": "string"},
        "name": {"type": "string", "maxLength": 200},
        "description": {"type": "string", "maxLength": 1000},
        "price": {"type": "number"},
        "quantity": {"type": "integer"},
        "category": {"type": "string", "maxLength": 50},
        "tags": {
            "type": "array",
            "items": {"type": "string", "maxLength": 30}
        },
        "reviews": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "rating": {"type": "integer"},
                    "comment": {"type": "string"}
                }
            }
        }
    },
    "required": ["_id", "name", "price"]
}

# Example 3: Order Collection
ORDER_SCHEMA = {
    "type": "object",
    "title": "Order",
    "properties": {
        "_id": {"type": "string"},
        "user_id": {"type": "string"},
        "order_date": {"type": "string"},
        "status": {"type": "string"},
        "total_amount": {"type": "number"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string"},
                    "quantity": {"type": "integer"},
                    "price": {"type": "number"}
                }
            }
        },
        "shipping_address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"},
                "zip": {"type": "string"}
            }
        }
    },
    "required": ["_id", "user_id", "order_date"]
}


def test_schema_analyzer():
    """Test SchemaAnalyzer functionality"""
    print("\n" + "="*70)
    print("TEST 1: Schema Analysis")
    print("="*70)
    
    analyzer = SchemaAnalyzer("ecommerce_db")
    
    # Load schemas
    analyzer.load_schema("users", USER_SCHEMA)
    analyzer.load_schema("products", PRODUCT_SCHEMA)
    analyzer.load_schema("orders", ORDER_SCHEMA)
    
    # Set document counts
    analyzer.add_documents("users", 10000)
    analyzer.add_documents("products", 5000)
    analyzer.add_documents("orders", 50000)
    
    print(f"\nDatabase: {analyzer.database}")
    print(f"Collections: {analyzer.list_collections()}")
    
    for col_name in analyzer.list_collections():
        col = analyzer.get_collection(col_name)
        print(f"\n  {col_name}: {len(col.fields)} fields")
        for field_name, field in col.fields.items():
            print(f"    - {field_name}: {field.type}")
    
    return analyzer


def test_size_calculator(analyzer):
    """Test size calculation"""
    print("\n" + "="*70)
    print("TEST 2: Size Calculation")
    print("="*70)
    
    db = analyzer.get_database()
    SizeCalculator.print_size_report(db)


def test_sharding_statistics(analyzer):
    """Test sharding statistics"""
    print("\n" + "="*70)
    print("TEST 3: Sharding Statistics Analysis")
    print("="*70)
    
    # Test sharding by user_id on orders collection
    orders_col = analyzer.get_collection("orders")
    
    # Define a custom key generator for user_id sharding
    def user_id_generator(i):
        # Simulate non-uniform distribution
        return f"user_{i % 7}"  # 7 users, creating some imbalance
    
    stats = StatisticsCalculator.analyze_sharding(
        orders_col,
        "user_id",
        key_value_generator=user_id_generator,
        sample_size=50000
    )
    
    StatisticsCalculator.print_sharding_report(stats)
    
    # Test multiple sharding strategies
    print("\n" + "="*70)
    print("TEST 3b: Comparing Sharding Strategies")
    print("="*70)
    
    products_col = analyzer.get_collection("products")
    
    def category_generator(i):
        categories = ["Electronics", "Books", "Clothing", "Home", "Sports"]
        return categories[i % len(categories)]
    
    results = StatisticsCalculator.compare_sharding_strategies(
        products_col,
        ["category", "_id"],
        key_generators={
            "category": category_generator
        }
    )
    
    StatisticsCalculator.print_comparison_report(results)


def test_save_config(analyzer):
    """Save configuration for future use"""
    print("\n" + "="*70)
    print("TEST 4: Save Configuration")
    print("="*70)
    
    config = {
        "database_name": analyzer.database.name,
        "collections": {
            col_name: {
                "schema": analyzer.get_schema(col_name),
                "document_count": analyzer.get_collection(col_name).document_count,
                "fields": list(analyzer.get_collection(col_name).fields.keys())
            }
            for col_name in analyzer.list_collections()
        }
    }
    
    with open("database_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\nConfiguration saved to: database_config.json")
    print(json.dumps(config, indent=2)[:500] + "...")


def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("SCHEMA ANALYZER PACKAGE - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    # Test 1: Schema Analysis
    analyzer = test_schema_analyzer()
    
    # Test 2: Size Calculation
    test_size_calculator(analyzer)
    
    # Test 3: Sharding Statistics
    test_sharding_statistics(analyzer)
    
    # Test 4: Save Configuration
    test_save_config(analyzer)
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED SUCCESSFULLY")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
