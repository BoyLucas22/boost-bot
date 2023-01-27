import discord, json, requests, os, httpx, base64, time, subprocess, fade, sys, random, platform, hashlib, threading, binascii
from pathlib import Path
import colorama
from colorama import Fore, init
from time import sleep
from datetime import datetime
from uuid import uuid4 


red = Fore.RED
green = Fore.GREEN
white = Fore.WHITE
cyan = Fore.CYAN


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

settings = json.load(open("settings.json", encoding="utf-8"))

if platform.system() == 'Windows':
    os.system('cls & title Boost Bot');                                                                                                                                                                                                                                                                                                                      os.system('cls & title If you bought this, you got scammed. Available at github.com/Pixens')
elif platform.system() == 'Linux':
    os.system('clear') 
    sys.stdout.write("\x1b]0; Boost Bot'\x07")  
elif platform.system() == 'Darwin':
    os.system("clear && printf '\e[3J'")  
    os.system('''echo "\033]0; Boost Bot\007"''')  





def validateInvite(invite):
    if '{"message": "Unknown Invite", "code": 10006}' in httpx.get(f"https://discord.com/api/v9/invites/{invite}").text:
        return False
    else:
        return True

def get_items(item):
    s = item[0]
    token = item[1]
    headers = item[2]
    profile = item[3]
    return s, token, headers, profile;                                                                                               

def find_token(token):
    if ':' in token:
        token_chosen = None
        tokensplit = token.split(":")
        for thing in tokensplit:
            if '@' not in thing and '.' in thing and len(
                    thing) > 30:
                token_chosen = thing
                break
        if token_chosen == None:
            print(f"Error finding token", Fore.RED)
            return None
        else:
            return token_chosen


    else:
        return token

def get_all_tokens(filename):
    all_tokens = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            token = line.strip()
            token = find_token(token)
            if token != None:
                all_tokens.append(token)

    return all_tokens


    
def getinviteCode(invite_input):
    if "discord.gg" not in invite_input:
        return invite_input
    if "discord.gg" in invite_input:
        invite = invite_input.split("discord.gg/")[1]
        return invite
    if "https://discord.gg" in invite_input:
        invite = invite_input.split("https://discord.gg/")[1]
        return invite

def get_super_properties():
    properties = '''{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-GB","browser_user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36","browser_version":"95.0.4638.54","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":102113,"client_event_source":null}'''
    properties = base64.b64encode(properties.encode()).decode()
    return properties

def get_fingerprint(s):
    try:
        fingerprint = s.get(f"https://discord.com/api/v9/experiments", timeout=5).json()["fingerprint"]
        return fingerprint
    except Exception as e:
        return "Error"

def get_cookies(s, url):
    try:
        cookieinfo = s.get(url, timeout=5).cookies
        dcf = str(cookieinfo).split('__dcfduid=')[1].split(' ')[0]
        sdc = str(cookieinfo).split('__sdcfduid=')[1].split(' ')[0]
        return dcf, sdc
    except:
        return "", ""

def get_proxy():
    pass


def get_headers(token):
    while True:
        s = httpx.Client(proxies=get_proxy())
        dcf, sdc = get_cookies(s, "https://discord.com/")
        fingerprint = get_fingerprint(s)
        if fingerprint != "Error":
            break
    super_properties = get_super_properties()
    headers = {
        'authority': 'discord.com',
        'method': 'POST',
        'path': '/api/v9/users/@me/channels',
        'scheme': 'https',
        'accept': '/',
        'accept-encoding': 'gzip, deflate',
        'accept-language': 'en-US',
        'authorization': token,
        'cookie': f'__dcfduid={dcf}; __sdcfduid={sdc}',
        'origin': 'https://discord.com',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-fingerprint': fingerprint,
        'x-super-properties': super_properties,
    }
    return s, headers

def validate_token(s, headers):
    check = s.get(f"https://discord.com/api/v9/users/@me", headers=headers)
    if check.status_code == 200:
        profile_name = check.json()["username"]
        profile_discrim = check.json()["discriminator"]
        profile_of_user = f"{profile_name}#{profile_discrim}"
        return profile_of_user
    else:
        return False

