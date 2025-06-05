import random

class SimpleKEM:
    def keygen(self):
        return b'public-key', b'secret-key'

    def encapsulate(self, pk):
        key = b'shared-secret-key'
        ct = b'ciphertext-from-encaps'
        return key, ct

    def decapsulate(self, sk, ct):
        if ct != b'ciphertext-from-encaps':
            raise ValueError("KEM decryption failed")
        return b'shared-secret-key'

def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def aead_encrypt(key: bytes, plaintext: bytes, associated_data: bytes = b'') -> (bytes, bytes):
    nonce = b'fixed-nonce'
    ciphertext = xor_bytes(plaintext, key + nonce + associated_data)
    return nonce, ciphertext

def aead_decrypt(key: bytes, nonce: bytes, ciphertext: bytes, associated_data: bytes = b'') -> bytes:
    decrypted = xor_bytes(ciphertext, key + nonce + associated_data)
    # Simulated integrity check: fail if "fail" is in the decrypted message
    if b'fail' in decrypted:
        raise ValueError("Decryption failed: authentication check failed")
    return decrypted

class KEMDEM:
    def __init__(self, kem):
        self.kem = kem

    def keygen(self):
        return self.kem.keygen()

    def encrypt(self, pk, message: bytes):
        key, ct_kem = self.kem.encapsulate(pk)
        nonce, ct_dem = aead_encrypt(key, message, associated_data=ct_kem)
        return ct_kem + b'||' + nonce + b'||' + ct_dem

    def decrypt(self, ciphertext_combined):
        try:
            ct_kem, nonce, ct_dem = ciphertext_combined.split(b'||', 2)
        except ValueError:
            raise ValueError("Ciphertext format invalid")

        key = self.kem.decapsulate(sk, ct_kem)
        return aead_decrypt(key, nonce, ct_dem, associated_data=ct_kem)


class Node:

    messages=[]
    gateType = "" #support for XOR and AND
    id = ""
    kem = SimpleKEM()
    scheme = KEMDEM(kem)
    pk, sk = scheme.keygen()


    
    def __init__(self, g0, g1, h0, h1, gate, i0, i1): #gate is XOR or AND
        self.id = random.randint(0, 1<<31)
        self.gateType = gate


        self.messages = [self.encrypt(i0, (int.from_bytes(g0, "big") ^ int.from_bytes(h0, "big")).to_bytes(4, "big")), 
                         self.encrypt(i0, (int.from_bytes(g1, "big") ^ int.from_bytes(h1, "big")).to_bytes(4, "big")), 
                         self.encrypt(i1, (int.from_bytes(g0, "big") ^ int.from_bytes(h1, "big")).to_bytes(4, "big")), 
                         self.encrypt(i1, (int.from_bytes(g1, "big") ^ int.from_bytes(h0, "big")).to_bytes(4, "big"))]

        
    
    def create(*args, **kwargs):
        i0 = random.randint(0, 1<<32 - 1).to_bytes(4, "big")
        i1 = random.randint(0, 1<<32 - 1).to_bytes(4, "big")
        n = Node(*args, **kwargs, i0=i0, i1=i1)
        # g0^h0, g1^h1, g0^h1, g1^h0
        
        return n, (i0, i1)

    def encrypt(self, i, key):
        return self.scheme.encrypt(i, key)

    def decrypt(self, g, h):
        for message in self.messages:
            try:
                attempt = self.scheme.decrypt(self.sk, message)
                return attempt
            except:
                continue
        return "nothing worked?"
    
    def __str__(self):
        return "rdtcyfvgubhijkn"

node, (i0, i1) = Node.create(b'1', b'2', b'4', b'8', "XOR")

print(str(int.from_bytes(i0, "big")) + " " + str(int.from_bytes(i1, "big")))
print(node)
print(node.messages[0])
print(node.decrypt(89, 789))
print(node.sk)
