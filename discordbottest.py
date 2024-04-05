import discord
from discord.ext import commands
import time
import random
import datafunctions
import content
import os
from discord import app_commands
TOKEN = os.environ.get("bottoken")

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!",intents=intents)
workoptions = ["Pipe Cleaner","King Koopa's Underling","Koopa Smasher (but not in a gay way)","Waa Inspector","Plumber","Carpenter"]
workcooldowns = {}
gamblecooldowns= {}
robcooldowns = {}

# Initiate Bot stuff
@client.event
async def on_ready():
    print("Bots ready")
    synced = await client.tree.sync()
    print (f"Synced {len(synced)} commands")




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


    if robcheck == 1:
        robstatus = True
    if robstatus and victimbalance > 0:
        
        robembed = discord.Embed(title = "Robbery Success!",description=f"Successfuly stole {content.coinemoji} {victimbalance//10} from <@{recep}>")
        robembed.set_image(url="https://i.ytimg.com/vi/dISuBAGxw4w/maxresdefault.jpg")
        await interaction.response.send_message(embed=robembed)
        thiefbalance += victimbalance // 10
        victimbalance -= victimbalance // 10
        datafunctions.updatecoins(thiefbalance,useridentify)
        datafunctions.updatecoins(victimbalance,recepid)
    
    elif victimbalance < 0:
        robembed = discord.Embed(title="Robbery Failed",description="Victim is to poor to be robbed. They gotta get they money up not funny up")
        await interaction.response.send_message(embed=robembed)
    else:
        robembed = discord.Embed(title="Robbery Failed",description="You were to slow and they got away")
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
        if time_passed < 300:
            # Calculate remaining time
            remaining_time = 300 - time_passed
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

    async def button_callback(interaction):
        # Assuming this inner function can access 'useridentify' directly
        # Recalculate the balance in case it has changed
        new_balance = datafunctions.checkcoins(useridentify)
        new_embed = discord.Embed(title=f"{content.coinemoji}Bank Balance:", description=f"{content.coinemoji}{str(new_balance)}", color=0x4dff4d)
        # Acknowledge the interaction by editing the message with the new embed
        await interaction.response.edit_message(embed=new_embed, view=view)

    # Button creation with the callback function
    refreshbutton = discord.ui.Button(style=discord.ButtonStyle.primary, label="Check Again", custom_id="check_balance")
    refreshbutton.callback = button_callback  # Assign the callback

    bankembed = discord.Embed(title=f"{content.coinemoji}Bank Balance:", description=f"{content.coinemoji}{str(balance)}", color=0x4dff4d)
    view = discord.ui.View()
    view.add_item(refreshbutton)
    await interaction.response.send_message(embed=bankembed, view=view)



@client.tree.command()
async def register(interaction: discord.Interaction):
    useridentify = interaction.user.id
    datafunctions.userdbcheck(useridentify)
    regembed = discord.Embed(title="New User Registration",description = "Congrats! You are now Registerd",color=content.purple)
    regembed.set_image(url='https://www.kotaku.com.au/wp-content/uploads/2018/06/15/umkr4qwixrkw7txyv40m.jpg?quality=75&w=640&h=360&crop=1')
    await interaction.response.send_message(embed=regembed)



@client.tree.command()
@app_commands.describe(recipient = "Enter person you want to transfer coins to",transferamount = "Enter amount to transfer")
async def transfer(interaction:discord.Interaction, recipient: discord.Member,transferamount:int):
    sender = interaction
    datafunctions.userdbcheck(sender.user.id)
    datafunctions.userdbcheck(recipient.id)
    sender_balance = datafunctions.checkcoins(sender.user.id)
    recipient_balance = datafunctions.checkcoins(recipient.id)
    fail_embed = discord.Embed(title="Transfer Failed", description="Transfer has failed since you don't have enough money to transfer the requested amount.")
    fail_embed.set_image(url='https://i.redd.it/9bpmrcwpa7ra1.jpg')
    
    if transferamount <= 0:
        await interaction.response.send_message("Please enter a valid amount to transfer.")
        return

    if sender_balance < transferamount:
        await interaction.response.send_message(embed=fail_embed)
    else:
        sender_balance -= transferamount
        recipient_balance += transferamount
        datafunctions.updatecoins(sender_balance, sender.user.id)
        datafunctions.updatecoins(recipient_balance, recipient.id)
        transfer_embed = discord.Embed(title="Transfer Success!", description=f"You have transferred {content.coinemoji} {transferamount} to {recipient.mention}!")
        await interaction.response.send_message(embed=transfer_embed)
    






client.run(TOKEN)
