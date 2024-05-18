import random
########################################## EMOJIS
coinemoji = "<a:Coin:1224446854708727908>"




########################################### COLOURS

green = 0x4dff4d
purple = 800080


###################################### Constants
WORKCD = 300
ROBCD = 600
GAMBLECD = 400

bankupgeq = {1:1000}
bankitemreq = {1:[]}
maxbankbalance = {1:1000,2:10000}


######################################## FISH

fishcategories = {"Common":["Green","Red","White"],
                "Uncommon":["Blue"],
                "Rare":["Blooper"],
                "Epic":["Albino"],
                "Legendary":["Rainbow"],
                "Exotic":["Squid"],
                "Unusual":["Puffer","Magi"],
                "Mythic":["Gold"],
                "Unreal":["Mario"],
                "WAHH":["WAH"],
                "???":["Goku"],
                "SMB3":["s1","s2","s3","s4"],
                "SMW":["Goggles","VanFish"],
                "SMB2":["Trout"]}
fishemojis = {"Red":"<a:CheepCheepRed:1225648789461667981>",
              "Green":"<a:CheepCheepGreen:1225649580423512175>",
              "White":"<a:CheepCheepWhite:1225648968818626661>",
              "Blue":"<a:CheepCheepBlue:1227798954549444728>",
              "Rainbow":"<a:Cheepcheeprainbow:1225670926188937247>",
              "Blooper":"<a:Blooper:1225650789209608313>",
              "Albino":"",
              "Squid":"",
              "Puffer":"<a:Pufferfish:1225952106884890725>",
              "Magi":"<a:Magikarp:1225953667199537172>",
              "Gold":"<a:Goldfish:1225663431399702558>",
              "Mario":"<a:CheepcheepMario:1227799195168014337>",
              "WAH":"<a:CheepcheepWAAAAAA:1227799149118754826>",
              }

fishchances = {
        (1, 2000): "Common",
        (2001, 3000): "Uncommon",
        (3001, 4000): "SMB3",
        (4001, 5250): "SMW",
        (5251, 6250): "SMB2",
        (6251, 7500): "Rare",
        (7501, 7750): "Epic",
        (7751, 7850): "Legendary",
        (7851, 7860): "Exotic",
        (7861, 7870): "Unusual",
        (7871, 7900): "Mythic",
        (7901, 8400): "Unreal",
        (8401, 9400): "WAHH",
        (9401, 10000): "???"
    }

fishpropernames= {"Green":"Green Cheep-Cheep",
                   "Red":"Red Cheep-Cheep",
                   "White":"White Cheep-Cheep",
                   "Blue": "Blue Cheep-Cheep",
                   "Rainbow": "Rainbow Cheep-Cheep",
                   "Blooper":"Blooper",
                   "Albino":"Albino Cheep-Cheep",
                   "Squid":"Squid Games",
                   "Puffer":"Pufferfish",
                   "Magi":"Magikarp",
                   "Gold":"Gold Cheep-Cheep",
                   "Mario":"Mario Cheep-Cheep",
                   "WAH":"WAAAH FISH",
                   "Goku":"Goku Cheep-Cheep",
                   "Goggles":"",
                   "VanFish":"Rip Van Fish",
                   "Trout":"Trouter"
                  }

banklevelreq = {"2":{"Coins":1000,"Red":2,"Green":2}}


def fish_roll(ranges:dict):
    # Generate a random integer between 1 and 10000 (inclusive)
    roll = random.randint(1, 10000)
    

    # Check which range the random number falls into and return the corresponding outcome
    for (start, end), outcome in ranges.items():
        if start <= roll <= end:
            return outcome