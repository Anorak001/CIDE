"""
Batch Comparison Module
=======================
Process multiple code files and generate comparison matrices.
Supports both full comparison and MinHash-accelerated mode.
"""

from typing import List, Dict, Any, Optional
from code_similarity import CodeSimilarityAnalyzer
from ast_analyzer import HybridSimilarityAnalyzer
from minhash import FastSimilarityDetector
import itertools


class BatchComparator:
    """Compare multiple code files against each other."""
    
    def __init__(self, mode='hybrid', use_minhash=False):
        self.mode = mode
        self.use_minhash = use_minhash
        self.basic_analyzer = CodeSimilarityAnalyzer()
        self.hybrid_analyzer = HybridSimilarityAnalyzer()
        
        # MinHash detector (initialized when needed)
        self.minhash_detector = None
    
    def compare_all_pairs(self, files: List[Dict[str, str]], language='python') -> Dict[str, Any]:
        """
        Compare all file pairs and generate a comparison matrix.
        
        Args:
            files: List of dicts with 'name' and 'content' keys
            language: Programming language of the files
            
        Returns:
            Dictionary containing comparison matrix and summary statistics
        """
        n = len(files)
        
        # Initialize matrix
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        comparisons = []
        
        # Compare all pairs
        for i in range(n):
            for j in range(i + 1, n):
                file1 = files[i]
                file2 = files[j]
                
                # Perform comparison
                if self.mode == 'hybrid' and language == 'python':
                    result = self.hybrid_analyzer.analyze(file1['content'], file2['content'])
                    similarity = result['weighted_score']
                    
                    comparison = {
                        'file1': file1['name'],
                        'file2': file2['name'],
                        'similarity': similarity,
                        'percentage': f"{similarity * 100:.1f}%",
                        'structure_similarity': result['structure_similarity'],
                        'identical_structure': result['identical_structure']
                    }
                else:
                    result = self.basic_analyzer.analyze(
                        file1['content'], 
                        file2['content'], 
                        mode='basic', 
                        language=language
                    )
                    similarity = result['similarity_score']
                    
                    comparison = {
                        'file1': file1['name'],
                        'file2': file2['name'],
                        'similarity': similarity,
                        'percentage': result['similarity_percentage']
                    }
                
                # Store in matrix (symmetric)
                matrix[i][j] = similarity
                matrix[j][i] = similarity
                
                comparisons.append(comparison)
            
            # Diagonal (self-comparison) is always 1.0
            matrix[i][i] = 1.0
        
        # Calculate statistics
        similarities = [comp['similarity'] for comp in comparisons]
        
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0
        max_similarity = max(similarities) if similarities else 0
        min_similarity = min(similarities) if similarities else 0
        
        # Find most similar pair
        most_similar = max(comparisons, key=lambda x: x['similarity']) if comparisons else None
        
        # Find files with high average similarity (potential plagiarism sources)
        file_avg_similarities = []
        for i in range(n):
            avg = sum(matrix[i][j] for j in range(n) if i != j) / (n - 1) if n > 1 else 0
            file_avg_similarities.append({
                'file': files[i]['name'],
                'average_similarity': avg,
                'percentage': f"{avg * 100:.1f}%"
            })
        
        file_avg_similarities.sort(key=lambda x: x['average_similarity'], reverse=True)
        
        return {
            'mode': self.mode,
            'language': language,
            'file_count': n,
            'comparison_count': len(comparisons),
            'matrix': matrix,
            'comparisons': comparisons,
            'statistics': {
                'average_similarity': avg_similarity,
                'average_percentage': f"{avg_similarity * 100:.1f}%",
                'max_similarity': max_similarity,
                'max_percentage': f"{max_similarity * 100:.1f}%",
                'min_similarity': min_similarity,
                'min_percentage': f"{min_similarity * 100:.1f}%",
                'most_similar_pair': most_similar
            },
            'file_rankings': file_avg_similarities,
            'files': [{'name': f['name'], 'lines': len(f['content'].splitlines())} for f in files]
        }
    
    def compare_all_pairs_optimized(self, files: List[Dict[str, str]], 
                                    language='python',
                                    minhash_threshold=0.5) -> Dict[str, Any]:
        """
        Optimized comparison using MinHash for candidate filtering.
        Much faster for large batches (10+ files).
        
        Args:
            files: List of dicts with 'name' and 'content' keys
            language: Programming language of the files
            minhash_threshold: MinHash similarity threshold for filtering candidates
            
        Returns:
            Dictionary containing comparison matrix and summary statistics
        """
        n = len(files)
        
        # Initialize MinHash detector
        detector = FastSimilarityDetector(
            num_hashes=128,
            num_bands=16,
            similarity_threshold=minhash_threshold
        )
        
        # Add all files to MinHash index
        file_ids = {}
        for i, file in enumerate(files):
            doc_id = detector.add_document(file['content'], file['name'])
            file_ids[i] = doc_id
        
        # Get candidate pairs using MinHash
        candidate_pairs = detector.find_all_similar_pairs(min_similarity=minhash_threshold)
        
        # Create reverse mapping
        id_to_index = {doc_id: idx for idx, doc_id in file_ids.items()}
        
        # Initialize matrix with zeros
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]
        comparisons = []
        
        # Perform detailed analysis only on candidate pairs
        for doc1_id, doc2_id, minhash_sim in candidate_pairs:
            i = id_to_index[doc1_id]
            j = id_to_index[doc2_id]
            
            file1 = files[i]
            file2 = files[j]
            
            # Perform detailed comparison
            if self.mode == 'hybrid' and language == 'python':
                result = self.hybrid_analyzer.analyze(file1['content'], file2['content'])
                similarity = result['weighted_score']
                
                comparison = {
                    'file1': file1['name'],
                    'file2': file2['name'],
                    'similarity': similarity,
                    'percentage': f"{similarity * 100:.1f}%",
                    'structure_similarity': result['structure_similarity'],
                    'identical_structure': result['identical_structure'],
                    'minhash_estimate': minhash_sim
                }
            else:
                result = self.basic_analyzer.analyze(
                    file1['content'], 
                    file2['content'], 
                    mode='basic', 
                    language=language
                )
                similarity = result['similarity_score']
                
                comparison = {
                    'file1': file1['name'],
                    'file2': file2['name'],
                    'similarity': similarity,
                    'percentage': result['similarity_percentage'],
                    'minhash_estimate': minhash_sim
                }
            
            # Store in matrix (symmetric)
            matrix[i][j] = similarity
            matrix[j][i] = similarity
            
            comparisons.append(comparison)
        
        # Set diagonal to 1.0
        for i in range(n):
            matrix[i][i] = 1.0
        
        # Calculate statistics
        similarities = [comp['similarity'] for comp in comparisons]
        
        if similarities:
            avg_similarity = sum(similarities) / len(similarities)
            max_similarity = max(similarities)
            min_similarity = min(similarities)
            most_similar = max(comparisons, key=lambda x: x['similarity'])
        else:
            avg_similarity = 0
            max_similarity = 0
            min_similarity = 0
            most_similar = None
        
        # File rankings
        file_avg_similarities = []
        for i in range(n):
            # Calculate average from non-zero entries
            non_zero_similarities = [matrix[i][j] for j in range(n) if i != j and matrix[i][j] > 0]
            avg = sum(non_zero_similarities) / len(non_zero_similarities) if non_zero_similarities else 0
            
            file_avg_similarities.append({
                'file': files[i]['name'],
                'average_similarity': avg,
                'percentage': f"{avg * 100:.1f}%"
            })
        
        file_avg_similarities.sort(key=lambda x: x['average_similarity'], reverse=True)
        
        # Calculate performance metrics
        total_possible_pairs = n * (n - 1) // 2
        comparisons_saved = total_possible_pairs - len(comparisons)
        efficiency = (comparisons_saved / total_possible_pairs * 100) if total_possible_pairs > 0 else 0
        
        return {
            'mode': self.mode,
            'language': language,
            'file_count': n,
            'comparison_count': len(comparisons),
            'total_possible_pairs': total_possible_pairs,
            'comparisons_saved': comparisons_saved,
            'efficiency_percentage': f"{efficiency:.1f}%",
            'matrix': matrix,
            'comparisons': comparisons,
            'statistics': {
                'average_similarity': avg_similarity,
                'average_percentage': f"{avg_similarity * 100:.1f}%",
                'max_similarity': max_similarity,
                'max_percentage': f"{max_similarity * 100:.1f}%",
                'min_similarity': min_similarity,
                'min_percentage': f"{min_similarity * 100:.1f}%",
                'most_similar_pair': most_similar
            },
            'file_rankings': file_avg_similarities,
            'files': [{'name': f['name'], 'lines': len(f['content'].splitlines())} for f in files],
            'optimization': {
                'minhash_enabled': True,
                'threshold': minhash_threshold,
                'speedup': f"{total_possible_pairs / max(len(comparisons), 1):.1f}x"
            }
        }
    
    def find_clusters(self, files: List[Dict[str, str]], threshold=0.75, language='python') -> Dict[str, Any]:
        """
        Find clusters of similar files (potential plagiarism groups).
        
        Args:
            files: List of dicts with 'name' and 'content' keys
            threshold: Similarity threshold for clustering (0.0 to 1.0)
            language: Programming language of the files
            
        Returns:
            Dictionary containing identified clusters
        """
        result = self.compare_all_pairs(files, language)
        matrix = result['matrix']
        n = len(files)
        
        # Simple clustering: group files with similarity above threshold
        clusters = []
        processed = set()
        
        for i in range(n):
            if i in processed:
                continue
            
            cluster = [i]
            for j in range(i + 1, n):
                if matrix[i][j] >= threshold:
                    cluster.append(j)
                    processed.add(j)
            
            if len(cluster) > 1:
                clusters.append({
                    'cluster_id': len(clusters) + 1,
                    'file_count': len(cluster),
                    'files': [files[idx]['name'] for idx in cluster],
                    'average_similarity': sum(matrix[cluster[i]][cluster[j]] 
                                            for i in range(len(cluster)) 
                                            for j in range(i + 1, len(cluster))) / 
                                         (len(cluster) * (len(cluster) - 1) / 2)
                })
        
        return {
            'threshold': threshold,
            'threshold_percentage': f"{threshold * 100:.1f}%",
            'cluster_count': len(clusters),
            'clusters': clusters,
            'full_comparison': result
        }


