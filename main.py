import datetime
import discord
import asyncio
from discord.ext import commands
from discord import utils
from colorama import init, Fore, Style
from os import system
from time import sleep
import sqlite3
import string

# _____________________________________________________________________#
TOKEN = ' '
GUILD_IDD = 824377440972439603  # 824377440972439603          #GUILD_ID
POST_ID = 826183752211234886  # POST_ID

AUTOROLE = 826181085154770974  # id roles for beginners 824377824818888744

ROLES = {
'🎮': 826181085154770974, #Геймер
'🐍': 826181258022879304, #Программист
'🧱': 826181335071981598, #3D'шник
'👶': 826181430618751008, #Начинающий
}

ROLETYPE = {
'🎮': 'Геймер',
'🐍': 'Программист',
'🧱': '3D',
'👶': 'Начинающий'

            }

RPG = {
    '1': 826181085154770974,  # Role ID for the rpg system
    '2': 826181258022879304,  # Role ID for the rpg system
    '3': 826181335071981598,  # Role ID for the rpg system
    '4': 826181430618751008,  # Role ID for the rpg system
    '5': 824721801959440404,  # Role ID for the rpg system
    '6': 824721801266462720,  # Role ID for the rpg system
    '7': 824721797428936734,  # Role ID for the rpg system
    '8': 824377824818888744,  # Role ID for the rpg system 824722817102249994
}

new_exp = 0  # exp for beginners
new_status = 0  # status for beginners


# _____________________________________________________________________#


def log(x):  # log-database function
    now = datetime.datetime.now()
    cur.execute("INSERT INTO log (action, time) VALUES (?, ?)", (x, now))
    db.commit()


def lvl(memberid):  # get level from database function
    memberid = str(memberid)
    cur.execute("SELECT exp FROM rpg WHERE member_id = ?", (memberid,))
    exp = cur.fetchone()
    exp = str(exp)
    exp = exp.replace('(', '')
    exp = exp.replace(')', '')
    exp = exp.replace(',', '')
    exp = int(exp)
    return exp


# Подключение к базе данных


def replacer(x, i):  # replacer for data from database func
    x[i] = x[i].replace('(', '')
    x[i] = x[i].replace(')', '')
    x[i] = x[i].replace(',', '')


def begin():  # begin function for creatin database
    try:
        cur.execute(
            "CREATE TABLE rpg (guild_id STRING, member STRING, member_name STRING, member_dis STRING, member_id STRING, role_id INTEGER, exp INTEGER, status INTEGER)")
        cur.execute("CREATE TABLE in_voice (member_id STRING, status INTEGER)")
        cur.execute("CREATE TABLE log (action STRING, time STRING)")
        db.commit()
    except Exception as e:
        print('Таблица уже создана')
        sleep(2)


db = sqlite3.connect('data.db')
cur = db.cursor()
begin()
init(convert=True)  # for save colors after compile to exe
system('cls')
intents = discord.Intents.all()
bot = discord.Client(intents=intents)  # creation bot-client


async def check_db():  # check database (exp of member) for RPG - system
    await asyncio.sleep(10)
    while True:
        z = []
        cur.execute("SELECT member_id from in_voice WHERE status = 1")
        x = cur.fetchall()
        for i in range(0, len(x)):
            x[i] = str(x[i])
            replacer(x, i)
            x[i] = int(x[i])
        for i in range(0, len(x)):
            cur.execute(
                "UPDATE rpg SET exp = exp + 1 WHERE member_id = ?", (str(x[i]),))
            db.commit()
        cur.execute("SELECT member_id from rpg WHERE exp>1")
        v = cur.fetchall()
        for i in range(0, len(v)):
            v[i] = str(v[i])
            replacer(v, i)
            memberid = int(v[i])
            member = bot.get_guild(GUILD_IDD).get_member(memberid)
            exp = lvl(memberid)
            # повышение до какого либо уровня
            expp = [[100, '2', '1'], [500, '3', '2'], [1000, '4', '3'], [
                2000, '5', '4'], [4000, '6', '5'], [8000, '7', '6'], [16000, '8', '7']]
            for o in range(0, len(expp)):
                if exp == int(expp[o][0]):
                    roleadd = utils.get(member.guild.roles, id=RPG[expp[o][1]])
                    roleremove = utils.get(
                        member.guild.roles, id=RPG[expp[o][2]])
                    await member.add_roles(roleadd)
                    await member.remove_roles(roleremove)
                    print(
                        f'Игрок {member} был повышен с {roleremove.name} до {roleadd.name}')
                    x = (
                        f'Игрок {member} был повышен с {roleremove.name} до {roleadd.name}')
                    log(x)
        # таймаут
        await asyncio.sleep(15)


