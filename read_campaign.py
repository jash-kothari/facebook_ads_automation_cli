from facebookads.adobjects.campaign import Campaign
from facebookads import exceptions
from datetime import date
import create_carousel as carousel
import commentjson as json
import psycopg2.extras
import urlparse
import psycopg2
import logging
import random
import header
import adset
import sys
import os

def check_number_of_ads(number_of_items,number_of_cards,number_of_ads,adset_id,caption):
	logging.info('In check number of ads')
	if number_of_ads > (number_of_items/number_of_cards):
		serialized_ads_creation(adset_id,rows,(number_of_items/number_of_cards),number_of_cards,caption)
		number_of_ads -= (number_of_items/number_of_cards)
		return number_of_ads
	else :
		serialized_ads_creation(adset_id,rows,(number_of_items/number_of_cards),number_of_cards,caption)
		return 0

def serialized_ads_creation(adset_id,rows,number_of_ads,number_of_cards,caption):
	j=0
	k=number_of_cards
	logging.info('In serialized ads creation')
	for i in xrange(number_of_ads):
		design_list = rows[j:k]
		ad_name = caption+' top items '+str(j)+'-'+str(k)
		ad_created = carousel.create_carousel_ad(caption,adset_id,ad_name,design_list,True,'',caption+'_'+str(i))
		if not(ad_created):
			logging.error('Error creating ad for design ids %s' % design_list)
		else:
			logging.info('Ad created successfully for design ids %s' % design_list)
		j = k
		k += number_of_cards
	return True;

connection1 = None
try:
	FORMAT = '%(asctime)-15s %(message)s %(pathname)s'
	logging.basicConfig(filename='%s-facebook-automated.log' % date.today(),format=FORMAT, level=logging.DEBUG)
	# Reading from config.json
	file = json.loads(open('config.json').read())

	campaign_id = file['campaign_id']
	categories = file['categories'].split(',')
	number_of_ads = int(file['number_of_ads'])
	number_of_items = int(file['number_of_items'])
	number_of_cards = int(file['number_of_cards'])
	interest_list = file['interest_list'].split(',')
	age_min = int(file['age_min'])
	age_max = int(file['age_max'])
	daily_budget = file['daily_budget']
	bid_amount = file['bid_amount']
	start_time = file['start_time']
	end_time = file['end_time']

	campaign = Campaign(campaign_id)
	campaign.remote_read(fields=[Campaign.Field.name,Campaign.Field.id])
	countries = campaign[Campaign.Field.name].split(',')

	urlparse.uses_netloc.append("postgres")
	database_url = urlparse.urlparse(header.database_url)
	connection1 = psycopg2.connect( database=database_url.path[1:], user=database_url.username, password=database_url.password, host=database_url.hostname, port=database_url.port)
	dbCursor = connection1.cursor(cursor_factory=psycopg2.extras.DictCursor)

	for country in countries:
		for name in categories:
			for interests in interest_list:
				adset_name = interests+'-'+name
				adset_id = adset.create_adset(country,interests,age_min,age_max,adset_name,campaign_id,daily_budget,bid_amount,start_time,end_time)
				dbCursor.execute("SELECT l.design_id FROM line_items l,categories_designs cd,categories c WHERE cd.design_id=l.design_id AND c.id=cd.category_id AND l.created_at > current_date - interval '90' day and c.name like '" + name + "' GROUP BY l.design_id,c.name ORDER BY count(l.id) DESC LIMIT "+str(number_of_items))
				rows=dbCursor.fetchall()
				number_of_items = max(number_of_items,len(rows))
				if number_of_items%number_of_cards!=0:
					number_of_items -= (number_of_items%number_of_cards)
				remaining = number_of_ads
				while remaining > 0:
					remaining=check_number_of_ads(number_of_items,number_of_cards,remaining,adset_id,name)
					random.shuffle(rows)
			sleep(30)
		sleep(30)

except psycopg2.DatabaseError, e:
	logging.error('Error %s' % e)
	print 'Error %s' % e

except exceptions.FacebookError, e:
	logging.error('Error %s' % e)
	print 'Error %s' % e

except StandardError, e:
	logging.error('Error %s' % e)
	print 'Error %s' % e

finally:
	if connection1:
		connection1.close()