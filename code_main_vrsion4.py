import json
import os
from bs4 import BeautifulSoup
import pandas as pd
import requests

base_url = 'https://github.com'



def get_topic_description(doc): #done
    # topic_description
    desc_selector = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p', {'class': desc_selector})
    # topic_descripton
    topic_descs = []
    for tag in topic_desc_tags:
        topic_descs.append(tag.text.strip())
    return topic_descs


def get_topic_urls(doc): #done
    # topic_anchor tags
    topic_link_tags = doc.find_all('a', {'class': 'd-flex no-underline'})
    # topic_url
    topic_urls = []
    for tag in topic_link_tags:
        topic_urls.append(base_url + tag['href'])
    return topic_urls

def scrape_topics(): #return dataframe of topics
    #create folder
    os.makedirs('./Data/Topic',exist_ok=True)
    topic_url='https://github.com/topics'
    response=requests.get('https://github.com/topics')
    if response.status_code!=200:
        raise Exception("Unable to get the required page :error downloading {}".format(topic_url))
    page_content=response.text
    doc=BeautifulSoup(page_content,'lxml')
    selection_class='f3 lh-condensed mb-0 mt-1 Link--primary'
    # creating csv files
    topics_dict = {'Title':get_topic_title(doc), 'Description':get_topic_description(doc), 'Url':get_topic_urls(doc)}
    topics_df = pd.DataFrame(topics_dict)
    topics_df.to_csv('./Data/Topic/Topics.csv', index=None)  # file created
    print('./Data/Topic/Topics.csv file generated.')
    return topics_df

########################################################################################################################
#converting stars to int
def parse_star_count(stars_str):
    stars_str=stars_str.strip()
    if stars_str[-1]=='k':
        return int(float(stars_str[:-1])*1000)
    else:
        int(stars_str)

def get_topic_page(topic_url): #the page contain the topics(topics has to be extracted)
    # downloading the page
    response = requests.get(topic_url)
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    topic_doc = BeautifulSoup(response.text, 'lxml')
    return topic_doc

def get_topic_title(doc): #topics return
    #topis names inside these tags with class..
    selection_class='f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags=doc.find_all('p',{'class':selection_class})
    # inside topic_title_tags
    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    return topic_titles

#info about this topic repo
def get_repo_info(h3_tag,star_tag): #return (username,repo_name,stars,repo_url)
    #return all required info about the repo
    a_tags=h3_tag.find_all('a')
    username=a_tags[0].text.strip()
    repo_name=a_tags[1].text.strip()
    repo_url=base_url+a_tags[1]['href']
    stars=parse_star_count(star_tag.text.strip())
    return username,repo_name,stars,repo_url

def get_topic_repos(topic_doc):
    h3_selection_class = 'f3 color-fg-muted text-normal lh-condensed'
    repo_tags = topic_doc.find_all('h3', {'class': h3_selection_class})
    start_tags = topic_doc.find_all('a', {'class': 'social-count js-social-count'})
    #create csv
    topic_repos_dict = {'Username': [], 'Repo_name': [], 'Stars': [], 'Repo_Url': []}

    for i in range(len(repo_tags)):
        repo_info = get_repo_info(repo_tags[i], start_tags[i])
        topic_repos_dict['Username'].append(repo_info[0])
        topic_repos_dict['Repo_name'].append(repo_info[1])
        topic_repos_dict['Stars'].append(repo_info[2])
        topic_repos_dict['Repo_Url'].append(repo_info[3])
    topic_repos_df=pd.DataFrame(topic_repos_dict)
    return topic_repos_df

#now call and save
def scrape_topic(topic_url,path):
    if os.path.exists(path):
        print('The file {0} already exist.Skipping...'.format(path))
        return
    else:
        topic_df=get_topic_repos(get_topic_page(topic_url))
        topic_df.to_csv(path,index=None)
        print(path+' generated')
########################################################################################################################



def scrape_topics_repos():
    #create folder
    os.makedirs('./data',exist_ok=True)
    topics_df=scrape_topics()
    for index,row in topics_df.iterrows():
        scrape_topic(row['Url'],'./Data/{}.csv'.format(row['Title']))

