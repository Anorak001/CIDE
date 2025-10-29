"""
Test MinHash-Optimized Batch Comparison
========================================
Compare performance of standard vs MinHash-optimized batch analysis.
"""

from batch_comparator import BatchComparator
import time

print("=" * 80)
print("MINHASH OPTIMIZATION TEST")
print("=" * 80)

# Create test files
files = [
    {
        'name': 'file1.py',
        'content': '''
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

def find_max(numbers):
    maximum = numbers[0]
    for num in numbers[1:]:
        if num > maximum:
            maximum = num
    return maximum
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

def get_maximum(data):
    max_val = data[0]
    for val in data[1:]:
        if val > max_val:
            max_val = val
    return max_val
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

def find_min(numbers):
    minimum = numbers[0]
    for num in numbers[1:]:
        if num < minimum:
            minimum = num
    return minimum
'''
    },
    {
        'name': 'file4.py',
        'content': '''
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b
'''
    },
    {
        'name': 'file5.py',
        'content': '''
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr
'''
    },
    {
        'name': 'file6.py',
        'content': '''
# Very similar to file1
def calculate_sum(nums):
    sum_val = 0
    for n in nums:
        sum_val += n
    return sum_val

def find_max(nums):
    max_val = nums[0]
    for n in nums[1:]:
        if n > max_val:
            max_val = n
    return max_val
'''
    }
]

print(f"\nTest files: {len(files)}")
print(f"Total possible pairs: {len(files) * (len(files) - 1) // 2}")

# Test 1: Standard comparison
print("\n" + "-" * 80)
print("[TEST 1] Standard All-Pairs Comparison")
print("-" * 80)

comparator_standard = BatchComparator(mode='hybrid', use_minhash=False)

start = time.time()
result_standard = comparator_standard.compare_all_pairs(files, language='python')
time_standard = time.time() - start

print(f"Time taken: {time_standard:.3f}s")
print(f"Comparisons performed: {result_standard['comparison_count']}")
print(f"Average similarity: {result_standard['statistics']['average_percentage']}")
print(f"Max similarity: {result_standard['statistics']['max_percentage']}")

# Test 2: MinHash-optimized comparison
print("\n" + "-" * 80)
print("[TEST 2] MinHash-Optimized Comparison")
print("-" * 80)

comparator_optimized = BatchComparator(mode='hybrid', use_minhash=True)

start = time.time()
result_optimized = comparator_optimized.compare_all_pairs_optimized(
    files, 
    language='python',
    minhash_threshold=0.3  # Lower threshold to catch more candidates
)
time_optimized = time.time() - start

print(f"Time taken: {time_optimized:.3f}s")
print(f"Comparisons performed: {result_optimized['comparison_count']}")
print(f"Comparisons saved: {result_optimized['comparisons_saved']}")
print(f"Efficiency: {result_optimized['efficiency_percentage']}")
print(f"Average similarity: {result_optimized['statistics']['average_percentage']}")
print(f"Max similarity: {result_optimized['statistics']['max_percentage']}")
print(f"Speedup: {result_optimized['optimization']['speedup']}")

# Performance comparison
print("\n" + "=" * 80)
print("PERFORMANCE COMPARISON")
print("=" * 80)

speedup = time_standard / time_optimized if time_optimized > 0 else float('inf')

print(f"Standard time:    {time_standard:.3f}s")
print(f"Optimized time:   {time_optimized:.3f}s")
print(f"Actual speedup:   {speedup:.2f}x faster")
print(f"Comparisons:      {result_standard['comparison_count']} → {result_optimized['comparison_count']}")
print(f"Reduction:        {result_optimized['comparisons_saved']} saved ({result_optimized['efficiency_percentage']})")

# Accuracy comparison
print("\n" + "=" * 80)
print("ACCURACY VERIFICATION")
print("=" * 80)

# Find the most similar pair from both methods
most_similar_std = result_standard['statistics']['most_similar_pair']
most_similar_opt = result_optimized['statistics']['most_similar_pair']

if most_similar_std and most_similar_opt:
    print(f"Standard method found:")
    print(f"  {most_similar_std['file1']} <-> {most_similar_std['file2']}")
    print(f"  Similarity: {most_similar_std['percentage']}")
    
    print(f"\nOptimized method found:")
    print(f"  {most_similar_opt['file1']} <-> {most_similar_opt['file2']}")
    print(f"  Similarity: {most_similar_opt['percentage']}")
    
    # Check if same pair identified
    std_pair = tuple(sorted([most_similar_std['file1'], most_similar_std['file2']]))
    opt_pair = tuple(sorted([most_similar_opt['file1'], most_similar_opt['file2']]))
    
    if std_pair == opt_pair:
        print(f"\n✓ Both methods identified the same most similar pair!")
    else:
        print(f"\n⚠ Different pairs identified (MinHash filtered some candidates)")

# Scaling projection
print("\n" + "=" * 80)
print("SCALING PROJECTION")
print("=" * 80)

print("Performance estimates for larger datasets:")
print()
print("| Files | Pairs | Standard Time | Optimized Time | Speedup |")
print("|-------|-------|---------------|----------------|---------|")

for n_files in [10, 20, 50, 100]:
    n_pairs = n_files * (n_files - 1) // 2
    # Assume 50% reduction in comparisons with MinHash
    estimated_comparisons = n_pairs * 0.5
    
    # Estimate times (assuming ~200ms per comparison)
    time_per_comparison = 0.2
    est_standard = n_pairs * time_per_comparison
    est_optimized = estimated_comparisons * time_per_comparison + 0.1  # +0.1 for MinHash overhead
    est_speedup = est_standard / est_optimized
    
    print(f"| {n_files:5d} | {n_pairs:5d} | {est_standard:11.1f}s | {est_optimized:12.1f}s | {est_speedup:5.1f}x |")

print("\n" + "=" * 80)
print("✓ MinHash optimization test complete!")
print("=" * 80)
