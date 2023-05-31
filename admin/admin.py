import os
import subprocess
import time
from dotenv import load_dotenv
from requests import get
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

load_dotenv()
domain = os.getenv('DOMAIN')

bitcoind_rpc_connection = AuthServiceProxy("http://%s:%s@bitcoind:18443"%('user', 'pass'))
bitcoind_rpc_connection.createwallet('testwallet')
bitcoindaddress = bitcoind_rpc_connection.getnewaddress('address1', 'bech32m')
bitcoind_rpc_connection.generatetoaddress(101, bitcoindaddress)

# give lnd time to start
time.sleep(120)

# make first RPC call to LND to trigger letsencrypt 
url = 'https://' + domain + ':' + '10009' + '/v1/getinfo'
admin_macaroon = open('/app/.lnd/data/chain/bitcoin/regtest/admin.macaroon', 'rb').read().hex()
headers = {'Grpc-Metadata-macaroon':admin_macaroon}
response = get(url=url, headers=headers)
print(response.json())
print('')

# check if cert is present
time.sleep(5)
cert_folder_content = subprocess.run('ls /app/.lnd/letsencrypt', shell=True, capture_output=True, text=True)
print(cert_folder_content.stdout.strip())