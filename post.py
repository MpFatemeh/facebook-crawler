from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import json
from pipeline import RabbitMQ

def post_crawler(userId, postId):
    postURL = "https://www.facebook.com/permalink.php?story_fbid=" + str(postId) + "&id=" + str(userId)

    driver = webdriver.Firefox()
    driver.get(postURL)
    time.sleep(25)
    page_text = (driver.page_source).encode('utf-8')
    soup = BeautifulSoup(page_text,features="lxml")

    name = soup.find('h5').find('span').find('span').find('a').text
    print("name : ", name)

    postList =  [member.text for member in soup.find_all('p')]
    post = ' '.join(postList)
    print("post : ", post)

    aSpanTagList = [member.find('span') for member in soup.find_all('a')]
    aSpanTagList = [member.find('span') for member in aSpanTagList if member is not None]
    aSpanTagList = [member.find('span') for member in aSpanTagList if member is not None]
    likeCount = aSpanTagList[0].text
    print("likeCount : ", likeCount)

    aTagList = [member.text for member in soup.find_all('a')]
    aTagShares = [member for member in aTagList if 'Shares' in member]
    shares = aTagShares[0]
    sharesCountList = [int(s) for s in shares.split() if s.isdigit()]
    sharesCount = sharesCountList[0]
    print("sharesCount : ", sharesCount)

    driver.close()
    postObj = {
        'name' : name,
        'likeCount' : likeCount,
        'sharesCount' : sharesCount,
        'post' : post
    }

    print("postObj: ", postObj)
    RabbitMQ("post", str(postObj))