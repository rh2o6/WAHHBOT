#Discord API
import discord
from discord.ext import commands

#Standard Module Imports
import time
import random

#File Imports
import datafunctions
import content


import os
from discord import app_commands
TOKEN = os.environ.get("bottoken") #String for Bot Token



intents = discord.Intents.all()
client = commands.Bot(command_prefix="!",intents=intents)

workoptions = ["Pipe Cleaner","King Koopa's Underling","Koopa Smasher (but not in a gay way)","Waa Inspector","Plumber","Carpenter"]
workcooldowns = {}
gamblecooldowns= {}
gamblecooldowns = {}

# Initiate Bot stuff
@client.event
async def on_ready():
    print("Bots ready")
    synced = await client.tree.sync()
    print (f"Synced {len(synced)} commands")


class depositModal(discord.ui.Modal,title="Bank Deposit"):
    depositamount = discord.ui.TextInput(label="Enter amount to deposit",placeholder="Enter money here",style=discord.TextStyle.short)

    async def on_submit(self,interaction:discord.Interaction):
        if not(self.depositamount.value.isnumeric()):
            await interaction.response.send_message("Invalid Amount, Please enter a valid amount")
        depositamt = int(self.depositamount.value)
        useridentify = interaction.user.id
        usercoins = datafunctions.checkcoins(useridentify)
        currentbal = datafunctions.checkbankbal(useridentify)
        banklvl = datafunctions.checkbanklvl(useridentify)
        newbal = currentbal + depositamt
        if newbal > content.maxbankbalance[banklvl]:
            await interaction.response.send_message("Deposit will exceed bank capacity, try again with a lower amount")
        elif depositamt > usercoins:
            await interaction.response.send_message("Deposit failed, not enough coins to depoist that amount")

        elif depositamt < 0:
            await interaction.response.send_message("Invalid Amount, Please enter a valid amount")

        else:
            newcoinsval = usercoins - depositamt
            datafunctions.updatecoins(newcoinsval,useridentify)
            datafunctions.updatebank(newbal,useridentify)

            await interaction.response.send_message("Deposit Successful")


class withdrawModal(discord.ui.Modal,title="Bank Withdraw"):
    withdrawamt = discord.ui.TextInput(label="Enter amount to withdraw",placeholder="Enter money here",style=discord.TextStyle.short)

    async def on_submit(self,interaction:discord.Interaction):
        useridentify = interaction.user.id

        if not(self.withdrawamt.value.isnumeric()):
            await interaction.response.send_message("Invalid Amount, Please enter a valid amount")


        withdrawamt = int(self.withdrawamt.value)
        currentbal = datafunctions.checkbankbal(useridentify)
        banklvl = datafunctions.checkbanklvl(useridentify)
        usercoins = datafunctions.checkcoins(useridentify)
        newbal = currentbal - withdrawamt
        if newbal < 0:
            await interaction.response.send_message("Withdraw failed, insufficient balance to withdraw amount")
        
        elif withdrawamt < 0:
            await interaction.response.send_message("Invalid Amount, Please enter a valid amount")

        else:
            datafunctions.updatebank(newbal,useridentify)
            usercoins += withdrawamt
            datafunctions.updatecoins(usercoins,useridentify)
        
            await interaction.response.send_message("Withdrawl Successful")


@client.tree.command()
@app_commands.describe(robvictim="Enter rob target")
async def rob(interaction:discord.Interaction, robvictim:discord.Member):
    datafunctions.userdbcheck(interaction.user.id)
    recep = robvictim
    recepid = recep.id
    datafunctions.userdbcheck(recepid)
    robstatus = False
    robcheck = random.randint(1,4)
    useridentify = interaction.user.id
    thiefbalance = datafunctions.checkcoins(useridentify)
    victimbalance = datafunctions.checkcoins(recepid)
    if useridentify in gamblecooldowns:
        time_passed = time.time() - gamblecooldowns[useridentify]
        if time_passed < content.GAMBLECD:
            # Calculate remaining time
            remaining_time = content.GAMBLECD - time_passed
            # Format remaining time into minutes and seconds
            minutes, seconds = divmod(int(remaining_time), 60)
            await interaction.response.send_message(f"You're on cooldown. Please wait {minutes} minutes and {seconds} seconds before attempting to rob again.")
            return
        else:
            # If cooldown is over, delete the user from cooldowns
            del gamblecooldowns[useridentify]

    if robcheck == 1:
        robstatus = True
    if robstatus and victimbalance > 0:
        
        robembed = discord.Embed(title = "Robbery Success!",description=f"Successfuly stole {content.coinemoji} {victimbalance//10} from {recep.mention}")
        robembed.set_image(url="https://i.ytimg.com/vi/dISuBAGxw4w/maxresdefault.jpg")
        await interaction.response.send_message(embed=robembed)
        thiefbalance += victimbalance // 10
        victimbalance -= victimbalance // 10
        datafunctions.updatecoins(thiefbalance,useridentify)
        datafunctions.updatecoins(victimbalance,recepid)
        gamblecooldowns[useridentify] = time.time()
    
    elif victimbalance < 0:
        robembed = discord.Embed(title="Robbery Failed",description="Victim is to poor to be robbed. They gotta get they money up not funny up")
        await interaction.response.send_message(embed=robembed)
    else:
        robembed = discord.Embed(title="Robbery Failed",description="You were to slow and they got away")
        gamblecooldowns[useridentify] = time.time()
        await interaction.response.send_message(embed=robembed)

    return



