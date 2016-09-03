from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.targetingsearch import TargetingSearch
from facebookads.adobjects.targeting import Targeting
import header
import json
import create_campaign as campaign

def create_adset():
	choice = raw_input("Please enter yes to create a new campaign and anything else to to enter id for existing campaign.\n").lower()
	print choice
	if 'yes' in choice:
		campaign_id = campaign.create_campaign()
	else:
		campaign_id = raw_input("Please enter campaign id.\n")	
	query = raw_input("Enter query for targeting customer type.\n")
	params = {
		'q': query,
		'type': 'adinterest',

	}

	resp = TargetingSearch.search(params=params)
	print resp
	resp=json.loads(str(resp).replace('<TargetingSearch> ',''))
	print(resp)

	number_of_interests = int(raw_input("Please enter number of interests.\n"))
	interest_list = []
	for i in xrange(number_of_interests):
		a = int(raw_input("Enter Interest Ids.\n"))
		interest_list.append(a)

	number_of_countries = int(raw_input("Please enter number of countries for targeting.\n"))
	country_list = []
	for i in xrange(number_of_countries):
		a = raw_input("Enter Country Codes.\n")
		country_list.append(a)
	age_min = raw_input("Please enter minimum targeting age.\n")
	age_max = raw_input("Please enter maximum targeting age.\n")
	targeting = {
		Targeting.Field.geo_locations: {
			Targeting.Field.countries: country_list,
		},
		Targeting.Field.interests: interest_list,
		Targeting.Field.age_min: age_min,
		Targeting.Field.age_max: age_max,
	}

	adset_name = raw_input("Please enter a name for the adset.\n")
	daily_budget = int(raw_input("Please enter daily_budget(in paise).\n"))
	bid_amount = int(raw_input("Please enter bid_amount(in paise).\n"))
	start_time = raw_input("Please enter start date for AdSet format(YYYY-MM_DD).\n")
	end_time = raw_input("Please enter end date for AdSet format(YYYY-MM_DD).\n")

	adset = AdSet(parent_id=header.my_account['id'])
	adset.update({
		AdSet.Field.name: adset_name,
		AdSet.Field.campaign_id: campaign_id,
		AdSet.Field.daily_budget: daily_budget,
		AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
		AdSet.Field.optimization_goal: AdSet.OptimizationGoal.reach,
		AdSet.Field.bid_amount: bid_amount,
		AdSet.Field.targeting: targeting,
		AdSet.Field.start_time: start_time,
		AdSet.Field.end_time: end_time,
	})

	adset.remote_create(params={
		'status': AdSet.Status.paused,
	})
	adset = json.loads(str(adset).replace('<AdSet> ',''))
	return adset['id']