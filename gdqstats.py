import bs4
import urllib.request
from datetime import datetime

def get_url(url, timeout=120):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    with urllib.request.urlopen(req, timeout=timeout) as fd:
        return fd.read().decode()

def parse_gdq_sched():
    rawdata = get_url('https://gamesdonequick.com/schedule')
    soup = bs4.BeautifulSoup(rawdata,'lxml')
    rows = soup.select('table#runTable tr')
    date = None
    celldata = None
    data = []
    dataitem = {}
    for row in rows:
        if 'class' in row.attrs:
            if 'day-split' in row['class']:
                pass
            elif 'second-row' in row['class']:
                tabledata = row.select('td')
                tmp = tabledata[0].text.strip().split(':')
                tmp = int(tmp[0])*3600+int(tmp[1])*60+int(tmp[2])
                dataitem['runtime']=tmp
                dataitem['category']=tabledata[1].text.strip()
                data.append(dataitem)
                dataitem = {}
        else:
            tabledata = row.select('td')
            dataitem['time'] = tabledata[0].text.strip()
            dataitem['game'] = tabledata[1].text.strip()
            dataitem['players'] = tabledata[2].text.strip()
            if(len(tabledata) > 3):
                tmp = tabledata[3].text.strip()
                if tmp != '':
                    tmp = tmp.split(':')
                    tmp = int(tmp[0])*3600+int(tmp[1])*60+int(tmp[2])

                dataitem['setup'] = tmp
            else:
                dataitem['setup'] = ''

    return data

import pandas as pa
if __name__ == "__main__":
    fmtstring = '%Y-%m-%dT%H:%M:%SZ'
    df = pa.DataFrame(parse_gdq_sched())
    df['setup'] = pa.to_numeric(df['setup'],errors='coerce')
    df['time'] = df['time'].apply(lambda x : datetime.strptime(x,fmtstring))
    df['runtime'] = pa.to_numeric(df['runtime'],errors='coerce')
    shortdf = df[df['time'] < datetime.utcnow()]
    setup = shortdf['setup'].sum()/3600
    runtime = shortdf['runtime'].sum()/3600
    print('setup: ' + str(setup))
    print('runtime: ' + str(runtime))
    print('% setup: ' + str(setup/(setup+runtime)))