# создание параллельного процесса
bot.loop.create_task(check_db())


@bot.event
async def on_ready():
    x = (f'Был запущен бот...\n' + Fore.CYAN +
         f'USERNAME: {bot.user.name}\n' + Fore.GREEN + f'ID: {bot.user.id}\n' + Style.RESET_ALL + 'Была подключена база данных')
    print(x)
    x = f'Был запущен бот:{bot.user.name}|||ID:{bot.user.id}|||Была подключена база данных'
    log(x)


# добавление роли по реакции
@bot.event
async def on_raw_reaction_add(payload):  # add reaction async-func
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(POST_ID)
    member = utils.get(message.guild.members, id=payload.user_id)
    emoji = str(payload.emoji)
    role = utils.get(message.guild.roles, id=ROLES[emoji])
    await member.add_roles(role)  # выдача роли
    x = ('Была выдана роль ' + '"{}" '.format(
        ROLETYPE[emoji]) + 'игроку ' + '{}'.format(member))
    print(x)
    log(x)


# удаление роли по реакции
@bot.event
async def on_raw_reaction_remove(payload):  # remove reaction async-func
    channel = bot.get_channel(payload.channel_id)

    print(channel)
    print(payload.channel_id)
    # выбор сообщения в канале, к которому прибавилась реакция
    message = await channel.fetch_message(POST_ID)
    print(message)
    # получение юзера, который поставил реакцию
    member = utils.get(message.guild.members, id=payload.user_id)
    print(member)
    # создание переменной, в которую включены роли канала и конкретная роль, которую будет выдана при нажатии
    emoji = str(payload.emoji)
    role = utils.get(message.guild.roles, id=ROLES[emoji])
    print(role)
    await member.remove_roles(role)  # удаление роли
    x = ('Была удалена роль ' + Fore.YELLOW + '"{}" '.format(
        ROLETYPE[emoji]) + Style.RESET_ALL + 'игроку ' + Fore.CYAN + '{}'.format(member) + Style.RESET_ALL)
    print(x)
    x = f'Была удалена роль {ROLETYPE[emoji]} игроку "{member}"'
    log(x)


@bot.event
async def on_member_remove(member):  # func for remove user from database when user leave from channel
    cur.execute("DELETE FROM rpg WHERE member_id = ?", (str(member.id),))
    db.commit()
    print(f'Игрок {member} покинул сервер')
    x = f'Игрок {member} покинул сервер'
    log(x)


