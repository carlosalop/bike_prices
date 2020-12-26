import requests
import yagmail
from bs4 import BeautifulSoup
from csv import DictWriter

def read_credentials(file_name):
    with open(file_name, 'r') as file:
        credentials = file.read()
        return credentials.split(':')

def scrape_bikes(url):
    bike_list = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    bikes = soup.find_all(class_='ui-search-layout__item')

    for bike in bikes:
        link = bike.find(class_='ui-search-item__group__element ui-search-link')['href']
        title = bike.find(class_='ui-search-item__group__element ui-search-link')['title']
        price = bike.find(class_='price-tag-fraction').get_text()
        bike_list.append({
            'title': title,
            'price': price,
            'link': link
        })
    return bike_list

def export_bikes(bike_list):
    with open('bikes.csv', 'w', encoding='utf-8', newline='') as file:
        headers = ['title', 'price', 'link']
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for bike in bike_list:
            csv_writer.writerow(bike)

def send_gmail(gmail_sender, gmail_sender_pass, email_receiver, email_subject, email_body, filename):
    yag = yagmail.SMTP(gmail_sender, gmail_sender_pass)
    yag.send(
        to = email_receiver, 
        subject = email_subject,
        contents= email_body,
        attachments=filename
    )    
    
def main():
    url = 'https://deportes.mercadolibre.com.co/bicicletas-ciclismo/bicicletas/antioquia/_BICYCLE*TYPE_240449'
    email_receiver = "carlosandreslopez@gmail.com"
    email_subject = 'Bike Scrapping'
    email_body = "File with bikes from mercadolibre.com.co"
    filename = "bikes.csv"
    credential_file_name = 'gmail_login.txt'
    gmail_sender, gmail_sender_pass = read_credentials(credential_file_name)
    bike_list = scrape_bikes(url)
    export_bikes(bike_list)
    send_gmail(gmail_sender, gmail_sender_pass, email_receiver, email_subject, email_body, filename)

if __name__ == '__main__':
    main()
