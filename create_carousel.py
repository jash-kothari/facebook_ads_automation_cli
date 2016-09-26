from facebookads.adobjects.adcreativelinkdatachildattachment import AdCreativeLinkDataChildAttachment
from facebookads.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebookads.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebookads.adobjects.adcreative import AdCreative
from facebookads.adobjects.campaign import Campaign
from facebookads.objects import Ad
from facebookads import exceptions
from datetime import date
from time import sleep
import header
import json
import psycopg2
import psycopg2.extras
import image_hash
import sys
import urlparse
import logging

def create_carousel_ad(caption,adset_id,ad_name,design_list,land_on_design,url,campaign_tag):
	FORMAT = '%(asctime)-15s %(message)s %(pathname)s'
	logging.basicConfig(filename='%s-facebook-automated.log' % date.today(),format=FORMAT, level=logging.DEBUG)
	logging.info('In create carousel')
	connection = None
	simple_list=[]
	utm_medium='fb-acpm'
	try:
		urlparse.uses_netloc.append("postgres")
		database_url = urlparse.urlparse(header.database_url)
		connection = psycopg2.connect( database=database_url.path[1:], user=database_url.username, password=database_url.password, host=database_url.hostname, port=database_url.port )
		cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
		for design_id in design_list:
			cursor.execute('SELECT discount_percent,designer_id from designs where id='+str(design_id[0]))
			row=cursor.fetchone()
			cursor.execute('SELECT id,photo_file_name FROM images where design_id = '+str(design_id[0]))
			rows=cursor.fetchone()
			cursor.execute('SELECT name FROM "categories" INNER JOIN "categories_designs" ON "categories"."id" = "categories_designs"."category_id" WHERE design_id ='+str(design_id[0]))
			category_name = cursor.fetchone()
			image_link=""
			if 'jpg' in rows['photo_file_name']:
				image_link = 'https://assets1.mirraw.com/images/'+str(rows['id'])+'/'+rows['photo_file_name'].replace('.jpg','')+'_large.jpg' 
			elif 'tif' in rows['photo_file_name']:
				image_link = 'https://assets1.mirraw.com/images/'+str(rows['id'])+'/'+rows['photo_file_name'].replace('.tif','')+'_large.tif' 
			elif 'gif' in rows['photo_file_name']:
				image_link = 'https://assets1.mirraw.com/images/'+str(rows['id'])+'/'+rows['photo_file_name'].replace('.gif','')+'_large.gif' 
			elif 'bmp' in rows['photo_file_name']:
				image_link = 'https://assets1.mirraw.com/images/'+str(rows['id'])+'/'+rows['photo_file_name'].replace('.bmp','')+'_large.bmp' 
			elif 'png' in rows['photo_file_name']:
				image_link = 'https://assets1.mirraw.com/images/'+str(rows['id'])+'/'+rows['photo_file_name'].replace('.png','')+'_large.png' 
			if row['discount_percent'] is None:
				row['discount_percent']=0
			product1 = AdCreativeLinkDataChildAttachment()
			if land_on_design:
				product1[AdCreativeLinkDataChildAttachment.Field.link] = 'www.mirraw.com/designers/'+str(row['designer_id'])+'/designs/'+str(design_id[0])+'?utm_source=facebook-auto&utm_medium='+utm_medium+'&utm_campaign='+campaign_tag
			else:
				product1[AdCreativeLinkDataChildAttachment.Field.link] = url+'?'+str(design_id)+'&utm_source=facebook&utm_medium='+utm_medium+'&utm_campaign='+campaign_tag
			product1[AdCreativeLinkDataChildAttachment.Field.name] = category_name['name']
			product1[AdCreativeLinkDataChildAttachment.Field.description] = 'Discount '+str(row['discount_percent'])+'%'
			logging.info(image_link)
			logging.info(rows['photo_file_name'])
			product1[AdCreativeLinkDataChildAttachment.Field.image_hash] = image_hash.get_image_hash(image_link,rows['photo_file_name'])
			sleep(0.5)
			simple_list.append(product1)

		link = AdCreativeLinkData()
		link[link.Field.link] = 'www.mirraw.com'
		link[link.Field.child_attachments] = simple_list
		link[link.Field.caption] = caption

		story = AdCreativeObjectStorySpec()
		story[story.Field.page_id] = header.page_id
		story[story.Field.link_data] = link

		creative = AdCreative(parent_id=header.my_account['id'])
		creative[AdCreative.Field.name] = 'MPA Creative'
		creative[AdCreative.Field.object_story_spec] = story
		creative.remote_create()
		creative=json.loads(str(creative).replace('<AdCreative> ',''))

		ad = Ad(parent_id=header.my_account['id'])
		ad[Ad.Field.name] = ad_name
		ad[Ad.Field.adset_id] = adset_id
		ad[Ad.Field.status] = Campaign.Status.paused
		ad[Ad.Field.creative] = {'creative_id': str(creative['id'])}
		print 'Creating Ad'
		logging.info('Creating Ad')
		ad.remote_create()
		print ad
		logging.info

	except psycopg2.DatabaseError, e:
		print 'Error %s' % e
		logging.error('Error %s' % e)
		return False

	except StandardError, e:
		print 'Error %s' % e
		logging.error('Error %s' % e)
		return False
	
	except exceptions.FacebookError, e:
		print 'Error %s' % e
		logging.error('Error %s' % e)
		return False

	finally:
		if connection:
			connection.close()
	
	sleep(60)
	return True