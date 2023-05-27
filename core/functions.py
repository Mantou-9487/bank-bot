import disnake
import json
import os
import aiohttp
import asyncio

import time
from disnake import ApplicationCommandInteraction,Embed,Member,User,MessageInteraction,ButtonStyle,MessageInteraction
from disnake.ext import commands,tasks
from disnake.ui import Button
from disnake.ext.commands import Bot
from datetime import timedelta, date,datetime
from disnake import Webhook
from typing import List
         

async def search(interaction:ApplicationCommandInteraction,member:Member):
    try:
        with open(f"./database/{member.id}.json", "r") as f:
            deposits = json.load(f)
        if not deposits:
            embed = disnake.Embed(title="❌ | 目前定存紀錄為空!",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            embed = Embed(title="",description = "\n".join(f"第{i}筆資料：定存金額 `{deposit['money']}$`, 到期時間 <t:{int(time.mktime(datetime.strptime(deposit['time'], '%Y-%m-%d').timetuple()))}:R>" for i, deposit in enumerate(deposits)),colour=disnake.Colour.random())
            embed.set_author(name=f"{member.name} 的定存紀錄",icon_url=member.avatar.url)
            embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
            await interaction.response.send_message(embed=embed)
    except (FileNotFoundError,json.decoder.JSONDecodeError):
        embed = disnake.Embed(title="❌ | 目前定存紀錄為空!",colour=disnake.Colour.red())
        await interaction.response.send_message(embed=embed,ephemeral=True)

async def remove(interaction:ApplicationCommandInteraction,member:Member, order):
    try:
        with open(f"./database/{member.id}.json", "r") as f:
            deposits = json.load(f)
        if order is None:
            deposits = []
            with open(f"./database/{member.id}.json","w",encoding="utf-8'") as f:
                        json.dump(deposits,f)
            embed = disnake.Embed(title="✅ | 已成功刪除!",description=f"已將 {member.name} 的所有定存紀錄移除!",colour=disnake.Colour.green())
            embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            deposits.pop(int(order))
            with open(f"./database/{member.id}.json","w",encoding="utf-8'") as f:
                        json.dump(deposits,f)
            embed = disnake.Embed(title="✅ | 已成功刪除!",description=f"已將 {member.name} 的第`{int(order)}`筆定存移除!",colour=disnake.Colour.green())
            embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
            await interaction.response.send_message(embed=embed,ephemeral=True)
    except (FileNotFoundError,json.decoder.JSONDecodeError):
        embed = disnake.Embed(title="❌ | 此使用者目前還沒有定存紀錄",colour=disnake.Colour.red())
        await interaction.response.send_message(embed=embed,ephemeral=True)


async def generate_messages(bot:Bot, user:disnake.User, data:list):
    try:
        with open(f"./database/{user.id}.json","r",encoding="utf-8'") as f:
            deposits = json.load(f)
    except json.decoder.JSONDecodeError:
            deposits = []
    for item in enumerate(data):
        buttons = [
            Button(
                style=ButtonStyle.green,
                label="同意",
                custom_id=f"view_{deposits[-1]['message_id']}_{deposits[-1]['index']}_agree",
            ),
            Button(
                style=ButtonStyle.red,
                label="拒絕",
                custom_id=f"view_{deposits[-1]['message_id']}_{deposits[-1]['index']}_deny",
            )
        ]
        channel = bot.get_channel(int(os.getenv("CHANNEL_ID")))
        money = deposits[-1]['temp_money']
        date_time_str = deposits[-1]['temp_date']
        admin_embed = Embed(title="<:emoji_107:1067077063246368799> | 定存通知!",description=f"{user.name} 想要定存!\n金額:`{money}$`\n到期日: {date_time_str}",colour=disnake.Colour.random())
        admin_embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
        message = await channel.send(embed=admin_embed, components=buttons)
        yield message
        

async def generate(bot:Bot,interaction:ApplicationCommandInteraction, money:int):
    if os.path.isfile(f"./database/{interaction.user.id}.json"):
        try:
            with open(f"./database/{interaction.user.id}.json","r",encoding="utf-8'") as f:
                deposits = json.load(f)
        except json.decoder.JSONDecodeError:
            deposits = []
        if len(deposits) >= 3:
            embed = disnake.Embed(title="❌ | 產生失敗",description="你的定存已經有三筆了!",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            if len(deposits) >= 2 and money < 5000:
                 pass
            else:
                add_days = int(money) / 200 
                Date_required = date.today() + timedelta(days=add_days)
                date_time = Date_required    
                contract_text = f"[存款條] 本人 {interaction.user.mention} 於NN銀行存入yeecord幣 {int(money)}$, 依協調定存一日利息10$, {date_time}可領取原存入全額與相應利息, 若本人要求早於{date_time}\n領出, 只可領取原存入金額之一半, 利息悉數取消。\n本人簽名 :{interaction.user.name} \n銀行方簽名: "
                async with aiohttp.ClientSession() as session:
                    try:
                        webhook = Webhook.from_url(os.getenv("WEBHOOK_URL"), session=session)
                        try:
                            message = await webhook.send(f'{contract_text}', username=f'{interaction.user.display_name}',avatar_url=f"{interaction.user.display_avatar.url}",wait=True)
                        except disnake.NotFound:
                            channel = interaction.guild.get_channel(int(os.getenv("CHANNEL_ID")))
                            channel_webhook = await channel.create_webhook(name="bank",avatar=None, reason=None)
                            print(channel_webhook.url)
                            webhook = Webhook.from_url(channel_webhook.url, session=session)
                            message = await webhook.send(f'{contract_text}', username=f'{interaction.user.display_name}',avatar_url=f"{interaction.user.display_avatar.url}",wait=True)
                    except RuntimeError:
                        session.close()
                        raise
                channel = bot.get_channel(int(os.getenv("CHANNEL_ID")))
                embed = disnake.Embed(title="✅ | 已產生成功!",description=f"已發送，︀請先至 {channel.mention}支付存入金額給NN#3093，︀並等待銀行方確認。 | 你的定存次數目前為:`{len(deposits)}`筆!",colour=disnake.Colour.green())
                embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
                await interaction.response.defer(ephemeral=True)
                await interaction.followup.send(embed=embed,ephemeral=True)
                full_date_time = Date_required
                date_time_str = full_date_time.strftime("%Y-%m-%d")
                return date_time_str,message, interaction.user, len(deposits)
    else:
        with open(f"./database/{interaction.user.id}.json","w+",encoding="utf-8'") as f:
            try:
                with open(f"./database/{interaction.user.id}.json","r",encoding="utf-8'") as f:
                    deposits = json.load(f)
            except json.decoder.JSONDecodeError:
                    deposits = []
        if len(deposits) >= 3:
            embed = disnake.Embed(title="❌ | 產生失敗",description="你的定存已經有三筆了!",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            add_days = int(money) / 200 
            Date_required = date.today() + timedelta(days=add_days)
            date_time = Date_required    
            contract_text = f"[存款條] 本人 {interaction.user.mention} 於NN銀行存入yeecord幣 {int(money)}$, 依協調定存一日利息10$, {date_time}可領取原存入全額與相應利息, 若本人要求早於{date_time}\n領出, 只可領取原存入金額之一半, 利息悉數取消。\n本人簽名 :{interaction.user.name} \n銀行方簽名: "
            async with aiohttp.ClientSession() as session:
                try:
                    webhook = Webhook.from_url(os.getenv("WEBHOOK_URL"), session=session)
                    try:
                        message = await webhook.send(f'{contract_text}', username=f'{interaction.user.display_name}',avatar_url=f"{interaction.user.display_avatar.url}",wait=True)
                    except disnake.NotFound:
                        channel = interaction.guild.get_channel(int(os.getenv("CHANNEL_ID")))
                        channel_webhook = await channel.create_webhook(name="bank",avatar=None, reason=None)
                        webhook = Webhook.from_url(channel_webhook.url, session=session)
                        message = await webhook.send(f'{contract_text}', username=f'{interaction.user.display_name}',avatar_url=f"{interaction.user.display_avatar.url}",wait=True)
                except RuntimeError:
                    session.close()
                    raise
            channel = bot.get_channel(int(os.getenv("CHANNEL_ID")))
            embed = disnake.Embed(title="✅ | 已產生成功!",description=f"已發送，︀請先至{channel.mention}支付存入金額給NN#3093，︀並等待銀行方確認。 | 你的定存次數目前為:`{len(deposits)}`筆!",colour=disnake.Colour.green())
            embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(embed=embed,ephemeral=True)
            full_date_time = Date_required
            date_time_str = full_date_time.strftime("%Y-%m-%d")
            return channel_webhook, date_time_str