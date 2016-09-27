from facebookads.adobjects.adimage import AdImage
import header
import urllib
import os
def get_image_hash(url,name):
	urllib.urlretrieve(url,name)
	image = AdImage(parent_id=header.my_account['id'])
	image[AdImage.Field.filename] = name
	image.remote_create()
	os.remove(name)
	# Output image Hash
	return image[AdImage.Field.hash]

def get_image_link(name,image_id):
	image_link=""
	extensions=['jpg','tif','gif','bmp','png']
	for extension in extensions:
		if extension in name:
			image_link = header.base_url+str(image_id)+'/'+name.replace('.'+extension,'') + header.size+'.'+extension 
	return image_link