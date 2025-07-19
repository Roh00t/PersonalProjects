# test_encryptor.py

from encryptor import (
    aes_encrypt_decrypt, 
    des3_encrypt_decrypt, 
    rc4_encrypt_decrypt, 
    twofish_encrypt_decrypt, 
    ecc_sign_verify, 
    rsa_encrypt_sign
)
import time
import pandas as pd
from tabulate import tabulate
import sys
from collections import defaultdict

class EncryptionBenchmark:
    def __init__(self):
        self.results = defaultdict(dict)
        self.security_levels = {
            'AES-256-GCM': 'Very High (256-bit)',
            '3DES': 'Medium (168-bit effective)',
            'RC4': 'Low (Deprecated)',
            'Twofish': 'Very High (256-bit)',
            'RSA-2048': 'High (2048-bit)',
            'ECC P-256': 'High (256-bit)'
        }

    def format_size(self, size_bytes):
        """Format byte size to human readable format"""
        return f"{size_bytes} bytes ({size_bytes * 8} bits)"

    def run_benchmarks(self, data, password, num_iterations=5):
        print("\n" + "="*60)
        print("ENCRYPTION ALGORITHM BENCHMARK")
        print("="*60)
        print(f"\nInput Data Size: {len(data)} bytes")
        print(f"Number of iterations per algorithm: {num_iterations}")
        print("\nRunning benchmarks...")

        # Run multiple iterations for each algorithm
        for _ in range(num_iterations):
            # Symmetric Encryption Tests
            self.benchmark_symmetric('AES-256-GCM', aes_encrypt_decrypt, data, password)
            self.benchmark_symmetric('3DES', des3_encrypt_decrypt, data, password)
            self.benchmark_symmetric('RC4', rc4_encrypt_decrypt, data, password)
            self.benchmark_symmetric('Twofish', twofish_encrypt_decrypt, data, password)
            
            # Asymmetric Tests
            self.benchmark_asymmetric('ECC P-256', ecc_sign_verify, data)
            self.benchmark_asymmetric('RSA-2048', rsa_encrypt_sign, data)

        self.print_results()

    def benchmark_symmetric(self, algo_name, func, data, password):
        start_time = time.perf_counter()
        ciphertext, decrypted = func(data, password)
        end_time = time.perf_counter()
        
        # Store results
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.update_results(algo_name, execution_time, len(ciphertext), len(decrypted))

    def benchmark_asymmetric(self, algo_name, func, data):
        start_time = time.perf_counter()
        if algo_name == 'RSA-2048':
            ciphertext, decrypted, signature = func(data)
            output_size = len(ciphertext) + len(signature)
        else:  # ECC
            signature = func(data)
            output_size = len(signature)
        end_time = time.perf_counter()
        
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.update_results(algo_name, execution_time, output_size, len(data))

    def update_results(self, algo_name, time, output_size, input_size):
        if 'times' not in self.results[algo_name]:
            self.results[algo_name]['times'] = []
        self.results[algo_name]['times'].append(time)
        self.results[algo_name]['output_size'] = output_size
        self.results[algo_name]['input_size'] = input_size

    def print_results(self):
        print("\n" + "="*60)
        print("BENCHMARK RESULTS")
        print("="*60 + "\n")

        # Prepare results table
        table_data = []
        headers = ['Algorithm', 'Avg Time (ms)', 'Size Overhead', 'Security Level']

        for algo, data in self.results.items():
            avg_time = sum(data['times']) / len(data['times'])
            size_overhead = data['output_size'] - data['input_size']
            size_overhead_str = f"+{size_overhead} bytes" if size_overhead > 0 else "0 bytes"
            
            table_data.append([
                algo,
                f"{avg_time:.3f}",
                size_overhead_str,
                self.security_levels[algo]
            ])

        # Sort by average time
        table_data.sort(key=lambda x: float(x[1]))

        # Print comparison table
        print(tabulate(table_data, headers=headers, tablefmt='grid'))

        # Print additional analysis
        fastest = table_data[0][0]
        slowest = table_data[-1][0]
        
        print("\nANALYSIS:")
        print("-" * 60)
        print(f"✓ Fastest Algorithm: {fastest}")
        print(f"✓ Slowest Algorithm: {slowest}")
        
        # Security recommendations
        print("\nSECURITY RECOMMENDATIONS:")
        print("-" * 60)
        print("• For general data encryption: AES-256-GCM")
        print("• For key exchange: RSA-2048 or ECC P-256")
        print("• For digital signatures: ECC P-256")
        print("\nNOTES:")
        print("-" * 60)
        print("• RC4 is considered cryptographically broken and should be avoided")
        print("• 3DES is being phased out and should be replaced with AES")
        print("• ECC provides similar security to RSA with smaller key sizes")

def run_encryption_tests():
    # Test data
    text = "Confidential Data"
    data = text.encode()
    password = "strongpassword"

    # Run benchmarks
    benchmark = EncryptionBenchmark()
    benchmark.run_benchmarks(data, password)

if __name__ == "__main__":
    run_encryption_tests()