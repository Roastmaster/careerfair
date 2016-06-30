import requests
import json

url = 'https://api.sandbox.paypal.com/v1/invoicing/invoices/'
invoice = {"merchant_info":{
		"email": "roastmiester@gmail.com"
	},
	"billing_info": [
		{"email": "m.ruben1234@gmail.com"}
	],
	"items": [
		{"name" :"Butues",
		"quantity":100,
		"unit_price":{
			"currency": "USD",
			"value": "4"
			}
		}
	],
	}
data= json.dumps(invoice)
res = requests.post(url, data=data)
print res.status_code, res.text
print "hello"
