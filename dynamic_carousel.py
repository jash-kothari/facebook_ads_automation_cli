from facebookads.objects import Ad
from facebookads.adobjects.campaign import Campaign
import header
import create_adset
import dynamic_cards

ad = Ad(parent_id=header.my_account['id'])
ad[Ad.Field.name] = 'My Ad'
ad[Ad.Field.adset_id] = create_adset.adset['id']
ad[Ad.Field.status] = Campaign.Status.paused
ad[Ad.Field.creative] = {'creative_id': str(dynamic_cards.creative['id'])}
ad.remote_create()