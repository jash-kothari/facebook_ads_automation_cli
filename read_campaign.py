from facebookads.adobjects.campaign import Campaign
import urlparse
import psycopg2
import psycopg2.extras
import sys
import header
import os
import commentjson as json
import create_carousel as carousel
import adset
import random

campaign_id = raw_input('Enter campaign ID\n')
campaign = Campaign(campaign_id)
campaign.remote_read(fields=[Campaign.Field.name,Campaign.Field.id])
countries = campaign[Campaign.Field.name].split(',')

try:
	urlparse.uses_netloc.append("postgres")
	database_url = urlparse.urlparse(header.database_url)
	conn = psycopg2.connect( database=database_url.path[1:], user=database_url.username, password=database_url.password, host=database_url.hostname, port=database_url.port)
	curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	file = json.loads(open('config.json').read())
	print file
	sys.exit(1)
	categories = file['categories'].split(',')
	number_of_ads = int(file['number_of_ads'])
	number_of_items = int(file['number_of_items'])
	interest_list = file['interest_list'].split(',')
	age_min = int(file['age_min'])
	age_max = int(file['age_max'])
	# print categories,number_of_items,number_of_ads
	number_of_cards = int(file['number_of_cards'])
	for country in countries:
		for name in categories:
			for interests in interest_list:
				adset_name=interests+'-'+name
				adset_id=create_adset(country,interests,age_min,age_max,adset_name,campaign_id,daily_budget,bid_amount,start_time,end_time)
				curr.execute("SELECT l.design_id FROM line_items l,categories_designs cd,categories c WHERE cd.design_id=l.design_id AND c.id=cd.category_id AND l.created_at > current_date - interval '90' day and c.name =" + name + "GROUP BY l.design_id,c.name ORDER BY count(l.id) DESC LIMIT "+number_of_items)
				rows=curr.fetchall()
				number_of_items = max(number_of_items,len(rows))
				if number_of_items%number_of_cards!=0:
					number_of_items-=(number_of_items%number_of_cards)
				remaining=number_of_ads
				while remaining > 0:
					remaining=check_number_of_ads(number_of_items,number_of_cards,remaining,adset_id)
					random.shuffle(rows)
except psycopg2.DatabaseError, e:
	print 'Error %s' % e

except exceptions.FacebookError, e:
	print 'Error %s' % e

finally:
	if conn:
		conn.close()

def check_number_of_ads(number_of_items,number_of_cards,number_of_ads,adset_id):
	if number_of_ads > (number_of_items/number_of_cards):
		serialized_ads_creation(adset_id,rows,(number_of_items/number_of_cards),number_of_cards)
		number_of_ads -= (number_of_items/number_of_cards)
		return number_of_ads
	else :
		serialized_ads_creation(rows,(number_of_items/number_of_cards),number_of_cards)
		return 0

def serialized_ads_creation(adset_id,rows,number_of_ads,number_of_cards):
	j=0
	k=number_of_cards
	for i in xrange(number_of_ads):
		design_list=rows[j:k]
		carousel.create_carousel_ad(caption,adset_id,ad_name,design_list,account_id,land_on_design,url,campaign_tag)
		j=k
		k+=number_of_cards
	return True;