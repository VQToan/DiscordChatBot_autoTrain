import os

import discord

import brian.AI as train
import brian.getreply as rp
from brian.update_dataset import main

train_bot = train.AI()
client = discord.Client()
token = str(os.getenv('discord_token'))
cachemsg = []
dataset_raw = []
reply = rp.getrply()


def save_text_raw(fpath: dir, data):
    file = open(fpath, "a+", encoding="utf-8")
    for item in data:
        file.write("{}=>{}\n".format(item[0], item[1]))
    file.close()


@client.event
async def on_ready():
    print('Đang khởi chạy')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(ctx):
    cachemsg.append((ctx.id, ctx.content))
    if ctx.author == client.user:
        return
    idref = ctx.reference
    if idref != None:
        idref = idref.message_id
        for item in cachemsg:
            if item[0] == idref:
                dataset_raw.append((item[1], ctx.content))
    print(cachemsg)
    print(dataset_raw)
    if len(cachemsg) >= 100:
        for item in cachemsg[0:50]:
            cachemsg.remove(item)
    if len(dataset_raw) >= 100:
        save_text_raw('../brian/data/raw.txt', dataset_raw)
        dataset_raw.clear()
        main('../brian/data/raw.txt', '../brian/data/intents.json')
    if 'bot' in ctx.content.lower().replace(',', '').replace('.', '').split(" "):
        msg, tag = reply.chatbot_response(msg=ctx.content)
        if tag == 'học':
            if ctx.channel.id == 861544200045592597:
                save_text_raw('../brian/data/raw.txt', dataset_raw)
                dataset_raw.clear()
                main('../brian/data/raw.txt', '../brian/data/intents.json')
                train_bot.train()
                reply.__init__()
                await ctx.reply("học xong gòi nè", mention_author=True)
        await ctx.reply(msg, mention_author=True)


client.run("ODEzMzIyMTE1OTE0NzkyOTYx.YDNnPw.OZ-t6iiU2Cfq6-colcBa5HrdXo0")
