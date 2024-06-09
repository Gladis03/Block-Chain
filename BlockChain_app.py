import hashlib
import time
import streamlit as st

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update((str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.data)).encode('utf-8'))
        return sha.hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True

def create_diploma_block(blockchain, diploma_data):
    latest_block = blockchain.get_latest_block()
    new_block_index = latest_block.index + 1
    new_block_timestamp = time.time()
    new_block = Block(new_block_index, latest_block.hash, new_block_timestamp, diploma_data, "")
    blockchain.add_block(new_block)

# Menginisialisasi Blockchain di session state
if 'diploma_blockchain' not in st.session_state:
    st.session_state.diploma_blockchain = Blockchain()

diploma_blockchain = st.session_state.diploma_blockchain

st.title("Blockchain untuk Dokumentasi Ijazah")

diploma_data = st.text_input("Masukkan Data Ijazah (e.g., Nama, IPK, Program Studi):")

if st.button("Tambah Blok"):
    if diploma_data:
        create_diploma_block(diploma_blockchain, diploma_data)
        st.success("Blok berhasil ditambahkan!")
    else:
        st.error("Data ijazah tidak boleh kosong.")

if st.button("Cek Validitas Blockchain"):
    if diploma_blockchain.is_chain_valid():
        st.success("Blockchain valid.")
    else:
        st.error("Blockchain tidak valid.")

st.write("Blockchain:")

for block in diploma_blockchain.chain:
    st.write(f"Index: {block.index}")
    st.write(f"Previous Hash: {block.previous_hash}")
    st.write(f"Timestamp: {block.timestamp}")
    st.write(f"Data: {block.data}")
    st.write(f"Hash: {block.hash}")
    st.write("\n")
