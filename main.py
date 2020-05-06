from prepare import *
import asyncio
import datetime
import discord
from discord.ext.commands import Bot


#### Run
#create token.md and paste bot token into.
token = read_token()

#ID of user who is send by bot when time has come
ID = int(open('myAccountID.md','r').readlines()[0])

client = Bot(command_prefix='!', description='My shedule.')



#### Discord client

@client.event
async def on_ready():
    print('On mic, Check Check 1 2 1 2\n')


@client.event
async def on_message(message):
    s = '!help,!h,!list,!l,!add,!a,!remove,!rm,!setup,!s'.split(',')
    if message.content[0] == '!' and message.content.split(' ')[0] not in s:
        await message.channel.send('```Type !help for more details.```')
        
    await client.process_commands(message)


@client.command(name = 'list', aliases = ['l'])
async def list(ctx):
    """Show my schedule."""

    show = get_list()
    await ctx.send("```Number of work: {}.\n\n{}```".format(show['cnt'], show['list']))


@client.command(name = 'add', aliases = ['a'])
async def add(ctx, *, arg):
    """Add new schedules to list.
       
        <content> <day>/<month> <hour>:<minute> [-w <week>] [-m <month>] [-r <alarm_before>] [-n <note>]

        Compulsory:
            content         Alarm for?
            month/day       On day ?
            hour:minutes    When ? (24-hour format)

        Optional:
            -w week             repeat in next n (int) weeks. Default is 0.
            -m month            repeat in next n (int) months. Default is 0.

            CAUTION: Only week or month. If both is exist, bot use week first.

            -b before           ring before n (int) minutes. Default is 5.
            -n note             note for this shedule
        
        Example:
            !add test 30/4 11:30 -w 1 -m 2 -b 3 -n abcxyz
    """

    add_list(detect_add(arg.strip()))
    await ctx.send("```Added.```")


@client.command(name = 'remove', aliases = ['rm'])
async def remove(ctx, order: str):
    """Remove a schedule from list.
        CAUTION: CANNOT UNDO.
        
        Example:
            !rm <order> / <all>
    """

    if order == 'all':
        await ctx.send('Sure? (10s) Y/N:')

        def check(message):
            return message.author == ctx.author
        
        try:
            msg = await client.wait_for('message', check = check, timeout = 10 )
        except asyncio.TimeoutError:
            await ctx.send("```Timeout!```")
            return

        rep = msg.content.upper()
        if rep == 'N':
            await ctx.send("```Out!```")
            return
        elif rep == 'Y':
            while get_list()['cnt']: del_list(0)
            await ctx.send("```Deleted.```")
            return
        else:
            await ctx.send("```Wrong key. Out!```")
            return

    data = get_list()
    if int(order) > data['cnt'] - 1:
        await ctx.send("```Order is not in list.```")
        return

    del_list(int(order))
    await ctx.send("```Deleted.```")


@client.command(name = 'setup', aliases = ['s'])
async def setup(ctx, *, arg):
    """Change optional setting for ordered schedule.
        <order> [-w <week>] [-m <month>] [-r <alarm_before>] [-n <note>]

        Compulsory:
            order               Which is the order need to repair?

        Optional:
            -w week             repeat per week in n (int) weeks. Default is 0.
            -m month            repeat per month in n (int) months. Default is 0.
            -r before           ring before n (int) minutes. Default is 5.
            -n note             note for this shedule
        
        Example:
            !s 0 -w 1 -m 2 -r 3 -n abcxyz
    """

    if not fix_order(arg):
        await ctx.send("```Order is not available.```")
    else:
        await ctx.send("```Done.```")


async def update_stats():
    await client.wait_until_ready()

    while not client.is_closed():

        show = get_list()['list'].split('\n')[:-1]
        s = [[i.split(' ')[6][:-1], i.split(' ')[8][:-1], int(i.split(' ')[14][:-1])] for i in show]

        for i, c in enumerate(s):
            on_time = datetime.datetime.now() + datetime.timedelta(hours=+7) + datetime.timedelta(minutes = +c[2])
            
            if on_time.strftime("%d/%m %H:%M") == c[0] + ' ' + c[1]:
                for j in range(15):
                    user = client.get_user(ID)
                    await user.send("```{}```".format(show[i]))
                    await asyncio.sleep(1)

                update_schedule(i, show[i], on_time) 

        await asyncio.sleep(1)

client.loop.create_task(update_stats())
client.run(token)