def do_join_server(s, token, headers, profile, invite):
    join_outcome = False;
    server_id = None
    try:
        headers["content-type"] = 'application/json'
        for i in range(15):
            try:
                join_server = requests.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={
                })
                if "captcha_sitekey" in join_server.text:
                            createTask = requests.post("https://api.capmonster.cloud/createTask", json={
                                "clientKey": settings["capmonsterKey"],
                                "task": {
                                    "type": "HCaptchaTaskProxyless",
                                    "websiteURL": "https://discord.com/channels/@me",
                                    "websiteKey": join_server.json()['captcha_sitekey']
                                }
                            }).json()["taskId"]
                            getResults = {}
                            getResults["status"] = "processing"
                            while getResults["status"] == "processing":
                                getResults = requests.post("https://api.capmonster.cloud/getTaskResult", json={
                                    "clientKey": settings["capmonsterKey"],
                                    "taskId": createTask
                                }).json()
                                time.sleep(1)
                            solution = getResults["solution"]["gRecaptchaResponse"]
                            join_server = requests.post(f"https://discord.com/api/v9/invites/{invite}", headers=headers, json={
                                "captcha_key": solution
                            }) 
                break
            except:
                pass
        server_invite = invite
        if join_server.status_code == 200:
            join_outcome = True
            server_name = join_server.json()["guild"]["name"]
            server_id = join_server.json()["guild"]["id"]
    except:
        pass
    
    return join_outcome, server_id
    

def do_boost(s, token, headers, profile, server_id, boost_id):
    boost_data = {"user_premium_guild_subscription_slot_ids": [f"{boost_id}"]}
    headers["content-length"] = str(len(str(boost_data)))
    headers["content-type"] = 'application/json'
    boosted = s.put(f"https://discord.com/api/v9/guilds/{server_id}/premium/subscriptions", json=boost_data,
                    headers=headers)
    if boosted.status_code == 201:
        return True
    else:
        return boosted.status_code, boosted.json()


def removeToken(token: str, file:str):
    with open(file, "r") as f:
        fulltokens = f.read().splitlines()
        Tokens = []
        for j in fulltokens:
            p = find_token(j)
            Tokens.append(p)
        for t in Tokens:
            if len(t) < 5 or t == token:
                Tokens.remove(t)
        open(file, "w").write("\n".join(Tokens))


def boostserver(invite: str, amount: int, expires: bool, token:str):
    if expires == True:
        file = "1m_tokens.txt"
        days = 30
    if expires == False:
        file = "3m_tokens.txt"
        days = 90
    


    data_piece = []
    all_data = []



    s, headers = get_headers(token)
    profile = validate_token(s, headers)

    data_piece = [s, token, headers, profile]
    all_data.append(data_piece)

    for data in all_data:
        s, token, headers, profile = get_items(data)
        boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=headers)
        if boost_data.status_code == 200:
            join_outcome, server_id = do_join_server(s, token, headers, profile, invite)
            if join_outcome:
                for boost in boost_data.json():
                    boost_id = boost["id"]
                    bosted = do_boost(s, token, headers, profile, server_id, boost_id)
                    if bosted:
                        print(f"{green} ✓ {white}{token} - {profile}{green} [BOOSTED] {white}")
                    else:
                        print(f"{green} ✗ {white}{token} - {profile}{red} [ERROR BOOSTING] {white}")
                        
                removeToken(token, file)
            else:
                print(f"{red} ✗ {white}{token} - {profile}{red} [ERROR JOINING] {white}")

def checktoken(token, file):

    s, headers = get_headers(token)
    profile = validate_token(s, headers)

    if profile != False:

        boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={'Authorization': token})


        if boost_data.status_code == 403:
            print(red + f" ✗ {white}{token} - {profile}{red} [LOCKED]" + white)
            removeToken(token, file)
            return False

        if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
            if boost_data.json()[0]['cooldown_ends_at'] != None:
                print(red + f" ✗ {white}{token} - {profile}{red} [USED]" + white)
                removeToken(token, file)
                return False

        if len(boost_data.json()) == 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
            print(f"{red} ✗ {white}{token} - {profile}{red} [NO NITRO]" + white)
            removeToken(token, file)
            return False

        else:
            if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                if boost_data.json()[0]['cooldown_ends_at'] == None:
                    print(f"{green} ✓ {white}{token} - {profile}{green} [WORKING]" + white)
                    return True

    else:
        print(red + f" ✗ {white}{token}{red} [INVALID]" + white)
        removeToken(token, file)
        return False