@client.tree.command()
@app_commands.describe(betamt = "Enter amount to gamble")
async def gamble(interaction:discord.Interaction,betamt:int):
    useridentify = interaction.user.id
    datafunctions.userdbcheck(useridentify)
    data = datafunctions.checkcoins(useridentify)
    

    if betamt < 0:
        await interaction.response.send_message("Invalid bet amount")

    elif  data < betamt:
        await interaction.response.send_message("To poor to gamble")
        return


    if useridentify in gamblecooldowns:
        time_passed = time.time() - gamblecooldowns[useridentify]
        if time_passed < content.GAMBLECD:
            # Calculate remaining time
            remaining_time = content.GAMBLECD - time_passed
            # Format remaining time into minutes and seconds
            minutes, seconds = divmod(int(remaining_time), 60)
            await interaction.response.send_message(f"You're on cooldown. Please wait {minutes} minutes and {seconds} seconds before attempting to gamble again.")
            return
        else:
            # If cooldown is over, delete the user from cooldowns
            del gamblecooldowns[useridentify]



    roll = random.randint(1,2)
    dictbool = {True:"Won",False:"Lost"}
    if roll == 1:
        status = False
    else:
        status = True

    if status == True:
        final = data + betamt*2
        mystr = f"You Won {content.coinemoji}{betamt*2}"
    else:
        status == False
        final = data - betamt
        mystr = f"You Lost {content.coinemoji}{betamt}"
    
    embed = discord.Embed(title="Rolling...",description=f'{mystr}',color=0x4dff4d)
    embed.set_footer(text="Did you know that 99%, of gamblers give up before a jackpot!")
    embed.set_image(url = "https://static.wikia.nocookie.net/siivagunner/images/e/e0/Waluigi-Pinball.png/revision/latest?cb=20200515232537")
    datafunctions.updatecoins(final,useridentify)
    gamblecooldowns[useridentify] = time.time()
    await interaction.response.send_message(embed=embed)



@client.tree.command(name="work")
async def work(interaction:discord.Interaction):
    useridentify = interaction.user.id
    datafunctions.userdbcheck(useridentify)
    existingcoins = datafunctions.checkcoins(useridentify)
    jobselect = random.choice(workoptions)
    earnings = random.randint(20,50)
    if useridentify in workcooldowns:
        time_passed = time.time() - workcooldowns[useridentify]
        if time_passed < content.WORKCD:
            # Calculate remaining time
            remaining_time = content.WORKCD - time_passed
            # Format remaining time into minutes and seconds
            minutes, seconds = divmod(int(remaining_time), 60)
            await interaction.response.send_message(f"You're on cooldown. Please wait {minutes} minutes and {seconds} seconds before working again.")
            return
        else:
            # If cooldown is over, delete the user from cooldowns
            del workcooldowns[useridentify]
    workstr = f"You made <a:Coin:1224446854708727908>{earnings}"
    workembed = discord.Embed(title="Off to work!",description=workstr,color =0x4dff4d)
    workembed.set_footer(text=f"Worked a shift as a {jobselect}")
    await interaction.response.send_message(embed=workembed)
    datafunctions.updatecoins(earnings+existingcoins, useridentify)
    currentshifts = datafunctions.checktotalshifts(useridentify)
    if currentshifts == None:
        currentshifts = 0
    currentshifts += 1
    
    datafunctions.workadjust(currentshifts,useridentify)
    workcooldowns[useridentify] = time.time()
    

