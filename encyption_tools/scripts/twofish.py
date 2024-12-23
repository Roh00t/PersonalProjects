class Twofish:
    def __init__(self, key):
        if len(key) not in (16, 24, 32):
            raise ValueError("Key length must be 16, 24, or 32 bytes.")
        self.key = key

    def encrypt(self, block):
        if len(block) != 16:
            raise ValueError("Block size must be exactly 16 bytes.")
        return self._xor_bytes(block, self.key[:16])  # Simplified operation

    def decrypt(self, block):
        if len(block) != 16:
            raise ValueError("Block size must be exactly 16 bytes.")
        return self._xor_bytes(block, self.key[:16])  # Simplified operation

    @staticmethod
    def _xor_bytes(block, key):
        """Utility function to XOR two byte arrays."""
        return bytes(a ^ b for a, b in zip(block, key))