def batch_compare(file_list: List[Dict[str, str]], mode='hybrid', language='python') -> Dict[str, Any]:
    """
    Convenience function for batch comparison.
    
    Args:
        file_list: List of files with 'name' and 'content'
        mode: Analysis mode ('basic' or 'hybrid')
        language: Programming language
        
    Returns:
        Comparison results dictionary
    """
    comparator = BatchComparator(mode=mode)
    return comparator.compare_all_pairs(file_list, language)


if __name__ == "__main__":
    # Example usage
    print("=" * 80)
    print("BATCH COMPARISON MODULE")
    print("=" * 80)
    
    # Sample files
    files = [
        {
            'name': 'file1.py',
            'content': '''
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
'''
        },
        {
            'name': 'file2.py',
            'content': '''
def sum_values(data):
    result = 0
    for value in data:
        result += value
    return result
'''
        },
        {
            'name': 'file3.py',
            'content': '''
def multiply_list(numbers):
    product = 1
    for num in numbers:
        product *= num
    return product
'''
        }
    ]
    
    comparator = BatchComparator(mode='hybrid')
    result = comparator.compare_all_pairs(files)
    
    print(f"\nAnalyzed {result['file_count']} files")
    print(f"Performed {result['comparison_count']} comparisons")
    print(f"\nAverage similarity: {result['statistics']['average_percentage']}")
    print(f"Most similar pair: {result['statistics']['most_similar_pair']['file1']} <-> "
          f"{result['statistics']['most_similar_pair']['file2']} "
          f"({result['statistics']['most_similar_pair']['percentage']})")
    
    print("\n" + "=" * 80)
    print("Batch comparison module ready!")
    print("=" * 80)
