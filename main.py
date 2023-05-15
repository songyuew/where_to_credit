import airportsdata
from beautifultable import BeautifulTable
from PyInquirer import prompt
import requests
import os
import math
import json

url = "https://www.wheretocredit.com/api/2.0/calculate"

airports = airportsdata.load('IATA')
segments = []

def checkAirportCode(code):
  try:
    airport = airports[code]
    return airport
  except Exception:
    False

def getFromList(list, i):
  try:
    return list[i]
  except IndexError:
      return "N/A"

questions1 = [
  {
    'type': 'input',
    'message': 'TICKETING CARRIER',
    'name': 'ticketingCarrier',
    },
  {
    'type': 'input',
    'message': 'BASE FARE USD',
    'name': 'baseFareUSD',
  }
]

questions2 = [
    {
      'type': 'input',
      'message': 'ORIGIN',
      'name': 'origin',
    },
    {
      'type': 'input',
      'message': 'DESTINATION',
      'name': 'destination',
    },
    {
      'type': 'input',
      'message': 'CARRIER',
      'name': 'carrier',
    },
    {
      'type': 'input',
      'message': 'OPERATING CARRIER',
      'name': 'operatingCarrier',
    },
    {
      'type': 'input',
      'message': 'BOOKING CLASS',
      'name': 'bookingClass',
    },
]

continueCheck = [
  {
    'type': 'confirm',
    'message': 'Add Segment',
    'name': 'addSegment',
    'default': False
  }
]

windowCol, windowWidth = os.get_terminal_size()
paddingWidth = math.floor(windowCol * 0.9)

segment = 1

header = prompt(questions1)

while True:
  print('{:*^{paddingWidth}}'.format("SEGMENT "+str(segment), paddingWidth = paddingWidth))
  flight = prompt(questions2)
  departureAirport = checkAirportCode(flight["origin"])
  arrivalAirport = checkAirportCode(flight["destination"])
  if(departureAirport and arrivalAirport):
    flight["departureAirportName"] = departureAirport["name"]
    flight["arrivalAirportName"] = arrivalAirport["name"]
  else:
    print("INVALID AIRPORT CODE")
    pass
  
  segments.append(flight)
  continueSel = prompt(continueCheck)
  if (not continueSel["addSegment"]): break
  else: segment += 1

header["segments"] = segments

payload = json.dumps([header])

reqHeaders = {'Content-Type': 'application/json'}

try:
  response = requests.request("POST", url, headers=reqHeaders, data=payload)
except Exception:
  print("QUERY FAILURE")
  exit()

res = response.json()["value"][0]["value"]["totals"]

print('{:*^{paddingWidth}}'.format("", paddingWidth = paddingWidth))
print('{:*^{paddingWidth}}'.format("ITERNARY", paddingWidth = paddingWidth))
print('{:*^{paddingWidth}}'.format("TICKETED BY " + header["ticketingCarrier"], paddingWidth = paddingWidth))
print('{:*^{paddingWidth}}'.format("", paddingWidth = paddingWidth))

iternary = BeautifulTable(maxwidth=paddingWidth)

iternary.rows.append(["SEGMENT","TIC CARRIER","OP CARRIER","CLASS","ORIGIN","DESTINATION"])
for i in range(segment):
  a = segments[i]
  iternary.rows.append([i+1,a["carrier"],a["operatingCarrier"],a["bookingClass"],f'{a["origin"]} - {a["departureAirportName"]}',f'{a["destination"]} - {a["arrivalAirportName"]}'])
print(iternary)

print('{:*^{paddingWidth}}'.format("", paddingWidth = paddingWidth))
print('{:*^{paddingWidth}}'.format("MILEAGE ACCUMULATION", paddingWidth = paddingWidth))
print('{:*^{paddingWidth}}'.format("", paddingWidth = paddingWidth))

mileage = BeautifulTable(maxwidth=paddingWidth)

mileage.rows.append(["AIRLINES","RB","RDM","TIER 1","TIER 2","TIER 3","TIER 4"])
for i in range(len(res)):
  a = res[i]
  mileage.rows.append([f'{a["id"]} - {a["name"]}',a["revenueBased"], getFromList(a["rdm"],0),getFromList(a["rdm"],1),getFromList(a["rdm"],2),getFromList(a["rdm"],3),getFromList(a["rdm"],4)])
print(mileage)

print('{:*^{paddingWidth}}'.format("", paddingWidth = paddingWidth))
print('{:*^{paddingWidth}}'.format("END OF PAGE", paddingWidth = paddingWidth))
print('{:*^{paddingWidth}}'.format("", paddingWidth = paddingWidth))