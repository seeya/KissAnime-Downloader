import sys
from urlparse import urlparse
from subprocess import call
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

baseURL = ""
idmPath = "C:\Program Files (x86)\Internet Download Manager\IDMan.exe"


def kissDrama(browser, mainLink):
	print "Getting Total Number Of Episodes..."
	browser.get(mainLink);
	folderName = browser.find_element_by_class_name("bigChar").text
	episodeList = browser.find_elements_by_class_name("episodeSub")

	episodeLinks = []

	for links in episodeList:
		episodeLinks.append(links.find_element(By.TAG_NAME, "a").get_attribute("href"))

	print "Found: " + str(len(episodeLinks))

	for link in episodeLinks:
		browser.get(link)
		print "Getting " + browser.title.split("-")[0]
		videoTag = browser.find_element(By.TAG_NAME, "video")
		print "Link: " + videoTag.get_attribute("src")
		downloadFile(idmPath, videoTag.get_attribute("src"), folderName, browser.title.split(" -")[0] + ".mp4")

def downloadFile(idmPath, downloadLink, folder, fileName):
		call([idmPath, "/d", downloadLink, "/n", "/a", "/f", fileName])

def kissAnime(browser, mainLink):
	browser.get(mainLink)
	episodeTable = browser.find_elements_by_class_name("listing")[0].find_elements(By.TAG_NAME, "a")

	episodeLinks = []

	for rows in episodeTable:
		episodeLinks.append(rows.get_attribute("href"))

	for link in episodeLinks:
		browser.get(link)
		print "Getting " + browser.title.split("-")[0]
		videoTag = browser.find_element(By.TAG_NAME, "video")
		print "Link: " + videoTag.get_attribute("src")
		downloadFile(idmPath, videoTag.get_attribute("src"), folderName, browser.title.split(" -")[0] + ".mp4")

if __name__ == "__main__":
	showURL = sys.argv[1]

	# hide images
	extensions = webdriver.ChromeOptions()
	prefs = {"profile.managed_default_content_settings.images": 2}
	extensions.add_experimental_option("prefs", prefs)
	extensions.add_extension('adblock.crx')	

	browser = webdriver.Chrome(chrome_options=extensions)
	browser.implicitly_wait(7)

	baseURL = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(showURL))

	if "anime" in baseURL:
		kissAnime(browser, showURL)
	else:
		kissDrama(browser, showURL);

	browser.quit()



