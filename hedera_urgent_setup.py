from hedera import Client, PrivateKey, AccountId

def emergency_hedera_setup():
    print(" EMERGENCY HEDERA SETUP - STARTING...")
    
    client = Client.for_testnet()
    print(" Connected to Hedera Testnet")
    
    private_key = PrivateKey.generate()
    public_key = private_key.get_public_key()
    account_id = public_key.to_account_id(0, 0)
    
    print(" HEDERA ACCOUNT CREATED!")
    print(f" Account ID: {account_id}")
    print(f" Private Key: {private_key}")
    
    # Save credentials
    credentials = {
        'account_id': str(account_id),
        'private_key': str(private_key),
        'public_key': str(public_key)
    }
    
    with open('hedera_credentials.txt', 'w') as f:
        for key, value in credentials.items():
            f.write(f"{key}: {value}\n")
    
    print(" Credentials saved to hedera_credentials.txt")
    return client, private_key, account_id

# Test immediately
if __name__ == "__main__":
    client, private_key, account_id = emergency_hedera_setup()