def nitrochecker():

    three_m_working = 0
    one_m_working = 0

    three_m_used = 0
    one_m_used = 0

    three_m_nonitro = 0
    one_m_nonitro = 0

    three_m_invalid = 0
    one_m_invalid = 0

    three_m_locked = 0
    one_m_locked = 0

    three_m_tokens = get_all_tokens("3m_tokens.txt")
    one_m_tokens = get_all_tokens("1m_tokens.txt")
    print("Checking 3 Months Nitro Tokens")

    if checkEmpty("3m_tokens.txt"):
        print(red + "No Stock To Check" + white)

    else:

        for token in three_m_tokens:    
            file = "3m_tokens.txt"
            s, headers = get_headers(token)
            profile = validate_token(s, headers)

            if profile != False:
                boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={'Authorization': token})

                if boost_data.status_code == 403:
                    print(red + f" ✗ {white}{token} - {profile}{red} [LOCKED]" + white)
                    removeToken(token, file)
                    three_m_locked += 1
                if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                    if boost_data.json()[0]['cooldown_ends_at'] != None:
                        print(red + f" ✗ {white}{token} - {profile}{red} [USED]" + white)
                        removeToken(token, file)
                        three_m_used += 1
                if len(boost_data.json()) == 0:
                    removeToken(token, file)
                    print(f"{red} ✗ {white}{token} - {profile}{red} [NO NITRO]" + white)
                    three_m_nonitro += 1
                else:
                    if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                        if boost_data.json()[0]['cooldown_ends_at'] == None:

                            print(f"{green} ✓ {white}{token} - {profile}{green} [WORKING]" + white)
                            three_m_working += 1
            else:
                print(red + f" ✗ {white}{token}{red} [INVALID]" + white)
                removeToken(token, file)
                three_m_invalid += 1
    print()
    print("Checking 1 Month Nitro Tokens")
    if checkEmpty("1m_tokens.txt"):
        print(red + "No Stock To Check" + white)  
    else:
        for token in one_m_tokens:    
            file = "1m_tokens.txt"
            s, headers = get_headers(token)
            profile = validate_token(s, headers)
            if profile != False:
                boost_data = s.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers={'Authorization': token})

                if boost_data.status_code == 403:
                    print(red + f" ✗ {white}{token} - {profile}{red} [LOCKED]" + white)
                    removeToken(token, file)
                    one_m_locked += 1
                if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                    if boost_data.json()[0]['cooldown_ends_at'] != None:
                        print(red + f" ✗ {white}{token} - {profile}{red} [USED]" + white)
                        removeToken(token, file)
                        one_m_used += 1
                if len(boost_data.json()) == 0:
                    removeToken(token, file)
                    print(f"{red} ✗ {white}{token} - {profile}{red} [NO NITRO]" + white)
                    one_m_nonitro += 1
                else:
                    if len(boost_data.json()) != 0 and boost_data.status_code == 200 or boost_data.status_code == 201:
                        if boost_data.json()[0]['cooldown_ends_at'] == None:

                            print(f"{green} ✓ {white}{token} - {profile}{green} [WORKING]" + white)
                            one_m_working += 1
            else:
                print(red + f" ✗ {white}{token}{red} [INVALID]" + white)
                removeToken(token, file)
                one_m_invalid += 1

def checkEmpty(file):
    mypath = Path(file)

    if mypath.stat().st_size == 0:
        return True
    else:
        return False

def isWhitelisted(ctx):
    return str(ctx.author.id) in settings["botWhitelistedId"]

def isAdmin(ctx):
    return str(ctx.author.id) in settings["botAdminId"]

activity = discord.Activity(type=discord.ActivityType.watching, name=settings["botstatus"])
bot = discord.Bot(command_prefix='$', activity=activity, status=discord.Status.online, intents=discord.Intents.all())


@bot.event
async def on_ready():
    cls()


    print(green + f"{bot.user.name} Is Online And Ready For Use." + white)

@bot.slash_command(guild_ids=[settings["guildID"]], name="ping", description="Check the bots latency")
async def ping(ctx):
    await ctx.respond(f"`{round(bot.latency * 1000)}ms`")

@bot.slash_command(guild_ids=[settings["guildID"]], name="vouch", description="Allows Customers To Leave A Vouch")
async def vouch(ctx, member: discord.Option(discord.Member, "Member to vouch.", required=True), reason: discord.Option(str, "Reason for vouch", required = True)):
    return await ctx.respond(embed=discord.Embed(description=f"{member} has been vouched by {ctx.author} for {reason}", color=0x00FF00))


