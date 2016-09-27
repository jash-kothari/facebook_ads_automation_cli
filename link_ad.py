from facebookads.adobjects.adcreative import AdCreative
from facebookads.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebookads.adobjects.adimage import AdImage
from facebookads.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
import header
import json
import create_adset
import psycopg2
import image_hash

con = None
try:
	con = header.create_connection()
	cur = con.cursor()
	design_id=raw_input("Please enter design id.\n")
	cur.execute('SELECT id,title,price from designs where id='+str(design_id))
	row=cur.fetchone()
	cur.execute('SELECT id,photo_file_name FROM images where design_id = '+str(design_id))
	rows=cur.fetchone()
	image_link=image_hash.get_image_link(rows[1],rows[0])

except psycopg2.DatabaseError, e:
	print 'Error %s' % e	
	sys.exit(1)

finally:
	if con:
		con.close()
caption = raw_input("Please enter caption for the ad")

link_data = AdCreativeLinkData()
link_data[AdCreativeLinkData.Field.message] = 'try it out'
link_data[AdCreativeLinkData.Field.link] = 'www.mirraw.com'
link_data[AdCreativeLinkData.Field.caption] = caption
link_data[AdCreativeLinkData.Field.image_hash] = image_hash.get_image_hash(image_link,rows[1])
object_story_spec = AdCreativeObjectStorySpec()
object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = header.page_id
object_story_spec[AdCreativeObjectStorySpec.Field.link_data] = link_data

creative = AdCreative(parent_id=header.my_account['id'])
creative[AdCreative.Field.name] = 'AdCreative for Link Ad'
creative[AdCreative.Field.object_story_spec] = object_story_spec
creative.remote_create()
creative=json.loads(str(creative).replace('<AdCreative> ',''))
print(creative)