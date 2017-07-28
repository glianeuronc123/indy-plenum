import base58
import pytest
from ledger.compact_merkle_tree import CompactMerkleTree
from ledger.ledger import Ledger
from plenum.common.constants import TXN_TYPE, TARGET_NYM, DATA, NAME, ALIAS, SERVICES, VALIDATOR, VERKEY
from plenum.common.stack_manager import TxnStackManager

whitelist = ['substring not found']


@pytest.fixture(scope="module")
def tdirWithLedger(tdir):
    ledger = Ledger(CompactMerkleTree(), dataDir=tdir)
    for d in range(3):
        txn = {TXN_TYPE: '0',
               TARGET_NYM: base58.b58encode(b'whatever'),
               DATA: {
                   NAME: str(d),
                   ALIAS: 'test' + str(d),
                   SERVICES: [VALIDATOR],
               }
               }
        if d == 1:
            txn[TARGET_NYM] = "invalid===="
        ledger.add(txn)
    return ledger


"""
Test that invalid base58 TARGET_NYM in pool_transaction raises the proper exception (INDY-150)
"""


def test_parse_non_base58_txn_type_field_raises_descriptive_error(tdirWithLedger, tdir):
    with pytest.raises(ValueError) as excinfo:
        ledger = tdirWithLedger
        _, _, nodeKeys = TxnStackManager.parseLedgerForHaAndKeys(ledger)
    assert (VERKEY in str(excinfo.value))
    ledger.stop()
