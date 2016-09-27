from facebookads.adobjects.adcreative import AdCreative
from facebookads.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebookads.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebookads.adobjects.adcreativelinkdatachildattachment import AdCreativeLinkDataChildAttachment
import header
import json
import psycopg2
import image_hash
import sys

def create_creative():
	con = None
	simple_list=[]
	times = int(raw_input("Please enter the number of cards for carousel ads.\n"))
	try:
		con = header.create_connection()
		cur = con.cursor()
		for i in xrange(times):
			design_id=raw_input("Please enter design id.\n")
			cur.execute('SELECT id,title,price from designs where id='+str(design_id))
			row=cur.fetchone()
			cur.execute('SELECT id,photo_file_name FROM images where design_id = '+str(design_id))
			rows=cur.fetchone()
			image_link=image_hash.get_image_link()
			product1 = AdCreativeLinkDataChildAttachment()
			product1[AdCreativeLinkDataChildAttachment.Field.link] = 'www.mirraw.com/d/'+str(row[0])
			product1[AdCreativeLinkDataChildAttachment.Field.name] = str(row[1])
			product1[AdCreativeLinkDataChildAttachment.Field.description] = row[2]
			product1[AdCreativeLinkDataChildAttachment.Field.image_hash] = image_hash.get_image_hash(image_link,rows[1])
			simple_list.append(product1)

	except psycopg2.DatabaseError, e:
		print 'Error %s' % e	
		sys.exit(1)

	finally:
		if con:
			con.close()
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