@client.tree.command()
async def balance(interaction: discord.Interaction):
    useridentify = interaction.user.id
    datafunctions.userdbcheck(useridentify)
    balance = datafunctions.checkcoins(useridentify)
    bankbalance = datafunctions.checkbankbal(useridentify)
    banklvl = datafunctions.checkbanklvl(useridentify)

    async def refresh_callback(interaction):
        # Assuming this inner function can access 'useridentify' directly
        # Recalculate the balance in case it has changed

        if interaction.user.id == useridentify:
            new_balance = datafunctions.checkcoins(useridentify)
            newbankbal = datafunctions.checkbankbal(useridentify)
            new_embed = discord.Embed(title=f"{content.coinemoji}{interaction.user} Currency:", description=f"**Coins**:\n{content.coinemoji}{str(new_balance)} \n **Bank Balance**: \n{newbankbal}/{content.maxbankbalance[banklvl]}\n**Bank Level**:{banklvl}", color=0x4dff4d)
            # Acknowledge the interaction by editing the message with the new embed
            await interaction.response.edit_message(embed=new_embed, view=view)
        else:
           await interaction.response.send_message("Not for you!",ephemeral=True)


    async def deposit_callback(interaction):
        if interaction.user.id == useridentify:
            await interaction.response.send_modal(depositModal())
        else:
           await interaction.response.send_message("Not for you!",ephemeral=True)
    
    async def withdraw_callback(interaction):
        if interaction.user.id == useridentify:
            await interaction.response.send_modal(withdrawModal())
        else:
            await interaction.response.send_message("Not for you!",ephemeral=True)
            
       

    # Button creation with the callback function
    refreshbutton = discord.ui.Button(style=discord.ButtonStyle.primary, label="Refresh", custom_id="check_balance")
    refreshbutton.callback = refresh_callback  # Assign the callback

    depositbutton = discord.ui.Button(style=discord.ButtonStyle.blurple,label="Deposit")
    depositbutton.callback = deposit_callback

    withdrawbutton = discord.ui.Button(style=discord.ButtonStyle.blurple,label="Withdraw")
    withdrawbutton.callback = withdraw_callback


    bankembed = discord.Embed(title=f"{content.coinemoji}{interaction.user} Currency:", description=f"**Coins**:\n{content.coinemoji}{str(balance)} \n **Bank Balance**: \n{bankbalance}/{content.maxbankbalance[banklvl]}\n **Bank Level**: {banklvl}", color=0x4dff4d)
    view = discord.ui.View()
    view.add_item(refreshbutton)
    view.add_item(depositbutton)
    view.add_item(withdrawbutton)
    await interaction.response.send_message(embed=bankembed, view=view)



@client.tree.command()
async def register(interaction: discord.Interaction):
    useridentify = interaction.user.id
    datafunctions.userdbcheck(useridentify)
    regembed = discord.Embed(title="New User Registration",description = "Congrats! You are now Registerd",color=content.purple)
    regembed.set_image(url='https://www.kotaku.com.au/wp-content/uploads/2018/06/15/umkr4qwixrkw7txyv40m.jpg?quality=75&w=640&h=360&crop=1')
    await interaction.response.send_message(embed=regembed)


@client.tree.command()
async def fish(interaction: discord.Interaction):
    useridentify = interaction.user.id
    catchornot = random.randint(1,2)
    rodtype = datafunctions.checkrod(useridentify)
    if catchornot == 1:
        failembed = discord.Embed(title="Caught Nothing",description="Unlucky, Nothing bit...")
        await interaction.response.send_message(embed=failembed)

    else:
        fishtier = content.fish_roll(content.fishchances)
        fishcaught = random.choice(content.fishcategories[fishtier])
        #quant = datafunctions.checkfishamt(useridentify,fishcaught)
        #quant += 1
        #datafunctions.updatefishbucket(useridentify,fishcaught,quant)
        await interaction.response.send_message(f"Congrats You Caught a {content.fishemojis[fishcaught]}{content.fishpropernames[fishcaught]} of {fishtier} Rarity with your {rodtype}!")



@client.tree.command()
@app_commands.describe(recipient = "Enter person you want to transfer coins to",transferamount = "Enter amount to transfer")
async def transfer(interaction:discord.Interaction, recipient: discord.Member,transferamount:int):
    sender = interaction
    datafunctions.userdbcheck(sender.user.id)
    datafunctions.userdbcheck(recipient.id)
    sender_balance = datafunctions.checkcoins(sender.user.id)
    recipient_balance = datafunctions.checkcoins(recipient.id)
    mystr = ''
    
    if transferamount <= 0:
        mystr ='Please enter a valid amount of coins to transfer'
        fail_embed = discord.Embed(title="Transfer Failed", description=mystr)
        fail_embed.set_image(url='https://i.redd.it/9bpmrcwpa7ra1.jpg')
        await interaction.response.send_message(embed=fail_embed)
        return

    if sender_balance < transferamount:
        mystr = "Transfer has failed since you don't have enough money to transfer the requested amount."
        fail_embed = discord.Embed(title="Transfer Failed", description=mystr)
        fail_embed.set_image(url='https://i.redd.it/9bpmrcwpa7ra1.jpg')
        await interaction.response.send_message(embed=fail_embed)
    else:
        sender_balance -= transferamount
        recipient_balance += transferamount
        datafunctions.updatecoins(sender_balance, sender.user.id)
        datafunctions.updatecoins(recipient_balance, recipient.id)
        transfer_embed = discord.Embed(title="Transfer Success!", description=f"You have transferred {content.coinemoji} {transferamount} to {recipient.mention}!")
        await interaction.response.send_message(embed=transfer_embed)
    

    useridentify = interaction.user.id
    currentbal = datafunctions.checkbankbal(useridentify)
    banklvl = datafunctions.checkbanklvl(useridentify)
    usercoins = datafunctions.checkcoins(useridentify)
    newbal = currentbal - withdrawamt
    if newbal < 0:
        await interaction.repsonse.send_message("Withdraw failed, insufficient balance to withdraw amount")
    else:
        datafunctions.updatebank(newbal,useridentify)
        usercoins += withdrawamt
        datafunctions.updatecoins(usercoins,useridentify)
        
        await interaction.response.send_message("Withdrawl Successful")






client.run(TOKEN)
