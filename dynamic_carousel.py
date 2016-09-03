from facebookads.objects import Ad
from facebookads.adobjects.campaign import Campaign
import header
import create_adset
import dynamic_cards

choice = raw_input("Please enter yes to create a new Adset or enter no to choose existing one.\n").lower()
if 'yes' in choice:
	adset_id = create_adset.create_adset()
else:
	adset_id =  raw_input("Please enter adset id.\n")
dynamic_cards.create_creative()
ad = Ad(parent_id=header.my_account['id'])
ad[Ad.Field.name] = 'My Ad'
ad[Ad.Field.adset_id] = adset_id
ad[Ad.Field.status] = Campaign.Status.paused
ad[Ad.Field.creative] = {'creative_id': str(dynamic_cards.creative['id'])}
ad.remote_create()
print ad[Ad.Field.success]