"""
StatisticsCalculator: Module to compute statistics about document distribution with sharding keys
"""

from typing import Any, Dict, List, Callable
from collections import defaultdict
import math
from .schema_analyzer import Collection


class ShardingStatistics:
    """Statistics about document distribution with a sharding key"""
    
    def __init__(self, collection_name: str, sharding_key: str):
        self.collection_name = collection_name
        self.sharding_key = sharding_key
        self.distribution = defaultdict(int)  # key_value -> count
        self.total_documents = 0
    
    def add_document(self, key_value: Any):
        """Add a document with given sharding key value"""
        self.distribution[key_value] += 1
        self.total_documents += 1
    
    def add_documents_batch(self, key_values: List[Any]):
        """Add multiple documents"""
        for key_value in key_values:
            self.add_document(key_value)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Calculate detailed statistics about the distribution
        
        Returns:
            Dict with statistics
        """
        if self.total_documents == 0:
            return {
                "collection": self.collection_name,
                "sharding_key": self.sharding_key,
                "total_documents": 0,
                "unique_shard_values": 0,
                "error": "No documents in collection"
            }
        
        values = list(self.distribution.values())
        unique_shards = len(self.distribution)
        
        # Calculate statistics
        min_docs = min(values)
        max_docs = max(values)
        avg_docs = self.total_documents / unique_shards
        
        # Calculate standard deviation
        variance = sum((x - avg_docs) ** 2 for x in values) / unique_shards
        std_dev = math.sqrt(variance)
        
        # Calculate balance factor (0 = perfectly balanced, 1 = completely imbalanced)
        balance_factor = (max_docs - min_docs) / avg_docs if avg_docs > 0 else 0
        
        return {
            "collection": self.collection_name,
            "sharding_key": self.sharding_key,
            "total_documents": self.total_documents,
            "unique_shard_values": unique_shards,
            "min_documents_per_shard": min_docs,
            "max_documents_per_shard": max_docs,
            "avg_documents_per_shard": round(avg_docs, 2),
            "std_deviation": round(std_dev, 2),
            "variance": round(variance, 2),
            "balance_factor": round(balance_factor, 4),
            "distribution": dict(self.distribution)
        }


class StatisticsCalculator:
    """Calculate statistics for document distribution with sharding keys"""
    
    @staticmethod
    def analyze_sharding(
        collection: Collection,
        sharding_key: str,
        key_value_generator: Callable[[int], Any] = None,
        sample_size: int = None
    ) -> ShardingStatistics:
        """
        Analyze how documents would be distributed with a given sharding key
        
        Args:
            collection: Collection object
            sharding_key: The field name to use as sharding key
            key_value_generator: Optional function to generate key values for documents
            sample_size: Number of documents to analyze (default: all)
            
        Returns:
            ShardingStatistics object with analysis results
        """
        stats = ShardingStatistics(collection.name, sharding_key)
        
        # Check if sharding key exists in schema
        if sharding_key not in collection.fields:
            raise ValueError(f"Sharding key '{sharding_key}' not found in collection schema")
        
        doc_count = sample_size or collection.document_count
        
        if key_value_generator:
            # Use provided generator
            key_values = [key_value_generator(i) for i in range(doc_count)]
            stats.add_documents_batch(key_values)
        else:
            # Generate default distribution (uniform)
            # Assume 10 shard values by default
            shard_count = min(10, max(1, doc_count // 100))
            shard_values = list(range(shard_count))
            key_values = [shard_values[i % len(shard_values)] for i in range(doc_count)]
            stats.add_documents_batch(key_values)
        
        return stats
    
    @staticmethod
    def compare_sharding_strategies(
        collection: Collection,
        sharding_keys: List[str],
        key_generators: Dict[str, Callable[[int], Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Compare multiple sharding strategies for a collection
        
        Args:
            collection: Collection object
            sharding_keys: List of field names to test as sharding keys
            key_generators: Optional dict mapping field names to generator functions
            
        Returns:
            List of statistics for each sharding strategy
        """
        key_generators = key_generators or {}
        results = []
        
        for key in sharding_keys:
            generator = key_generators.get(key)
            stats = StatisticsCalculator.analyze_sharding(collection, key, generator)
            results.append(stats.get_statistics())
        
        return results
    
    @staticmethod
    def print_sharding_report(stats: ShardingStatistics):
        """Print a formatted sharding statistics report"""
        report = stats.get_statistics()
        
        print("\n" + "="*70)
        print(f"SHARDING STATISTICS: {report['collection']}")
        print("="*70)
        print(f"Sharding Key: {report['sharding_key']}")
        print(f"Total Documents: {report['total_documents']:,}")
        print(f"Unique Shard Values: {report['unique_shard_values']}")
        print()
        print("Distribution Metrics:")
        print(f"  Min docs per shard: {report['min_documents_per_shard']:,}")
        print(f"  Max docs per shard: {report['max_documents_per_shard']:,}")
        print(f"  Avg docs per shard: {report['avg_documents_per_shard']:,.2f}")
        print(f"  Std Deviation: {report['std_deviation']:.2f}")
        print(f"  Balance Factor: {report['balance_factor']:.4f} (0=perfect, 1=worst)")
        print()
        print("Shard Weight Distribution (Partition Details):")
        print("-" * 70)
        print(f"{'Shard Key':<30} {'Count':>12} {'Weight':>12} {'Visual':>15}")
        print("-" * 70)
        
        # Show distribution with weight details
        total = report['total_documents']
        for key, count in sorted(report['distribution'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total) * 100 if total > 0 else 0
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            print(f"  {str(key):<28} {count:>12,} {percentage:>10.2f}%  {bar}")
        
        print("-" * 70)
        print(f"{'Total':<30} {total:>12,} {'100.00%':>10}")
        print("\n" + "="*70)
    
    @staticmethod
    def print_comparison_report(results: List[Dict[str, Any]]):
        """Print a formatted comparison report"""
        print("\n" + "="*70)
        print("SHARDING STRATEGIES COMPARISON")
        print("="*70)
        
        for report in results:
            print(f"\nSharding Key: {report['sharding_key']}")
            print(f"  Balance Factor: {report['balance_factor']:.4f}")
            print(f"  Std Deviation: {report['std_deviation']:.2f}")
            print(f"  Max/Avg Ratio: {report.get('max_documents_per_shard', 0) / report.get('avg_documents_per_shard', 1):.2f}")
        
        print("\n" + "="*70)
