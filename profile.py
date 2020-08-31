from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
from pipeline import RabbitMQ


def extract_educations(link, driver):
    driver.get(link)
    page_text = (driver.page_source).encode('utf-8')
    soup = BeautifulSoup(page_text,features="lxml")
    educationTages = soup.find(id='pagelet_eduwork').find_all('ul')[1].find_all('li')
    education_list = []
    for educationTage in educationTages:
        divDataTag = educationTage.find('div').find('div').find('div')
        
        if divDataTag is None :
            print("education_list : ", education_list)
            return education_list
        
        divDataTag = divDataTag.find('div').find_all('div')[1]
        aTag = divDataTag.find('a')
        education_list.append(
            {
                'link' : aTag.get('href'),
                'name' : aTag.getText(),
                'location' : divDataTag.find_all('div')[1].find('div').getText() 
            })
    print("education_list : ", education_list)
    return education_list

def extract_works(link, driver):
    driver.get(link)
    page_text = (driver.page_source).encode('utf-8')
    soup = BeautifulSoup(page_text,features="lxml")
    workTages = soup.find(id='pagelet_eduwork').find_all('ul')[0].find_all('li')
    work_list = []
    for workTage in workTages:
        divDataTag = workTage.find('div').find('div').find('div')

        if divDataTag is None :
            print("work_list : ", work_list)
            return work_list
        
        divDataTag = divDataTag.find('div').find_all('div')[1]

        aTag = divDataTag.find('a')
        work_list.append(
            {
                'link' : aTag.get('href'),
                'name' : aTag.getText(),
                'date' : divDataTag.find_all('div')[1].find('div').getText() if len(divDataTag.find_all('div')) > 1 else None
            })
    print("work_list : ", work_list)
    return work_list


def extract_livingPlaces(link, driver):
    driver.get(link)
    page_text = (driver.page_source).encode('utf-8')
    soup = BeautifulSoup(page_text,features="lxml")
    livingPlace_list = [] 
    livingPlacesTage = soup.find(id='pagelet_hometown').find('ul').find_all('li')
    for livingPlaceTage in livingPlacesTage:
        divTag = livingPlaceTage.find('div').find('div').find('div')
        
        if divTag is None:
            print("livingPlace_list : ", livingPlace_list)
            return livingPlace_list

        divTag = divTag.find('div').find('div').find_all('div')[1]
        aTag = divTag.find('span').find('a')
        livingPlace_list.append(
            {
                'link' : aTag.get('href'),
                'name' : aTag.getText(),
                'type' : divTag.find('div').getText()
            })
    print("livingPlace_list : ", livingPlace_list)
    return livingPlace_list

def extrct_contacts_basicInfo(link, driver, name):
    driver.get(link)
    page_text = (driver.page_source).encode('utf-8')
    soup = BeautifulSoup(page_text,features="lxml")
    info_list =[]
    info_tages = soup.find(id='pagelet_' + name).find('ul').find_all('li')
    for info_tag in info_tages:
        divTage = info_tag.find('div')
        
        if divTage is None:
            print("info_list : ", info_list)
            return info_list
        
        info_list.append(
            {
                divTage.find_all('div')[0].find('span').getText() : divTage.find_all('div')[1].find('span').getText(),
            })
    print("info_list : ", info_list)
    return info_list

def extract_families(link, driver):
    driver.get(link)
    page_text = (driver.page_source).encode('utf-8')
    soup = BeautifulSoup(page_text,features="lxml")
    family_list = []
    families_tage = soup.find(id = 'pagelet_relationships').find('ul').find_all('li')
    for familie_tage in families_tage:
        divTag = familie_tage.find('div').find('div').find('div')
        
        if divTag is None:
            print("family_list : ", family_list)
            return family_list
        
        divTag = divTag.find('div').find('div').find_all('div')[1]
        hoverCard = divTag.find('a').get('data-hovercard')
        userId = hoverCard[hoverCard.find('id')+3:]
        userId = userId[:userId.find('&')]
        family_list.append(
            {
                'name' : divTag.find('a').getText(),
                'link' : divTag.find('a').get('href'),
                'relation' : divTag.find_all('div')[1].getText(),
                'userId' : userId
            })
    print("family_list : ", family_list)
    return family_list

