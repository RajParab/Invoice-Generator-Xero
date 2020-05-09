import json
import requests
import webbrowser
import base64

client_id = '828A00E74A06468C8DD5DFFA8F08A423'#828A00E74A06468C8DD5DFFA8F08A423
client_secret = 'RrClUm3v1bn0ARPFwX_A8egcGqKDEM09kyfDdLKC_wdcYZzi'#RrClUm3v1bn0ARPFwX_A8egcGqKDEM09kyfDdLKC_wdcYZzi
redirect_url = 'https://xero.com/'
scope = 'offline_access accounting.transactions'
b64_id_secret = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')



class Xero():

	def __init__(self):
		self.client_id = '828A00E74A06468C8DD5DFFA8F08A423'
		self.client_secret = 'RrClUm3v1bn0ARPFwX_A8egcGqKDEM09kyfDdLKC_wdcYZzi'
		self.redirect_url= 'https://xero.com/'
		self.scope='offline_access accounting.transactions'
		self.b64_id_secret = base64.b64encode(bytes(client_id + ':' + client_secret, 'utf-8')).decode('utf-8')

	def XeroRefreshToken(self,refresh_token):
		token_refresh_url = 'https://identity.xero.com/connect/token'
		response = requests.post(token_refresh_url,headers= 
    							{
    							'Authorization' : 'Basic ' + self.b64_id_secret,
    							'Content-Type': 'application/x-www-form-urlencoded'
    							},
    							data = {
    								'grant_type' : 'refresh_token',
    								'refresh_token' : refresh_token
    								})
		json_response = response.json()
		new_refresh_token = json_response['refresh_token']
		rt_file = open('refresh_token.txt', 'w')
		rt_file.write(new_refresh_token)
		rt_file.close()

		access_token=json_response['access_token']
		at_file = open('access_token.txt', 'w')
		at_file.write(access_token)
		at_file.close()
		return [json_response['access_token'], json_response['refresh_token']]

	def XeroTenantID(self, access_token):
		connections_url = 'https://api.xero.com/connections'
		response = requests.get(connections_url,
                           headers = {
                               'Authorization': 'Bearer ' + access_token,
                               'Content-Type': 'application/json'
                           })
		json_response = response.json()
		tenant=json_response[0]
		print(json_response,"tenantsID")
		return tenant['tenantId']

	def XeroNewRefreshToken(self):
		rt_file=open('refresh_token.txt', 'r+')
		refresh_token=rt_file.read()
		rt_file.close()
		return refresh_token
    
		

		

	def XeroContactID(self,access_token,tenantId):
		contact_ref_url='https://api.xero.com/api.xro/2.0/Contacts'
		response=requests.get(contact_ref_url,
							 headers={
    						 		'Authorization': "Bearer " + access_token,
									'Accept': 'application/json',
									'Xero-tenant-id': tenantId,
    						 })

		json_response = response.json()
		print(json_response)
		return json_response['Contacts']['ContactID']

	def XeroCreateInvoice(self,access_token,tenantId, invoice_dict):
		create_invoice_url='https://api.xero.com/api.xro/2.0/Invoices'
		response=requests.post(create_invoice_url,
						headers={
						'Authorization': "Bearer " + access_token,
						'Accept': 'application/json',
						'Xero-tenant-id': tenantId,
						},
						json = {
						"Type": "ACCREC",
						"Contact": { 
						"ContactID": invoice_dict['contactID'],
						},
						"DateString": invoice_dict['date'] + "T00:00:00",
						"DueDateString": invoice_dict['dueDate'] + "T00:00:00",
						"LineAmountTypes": "Exclusive",
						"CurrencyCode": "INR",
						"LineItems": [
						{
						"Description": invoice_dict['description'],
						"Quantity": float(invoice_dict['quantity']),
						"UnitAmount": float(invoice_dict['amount_per_unit']),
						"AccountCode":"200",

						}]
						}
						)
		json_response = response.json()

		print(json_response)