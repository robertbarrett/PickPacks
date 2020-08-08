import gspread, random
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

def get_available(unavailable_list,entries):
  while True:
    random_pick = random.randint(0,entries)
    if random_pick not in unavailable_list:
      break
  return random_pick
  
def get_selection(minval, maxval):
  while True:
    try:
      userInput = int(input("Enter a selection " + str(minval) + "-" + str(maxval) + ": "))      
    except ValueError:
      print("Not an integer! Try again.")
      continue
    if (userInput>=minval and userInput<=maxval):
      return userInput
      break
    else:
      print("Not a valid selection (0-" + str(maxval) + ")! Try again.")
      
def get_option_list(unavailable_list,entries):
  option_list = []
  for i in range(3):
    option = get_available(unavailable_list,entries)
    unavailable_list.append(option)     
    option_list.append(option)
  return option_list
  
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

spreadsheet = client.open("jumpstart packs")

worksheet_list = spreadsheet.worksheets()

print("How many packs?")
packs_number=get_selection(1,5)


while True:
  for num,name in enumerate(worksheet_list):
    worksheet_name = str(name).split("'")[1]
    if worksheet_name != "summary":
      print(str(num) + ") " + worksheet_name)
  selection=get_selection(0,len(worksheet_list)-2)
  
  print("=====================================================")
  unavailable_list=[]
  selected_list=[]
  worksheet_name = str(worksheet_list[selection]).split("'")[1]
  print("Picking Packs for "  + worksheet_name)
  worksheet = spreadsheet.worksheet(worksheet_name)
  packs_list = worksheet.row_values(1)
  entries = len(packs_list)-1 #zero indexed
  
  
  

  for i in range (packs_number):
    option_list=get_option_list(unavailable_list,entries)
    print("Choice " + str(i) + ":\n0) " + packs_list[option_list[0]] + "\n1) " + packs_list[option_list[1]] + "\n2) " + packs_list[option_list[2]])
    selection=get_selection(0,2)
    selected_list.append(selection)
    unavailable_list=selected_list
    print ("PICKED: " + packs_list[option_list[selection]])
  
