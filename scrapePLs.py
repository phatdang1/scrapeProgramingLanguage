from bs4 import BeautifulSoup
import requests
import re
import json

url = 'https://en.wikipedia.org/wiki/List_of_programming_languages'
#Programming languages and link dictionary
pLanguageDict = {'programing_language': []}
paradigmList = []

try:
    # access the target website
    source = requests.get(url)
    source.raise_for_status()

    # get html
    html = BeautifulSoup(source.text, 'html.parser')

    # search for all column that contain programing languages 
    column = html.find('div', class_='mw-body-content').find_all('div', class_ = 'div-col')
    
    # loop through each column to extract programing languages and links
    for alphabet in column:
        pLanguages = alphabet.find_all('li')
        for pLanguage in pLanguages:
            pLanguageName = pLanguage.a.text
            pLanguageLink = 'https://en.wikipedia.org/' + pLanguage.a.get('href')
            #store each programming language and the link
            
            try:
                sourcePL = requests.get(pLanguageLink)
                sourcePL.raise_for_status()

                htmlPL = BeautifulSoup(sourcePL.text, 'html.parser')

                #get the number of header sections
                headers = len(htmlPL.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
                
                infoBox = htmlPL.find('table', class_='infobox vevent')

                #check if website has infobox
                if infoBox != None:

                    #check if infobox has "First appeared" section
                    if infoBox.find(text=re.compile("First.*")):
                        firstAppeared = infoBox.find(text=re.compile("First.*")).parent.parent
                        year = firstAppeared.find('td')
                        year = year.text.split(';')[0]

                        #check if infobox  has "Paradigm"
                        if infoBox.find(text=re.compile("Paradigm")):
                            paradigmList = []
                            sectionHasParadigm = infoBox.find(text=re.compile("Paradigm")).parent.parent.parent
                            paradigmsParent = sectionHasParadigm.find('td')
                            paradigms = paradigmsParent.find_all('a')

                            #get all paradigms
                            for item in paradigms:
                                paradigmList.append(item.text)
                            
                            #check if infobox  has "Filename extentions"
                            if infoBox.find(text=re.compile("extensions")):
                                sectionHasFileExtension = infoBox.find(text=re.compile("extensions")).parent.parent.parent
                                fileNameExtentions = sectionHasFileExtension.find('td').text
                                pLanguageDict['programing_language'].append({'name': pLanguageName, 'url': pLanguageLink, 'paradigm':paradigmList, 'first_appeared': year, 'file_extension': fileNameExtentions, 'number_of_header_section': headers})
                                
            except Exception as e:
                print(e)    
except Exception as e:
    print(e)

#write to a json file
json_object = json.dumps(pLanguageDict, indent=3)
with open("result.json", "w") as outfile:
    outfile.write(json_object)
    outfile.close()