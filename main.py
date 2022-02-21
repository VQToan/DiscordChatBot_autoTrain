import threading

import discord

import brian.AI as train
import brian.getreply as rp
from brian.update_dataset import main, create_text_review

train_bot = train.AI()
client = discord.Client()
cachemsg = []
dataset_raw = []
reply = rp.getrply()
idreply = []


def train_reload():
    train_bot.train()
    reply.__init__()
    print('reload models')

def save_text_raw(fpath: dir, data):
    file = open(fpath, "a+", encoding="utf-8")
    for item in data:
        file.write("{}<=:=>{}|=:=|{}\n".format(item[0], item[1], item[2]))
    file.close()


@client.event
async def on_ready():
    print('Đang khởi chạy')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(ctx):
    idnow = 0
    if ctx.reference:
        idnow = ctx.reference.message_id
    cachemsg.append((ctx.id, ctx.content))
    if (ctx.author == client.user):
        idreply.append(ctx.id)
        return
    idref = ctx.reference
    if idref != None:
        idref = idref.message_id
        for item in cachemsg:
            if item[0] == idref:
                msg, tag = reply.chatbot_response(msg=item[1])
                dataset_raw.append((item[1], ctx.content, tag))
    print(cachemsg)
    print(dataset_raw)
    if len(idreply) >= 100:
        for item in idreply[0:50]:
            idreply.remove(item)
    if len(cachemsg) >= 100:
        for item in cachemsg[0:50]:
            cachemsg.remove(item)
    if (ctx.channel.id == 863726369951580210) or (ctx.channel.id == 861883913009889290) or (idnow in idreply) or (
            'bot' in ctx.content.lower().replace(',', '').replace('.', '').split(" ")):
        msg, tag = reply.chatbot_response(msg=ctx.content)
        await ctx.reply(msg, mention_author=True)
    if len(dataset_raw) >= 100:
        save_text_raw('brian/data/raw.txt', dataset_raw)
        dataset_raw.clear()
        main('brian/data/raw.txt', 'brian/data/intents.json')
        # train and reload
        th1 = threading.Thread(target=train_reload)
        th1.start()
    if ctx.channel.id == 861544200045592597:
        if ctx.content == 'học':
            save_text_raw('brian/data/raw.txt', dataset_raw)
            dataset_raw.clear()
            main('brian/data/raw.txt', 'brian/data/intents.json')
            # train and reload
            th1 = threading.Thread(target=train_reload)
            th1.start()
        if ctx.content == 'xemdataset':
            create_text_review()
            await ctx.channel.send(file=discord.File('brian/data/textout.txt'))


client.run("ODE0OTQyNzkxMzMxMzQ4NTMx.YDlMng.2_c7rutZTZz3n3fDTnDpsVnl2U8")
