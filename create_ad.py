from facebookads.adobjects.ad import Ad
import header
import link_ad as created_ad

ad = Ad(parent_id=header.my_account['id'])
ad[Ad.Field.name] = 'My Ad'
ad[Ad.Field.adset_id] = created_ad.create_adset.adset['id']
ad[Ad.Field.creative] = {
    'creative_id': link_ad.creative['id'],
}
ad.remote_create(params={
    'status': Ad.Status.paused,
})