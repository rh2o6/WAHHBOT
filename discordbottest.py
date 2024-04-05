import discord
from discord.ext import commands
import time
import random
import datafunctions
import content
import os
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




@client.command()
async def rob(ctx, recipient:discord.Member):
    datafunctions.userdbcheck(ctx.message.author.id)
    recep = recipient
    recepid = recep.id
    datafunctions.userdbcheck(recepid)
    robstatus = False
    robcheck = random.randint(1,4)
    useridentify = ctx.message.author.id
    thiefbalance = datafunctions.checkcoins(useridentify)
    victimbalance = datafunctions.checkcoins(recepid)


    if robcheck == 1:
        robstatus = True
    if robstatus and victimbalance > 0:
        
        robembed = discord.Embed(title = "Robbery Success!",description=f"Successfuly stole {content.coinemoji} {victimbalance//10} from <@{recep}>")
        robembed.set_image(url="https://i.ytimg.com/vi/dISuBAGxw4w/maxresdefault.jpg")
        await ctx.send(embed=robembed)
        thiefbalance += victimbalance // 10
        victimbalance -= victimbalance // 10
        datafunctions.updatecoins(thiefbalance,useridentify)
        datafunctions.updatecoins(victimbalance,recepid)
    
    else:
        await ctx.send("Robbery attempt failed, try again")
    return

@client.command()
async def checkworkcd(ctx):
    user_id = ctx.message.author.id
    await ctx.send(workcooldowns[user_id])


@client.command()
async def gamble(ctx):
    useridentify = ctx.message.author.id
    datafunctions.userdbcheck(useridentify)
    data = datafunctions.checkcoins(useridentify)

    if  data < 50:
        await ctx.send("To poor to gamble")
        return

    data -= 10
    roll = random.randint(-100,100)
    dictbool = {True:"Won",False:"Lost"}
    if roll < 0:
        status = False
    else:
        status = True
    mystr = f"You {dictbool[status]} {content.coinemoji}{abs(roll)}"
    embed = discord.Embed(title="Rolling...",description=mystr,color=0x4dff4d)
    #embed.set_author(name="Skibidi Toilet")
    #embed.add_field(name="",value = "Field 1 Description!",inline = True)
    embed.set_footer(text="Did you know that 99%, of gamblers give up before a jackpot!")
    embed.set_image(url = "https://static.wikia.nocookie.net/siivagunner/images/e/e0/Waluigi-Pinball.png/revision/latest?cb=20200515232537")
    await ctx.send(embed=embed)
    final = data + roll
    datafunctions.updatecoins(final,useridentify)



@client.command()
async def work(ctx):
    useridentify = ctx.message.author.id
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
            await ctx.send(f"You're on cooldown. Please wait {minutes} minutes and {seconds} seconds before working again.")
            return
        else:
            # If cooldown is over, delete the user from cooldowns
            del workcooldowns[useridentify]
    workstr = f"You made <a:Coin:1224446854708727908>{earnings}"
    workembed = discord.Embed(title="Off to work!",description=workstr,color =0x4dff4d)
    workembed.set_footer(text=f"Worked a shift as a {jobselect}")
    await ctx.send(embed=workembed)
    datafunctions.updatecoins(earnings+existingcoins, useridentify)
    currentshifts = datafunctions.checktotalshifts(useridentify)
    if currentshifts == None:
        currentshifts = 0
    currentshifts += 1
    
    datafunctions.workadjust(currentshifts,useridentify)
    workcooldowns[useridentify] = time.time()
    

@client.command()
async def balance(ctx):
    useridentify = ctx.message.author.id
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
    await ctx.send(embed=bankembed, view=view)



@client.command()
async def register(ctx):
    useridentify = ctx.message.author.id
    datafunctions.userdbcheck(useridentify)
    regembed = discord.Embed(title="New User Registration",description = "Congrats! You are now Registerd",color=content.purple)
    regembed.set_image(url='https://www.kotaku.com.au/wp-content/uploads/2018/06/15/umkr4qwixrkw7txyv40m.jpg?quality=75&w=640&h=360&crop=1')
    await ctx.send(embed=regembed)



@client.command()
async def transfer(ctx, amount: int, recipient: discord.Member):
    sender = ctx.author
    datafunctions.userdbcheck(sender.id)
    datafunctions.userdbcheck(recipient.id)
    sender_balance = datafunctions.checkcoins(sender.id)
    recipient_balance = datafunctions.checkcoins(recipient.id)
    fail_embed = discord.Embed(title="Transfer Failed", description="Transfer has failed since you don't have enough money to transfer the requested amount.")
    fail_embed.set_image(url='https://i.redd.it/9bpmrcwpa7ra1.jpg')
    
    if amount <= 0:
        await ctx.send("Please enter a valid amount to transfer.")
        return

    if sender_balance < amount:
        await ctx.send(embed=fail_embed)
    else:
        sender_balance -= amount
        recipient_balance += amount
        datafunctions.updatecoins(sender_balance, sender.id)
        datafunctions.updatecoins(recipient_balance, recipient.id)
        transfer_embed = discord.Embed(title="Transfer Success!", description=f"You have transferred {content.coinemoji} {amount} to {recipient.mention}!")
        await ctx.send(embed=transfer_embed)
    






client.run(TOKEN)
