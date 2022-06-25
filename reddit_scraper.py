## Reddit Posts' Scraper
## Adapted from (https://github.com/ayaanzhaque/SDCNL/tree/main)


import requests
import time
import pandas as pd
from random import randint



# creating user agent
headers = {"User-agent" : "<REDDIT_USERNAME>"} # insert reddit username
test_url = "https://www.reddit.com/r/depression.json"

res = requests.get(test_url, headers=headers)
res.status_code


def reddit_scrape(url_string, number_of_scrapes, output_list):
	""" The Reddit data scraper function. It returns a list of scraped posts."""
	after = None 
	for i in range(number_of_scrapes):
		if i == 0:
		    print(f"Scraping {url_string}\n------------------------------------")
		    print("<<<Scraping In Progress...>>>") 
		    print(f"Downloading Batch {1} of {number_of_scrapes}...")
		elif (i+1) % 5 ==0:
		    print(f"Downloading Batch {(i + 1)} of {number_of_scrapes}...")
		
		if after == None:
		    params = {}
		else:
		    # Get next set after the Reddit 'after code'
		    params = {"after": after}             
		res = requests.get(url_string, params=params, headers=headers)
		if res.status_code == 200:
		    the_json = res.json()
		    output_list.extend(the_json["data"]["children"])
		    after = the_json["data"]["after"]
		else:
		    print(res.status_code)
		    break
		time.sleep(randint(1,6))

	print("<<<Scraping Process Complete...>>>")
	print(f"Number of posts downloaded: {len(output_list)}")
	print(f"Number of unique posts: {len(set([p['data']['name'] for p in output_list]))}")


def create_unique_list(original_scrape_list, new_list_name):
	"""Remove duplicate posts."""
	data_name_list=[]
	for i in range(len(original_scrape_list)):
		if original_scrape_list[i]["data"]["name"] not in data_name_list:
		    new_list_name.append(original_scrape_list[i]["data"])
		    data_name_list.append(original_scrape_list[i]["data"]["name"])
	#Check if data_name_list is same len as unique posts(new_list_name)
	print(f"Number of unique posts: {len(new_list_name)}")

# scraping suicide_watch data
suicide_data = []
reddit_scrape("https://www.reddit.com/r/SuicideWatch.json", 100, suicide_data)

suicide_data_unique = []
create_unique_list(suicide_data, suicide_data_unique)

# add suicide_watch to dataframe
suicide_watch = pd.DataFrame(suicide_data_unique)
suicide_watch["is_suicide"] = 1

# scraping suicide_watch data
depression_data = []
reddit_scrape("https://www.reddit.com/r/depression.json", 100, depression_data)

depression_data_unique = []
create_unique_list(depression_data, depression_data_unique)

# Create a suicide_watch data dataframe
depression = pd.DataFrame(depression_data_unique)
depression["is_suicide"] = 0

# writing the data to file (.csv)
suicide_watch.to_csv('suicide_watch.csv', index = False)
depression.to_csv('depression.csv', index = False)

# merging the data into one dataframe
depression = pd.read_csv('depression.csv')
suicide_watch = pd.read_csv('suicide_watch.csv')

dep_columns = depression[["title", "selftext", "author",  "num_comments", "is_suicide","url"]]
sui_columns = suicide_watch[["title", "selftext", "author",  "num_comments", "is_suicide","url"]]

combined_data = pd.concat([dep_columns, sui_columns], axis=0, ignore_index=True)  
combined_data["selftext"].fillna("emptypost",inplace=True)
combined_data.head()
combined_data.isnull().sum()

# saving combined CSV
combined_data.to_csv('data_3.csv', index=False)
