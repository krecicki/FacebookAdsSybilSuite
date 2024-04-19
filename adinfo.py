from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.campaign import Campaign

# Replace these with your access token and ad account ID
access_token = 'EAAJV0RWjKhcBAK9etZCf0egiqZC8K51UhZBagT8oKhUJ3P2IEEfdZC9WlvDFnxdN47IsDnEp39mPdUO9B3KSDeWbDgS6zYjHcJFEwOfz10P0AqCbXbxD1h3J1k8DuoJsndgNuZBTsVJD8i1BcCCgHnbvZCjAzaplOiGMvuQQ9a1VRtFKRxsOq2s3rjqJiEEg9XZBplzTTD8ygZDZD'
ad_account_id = 'act_1528844027360631'

# Initialize the FacebookAdsApi with your access token
FacebookAdsApi.init(access_token=access_token)

# Replace 'EXISTING_AD_ID' with the ID of the ad you want to replicate
existing_ad_id = '6375801652055'

# Get the existing ad details
existing_ad = Ad(existing_ad_id)

# Retrieve the corresponding campaign ID
campaign_id = existing_ad.get_campaign().get_id()

# Fetch the campaign with its fields
campaign = Campaign(campaign_id)
campaign.remote_read(fields=[Campaign.Field.objective])

# Print the objective of the existing ad's campaign
print("Ad Objective:", campaign[Ad.Field.objective])