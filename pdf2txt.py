import PyPDF2
import re
import icalendar
import uuid
from datetime import datetime

pattern1 = r'SIN-[A-Za-z]{3}$'
pattern2 = r'^[A-Za-z]{3}-SIN$'
pattern3 = r'\d{2}[A-Za-z]{3}\d{2}'
pattern4 = r'SQ \d{2,3}'
pattern5 = r'\d{8}'
pattern6 = r'SIN-[A-Za-z]{3}'
pattern7 = r'[A-Za-z]{3}-SIN'
pattern8 = r'\d{4}'

flightList, eventList = [], []
filename = 'apr'

stn_list = ['adl', 'akl', 'amd', 'ams', 'bcn', 'bdo', 'bkk', 'blr', 'bne', 'bom', 'bwn', 'can', 'ccu', 'cdg', 'ceb', 'cgk', 'chc', 'ckg', 'cmb', 'cns', 'cok', 'cph', 'cpt', 'cts', 'ctu', 'dac', 'dad', 'del', 'dme', 'dps', 'drw', 'dvo', 'dxb', 'ewr', 'fco', 'fra', 'fuk', 'han', 'hkg', 'hkt', 'hnd', 'hrb',
            'hyd', 'iah', 'icn', 'ist', 'jfk', 'jnb', 'khh', 'kix', 'kno', 'ktm', 'kul', 'lax', 'lhr', 'maa', 'man', 'mel', 'mle', 'mnl', 'muc', 'mxp', 'ngo', 'nrt', 'oka', 'pek', 'pen', 'per', 'pnh', 'pus', 'pvg', 'rep', 'rgn', 'rok', 'sea', 'sfo', 'sgn', 'sin', 'sub', 'syd', 'szx', 'tpe', 'xmn', 'yvr', 'zrh']

location_list = [('ADL', 'Adelaide, Australia'),
                 ('AKL', 'Auckland, New Zealand'),
                 ('AMD', 'Ahmedabad, India'),
                 ('AMS', 'Amsterdam, Netherlands'),
                 ('BCN', 'Barcelona, Spain'),
                 ('BDO', 'Bandung, Indonesia'),
                 ('BKK', 'Bangkok, Thailand'),
                 ('BLR', 'Bengaluru, India'),
                 ('BNE', 'Brisbane, Australia'),
                 ('BOM', 'Mumbai, India'),
                 ('BWN', 'Bandar Seri Begawan, Brunei'),
                 ('CAN', 'Guangzhou, China'),
                 ('CCU', 'Kolkata, India'),
                 ('CDG', 'Paris, France'),
                 ('CEB', 'Cebu City, Philippines'),
                 ('CGK', 'Jakarta, Indonesia'),
                 ('CHC', 'Christchurch, New Zealand'),
                 ('CKG', 'Chongqing, China'),
                 ('CMB', 'Colombo, Sri Lanka'),
                 ('CNS', 'Cairns, Australia'),
                 ('COK', 'Kochi, India'),
                 ('CPH', 'Copenhagen, Denmark'),
                 ('CPT', 'Cape Town, South Africa'),
                 ('CTS', 'Sapporo, Japan'),
                 ('CTU', 'Chengdu, China'),
                 ('DAC', 'Dhaka, Bangladesh'),
                 ('DAD', 'Da Nang, Vietnam'),
                 ('DEL', 'Delhi, India'),
                 ('DME', 'Moscow, Russia'),
                 ('DPS', 'Denpasar, Bali, Indonesia'),
                 ('DRW', 'Darwin, Australia'),
                 ('DVO', 'Davao City, Philippines'),
                 ('DXB', 'Dubai, United Arab Emirates'),
                 ('EWR', 'Newark, New Jersey, USA'),
                 ('FCO', 'Rome, Italy'),
                 ('FRA', 'Frankfurt, Germany'),
                 ('FUK', 'Fukuoka, Japan'),
                 ('HAN', 'Hanoi, Vietnam'),
                 ('HKG', 'Hong Kong'),
                 ('HKT', 'Phuket, Thailand'),
                 ('HND', 'Tokyo, Japan'),
                 ('HRB', 'Harbin, China'),
                 ('HYD', 'Hyderabad, India'),
                 ('IAH', 'Houston, Texas, USA'),
                 ('ICN', 'Seoul, South Korea'),
                 ('IST', 'Istanbul, Turkey'),
                 ('JFK', 'New York City, New York, USA'),
                 ('JNB', 'Johannesburg, South Africa'),
                 ('KHH', 'Kaohsiung, Taiwan'),
                 ('KIX', 'Osaka, Japan'),
                 ('KNO', 'Medan, Indonesia'),
                 ('KTM', 'Kathmandu, Nepal'),
                 ('KUL', 'Kuala Lumpur, Malaysia'),
                 ('LAX', 'Los Angeles, California, USA'),
                 ('LHR', 'London, United Kingdom'),
                 ('MAA', 'Chennai, India'),
                 ('MAN', 'Manchester, United Kingdom'),
                 ('MEL', 'Melbourne, Australia'),
                 ('MLE', 'Maldives'),
                 ('MNL', 'Manila, Philippines'),
                 ('MUC', 'Munich, Germany'),
                 ('MXP', 'Milan, Italy'),
                 ('NGO', 'Nagoya, Japan'),
                 ('NRT', 'Tokyo, Japan'),
                 ('OKA', 'Okinawa, Japan'),
                 ('PEK', 'Beijing, China'),
                 ('PEN', 'Penang, Malaysia'),
                 ('PER', 'Perth, Australia'),
                 ('PNH', 'Phnom Penh, Cambodia'),
                 ('PUS', 'Busan, South Korea'),
                 ('PVG', 'Shanghai, China'),
                 ('REP', 'Siem Reap, Cambodia'),
                 ('RGN', 'Yangon, Myanmar'),
                 ('ROK', 'Rockhampton, Australia'),
                 ('SEA', 'Seattle, Washington, USA'),
                 ('SFO', 'San Francisco, California, USA'),
                 ('SGN', 'Ho Chi Minh City, Vietnam'),
                 ('SIN', 'Singapore'),
                 ('SUB', 'Surabaya, Indonesia'),
                 ('SYD', 'Sydney, Australia'),
                 ('SZX', 'Shenzhen, China'),
                 ('TPE', 'Taipei, Taiwan'),
                 ('XMN', 'Xiamen, China'),
                 ('YVR', 'Vancouver, Canada'),
                 ('ZRH', 'Zurich, Switzerland')]

