# import discord library
import discord
# Imports commands
from discord.ext import commands
# Allows the code to retrieve data online
from datetime import datetime

LastKnownCodes = []

codes = {
    "1/7": ["18377506", "44985103", "24232724"],
    "1/14": ["68562307", "40602131", "31631987"],
    "1/21": ["17847687", "66192931", "57236425"],
    "1/28": ["04480388", "61083483", "64963683"],
    "2/4": ["77627521", "72337451", "64711555"],
    "2/11": ["89571844", "69022271", "78351129"],
    "2/18": ["43622457", "79424961", "13605405"],
    "2/25": ["89749398", "54136257", "56648960"],
    "3/3": ["59586541", "99725388", "00763938"],
    "3/10": ["09696878", "11112801", "44472900"],
    "3/17": ["05838035", "55293630", "69593915"],
    "3/24": ["69992662", "96107371", "12168475"],
    "3/31": ["12914939", "99286825", "35775253"],
    "4/7": ["84138947", "67623748", "51239897"],
    "4/14": ["63030899", "94112469", "93284143"],
    "4/21": ["61436701", "36758567", "79473176"],
    "4/28": ["82785065", "83050020", "30558622"],
    "5/5": ["32560743", "16321828", "76235245"],
    "5/12": ["61952546", "57631629", "58612449"],
    "5/19": ["44308932", "31814079", "57367175"],
    "5/26": ["24635428", "25029246", "08820735"],
    "6/2": ["94661753", "61618540", "89438601"],
    "6/9": ["59192086", "62667842", "05091983"],
    "6/16": ["99357501", "62285039", "45394000"],
    "6/23": ["48880142", "20284491", "38280383"],
    "6/30": ["31780265", "37559184", "86815399"],
    "7/7": ["32078894", "54410637", "90574792"],
    "7/14": ["80305790", "90690965", "99101593"],
    "7/21": ["34014750", "70792083", "27323149"],
    "7/28": ["89778792", "30910055", "70360840"],
    "8/4": ["06818772", "96391442", "77837886"],
    "8/11": ["74293332", "87904708", "39313471"],
    "8/18": ["61285272", "43893933", "92156152"],
    "8/25": ["92387092", "95631813", "73412010"],
    "9/1": ["34959739", "33701503", "98469385"],
    "9/8": ["45836295", "61311889", "17267573"],
    "9/16": ["24040350", "48194248", "07822996"],
    "9/23": ["80919313", "20605909", "04526567"],
    "9/30": ["66835244", "06206397", "17189221"],
    "10/7": ["04490528", "45988885", "56178122"],
    "10/14": ["08322063", "53088112", "32058791"],
    "10/21": ["54403282", "06979747", "41185730"],
    "10/28": ["82272317", "29555318", "89672304"],
    "11/4": ["89677226", "34236893", "93599937"],
    "11/11": ["30232798", "82294527", "49228524"],
    "11/18": ["45721821", "51798126", "05491289"],
    "11/25": ["37148779", "60715190", "46479683"],
    "12/2": ["87811875", "52407824", "23769267"],
    "12/9": ["48428717", "84728291", "39150256"],
    "12/16": ["61643305", "87894789", "95969349"],
    "12/23": ["75272864", "23462604", "39049838"],
    "12/30": ["44646696", "44002093", "22098388"],

}


class User_F76_NukeCodes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="codes", aliases=["nukecodes", "nukecode", "nc", "code", "cc"])
    async def codes(self, ctx):
        if ctx.guild:
            print(f"A user requested \"nuke codes\" in \"{ctx.guild.name}\" ")
        else:
            print("A user requested \"nuke codes\" in a private message")

        now = datetime.now()
        LastDate = None
        for date in codes.keys():
            split_date = date.split("/")
            d1 = datetime(now.year, int(split_date[0]), int(split_date[1]))
            d2 = datetime(now.year, now.month, now.day)

            if d1 > d2:
                break
            LastDate = date
        code_response = f'Nuke codes reset every Wednesday\nat 5 PM PST / 12 Midnight UTC\n\n' \
                        f'**Alpha**: {codes[LastDate][0]}\n' \
                        f'**Bravo**: {codes[LastDate][1]}\n' \
                        f'**Charlie**: {codes[LastDate][2]}'

        # Discords own embed.
        if ctx.invoked_with.lower() == "cc":
            await ctx.send(code_response)
        else:
            embed = discord.Embed(color=0xe7e9d3, title="Fallout 76 Nuclear Codes")

            embed.set_footer(text="Special thanks to https://nukacrypt.com/ for providing codes for all these years!")
            # embed.set_image(url="")
            embed.set_thumbnail(url="https://cdn.edb.tools/MODUS_Project/Services/76/Logos/NukeCodesLogo.png")

            embed.add_field(name="This week's nuclear codes",
                            value=code_response)

            # embed.add_field(name="Want nuke codes in your own server?",
            #                 value="Add MODUS to your server! [Click here to read more](https://discord.com/oauth2/authorize?client_id=532591107553624084&permissions=1879960790&scope=bot)",
            #                 inline=False)

            await ctx.send(embed=embed)

# ends the extension
def setup(client):
    client.add_cog(User_F76_NukeCodes(client))
