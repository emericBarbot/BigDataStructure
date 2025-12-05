"""
SchemaAnalyzer: Main module to parse JSON Schema and create data structures
"""

import json
from typing import Any, Dict, List, Optional, Union


class Field:
    """Represents a field in a schema"""
    
    def __init__(self, name: str, field_type: str, properties: Dict[str, Any] = None):
        self.name = name
        self.type = field_type
        self.properties = properties or {}
        self.is_array = field_type == "array"
        self.is_object = field_type == "object"
        self.required = self.properties.get("required", False)
        self.default = self.properties.get("default", None)
        self.items = self.properties.get("items", None)
    
    def __repr__(self):
        return f"Field(name={self.name}, type={self.type})"


class Collection:
    """Represents a collection with its schema"""
    
    def __init__(self, name: str, schema: Dict[str, Any]):
        self.name = name
        self.schema = schema
        self.fields: Dict[str, Field] = {}
        self.document_count = 0
        self.parse_schema()
    
    def parse_schema(self):
        """Parse JSON schema and extract fields"""
        if "properties" in self.schema:
            for field_name, field_schema in self.schema["properties"].items():
                field_type = field_schema.get("type", "unknown")
                self.fields[field_name] = Field(field_name, field_type, field_schema)
    
    def add_documents(self, count: int):
        """Set the number of documents in this collection"""
        self.document_count = count
    
    def get_field(self, field_name: str) -> Optional[Field]:
        """Get a field by name"""
        return self.fields.get(field_name)
    
    def __repr__(self):
        return f"Collection(name={self.name}, fields={list(self.fields.keys())})"


class Database:
    """Represents a database with multiple collections"""
    
    def __init__(self, name: str):
        self.name = name
        self.collections: Dict[str, Collection] = {}
        self.statistics = {}
    
    def add_collection(self, collection: Collection):
        """Add a collection to the database"""
        self.collections[collection.name] = collection
    
    def get_collection(self, collection_name: str) -> Optional[Collection]:
        """Get a collection by name"""
        return self.collections.get(collection_name)
    
    def list_collections(self) -> List[str]:
        """List all collection names"""
        return list(self.collections.keys())
    
    def __repr__(self):
        return f"Database(name={self.name}, collections={self.list_collections()})"


class SchemaAnalyzer:
    """Main class to analyze JSON schemas and build database structures"""
    
    def __init__(self, name: str = "default_db"):
        self.database = Database(name)
        self.schemas: Dict[str, Dict[str, Any]] = {}
    
    def load_schema(self, collection_name: str, schema: Union[str, Dict[str, Any]]) -> Collection:
        """
        Load a JSON schema for a collection
        
        Args:
            collection_name: Name of the collection
            schema: JSON schema as dict or JSON string
            
        Returns:
            Collection object
        """
        if isinstance(schema, str):
            schema = json.loads(schema)
        
        self.schemas[collection_name] = schema
        collection = Collection(collection_name, schema)
        self.database.add_collection(collection)
        
        return collection
    
    def add_documents(self, collection_name: str, count: int):
        """Set the number of documents in a collection"""
        collection = self.database.get_collection(collection_name)
        if collection:
            collection.add_documents(count)
    
    def get_database(self) -> Database:
        """Get the database object"""
        return self.database
    
    def get_collection(self, collection_name: str) -> Optional[Collection]:
        """Get a collection by name"""
        return self.database.get_collection(collection_name)
    
    def list_collections(self) -> List[str]:
        """List all collections"""
        return self.database.list_collections()
    
    def get_schema(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """Get schema for a collection"""
        return self.schemas.get(collection_name)