month_dict = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

print('Start')
pdf_file = open(f'pdf/{filename}.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)
txt_file = open(f'txt/{filename}.txt', 'w', encoding='utf-8')

for page in pdf_reader.pages:
    page_text = page.extract_text()
    txt_file.write(page_text)

# deleting useless lines
pg_toDel, randomD = [], []
tempH = ''

txt_file = open(f'txt/{filename}.txt', 'r')
lines = txt_file.readlines()
new_lines = lines[17:]


for i, line in enumerate(new_lines):
    if 'Duty Duty' in line or 'Training Codes' in line:
        codeMean = new_lines[i:]
        del new_lines[i:]

for i, line in enumerate(new_lines):
    if re.search(pattern3, line):
        tDate = re.search(pattern3, line).group()
    else:
        new_lines[i] = f'{line[:-2]} {tDate}\n'
    if line[:6] == tempH and re.match(pattern1, line[7:14]):
        pg_toDel.append(i)
    if line[:6] == tempH and re.match(pattern2, line[7:14]):
        pg_toDel.append(i-1)
    tempH = line[:6]
    if 'OFFD' in line or 'ATDO' in line or 'LO' in line or 'AALV' in line:
        pg_toDel.append(i)
for i in sorted(pg_toDel, reverse=True):
    del new_lines[i]
    pg_toDel = []
for i, line in enumerate(new_lines):
    if re.search(pattern4, line):
        pass
    else:
        randomD.append(line)
        pg_toDel.append(i)
for i in sorted(pg_toDel, reverse=True):
    del new_lines[i]

list1 = ['SSS1', 'STBY', 'SSN1']
for i in randomD:
    stbyDetail = i.split()
    tDate = re.search(pattern3, i).group()
    if stbyDetail[0] == 'SIN':
        for word in list1:
            if word in i:
                startTime = '0000'
                endTime = '2359'
                duty = 'STBY'
            else:
                startTime = stbyDetail[5][:4]
                endTime = stbyDetail[5][4:]
                duty = stbyDetail[3]
    else:
        TimeMix = re.search(pattern5, i).group()
        startTime = TimeMix[:4]
        endTime = TimeMix[4:]
        duty = 'STBY'
    testPr = f'{duty} @ {stbyDetail[0]} on {tDate} | {startTime}~{endTime}'
    summary = f'{duty} @ {stbyDetail[0]}'
    eventDetail = [summary, tDate, startTime, endTime]
    eventList.append(eventDetail)

for i in new_lines:
    # print (i)
    fD = i.split()
    # print (fD)
    summary = f'{fD[0]}{fD[1]} {fD[2]}'
    if re.search(pattern6, i):
        # if re.search(pattern5, fD[7]):
        #     startTime = fD[7][4:]
        # else:
        startTime = fD[9]
        startDate = re.search(pattern3, i).group()
        eventDetail = [summary, startDate, startTime]
    elif re.search(pattern7, i):
        if re.search(pattern5, fD[5]):
            endTime = fD[5][4:]
        else:
            endTime = fD[7]
        endDate = re.search(pattern3, i).group()
        eventDetail.append(endDate)
        eventDetail.append(endTime)
        flightList.append(eventDetail)
    # print (summary, tDate, time)


for i in flightList:
    stn = i[0][-3:].lower()
    if stn in stn_list:
        index = stn_list.index(stn)
        location = ', '.join(location_list[index])
        i.append(location)
    else:
        pass

for i in eventList:
    stn = i[0][-3:].lower()
    if stn in stn_list:
        index = stn_list.index(stn)
        location = ', '.join(location_list[index])
        i.append(location)
    else:
        pass


for i in flightList:
    for x, y in enumerate(i):
        # print (y)
        if re.search(pattern3, y):
            date_str = y
            month_num = month_dict[date_str[2:5]]
            date_str = date_str[:2] + month_num + date_str[5:]
            day = int(date_str[:2])
            month = int(date_str[2:4])
            year = int('20' + date_str[4:])
            i[x] = [year, month, day]
    for x, y in enumerate(i):
        if not isinstance(y, list):
            if re.search(pattern8, y):
                time_str = y
                hour = int(y[:2])
                minute = int(y[2:])
                second = 0
                i[x] = [hour, minute, second]

for i in eventList:
    for x, y in enumerate(i):
        # print (y)
        if re.search(pattern3, y):
            date_str = y
            month_num = month_dict[date_str[2:5]]
            date_str = date_str[:2] + month_num + date_str[5:]
            day = int(date_str[:2])
            month = int(date_str[2:4])
            year = int('20' + date_str[4:])
            i[x] = [year, month, day]
    for x, y in enumerate(i):
        if not isinstance(y, list):
            if re.search(pattern8, y):
                time_str = y
                hour = int(y[:2])
                minute = int(y[2:])
                second = 0
                i[x] = [hour, minute, second]

cal = icalendar.Calendar()

cal.add('prodid', '-//James//Schedule//EN')
cal.add('version', '2.0')

for y, i in enumerate(flightList):
    # # Create an event
    event = icalendar.Event()
    event.add('summary', f'{i[0]}')
    event.add('dtstart', datetime(
        i[1][0], i[1][1], i[1][2], i[2][0], i[2][1], i[2][2]))
    event.add('dtend', datetime(i[3][0], i[3][1],
              i[3][2], i[4][0], i[4][1], i[4][2]))
    event.add('location', f'{i[5]}')
    event['DTSTAMP'] = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    event['UID'] = str(uuid.uuid4())
    cal.add_component(event)

for y, i in enumerate(eventList):
    event = icalendar.Event()
    event.add('summary', f'{i[0]}')
    event.add('dtstart', datetime(
        i[1][0], i[1][1], i[1][2], i[2][0], i[2][1], i[2][2]))
    event.add('dtend', datetime(i[1][0], i[1][1],
              i[1][2], i[3][0], i[3][1], i[3][2]))
    event.add('location', f'{i[4]}')
    event['DTSTAMP'] = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    event['UID'] = str(uuid.uuid4())
    cal.add_component(event)


with open(f'ics/{filename}.ics', 'wb') as f:
    f.write(cal.to_ical())

pdf_file.close()
txt_file.close()
print('End')
