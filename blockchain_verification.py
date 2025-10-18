from hedera import Client, PrivateKey, AccountId, TransferTransaction, Hbar
import pandas as pd
import hashlib

class HederaVerifier:
    def __init__(self):
        try:
            self.client = Client.for_testnet()
            # These will be updated after setup
            self.private_key = None
            self.account_id = None
        except Exception as e:
            print(f" Hedera client failed: {e}")
    
    def setup_credentials(self, private_key_str, account_id_str):
        """Set credentials after generating them"""
        self.private_key = PrivateKey.from_string(private_key_str)
        self.account_id = AccountId.from_string(account_id_str)
    
    def verify_portfolio_decision(self, assets, risk_score, recommendation):
        """Verify portfolio decision on Hedera"""
        try:
            if not self.private_key or not self.account_id:
                return {
                    'success': False,
                    'error': 'Hedera credentials not set up. Run hedera_urgent_setup.py first'
                }
            
            # Create memo (limited to 100 chars)
            memo = f"WG:{risk_score}:{','.join(assets[:2])}"
            if len(memo) > 90:
                memo = memo[:90]
            
            # Create transaction
            transaction = (
                TransferTransaction()
                .add_hbar_transfer(self.account_id, Hbar(0))
                .set_transaction_memo(memo)
                .freeze_with(self.client)
            )
            
            signed_tx = transaction.sign(self.private_key)
            tx_response = signed_tx.execute(self.client)
            receipt = tx_response.get_receipt(self.client)
            
            return {
                'success': True,
                'transaction_id': str(receipt.transaction_id),
                'status': str(receipt.status),
                'memo': memo,
                'explorer_url': f"https://hashscan.io/testnet/transaction/{receipt.transaction_id}"
            }
            
        except Exception as e:
            print(f"Blockchain error: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Emergency mock version
class MockHederaVerifier:
    def verify_portfolio_decision(self, assets, risk_score, recommendation):
        return {
            'success': True,
            'transaction_id': f"0.0.1234567.8901234",
            'status': 'SUCCESS',
            'memo': f"WG:{risk_score}:{','.join(assets[:2])}",
            'explorer_url': "https://hashscan.io/testnet",
            'note': 'MOCK TRANSACTION - HEDERA IN PROGRESS'
        }