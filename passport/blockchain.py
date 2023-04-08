# -*- coding: utf-8 -*-

# from .RSA_AES import Aes
import hashlib
from hashlib import sha256
import json
from time import time


def _check_blockchain(blocks):
    for i in range(1, len(blocks)):
        currentBlock = blocks[i]
        prevBlock = blocks[i - 1]

        if (get_hash(currentBlock.date_of_birthday, currentBlock.number_of_phone, currentBlock.city,
                     currentBlock.address, prevBlock._hash) != currentBlock._hash):
            return False, currentBlock

    return True


def get_hash(*args) -> str:
    hash = sha256()
    for i in args:
        hash.update(str(i).encode('utf-8'))

    return hash.hexdigest()

# print(get_hash('1','1','1','1'))

class Blockchain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.new_block(prev_hash=1)

    def chek_blockchain(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            prevBlock = self.chain[i - 1]
            if (self.get_hash(prevBlock) != currentBlock['prev_hash']):
                return False, currentBlock

        return True

    def new_block(self, prev_hash=None) -> dict:
        block = {
            'id': len(self.chain) + 1,
            'timestamp': time(),
            'transact': self.current_transactions,
            'prev_hash': prev_hash or self.get_hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, user_login, dict_info) -> int:
        self.current_transactions.append({
            'user_login': user_login,
            'info_from_user': dict_info,
        })
        return self.last_block['id'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def get_hash(block: dict) -> str:
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()


block = Blockchain()

# def get_encript_info(dict_info) -> []:
#     '''
#     dict_info = {'picture': picture,
#      'first_name': first_name,
#      'second_name': second_name,
#      'date_birthday': date_birthday,
#      'city': city,
#      'adress': adress}
#     '''
#
#     aes = Aes()
#     key_aes = aes.print_key()
#     dict_enc_info = {
#         'picture': aes.enc_aes(dict_info['picture'], key_aes),
#         'first_name': aes.enc_aes(dict_info['first_name'], key_aes),
#         'second_name': aes.enc_aes(dict_info['second_name'], key_aes),
#         'date_birthday': aes.enc_aes(dict_info['date_birthday'], key_aes),
#         'city': aes.enc_aes(dict_info['city'], key_aes),
#         'adress': aes.enc_aes(dict_info['adress'], key_aes)
#     }
#
#     return dict_enc_info, key_aes

# def get_encript_info(open_key, secret_key) -> []:
#     '''
#     dict_info = {'picture': picture,
#      'first_name': first_name,
#      'second_name': second_name,
#      'date_birthday': date_birthday,
#      'city': city,
#      'adress': adress}
#     '''
#
#     rsa = Rsa()
#     aes = Aes(login)
#     key_aes = aes.print_key()
#     key_rsa = rsa.get_open_key(), rsa.get_secret_key()
#     dict_enc_info = {
#         'picture': aes.enc_aes(dict_info['picture'], key_aes),
#         'first_name': aes.enc_aes(dict_info['first_name'], key_aes),
#         'second_name': aes.enc_aes(dict_info['second_name'], key_aes),
#         'date_birthday': aes.enc_aes(dict_info['date_birthday'], key_aes),
#         'city': aes.enc_aes(dict_info['city'], key_aes),
#         'adress': aes.enc_aes(dict_info['adress'], key_aes)
#     }
#
#     enc_key_aes = rsa.encript(key_aes, key_rsa[0])
#     return dict_enc_info, enc_key_aes, key_rsa

# a = get_encript_info({'picture': 'picture',
#                         'first_name': 'first_name',
#                         'second_name': 'second_name',
#                         'date_birthday': 'date_birthday',
#                         'city': 'city',
#                         'adress': 'adress'})[0]
#
# blockchain = Blockchain()
# blockchain.new_transaction('asd',  a)
# blockchain.new_block()
# blockchain.new_transaction('asd2',  a)
# blockchain.new_block()
#
# blockchain.new_transaction('asd3', a)
# blockchain.new_block()
# blockchain.new_transaction('as4d',  a)
# blockchain.new_block()
# blockchain.new_transaction('a5sd',  a)
# blockchain.new_block()
#
# # blockchain.new_transaction('asd1', 'qwe1', a)
# # blockchain.new_transaction('asd2', 'qwe3', a)
# # blockchain.new_transaction('asd3', 'qwe4', a)
# print(blockchain.chek_blockchain())
# print(blockchain.chain)

# print(blockchain.current_transactions)
