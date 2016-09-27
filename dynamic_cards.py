from facebookads.adobjects.adcreative import AdCreative
from facebookads.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebookads.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebookads.adobjects.adcreativelinkdatachildattachment import AdCreativeLinkDataChildAttachment
import header
import json
import image_hash
import sys
import urlparse
import psycopg2
import psycopg2.extras

def create_creative():
	con = None
	simple_list=[]
	times = int(raw_input("Please enter the number of cards for carousel ads.\n"))
	try:
		urlparse.uses_netloc.append("postgres")
		database_url = urlparse.urlparse(header.database_url)
		conn = psycopg2.connect( database=database_url.path[1:], user=database_url.username, password=database_url.password, host=database_url.hostname, port=database_url.port )
		cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		for i in xrange(times):
			design_id=raw_input("Please enter design id.\n")
			cur.execute('SELECT id,title,price from designs where id='+str(design_id))
			row=cur.fetchone()
			cur.execute('SELECT id,photo_file_name FROM images where design_id = '+str(design_id))
			rows=cur.fetchone()
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

			product1 = AdCreativeLinkDataChildAttachment()
			product1[AdCreativeLinkDataChildAttachment.Field.link] = 'www.mirraw.com/d/'+str(row['id'])
			product1[AdCreativeLinkDataChildAttachment.Field.name] = str(row['title'])
			product1[AdCreativeLinkDataChildAttachment.Field.description] = row['price']
			product1[AdCreativeLinkDataChildAttachment.Field.image_hash] = image_hash.get_image_hash(image_link,rows['photo_file_name'])
			simple_list.append(product1)

	except psycopg2.DatabaseError, e:
		print 'Error %s' % e	
		sys.exit(1)

	finally:
		if conn:
			conn.close()
	caption=raw_input("Please enter a caption for the Ad.\n")
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
	print(creative)
	print creative['creative_id']
	print creative['success']