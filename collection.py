import re,json,sqlite3,requests,time, os

conn = sqlite3.connect('collections.db')

c = conn.cursor()


def updateCollection():
  path=os.environ['USERPROFILE'] + "\AppData\LocalLow\Wizards Of The Coast\MTGA\Player.log"
  file = open(path, "r")

  InventoryKeyword="PlayerInventory.GetPlayerCardsV3"
  #playerNameKeyword="Logged in successfully. Display Name"
  #playerNameKeyword="Successfully logged in to account"
  playerNameKeyword="Updated account. DisplayName"
  
  for line in file:
    if re.search(r"%s\b" % re.escape(InventoryKeyword), line):
      lastCatalogLine=line
    if re.search(r"%s\b" % re.escape(playerNameKeyword), line):
      lastLoginLine=line

  user=lastLoginLine.split("DisplayName:")[1].split('#')[0]
  
  if c.execute('''SELECT COUNT(*) FROM users WHERE name = "%s"''' %user).fetchone()[0] == 0:
    c.execute("INSERT INTO users VALUES (?)", (user,))
    conn.commit()

  catalog=json.loads('{' + lastCatalogLine.split('{')[2].split('}')[0] + '}')
  cardname=""
  for idval in catalog.keys():
    if c.execute('''SELECT COUNT(*) FROM ids WHERE id = "%s"''' %idval).fetchone()[0] == 0:
      scryfalltxt=requests.get('https://api.scryfall.com/cards/arena/' + idval)
      
      if scryfalltxt.json()["object"] == "card":
        cardname=scryfalltxt.json()["name"]
        if c.execute('''SELECT COUNT(*) FROM ids WHERE id = "%s"''' %idval).fetchone()[0] == 0:
          c.execute('''INSERT INTO ids VALUES (?,?)''', (idval,cardname))
          conn.commit()
          print("Grabbed data from Scryfall for " + cardname)
      else:
        print("ERROR: grabbing data for " + idval)
        c.execute('''INSERT INTO ids VALUES (?,?)''', (idval,"BADCARD"))
    cardname=c.execute('''SELECT name FROM ids WHERE id = "%s"''' %idval).fetchone()[0]
    if c.execute('''SELECT COUNT(*) FROM owners WHERE user = "%s" AND cardname = "%s"''' %(user,cardname)).fetchone()[0] == 0:
      c.execute('''INSERT INTO owners VALUES (?,?)''', (user,cardname))
      conn.commit()
      print("Adding " + cardname + " to owner " + user)

   
def getCube():      
  blocklist = ["Plains", "Island", "Mountain", "Swamp", "Forest", "BADCARD"]
  for cardinfo in c.execute("SELECT DISTINCT name FROM ids").fetchall():
    countnum=c.execute('''SELECT COUNT(*) FROM owners WHERE cardname = "%s"''' %cardinfo).fetchone()[0]
    if countnum == 5 and cardinfo[0] not in blocklist:
      print(cardinfo[0])

  
updateCollection()
getCube()