def extract_events(link, driver):
    driver.get(link)
    page_text = (driver.page_source).encode('utf-8')
    soup = BeautifulSoup(page_text,features="lxml")
    event_list = []
    events_tage = soup.find(id='pagelet_timeline_medley_about').find_all('div')[3].find('div').find_all('li')[1].find_all('li')
    for event_tage in events_tage:
        event_list.append(
            {
                'date' : event_tage.find('span').getText(),
                'event' : event_tage.find('a').find('span').getText()
            })
    print("event_list : ", event_list)
    return event_list

def profile_crawler(userURL, email, password):
    #userURL = "https://www.facebook.com/profile.php?id=" + userId

    driver = webdriver.Firefox()
    driver.get(userURL)
    inputEmail = driver.find_element_by_id("email")
    inputEmail.send_keys(email)
    inputPass = driver.find_element_by_id("pass")
    inputPass.send_keys(password)
    inputPass.submit()
    time.sleep(25)
    page_text = (driver.page_source).encode('utf-8')
    soup = BeautifulSoup(page_text,features="lxml")

    imgTages = soup.find_all('img')
    coverImage = imgTages[1].get('src')
    print("coverImage : ", coverImage)

    avatar = imgTages[3].get('src')
    print("avatar : ", avatar)

    avatarCaption = imgTages[3].get('alt')
    finishingNameIndex = imgTages[3].get('alt').find('\'s')
    name = avatarCaption[:finishingNameIndex]
    print("name : ", name)

    aTages =soup.find_all('a')
    filterFriends = str(aTages).find(userURL + '&amp;sk=friends">')
    startingFriendsCount = str(aTages)[filterFriends:].find('>')
    FinishingFriendsCount = str(aTages)[filterFriends:].find('</a>')
    friendsCount = str(aTages)[filterFriends:][startingFriendsCount+1:FinishingFriendsCount]
    print("friendsCount : ", friendsCount)

    joinedDateStr = soup.find(id='intro_container_id').find('div').find('div').find('ul').find('li').find('div').find('div').find('div').find('div').getText()
    joinedDate = joinedDateStr[7:]
    print("joinedDate : ", joinedDate)

    timeLineLink = soup.find(id='fbTimelineHeadline').find('ul').find('li').find('a').get('href')
    aboutLink = timeLineLink.replace('timeline','about')
    #aboutLinkOverview = aboutLink + '&section=overview'
    aboutLinkEducation = aboutLink + '&section=education'
    aboutLinkLiving = aboutLink + '&section=living'
    aboutLinkContact = aboutLink + '&section=contact-info'
    aboutLinkEvent = aboutLink + '&section=year-overviews'
    
    aboutLinkRelationship = aboutLink + '&section=relationship'
    driver.get(aboutLinkRelationship)
    page_text = (driver.page_source).encode('utf-8')
    soup = BeautifulSoup(page_text,features="lxml")
    relationship = soup.find(id = 'pagelet_relationships').find('li').getText()
    print("relationship : ", relationship)

    aboutLinkBio = aboutLink + '&section=bio'
    driver.get(aboutLinkBio)
    page_text = (driver.page_source).encode('utf-8')
    soup = BeautifulSoup(page_text,features="lxml")
    about = soup.find(id='pagelet_bio').find('ul').getText()
    print("about : ", about)
    
    quote_list = []
    for quoteTage in soup.find(id='pagelet_quotes').find_all('li'):
        quote_list.append(quoteTage.getText())
    print("quote_list : ", quote_list)
    
    nickNames = soup.find(id='pagelet_nicknames').getText()
    print("nickNames : ", nickNames)

    profileObj = {
        'name' : name,
        'avatar' : avatar,
        'coverImage' : coverImage,
        'friendsCount' : friendsCount,
        'joinedDate' : joinedDate,
        'educations' : extract_educations(aboutLinkEducation, driver),
        'works' :  extract_works(aboutLinkEducation, driver),
        'livingPlaces' : extract_livingPlaces(aboutLinkLiving, driver),
        'contacts' : extrct_contacts_basicInfo(aboutLinkContact, driver, 'contact'),
        'basic_information'  : extrct_contacts_basicInfo(aboutLinkContact, driver, 'basic'),
        'relationship' : relationship,
        'families' : extract_families(aboutLinkRelationship, driver),
        'about' : about,
        'quotes' : quote_list,
        'nickNames' : nickNames,
        'events' : extract_events(aboutLinkEvent, driver)
    }
    driver.close()
    
    print("profileObj: ", profileObj)
    RabbitMQ("profile", str(profileObj))