@bot.slash_command(guild_ids=[settings["guildID"]], name="restock", description="Allows you to restock Nitro Tokens.")
async def restock(ctx: discord.ApplicationContext, code: discord.Option(str, "paste.ee paste link or code", required=True), type: discord.Option(int, "Type of tokens you are restocking, 3 months or 1 month", required=True)):
    if not str(ctx.author.id) in settings["botAdminId"]:
        return await ctx.respond(embed=discord.Embed(description="You must be an admin to use this command.", color=0xFF0000))
    if type != 1 and type != 3:
        return await ctx.respond(embed=discord.Embed(description="Token type can only be `1` Month or `3` Months", color=0xFF0000))
    if type == 1:
        file = "1m_tokens.txt"
    elif type == 3:
        file = "3m_tokens.txt"

    code = code.replace("https://paste.ee/p/", "")
    temp_stock = requests.get(f"https://paste.ee/d/{code}", headers={ "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}).text
    f = open(file, "a", encoding="utf-8")
    f.write(f"{temp_stock}\n")
    f.close()
    embed = discord.Embed(title=f"Stock updated",
                        description="Your stock has been updated.",
                        color=0x00FF00)
    await ctx.respond(embed=embed)    

@bot.slash_command(guild_ids=[settings["guildID"]], name="addowner", description="Adds an Owner.")
async def addowner(ctx, member: discord.Option(discord.Member, "Member to owner.", required=True)):
    if not str(ctx.author.id) in settings["botOwnerId"]:
        return await ctx.respond(embed=discord.Embed(description="You must be an owner to use this command.", color=0xFF0000))
    settings["botOwnerId"].append(str(member.id))
    json.dump(settings, open("settings.json", "w", encoding="utf-8"), indent=4)
    return await ctx.respond(embed=discord.Embed(description=f"{member.mention} has been made an Owner", color=0x00FF00))

@bot.slash_command(guild_ids=[settings["guildID"]], name="whitelist", description="Adds a staff to use the bot.")
async def whitelist(ctx: discord.ApplicationContext,user: discord.Option(discord.Member, "Member to whitelist.", required=True)):
    if not str(ctx.author.id) in settings["botAdminId"]:
        return await ctx.respond(embed=discord.Embed(description="You must be an admin to use this command.", color=0xFF0000))
    settings["botWhitelistedId"].append(str(user.id))
    json.dump(settings, open("settings.json", "w", encoding="utf-8"), indent=4)
    return await ctx.respond(embed=discord.Embed(description=f"{user.mention} has been whitelisted.", color=0x00FF00))

@bot.slash_command(guild_ids=[settings["guildID"]], name="addadmin", description="Adds an Admin.")
async def addadmin(ctx, member: discord.Option(discord.Member, "Member to whitelist.", required=True)):
    if not str(ctx.author.id) in settings["botOwnerId"]:
        return await ctx.respond(embed=discord.Embed(description="You must be a owner to use this command.", color=0xFF0000))
    settings["botAdminId"].append(str(member.id))
    json.dump(settings, open("settings.json", "w", encoding="utf-8"), indent=4)
    return await ctx.respond(embed=discord.Embed(description=f"{member.mention} has been made an Admin", color=0x00FF00))

@bot.slash_command(guild_ids=[settings["guildID"]], name="stock", description="Allows you to see the current stock.")
async def stock(ctx):
    return await ctx.respond(embed=discord.Embed(description=f"Current 3 Months Nitro Tokens Stock: `{len(open('3m_tokens.txt', encoding='utf-8').read().splitlines())}`\nCurrent 1 Month Nitro Tokens Stock: `{len(open('1m_tokens.txt', encoding='utf-8').read().splitlines())}`", color = 0x00FF00))

@bot.slash_command(guild_ids=[settings["guildID"]], name="givetokens", description="Command That Sends All Your Tokens To DMs")
async def givetokens(ctx, type: discord.Option(int, "Type of tokens you are giving, 3 months or 1 month", required=True)):
    if not str(ctx.author.id) in settings["botOwnerId"]:
        return await ctx.respond(embed=discord.Embed(description="You Must Be Owner To Use This Command.", color=0xFF0000))
    if type != 1 and type != 3:
        return await ctx.respond(embed=discord.Embed(description="Token type can only be `1` Month or `3` Months", color=0xFF0000))
    if type == 1:
        file = "1m_tokens.txt"
    elif type == 3:
        file = "3m_tokens.txt"

    user = ctx.author
    await user.send(file=discord.File(file))
    await ctx.respond(embed=discord.Embed(title='', description=f"Sending Nitro Tokens To Dms!", color=0x00FF00))

@bot.slash_command(guild_ids=[settings["guildID"]], name="clearstock", description="Allows you to clear all stock of nitro tokens.") 
async def clearstock(ctx):
    if not str(ctx.author.id) in settings["botOwnerId"]:
        return await ctx.respond(embed=discord.Embed(description="You Must Be Owner To Use This Command.", color=0xFF0000))
    
    c = open("3m_tokens.txt", "w")
    c.write("")
    
    f = open("1m_tokens.txt", "w")
    f.write("")
    
    return await ctx.respond(embed=discord.Embed(description=f"Successfully cleared 3 Months and 1 Month nitro tokens stock", color=0x00FF00))


@bot.slash_command(guild_ids=[settings["guildID"]], name="boost",
                    description="Allows you to boost a server with Nitro Tokens.")
async def boost(ctx: discord.ApplicationContext,
                    invite: discord.Option(str, "Discord invite code.", required=True),
                    amount: discord.Option(int, "Number of times to boost.", required=True), 
                    days: discord.Option(int, "Number of days you want to boost for, 90 days or 30 days", required=True)):
    if not str(ctx.author.id) in settings["botWhitelistedId"]:
        return await ctx.respond(embed=discord.Embed(description="You must be whitelisted to use this command.", color=0xFF0000))

    if days != 90 and days != 30:
        return await ctx.respond(embed=discord.Embed(description="Number of Days can only be `30` Days or `90` Days", color=0xFF0000))
    if days == 30:
        file = "1m_tokens.txt"

    elif days == 90:
        file = "3m_tokens.txt"


    if checkEmpty(file) == True:
        return await ctx.respond(embed=discord.Embed(description="No Stock. Use /restock to upload tokens to the stock.", color=0xFF0000))
    
    invite = getinviteCode(invite)
    valid_invite = validateInvite(invite)
    if valid_invite == False:
        return await ctx.respond(embed=discord.Embed(description="Invalid Invite", color=0xFF0000))
    
    if amount % 2 != 0:
        return await ctx.respond(embed=discord.Embed(description="Amount must be even.", color=0xFF0000))
        
    if amount/2 > len(open(file , encoding='utf-8').read().splitlines()):
        return await ctx.respond(embed=discord.Embed(description="Not enough stock.Use /restock to upload more tokens to the stock.", color=0xFF0000))
    
    EXP = True
    if days == 90:
        EXP = False

    await ctx.respond(embed=discord.Embed(description=f"Invite - discord.gg/{invite}\nAmount - {amount}\nDays - {days}", color=0x00FF00))
    threads = []
    no_working = False
    r = 0
    numTokens = int(amount/2)
    all_tokens = get_all_tokens(file)
    tokens_to_use = []
    print(green + "Looking for working tokens" + white)
    while len(tokens_to_use) != numTokens:
        try:
            token = all_tokens[r]
            if checktoken(token, file) == True:
                tokens_to_use.append(token)
            r += 1
        except IndexError:
            print(red + "Not Enough Working Tokens in Stock" + white)
            no_working = True
            break
    
    if no_working == True:
        return await ctx.respond(embed=discord.Embed(description="Not Enough **working** tokens in stock. Use /restock to upload working tokens to the stock.", color=0xFF0000))
        cls()
        print(green + f"{bot.user.name} Is Online And Ready For Use." + white)


    else:
        time.sleep(2)
        cls()

        print(green + "Starting Boosts" + white)
        start = time.time()
        for i in range(numTokens):
            token = tokens_to_use[i]
            t = threading.Thread(target=boostserver, args=(invite, amount, EXP, token))
            t.daemon = True
            threads.append(t)
        for i in range(numTokens):
            threads[i].start()
            
        for i in range(numTokens):
            threads[i].join()
 
        end = time.time()
        
    time_taken = round(end-start)
    cls()

    print(green + f"{bot.user.name} Is Online And Ready For Use." + white)
    return await ctx.respond(embed=discord.Embed(title='', description=f"Successfully Boosted discord.gg/{invite}, {amount} times in {time_taken} seconds", color=0x00FF00))


@bot.slash_command(guild_ids=[settings["guildID"]], name="help", description="Allows you to view all the commands in the bot.")
async def help(ctx):
    return await ctx.respond(embed=discord.Embed(description=f"\n➜`/ping` | View The Bots Latency!\n➜`/clearstock` | Clears stock of 3 Months and 1 Month nitro tokens\n➜`/addadmin`| Allows The User To Use Most of The Bot!\n➜`/whitelist` | Whitelists A User To Use The Bot!\n➜`/addowner` | Add Someone To The Owners List!\n➜`/boost` | Boost Any Discord In Seconds!\n➜`/givetokens` | Allows Administration To Give Nitro Tokens\n➜`/help` | Displays This Message\n➜`/restock` | Restock Nitro Tokens using Paste.ee\n➜`/stock` | View Current Nitro Token Stock\n➜`/vouch` | Allows Customers To Leave A Vouch", color=0x00FF00))


bot.run(settings["botToken"])
