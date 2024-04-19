# Cody Krecicki's Choice Internet Brands 🚀
# Creator of Facebook Marketing API Sybil Suite 🐍
# https://github.com/krecicki
# https://twitter.com/krecicki

# Facebook Ads Sybil Suite
# Create massive influcene with automated ad creation, video creation and copy made by A.I. on Facebook.
# Create unlimited ads across unlimited pages, never the same exact ad twice: video or copy combo.
# Coming soon: Create unlimited sybil fan pages with human faces, profile photo, name, description all generated by A.I.
# Coming soon: Automated empty ad set creation so you don't need to copy and paste ad sets into the list.
# Coing soon: Use a list of multiple ad accounts instead of one single account.


#Whats it do?
# Using yarn.io GIFs and a MP4 with our phone number at the end of the ad
# takes entire folder of gifs and adds that video to the end of all of them
# These are then used as the new videos in a pre-made ad set(s).

###### BUGS & LOGIC #######
# Error Codes: https://developers.facebook.com/docs/marketing-api/error-reference/
# Ad Videos: https://developers.facebook.com/docs/marketing-api/reference/ad-account/advideos/
# Rate Limiting: https://developers.facebook.com/docs/marketing-apis/rate-limiting/
# Ad Creation Limits: https://www.facebook.com/business/help/766697140509126?id=561906377587030

# Facebook only allows 50 ads per ad set.
# Ad being copied need to be live and not in draft
# Rate limit throttle begins after about 100-120 API calls
# Facebook has an ad limit of 250 ads per page, make a new page to make more ads

# CREDIENTIALS & SETUP
 # Search this code and switch out the following varaibles to yours
 #   access_token = 'EAAccJV0RWjKhcBAK9etZCcf0egiqZC8K51UhZBagT8oKhUJ3P2IEEefdZC9WlvDFnxddN47IsDnEp39mPdUO9B3KSDeWbDgS6zYjHcJFEwOfz10P0AqCbXbxD1h3J1k8DuoJsndgNuZBTsVJD8i1BcCCgHnbvZCjAzaplOiGMvuQQ9a1VRtFKRxsOq2s3rjqJiEEg9XZBplzTTD8ygZDZD'
 #   ad_account_id = 'act_1252884403227360631'
 #   app_id = '6457330643529651815'

 #   thumb_url = 'https://scontent.flas1-2.fna.fbcdn.net/v/t39.3s0808-6/3632d96897_189575437435193_8242630814528158659_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=730e14&_nc_ohc=GyI7Kc_HuzAAX-YV1Sb&_nc_ht=scontent.flas1-2.fna&oh=00_AfDRwVJVRyjkeSxeqAIocZ905Qt3Kjj7o99Q8RZ_-E4t6w&oe=64C3DB8F'


# Look for the following code and add all of your ad set ids you've made manually
# List of ad sets and variations seperated by commas 6380441125855, 6380441125854, 6380441125855, etc.
#    ad_sets = [
#        6380713924255, 6380714974255, 6380714974455, 6380714973455, 
#        6380714974655, 6380714973655, 6380714974855, 6380714973855, 
#        6380714975055, 6380714974055
#    ]

# Look for this code and add any page ID's you want to post ads to, make sure you include their adsets
#    page_ids =[ # '105310649200654' # Cathy M. # Maxed 250 
#                # '101472119707829' # Lendara H. # Maxed 250
#                # '109680645544060' # Evelyn Wiseheart # Maxed 250
#                # '109801425531416' # Natalie Sinclair
#                # '102520676268397' # Grace Summers
#        102520676268397, 109801425531416
#    ]

# Run the script: python3 app.py

# Watch tons of ads be made.


# Import modules
import os
import subprocess
import random
import string
import time
import shutil
from moviepy.editor import VideoFileClip, concatenate_videoclips
from facebook_business.api import FacebookAdsApi, FacebookRequestError
from facebook_business.adobjects.advideo import AdVideo
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebook_business.adobjects.adcreativevideodata import AdCreativeVideoData

class VideoProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.call_clip_path = 'call.mp4'

    def convert_gif_to_mp4(self):
        os.makedirs(self.output_folder, exist_ok=True)

        for filename in os.listdir(self.input_folder):
            if filename.lower().endswith(".gif"):
                input_file = os.path.join(self.input_folder, filename)
                output_file = os.path.join(self.output_folder, os.path.splitext(filename)[0] + ".mp4")
                ffmpeg_cmd = f"ffmpeg -i {input_file} -vf \"scale=1280:720\" -y {output_file}"

                try:
                    subprocess.run(ffmpeg_cmd, shell=True, check=True)
                    print(f"Converted {input_file} to {output_file}")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to convert {input_file}: {e}")

    def concatenate_clips(self, video_clip_paths, method="compose"):
        os.makedirs(self.output_folder, exist_ok=True)
        done_folder = './combined_videos'  # New folder for the final concatenated videos
        os.makedirs(done_folder, exist_ok=True)  # Create the 'done' folder if it doesn't exist

        if not os.path.isfile(self.call_clip_path):
            raise FileNotFoundError("The 'call.mp4' file is missing.")
        call_clip = VideoFileClip(self.call_clip_path)

        for clip_path in video_clip_paths:
            clip = VideoFileClip(clip_path)

            if clip.duration > 0:
                final_clip = concatenate_videoclips([clip, call_clip], method=method)
            else:
                final_clip = clip

            random_filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
            output_path = os.path.join(done_folder, f"{random_filename}.mp4")  # Save in 'done' folder

            final_clip.write_videofile(output_path, codec='libx264')

            clip.close()
            final_clip.close()

        call_clip.close()

class FacebookAdsManager:
    def __init__(self, access_token, ad_account_id, app_id):
        self.access_token = access_token
        self.ad_account_id = ad_account_id
        self.app_id = app_id

    def init_api(self):
        FacebookAdsApi.init(access_token=self.access_token)

    def upload_video(self, video_path):
        self.init_api()
        new_video = AdVideo(parent_id=self.ad_account_id)
        new_video[AdVideo.Field.filepath] = video_path
        new_video.remote_create()
        return new_video['id']

    def create_unique_ad_name(self):
        return f"yarn{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}"

    def create_video_ad(self, video_filename, page_id, existing_ad_set_id, thumb_url, ad_text, ad_title):
        self.init_api()

        # Upload the video and get its video_id
        video_path = os.path.join('./combined_videos', video_filename)
        video_id = self.upload_video(video_path)

        # Create a random name for the ad creative
        ad_creative_name = self.create_unique_ad_name()
        
        # Create the ad creative using the video_id and the specified thumbnail URL
        video_data = {
            AdCreativeVideoData.Field.video_id: video_id,
            AdCreativeVideoData.Field.image_url: thumb_url,
            AdCreativeVideoData.Field.message: ad_text,
            AdCreativeVideoData.Field.title: ad_title
        }

        object_story_spec = {
            AdCreativeObjectStorySpec.Field.page_id: page_id,
            AdCreativeObjectStorySpec.Field.video_data: video_data
        }

        # Set the degrees_of_freedom_spec with standard_enhancements and enroll_status
        degrees_of_freedom_spec = {
            "creative_features_spec": {
                "standard_enhancements": {
                    "enroll_status": "OPT_OUT"
                }
            }
        }

        creative = AdCreative(parent_id=self.ad_account_id)
        creative[AdCreative.Field.name] = ad_creative_name
        creative[AdCreative.Field.object_story_spec] = object_story_spec
        creative[AdCreative.Field.degrees_of_freedom_spec] = degrees_of_freedom_spec  # Add this line
        creative.remote_create()

        # Get the creative ID
        ad_creative_id = creative.get_id()

        # Create the new ad using the existing ad_set_id and ad_creative_id
        fields = []
        params = {
            'name': ad_creative_name,
            'adset_id': existing_ad_set_id,
            'creative': {'creative_id': ad_creative_id},
            'status': 'ACTIVE',
        }

        # Create the ad
        new_ad = Ad(parent_id=self.ad_account_id)
        new_ad.remote_create(params=params)

        return new_ad
    
