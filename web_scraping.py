from bs4 import BeautifulSoup as soup
from pdf_scraping import PDF_scraper
import requests as req
import os

def load_data(url, limitFile, index):
    text = {}

    response = req.get(url)

    file = soup(response.text, 'html.parser')

    all_link = file.find_all('a')

    
    for link in all_link:
        
        try:
            pdf_link = ''
            if 'pdf' in  link['href']:

                # basecase: file limitation
                if index > limitFile:
                    break

                pdf_link = link['href'] + '.pdf'
                pdf_response = req.get(pdf_link)
                
                # extract file name
                pdf_url = 'https://arxiv.org/abs/' + link['href'].split("/")[-1]
                response_findFileName = req.get(pdf_url)
                file_findFileName = soup(response_findFileName.text, 'html.parser')
                pdf_fileName = file_findFileName.find('h1', class_='title mathjax')
                
                #change file name datatype (bs4 element tag -> string)
                pdf_fileName_str = pdf_fileName.get_text().replace(" ", "_").replace("Title:", "")

                #clean file name
                file_name = pdf_fileName_str.replace(":", "_").strip()
                
                #creating directory
                directory = "pdf/"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                
                with open('pdf/' + file_name + '.pdf' , "wb") as f:
                    f.write(pdf_response.content)
                
                print("File " ,index ,": " ,pdf_fileName_str)  
                
                text[file_name] = PDF_scraper.text_scraper('pdf/' + file_name + '.pdf')
                
                index+=1

                # insert pdf content (string) into database
                # print("File ", index , " content: " , text)

        except:
            pass

    # if there is next page, use recursion 
    try:
        next_link = file.find('a', class_='pagination-next')
        next_url = 'https://arxiv.org' + next_link['href']
        load_data(next_url, limitFile, index)

    except:
        exit()
        