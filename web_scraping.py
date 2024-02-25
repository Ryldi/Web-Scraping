from bs4 import BeautifulSoup as soup
from pdf_scraping import PDF_scraper
from pdf_autosave import PDF_autosave
import requests as req
import os

def load_data(url, limitFile, index, save_to):
    text = {}

    response = req.get(url)

    file = soup(response.text, 'html.parser')

    all_link = file.find_all('a')

    
    for link in all_link:
        
        try:
            pdf_link = ''
            if 'pdf' in  link['href']:

                text["file_name"] = []
                text["file_content"] = []

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

                # insert pdf content (string) into database
                
                text["file_name"].append(file_name)
                text["file_content"].append(PDF_scraper.text_scraper('pdf/' + file_name + '.pdf').replace("\n", ""))

                index+=1

                # insert into database
                PDF_autosave.auto_save(save_to, text)

        except:
            pass

    # if there is next page, use recursion 
    try:
        next_link = file.find('a', class_='pagination-next')
        next_url = 'https://arxiv.org' + next_link['href']
        load_data(next_url, limitFile, index, save_to)

    except:
        exit()
        