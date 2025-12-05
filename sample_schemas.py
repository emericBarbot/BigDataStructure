"""
Sample JSON Schemas for testing the Schema Analyzer Package
These are realistic examples that could be used in practice
"""

# Schema 1: Blog Post Collection
BLOG_POST_SCHEMA = {
    "title": "BlogPost",
    "type": "object",
    "properties": {
        "_id": {
            "type": "string",
            "description": "Unique identifier for the blog post"
        },
        "title": {
            "type": "string",
            "minLength": 5,
            "maxLength": 500,
            "description": "Title of the blog post"
        },
        "content": {
            "type": "string",
            "maxLength": 50000,
            "description": "Main content of the blog post"
        },
        "author_id": {
            "type": "string",
            "description": "ID of the author"
        },
        "published_date": {
            "type": "string",
            "description": "Publication date in ISO 8601 format"
        },
        "updated_date": {
            "type": "string",
            "description": "Last update date in ISO 8601 format"
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "string",
                "maxLength": 50
            },
            "description": "Tags associated with the blog post"
        },
        "view_count": {
            "type": "integer",
            "description": "Number of views"
        },
        "comments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "comment_id": {"type": "string"},
                    "author_id": {"type": "string"},
                    "text": {"type": "string", "maxLength": 5000},
                    "created_at": {"type": "string"},
                    "likes": {"type": "integer"}
                }
            },
            "description": "Comments on the blog post"
        }
    },
    "required": ["_id", "title", "content", "author_id", "published_date"]
}

# Schema 2: E-Commerce Customer Collection
CUSTOMER_SCHEMA = {
    "title": "Customer",
    "type": "object",
    "properties": {
        "_id": {
            "type": "string",
            "description": "Unique customer ID"
        },
        "first_name": {
            "type": "string",
            "maxLength": 50
        },
        "last_name": {
            "type": "string",
            "maxLength": 50
        },
        "email": {
            "type": "string",
            "maxLength": 100
        },
        "phone": {
            "type": "string",
            "maxLength": 20
        },
        "registration_date": {
            "type": "string"
        },
        "last_purchase_date": {
            "type": "string"
        },
        "is_premium": {
            "type": "boolean"
        },
        "total_spent": {
            "type": "number",
            "description": "Total amount spent in the platform"
        },
        "addresses": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "state": {"type": "string"},
                    "zip_code": {"type": "string"},
                    "country": {"type": "string"},
                    "is_default": {"type": "boolean"}
                }
            }
        },
        "preferences": {
            "type": "object",
            "properties": {
                "newsletter": {"type": "boolean"},
                "notifications": {"type": "boolean"},
                "language": {"type": "string"}
            }
        }
    },
    "required": ["_id", "email", "first_name", "last_name"]
}

# Schema 3: Social Network Post Collection
SOCIAL_POST_SCHEMA = {
    "title": "SocialPost",
    "type": "object",
    "properties": {
        "_id": {
            "type": "string"
        },
        "user_id": {
            "type": "string",
            "description": "ID of the post creator"
        },
        "text": {
            "type": "string",
            "maxLength": 500
        },
        "image_url": {
            "type": "string",
            "maxLength": 500
        },
        "created_at": {
            "type": "string"
        },
        "likes_count": {
            "type": "integer"
        },
        "shares_count": {
            "type": "integer"
        },
        "likes": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "description": "User IDs who liked this post"
        },
        "replies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "reply_id": {"type": "string"},
                    "user_id": {"type": "string"},
                    "text": {"type": "string", "maxLength": 500},
                    "created_at": {"type": "string"},
                    "likes": {"type": "integer"}
                }
            }
        },
        "hashtags": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["_id", "user_id", "text", "created_at"]
}

# Schema 4: Sensor Data Collection (IoT)
SENSOR_DATA_SCHEMA = {
    "title": "SensorReading",
    "type": "object",
    "properties": {
        "_id": {
            "type": "string"
        },
        "device_id": {
            "type": "string",
            "description": "ID of the IoT device"
        },
        "location_id": {
            "type": "string"
        },
        "timestamp": {
            "type": "string",
            "description": "ISO 8601 timestamp"
        },
        "temperature": {
            "type": "number"
        },
        "humidity": {
            "type": "number"
        },
        "pressure": {
            "type": "number"
        },
        "air_quality": {
            "type": "number"
        },
        "coordinates": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            }
        },
        "battery_level": {
            "type": "integer"
        },
        "signal_strength": {
            "type": "integer"
        }
    },
    "required": ["_id", "device_id", "timestamp", "temperature", "humidity"]
}

# Schema 5: Product Catalog Collection
PRODUCT_CATALOG_SCHEMA = {
    "title": "Product",
    "type": "object",
    "properties": {
        "_id": {
            "type": "string",
            "description": "Unique product ID / SKU"
        },
        "name": {
            "type": "string",
            "maxLength": 200
        },
        "description": {
            "type": "string",
            "maxLength": 2000
        },
        "category": {
            "type": "string",
            "maxLength": 100
        },
        "subcategory": {
            "type": "string",
            "maxLength": 100
        },
        "price": {
            "type": "number"
        },
        "original_price": {
            "type": "number"
        },
        "currency": {
            "type": "string"
        },
        "stock_quantity": {
            "type": "integer"
        },
        "rating": {
            "type": "number",
            "description": "Average rating 0-5"
        },
        "review_count": {
            "type": "integer"
        },
        "manufacturer": {
            "type": "string"
        },
        "specifications": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "value": {"type": "string"}
                }
            }
        },
        "images": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "url": {"type": "string"},
                    "alt_text": {"type": "string"}
                }
            }
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"}
        },
        "created_at": {
            "type": "string"
        },
        "updated_at": {
            "type": "string"
        },
        "is_active": {
            "type": "boolean"
        }
    },
    "required": ["_id", "name", "category", "price", "stock_quantity"]
}

# Dictionary with all schemas for easy access
SCHEMAS = {
    "blog_posts": BLOG_POST_SCHEMA,
    "customers": CUSTOMER_SCHEMA,
    "social_posts": SOCIAL_POST_SCHEMA,
    "sensor_data": SENSOR_DATA_SCHEMA,
    "products": PRODUCT_CATALOG_SCHEMA,
}

# Realistic document counts for different collections
DOCUMENT_COUNTS = {
    "blog_posts": 50000,
    "customers": 100000,
    "social_posts": 500000,
    "sensor_data": 1000000,
    "products": 75000,
}
