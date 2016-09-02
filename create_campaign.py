from facebookads.adobjects.campaign import Campaign
import header
import json

def create_campaign():
	campaign_name=raw_input("Please enter campaign name.\n")
	campaign = Campaign(parent_id=header.my_account['id'])
	campaign.update({
		Campaign.Field.name: campaign_name,
		Campaign.Field.objective: Campaign.Objective.link_clicks,
	})

	campaign.remote_create(params={
		'status': Campaign.Status.paused,
	})
	campaign=str(campaign)
	campaign=campaign.replace('<Campaign> ','')
	campaign=json.loads(campaign)
	return campaign['id']
