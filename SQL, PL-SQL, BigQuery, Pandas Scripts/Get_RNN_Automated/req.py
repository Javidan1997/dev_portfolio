def get_rrn(m_id, ref):
    import requests
    import json
    import re
    m_id = "mp_5716900531"
    ref = "4bcfbd58-a5fd-416f-b4c3-0077003f839a"
    ploads = {'mid':m_id,'reference':ref}
    r = requests.get('https://pay.millikart.az/gateway/payment/status',params=ploads)
    # print(r.text)
    # print(r.url)
    data = r.text

    # print(data)
    # stripped = (re.sub('<[^<]+?>', '', data)).strip()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(data, 'lxml')

    for tag in soup.findAll("rrn"):
        # print(tag)
        # print(tag["name"])
        print(tag.text)
    return tag.text

# get_rrn("mp_5716900531", "4bcfbd58-a5fd-416f-b4c3-0077003f839a")

import pandas as pd

# ex = pd.read_excel("ex.csv")
import os
df1=pd.read_excel(
     os.path.join("", "ex.xlsx"),
     engine='openpyxl',
)
# print(df1.head())
rnn = []
for i, j in zip(df1['tx_id'], df1['mid']):
    print(i, j)
    rnn.append(get_rrn(i, j))


# for i in df1['tx_id']
# print(stripped[:][2])
# import lxml.etree
# # xmlstr is your xml in a string
# root = lxml.etree.fromstring(data)
# textelem = root.find('response/rrn')
# print( textelem.text)
#
# print(r.status_code, r.headers)
# print("***********")
# print(r.text)
