import requests
import smtplib

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
MY_GMAAIL ="rpg736tanvir@gmail.com"
MY_PASSWORD ="01955005706#@"
MAIL_RECIVER ="tanzin736@gmail.com"
FUNCTION = "TIME_SERIES_DAILY"
SYMBOL = "TSLA"
INTERVAL = "5min"
ADJUSTED = "true"



STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "6726a5e0691b4a198f69c33d332ac2fe"
STOCK_API_KEY = "1P6N550R3QWTJ7E7"


YESTERDAY_STOCK_PRICE_FROM = '2021-12-28'
YESTERDAY_STOCK_PRICE_TO = '2021-12-29'
NEWS_SORT_BY = "popularity"

# now i am going to create the dectionary for the api endpoint
'''AFTER_THE_NEWS_URL = {
    'q':COMPANY_NAME,
    'from':YESTERDAY_STOCK_PRICE_FROM,
    'to':YESTERDAY_STOCK_PRICE_TO,
    'sortBy':NEWS_SORT_BY,
    'apiKey':NEWS_API_KEY
}'''

# ceating the url of the news endpoint
NEWS_URL = f'{NEWS_ENDPOINT}?q={COMPANY_NAME}&from={YESTERDAY_STOCK_PRICE_FROM}&to={YESTERDAY_STOCK_PRICE_TO}&sortBy={NEWS_SORT_BY}&apiKey={NEWS_API_KEY}'
STOCK_URL = f'{STOCK_ENDPOINT}?function={FUNCTION}&symbol={SYMBOL}&interval={INTERVAL}&adjusted={ADJUSTED}&apikey={STOCK_API_KEY}'
url_request = requests.get(url=NEWS_URL)
second_url_request = requests.get(url=STOCK_URL)

# now i am going to raise an execption if there is anykind of error
url_request.raise_for_status()
second_url_request.raise_for_status()

# nwo i need two data one is the closeing of the previous day and another one is the day after previous day
data_of_the_stock = second_url_request.json()['Time Series (Daily)']
data_yesterday = data_of_the_stock['2021-12-29']['4. close']
data_before_yesterday = data_of_the_stock['2021-12-28']['4. close']
print(data_yesterday)
print((data_before_yesterday))

# lets find the different between the two closing stock
sum_of_stock = int(((float(data_yesterday) - float(data_before_yesterday))/float(data_yesterday)) * 100)

print(sum_of_stock)
# to see all the data we are going to use the json
data_of_the_news = url_request.json()['articles']


# for i in data_of_the_news:
#     print(i)
title = []
text = []
for content in data_of_the_news[:3]:
    title.append(content['title'])
    text.append(content['content'])


# creating the method that will send the message
def send_mail(mail,subject,message):
    # i am going to established theh connection with the email server
    with smtplib.SMTP('smtp.gmail.com',port=587) as connection:
        # for secure our messge and server we are going to do this
        connection.starttls()
        # then we are going to login to the gmail that we went to send thhe message from
        connection.login(user=MY_GMAAIL,password=MY_PASSWORD,initial_response_ok=True)
        # now i am goingn to send the meesage
        connection.sendmail(from_addr=MY_GMAAIL,to_addrs=mail,msg=f"Subject: Stock market message{subject}\n\n\n{message}")
def proces(subject):
    message = ' '
    if len(title) == len(text):
        for i in range(len(title)):
            message = title[i] + text[i]
            # print(f"the message : {message.encode('ascii','ignore')}")
            send_mail(MAIL_RECIVER,subject.encode('ascii','ignore'),message.encode('ascii','ignore'))
            print("Message is sended....")


#Optional: Format the SMS message like this: 


if __name__ == '__main__':
    if sum_of_stock >0:
        subject = f"TSLA: 🔺{sum_of_stock}%"
        proces(subject)
    else:
        subject = f"TSLA: 🔻{sum_of_stock}%"
        proces(subject)