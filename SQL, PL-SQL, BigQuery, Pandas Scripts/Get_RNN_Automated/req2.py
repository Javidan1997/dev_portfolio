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

from flask_restplus import reqparse

parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted')
parser.add_argument('name')
args = parser.parse_args()

parser.add_argument('name', required=True, help="Name cannot be blank!")

# for type_tag in root.findall('response/rrn'):
#     value = type_tag.get('rrn')
#     print(value, "ok")

# import xml.parsers.expat
# parser = xml.parsers.expat.ParserCreate()
# parser.ParseFile(open('path.xml', 'r'))
