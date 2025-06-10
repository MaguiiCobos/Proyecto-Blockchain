import json
from web3 import Web3

#Conectarse a Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

#Leer el ABI (interfaz de aplicación binaria) del contrato
with open('build/contracts/Votacion.json') as file:
    votacion_json = json.load(file)
    abi = votacion_json['abi']
    address = votacion_json['networks']['5777']['address']

#Conectar al contrato
s_contrato = w3.eth.contract(address=address, abi=abi)
cuenta = w3.eth.accounts[0] #Desde esta cuenta se enviarán las transacciones