@bot.event
async def on_message(message):  # async func for check - messeges
    member = utils.get(message.guild.members, id=message.author.id)
    user = utils.get(member.guild.members, id=member.id)
    channel = bot.get_channel(message.channel.id)
    role = utils.get(member.guild.roles, id=RPG['1'])
    if message.content == '!start':
        cur.execute("SELECT member_id FROM rpg WHERE member_id = ?",
                    (str(member.id),))
        x = cur.fetchall()
        if x == []:
            cur.execute(
                f"INSERT INTO rpg (guild_id, member, member_name, member_dis, member_id, role_id, exp, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (str(member.guild.id), str(member), member.name, user.discriminator, member.id, RPG['1'], 0, 0))
            await member.add_roles(role)
            await channel.send('```RPG-система была запущена для вашего аккаунта!```')
            db.commit()
        else:
            await channel.send('```Ваш аккаунт уже подключен к RPG-системе```')
    if message.content == '!rank':
        cur.execute("SELECT exp FROM rpg WHERE member_id = ?",
                    (str(member.id),))
        x = cur.fetchall()
        if x == []:
            await channel.send(
                '```RPG-система не подключена для вашего канала.\nНапишите <!start>, чтобы подключиться к ней```')
        else:
            for i in range(0, len(x)):
                x[i] = str(x[i])
                replacer(x, i)
                x[i] = int(x[i])
                ex = [[100, 1], [500, 2], [1000, 3], [
                    2000, 4], [4000, 5], [8000, 6], [16000, 7]]
                for o in range(0, len(ex)):
                    if x[i] < int(ex[o][0]):
                        limit = int(ex[o][0])
                        lvl = int(ex[0][1])
                        break
                if x[i] >= 16000:
                    limit = '∞'
                    lvl = 8
                embed = discord.Embed()
                embed.add_field(name="USER:", value=f"{member}", inline=False)
                embed.add_field(
                    name="RANK:", value=f"{x[i]}/{limit} (LVL {lvl})", inline=False)
                embed.set_thumbnail(url=f"{member.avatar_url}")
                await channel.send(embed=embed)


@bot.event
async def on_member_join(member):  # async func for event when user join on server
    user = utils.get(member.guild.members, id=member.id)
    role1 = utils.get(member.guild.roles, id=AUTOROLE)
    role2 = utils.get(member.guild.roles, id=RPG['1'])
    await member.add_roles(role1)
    await member.add_roles(role2)
    category = member.guild.categories[0]
    channel = category.channels[0]
    await channel.send(
        f'```css\nПриветствуем тебя на сервере\n{member.name}!!! Желаем удачно провести время <3 <3 <3```')
    cur.execute(
        f"INSERT INTO rpg (guild_id, member, member_name, member_dis, member_id, role_id, exp, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (str(member.guild.id), str(member), member.name, user.discriminator, member.id, RPG['1'], 0, 0))
    db.commit()
    x = ('Автоматически была выдана роль ' + Fore.YELLOW + '"New" ' +
         Style.RESET_ALL + 'игроку ' + Fore.CYAN + '{}'.format(member) + Style.RESET_ALL)
    print(x)
    x = f'Автоматически была выдана роль "New" игроку {member}'
    log(x)
    y = ('Автоматически была выдана роль ' + Fore.YELLOW + '"LVL 1" ' +
         Style.RESET_ALL + 'игроку ' + Fore.CYAN + '{}'.format(member) + Style.RESET_ALL)
    print(y)
    y = f'Автоматически была выдана роль "LVL 1" игроку {member}'
    log(y)


@bot.event
async def on_voice_state_update(member, before, after):  # async-func for checking users in voice channels
    x = before.channel
    y = after.channel
    if ((str(x) != 'None') and (str(y) != 'None')) or ((str(x) == 'None') and (str(y) != 'None')):
        print(f'Игрок {member} подключился к голосовому каналу {after.channel}')
        x = f'Игрок {member} подключился к голосовому каналу {after.channel}'
        log(x)
        cur.execute(
            "SELECT member_id from in_voice WHERE (member_id = ?)", (str(member.id),))
        z = cur.fetchall()
        if z == []:
            cur.execute(
                "INSERT INTO in_voice (member_id, status) VALUES (?, ?)", (str(member.id), 1))
            cur.execute("SELECT member_id from in_voice WHERE status = 1")
            db.commit()
        else:
            cur.execute(
                "UPDATE in_voice SET status = 1 WHERE (member_id = ?)", (str(member.id),))
            db.commit()
    else:
        print(f'Игрок {member} покинул голосовой канал {before.channel}')
        x = f'Игрок {member} покинул голосовой канал {before.channel}'
        log(x)
        cur.execute(
            "UPDATE in_voice SET status = 0 WHERE (member_id = ?)", (str(member.id),))
        cur.execute("DELETE FROM in_voice WHERE status = 0")
        db.commit()


bot.run(TOKEN)  # run bot
