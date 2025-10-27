from copy import deepcopy
from collections import defaultdict
import Transactions as txn
import json
import os

class Reply:
    def __init__(self, txn_type):
        self.result = {
            txn.TXN_TYPE: txn_type,  
            txn.TXN_ID: "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
            txn.DATA: {"gas_limit": None, "is_admin": True},
        }


class Node:
    def __init__(self):
        self.ledgers = []

    def addSchemaTxnToGraph(self, tx):
        txnId = tx[txn.TXN_ID]
        data = tx.get(txn.DATA) #USING DATA 
        print("\tAdding to graph: ", data) 


    def addIssuerKeyTxnToGraph(self, tx):
        txnId = tx[txn.TXN_ID]
        data = tx.get(txn.DATA) #USING DATA 
        print("\tAdding to graph: ", data) 

    def storeTxnInGraph(self, result):
        result = deepcopy(result)

        if result[txn.TXN_TYPE] == txn.SCHEMA:
            self.addSchemaTxnToGraph(result)
        elif result[txn.TXN_TYPE] == txn.ISSUER_KEY:
            self.addIssuerKeyTxnToGraph(result)
        else:
            return 

    def storeTxnInLedger(self, txn):
        self.ledgers.append(txn)


    def storeTxnAndSendToClient(self, reply, do_deepcopy):
        result = reply.result

        if result[txn.TXN_TYPE] in (txn.SCHEMA, txn.ISSUER_KEY):

            if do_deepcopy:
                result = deepcopy(result) #Line in question

            result[txn.DATA] = json.dumps(result[txn.DATA]) #reply.result and result may have different DATA entries

        self.storeTxnInLedger(result) #ledger stores the unserialized result regardless of deepcopy

        self.storeTxnInGraph(reply.result) #Stores a different result depending on the deepcopy or not 



n = Node()
r_issuer = Reply(txn.ISSUER_KEY)

print("ISSUER KEY TRANSACTION:")

print("\tWith the deepcopy")
n.storeTxnAndSendToClient(r_issuer, True)
print("\tLedger", n.ledgers)
print()

n = Node()
r_issuer = Reply(txn.ISSUER_KEY)

print("Without the deepcopy")
n.storeTxnAndSendToClient(r_issuer, False)
print("\tLedger", n.ledgers)

print()
print("="*50)
print()


print("SCHEMA TRANSACTION:")

n = Node()
r_schema = Reply(txn.SCHEMA)


print("\tWith the deepcopy")
n.storeTxnAndSendToClient(r_schema, True)
print("\tLedger", n.ledgers)
print()

n = Node()
r_schema = Reply(txn.SCHEMA)

print("Without the deepcopy")
n.storeTxnAndSendToClient(r_schema, False)
print("\tLedger", n.ledgers)

