"""
SizeCalculator: Module to compute sizes of documents, collections, and databases
"""

from typing import Any, Dict
from .schema_analyzer import Collection, Database


class SizeCalculator:
    """Calculate sizes of documents, collections, and databases"""
    
    # Default sizes in bytes for different types
    TYPE_SIZES = {
        "string": 50,        # Average string size
        "number": 8,         # Integer or float
        "integer": 4,        # Integer
        "boolean": 1,        # Boolean
        "array": 16,         # Array overhead
        "object": 24,        # Object overhead
        "null": 0,
    }
    
    @staticmethod
    def get_type_size(field_type: str, properties: Dict[str, Any] = None) -> int:
        """
        Get the size in bytes for a given type
        
        Args:
            field_type: The JSON Schema type
            properties: Additional properties (minLength, maxLength, etc.)
            
        Returns:
            Size in bytes
        """
        properties = properties or {}
        base_size = SizeCalculator.TYPE_SIZES.get(field_type, 50)
        
        # Adjust for string length hints
        if field_type == "string":
            if "maxLength" in properties:
                base_size = properties["maxLength"]
            elif "minLength" in properties:
                base_size = properties["minLength"]
        
        return base_size
    
    @staticmethod
    def calculate_document_size(collection: Collection) -> int:
        """
        Calculate average size of a document in a collection
        
        Args:
            collection: Collection object
            
        Returns:
            Size in bytes
        """
        total_size = 24  # Document overhead (object wrapper)
        
        for field_name, field in collection.fields.items():
            field_size = SizeCalculator.get_type_size(field.type, field.properties)
            
            # If it's an array, estimate items
            if field.is_array and field.items:
                item_type = field.items.get("type", "object")
                item_size = SizeCalculator.get_type_size(item_type)
                # Average array with 5 items
                field_size = item_size * 5 + 16
            
            # If it's an object, add overhead
            if field.is_object:
                field_size = 24  # Object overhead
            
            total_size += field_size + 8  # Field name overhead
        
        return total_size
    
    @staticmethod
    def calculate_collection_size(collection: Collection) -> Dict[str, Any]:
        """
        Calculate total size of a collection
        
        Args:
            collection: Collection object
            
        Returns:
            Dict with breakdown of sizes
        """
        doc_size = SizeCalculator.calculate_document_size(collection)
        total_size = doc_size * collection.document_count
        
        return {
            "collection_name": collection.name,
            "document_count": collection.document_count,
            "average_document_size_bytes": doc_size,
            "total_collection_size_bytes": total_size,
            "total_collection_size_mb": round(total_size / (1024 ** 2), 2),
            "total_collection_size_gb": round(total_size / (1024 ** 3), 4),
        }
    
    @staticmethod
    def calculate_database_size(database: Database) -> Dict[str, Any]:
        """
        Calculate total size of a database
        
        Args:
            database: Database object
            
        Returns:
            Dict with breakdown of sizes
        """
        total_size = 0
        collections_info = []
        
        for collection in database.collections.values():
            collection_info = SizeCalculator.calculate_collection_size(collection)
            collections_info.append(collection_info)
            total_size += collection_info["total_collection_size_bytes"]
        
        return {
            "database_name": database.name,
            "collection_count": len(database.collections),
            "collections": collections_info,
            "total_database_size_bytes": total_size,
            "total_database_size_mb": round(total_size / (1024 ** 2), 2),
            "total_database_size_gb": round(total_size / (1024 ** 3), 4),
        }
    
    @staticmethod
    def print_size_report(database: Database):
        """Print a formatted size report"""
        report = SizeCalculator.calculate_database_size(database)
        
        print("\n" + "="*60)
        print(f"DATABASE SIZE REPORT: {report['database_name']}")
        print("="*60)
        print(f"Total Collections: {report['collection_count']}")
        print(f"Total Database Size: {report['total_database_size_mb']} MB ({report['total_database_size_gb']} GB)")
        print("\nCollection Details:")
        print("-"*60)
        
        for col_info in report["collections"]:
            print(f"\n  Collection: {col_info['collection_name']}")
            print(f"    Documents: {col_info['document_count']}")
            print(f"    Avg Document Size: {col_info['average_document_size_bytes']} bytes")
            print(f"    Total Size: {col_info['total_collection_size_mb']} MB")
        
        print("\n" + "="*60)