if __name__ == "__main__":
    input_folder = "./gif"
    output_folder = "./output"

    # Authentication
    access_token = 'EAAccJV0RWjKhcBAK9etZCcf0egiqZC8K51UhZBagT8oKhUJ3P2IEEefdZC9WlvDFnxddN47IsDnEp39mPdUO9B3KSDeWbDgS6zYjHcJFEwOfz10P0AqCbXbxD1h3J1k8DuoJsndgNuZBTsVJD8i1BcCCgHnbvZCjAzaplOiGMvuQQ9a1VRtFKRxsOq2s3rjqJiEEg9XZBplzTTD8ygZDZD'
    ad_account_id = 'act_1252884403227360631'
    app_id = '6457330643529651815'

    thumb_url = 'https://scontent.flas1-2.fna.fbcdn.net/v/t39.3s0808-6/3632d96897_189575437435193_8242630814528158659_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=730e14&_nc_ohc=GyI7Kc_HuzAAX-YV1Sb&_nc_ht=scontent.flas1-2.fna&oh=00_AfDRwVJVRyjkeSxeqAIocZ905Qt3Kjj7o99Q8RZ_-E4t6w&oe=64C3DB8F'


    # Process videos to begin 
    video_processor = VideoProcessor(input_folder, output_folder)

    # Convert GIFs to MP4s
    #video_processor.convert_gif_to_mp4()

    # Get the list of video files in the "./output" folder
    #video_files_in_output = [os.path.join('./output', f) for f in os.listdir('./output') if f.endswith('.mp4')]

    # Concatenate videos with the 'compose' method and save them in "./combined_videos" folder
    done_folder = './combined_videos'
    uploaded_videos = './uploaded_videos'
    #video_processor.concatenate_clips(video_files_in_output, method='compose')

    # Now, initialize the FacebookAdsManager and create new ads for each video in the "./combined_videos" folder
    facebook_ads_manager = FacebookAdsManager(access_token, ad_account_id, app_id)

    # List all video files in the 'done' folder
    video_files = os.listdir(done_folder)

    # List of ad sets and variations seperated by commas 6380441125855, 6380441125854, 6380441125855, etc.
    ad_sets = [
        6380713924255, 6380714974255, 6380714974455, 6380714973455, 
        6380714974655, 6380714973655, 6380714974855, 6380714973855, 
        6380714975055, 6380714974055
    ]

    page_ids =[ # '105310649200654' # Cathy M. # Maxed 250 
                # '101472119707829' # Lendara H. # Maxed 250
                # '109680645544060' # Evelyn Wiseheart # Maxed 250
                # '109801425531416' # Natalie Sinclair
                # '102520676268397' # Grace Summers
        102520676268397, 109801425531416
    ]

    ad_variations = [
        (  # Variation 1
            "Hey, stop paying credit cards now. \n\n Most money pays interest anyway. Great news! A retired debt collector found a solution. \n\n He had 1000s with the same problem. Until he met someone with ALL his credit card debt issues. \n\n One day at the bar, they discovered the root cause. The collector worked on a solution for everyone. \n\n He sent letters after studying SEC laws on debt protections. \n\n He discovered a letter to clear debts from credit scores and end creditor contact. A hotline started. \n\n Over 5,000,000 called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time offer: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 2
            "Attention: Stop paying credit cards now. \n\n Most money goes towards interest. Amazing news! A retired debt collector has the solution. \n\n He encountered the same issue with thousands. Until he met someone with ALL his credit card debt problems. \n\n One day at the bar, they discovered the root cause. The collector devised a solution for all. \n\n He sent letters after studying SEC laws on debt protections. \n\n He found a letter that clears debts from credit scores and stops creditor contact. A hotline was launched. \n\n Over 5,000,000 people called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 3
            "Don't pay credit cards now. \n\n Most money goes to interest payments anyway. Good news! A retired debt collector found the answer. \n\n He encountered the same issue with thousands. Until he met someone with ALL his credit card debt troubles. \n\n One day at the bar, they uncovered the root cause. The collector worked on a solution for everyone. \n\n He sent out letters after studying SEC laws on debt protections. \n\n He devised a letter that clears debts from credit scores and stops creditor contact. A hotline started. \n\n Over 5,000,000 called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time offer: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 4
            "Stop paying credit cards immediately. \n\n Most money goes to interest payments anyway. Fantastic news! A retired debt collector discovered a solution. \n\n He faced the same problem with thousands of others. Until he met someone with ALL the same credit card debt troubles. \n\n One day at the bar, they discovered the root cause. The collector developed a solution for everyone. \n\n He sent letters after studying SEC laws on debt protections. \n\n He found a letter that clears debts from credit scores and stops creditor contact. A hotline was launched. \n\n Over 5,000,000 people called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 5
            "Attention: Stop paying credit cards now. \n\n Most money goes towards interest. Great news! A retired debt collector has the solution. \n\n He had 1000s with the same problem. Until he met someone with ALL his credit card debt issues. \n\n One day at the bar, they discovered the root cause. The collector worked on a solution for everyone. \n\n He sent letters after studying SEC laws on debt protections. \n\n He discovered a letter to clear debts from credit scores and stops creditor contact. A hotline started. \n\n Over 5,000,000 called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time offer: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 6
            "Don't pay credit cards now. \n\n Most money goes to interest payments anyway. Good news! A retired debt collector found the answer. \n\n He faced the same issue with thousands. Until he met someone with ALL his credit card debt troubles. \n\n One day at the bar, they uncovered the root cause. The collector worked on a solution for everyone. \n\n He sent letters after studying SEC laws on debt protections. \n\n He devised a letter that clears debts from credit scores and stops creditor contact. A hotline started. \n\n Over 5,000,000 called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time offer: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 7
            "Hey, stop paying credit cards now. \n\n Most money pays interest anyway. Great news! A retired debt collector found a solution. \n\n He encountered the same issue with 1000s of others. Until he met someone with ALL the same credit card debt problems. \n\n One day at the bar, they discovered the root cause. The collector developed a solution for all. \n\n He sent letters after studying SEC laws on debt protections. \n\n He discovered a letter to clear debts from credit scores and end creditor contact. A hotline started. \n\n Over 5,000,000 people called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time offer: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 9
            "Stop paying credit card bills now. \n\n Most money goes to interest payments anyway. Fantastic news! A retired debt collector discovered the solution. \n\n He faced the same problem with thousands of others. Until he met someone with ALL the same credit card debt troubles. \n\n One day at the bar, they discovered the root cause. The collector developed a solution for all. \n\n He sent letters after studying SEC laws on debt protections. \n\n He found a letter that clears debts from credit scores and stops creditor contact. A hotline was launched. \n\n Over 5,000,000 people called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 10
            "Attention: Stop paying credit cards immediately. \n\n Most money goes towards interest. Amazing news! A retired debt collector has the solution. \n\n He had 1000s with the same problem. Until he met someone with ALL his credit card debt issues. \n\n One day at the bar, they discovered the root cause. The collector worked on a solution for everyone. \n\n He sent letters after studying SEC laws on debt protections. \n\n He discovered a letter to clear debts from credit scores and stops creditor contact. A hotline started. \n\n Over 5,000,000 called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time offer: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 11
            "Don't pay credit cards now. \n\n Most money pays interest anyway. Great news! A retired debt collector found the answer. \n\n He encountered the same issue with 1000s of others. Until he met someone with ALL the same credit card debt problems. \n\n One day at the bar, they discovered the root cause. The collector developed a solution for all. \n\n He sent letters after studying SEC laws on debt protections. \n\n He discovered a letter to clear debts from credit scores and end creditor contact. A hotline started. \n\n Over 5,000,000 people called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time offer: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 12
            "Hey, stop paying credit cards immediately. \n\n Most money goes to interest payments anyway. Fantastic news! A retired debt collector discovered a solution. \n\n He faced the same problem with thousands of others. Until he met someone with ALL the same credit card debt troubles. \n\n One day at the bar, they discovered the root cause. The collector developed a solution for everyone. \n\n He sent letters after studying SEC laws on debt protections. \n\n He found a letter that clears debts from credit scores and stops creditor contact. A hotline was launched. \n\n Over 5,000,000 people called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 13
            "Attention: Stop paying credit cards immediately. \n\n Most money goes to interest payments anyway. Amazing news! A retired debt collector has the solution. \n\n He encountered the same issue with 1000s of others. Until he met someone with ALL the same credit card debt problems. \n\n One day at the bar, they discovered the root cause. The collector developed a solution for all. \n\n He sent letters after studying SEC laws on debt protections. \n\n He found a letter to clear debts from credit scores and end creditor contact. A hotline started. \n\n Over 5,000,000 people called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time offer: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 14
            "Don't pay credit card bills now. \n\n Most money goes to interest payments anyway. Fantastic news! A retired debt collector discovered the solution. \n\n He faced the same problem with thousands of others. Until he met someone with ALL the same credit card debt troubles. \n\n One day at the bar, they discovered the root cause. The collector developed a solution for everyone. \n\n He sent letters after studying SEC laws on debt protections. \n\n He found a letter that clears debts from credit scores and stops creditor contact. A hotline was launched. \n\n Over 5,000,000 people called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 15
            "Attention: Stop paying credit cards immediately. \n\n Most money pays interest anyway. Great news! A retired debt collector found the answer. \n\n He encountered the same issue with 1000s of others. Until he met someone with ALL the same credit card debt problems. \n\n One day at the bar, they discovered the root cause. The collector developed a solution for all. \n\n He sent letters after studying SEC laws on debt protections. \n\n He discovered a letter to clear debts from credit scores and end creditor contact. A hotline started. \n\n Over 5,000,000 people called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time offer: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 16
            "Hey, stop paying credit cards immediately. \n\n Most money goes towards interest. Amazing news! A retired debt collector has the solution. \n\n He had 1000s with the same problem. Until he met someone with ALL his credit card debt issues. \n\n One day at the bar, they discovered the root cause. The collector devised a solution for all. \n\n He sent letters after studying SEC laws on debt protections. \n\n He found a letter that clears debts from credit scores and stops creditor contact. A hotline was launched. \n\n Over 5,000,000 called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time offer: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        ),
        (  # Variation 17
            "Don't pay credit card bills now. \n\n Most money goes towards interest. Great news! A retired debt collector discovered the answer. \n\n He encountered the same issue with 1000s of others. Until he met someone with ALL the same credit card debt problems. \n\n One day at the bar, they discovered the root cause. The collector developed a solution for all. \n\n He sent letters after studying SEC laws on debt protections. \n\n He discovered a letter to clear debts from credit scores and end creditor contact. A hotline started. \n\n Over 5,000,000 people called (833) 294-4579 for help with $5000 to $10000+ debt. Limited time offer: almost free. \n\n We send the letter now, pay later or never pay.",
            "Stop Paying, Call Us",
            "We'll Send a Letter."
        )
    ]

    # Initialize counters
    ad_set_index = 0
    variation_index = 0
    page_id_index = 0
    iteration_count = 0

    # Initializations before the loop
    ad_text = ad_variations[0][0]   # Set to the first variation of ad text
    ad_title = ad_variations[0][1]  # Set to the first variation of ad title
    ad_desc = ad_variations[0][2]   # Set to the first variation of ad description


    # Create a new ad for each .mp4 in the ./upload folder
    for video_file in video_files:
        new_ad = facebook_ads_manager.create_video_ad(video_file, page_ids[page_id_index], ad_sets[ad_set_index], thumb_url, ad_text, ad_title)
        print(f"Created new ad for video {video_file} in ad set {ad_sets[ad_set_index]}: {new_ad}")

        # Move the file to the "./done_uploaded" folder
        done_video_path = os.path.join(done_folder, video_file)
        uploaded_video_path = os.path.join(uploaded_videos, video_file)

        shutil.move(done_video_path, uploaded_video_path)
        print(f"Moved uploaded video {video_file} to the uploaded_videos folder.")

        # Sleep for a bit to beat the rate limit
        time.sleep(60)

        # Update the variation_index to get the next variation for the ad text, title, and description
        variation_index = (variation_index + 1) % len(ad_variations)
        ad_text = ad_variations[variation_index][0]
        ad_title = ad_variations[variation_index][1]
        ad_desc = ad_variations[variation_index][2]

        # Update the ad_set_index every 50 iterations if you still want to change ad sets (optional)
        iteration_count += 1
        if iteration_count % 50 == 0:
            ad_set_index = (ad_set_index + 1) % len(ad_sets)

        # Update the page_id_index every 250 iterations
        if iteration_count % 250 == 0:
            page_id_index = (page_id_index + 1) % len(page_ids)