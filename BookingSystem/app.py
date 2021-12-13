from os import write
from unicodedata import name
from flask import Flask, render_template, url_for, request
import pip._vendor.requests as requests
from flask_cors import CORS
from bs4 import BeautifulSoup
app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return render_template('entry.html')


@app.route("/search", methods=['POST'])
def search():
    startstation = request.form.get('startstation')
    # startstation = '7210-礁溪'
    endstation = request.form.get('endstation')
    # endstation = '7000-花蓮'
    currentdate = request.form.get('datepicker')
    currenttime = request.form.get('time')
    # currenttime = '01:00'

    target_url = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime"

    response = requests.request("GET", target_url)
    origin_content = response.text
    soup = BeautifulSoup(origin_content, "html.parser")
    csrf = soup.html.form.find("input").get('value')
    rideDate = '{}/{}/{}'.format(currentdate.split('-')
                                 [0], currentdate.split('-')[1], currentdate.split('-')[2])
    payload = {
        '_csrf': csrf,
        'startStation': startstation,
        'endStation': endstation,
        'transfer': 'ONE',
        'rideDate': rideDate,
        'startOrEndTime': True,
        'startTime': currenttime,
        'endTime': '23:59',
        'trainTypeList': 'ALL',
        '_isQryEarlyBirdTrn': 'on',
        'query': '查詢'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    search_url = 'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime'
    response = requests.request(
        "POST", search_url, headers=headers, data=payload)
    search_content = response.text

    try:
        txt_content = BeautifulSoup(search_content, 'html.parser').table.tbody.find_all(
            "tr", class_="trip-column")
    except:
        return "<h1>no result</h1>"

    allinfo = []

    for item in txt_content:
        siteinfo = []
        train_code = item.find('a', class_="links").decode_contents()
        train_from_to_price = item.find_all('span')
        train_arrive_leave_total_time = item.find_all('td')
        booking_form = ''
        try:
            booking_form = item.find('form', {
                                     'action': "/tra-tip-web/tip/tip001/tip117/tra2traUrl", 'method': "post", 'target': "_blank"})
            booking_form["action"] = "https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip117/tra2traUrl"
        except:
            booking_form = ''

        is_train_booking_button = ''
        if item.find('button', class_='icon-ticket'):
            is_train_booking_button = item.find('button', class_='icon-ticket')

        train_from = train_from_to_price[2].text
        train_to = train_from_to_price[4].text
        train_price = train_from_to_price[6].text
        train_arrive_time = train_arrive_leave_total_time[1].text
        train_total_time = train_arrive_leave_total_time[3].text

        siteinfo.append(train_code)
        siteinfo.append(train_arrive_time)
        siteinfo.append(train_from)
        siteinfo.append(train_to)
        siteinfo.append(train_price)
        
        siteinfo.append(train_total_time)

        if(len(is_train_booking_button) > 0):
            siteinfo.append(is_train_booking_button.text)

        siteinfo.append(booking_form)
        allinfo.append(siteinfo)

    # return render_template('output.html', data=allinfo, start_station=startstation, end_station=endstation, current_date=currentdate)
    return render_template('output.html',data=allinfo)