import disnake
import json
import os
import aiohttp
import asyncio

import time
from disnake import ApplicationCommandInteraction,Embed,Member,User,MessageInteraction
from disnake.ext import commands,tasks
from disnake.ext.commands import Bot
from datetime import timedelta, date,datetime
from disnake import Webhook
from asyncio import ensure_future
         

async def send_private_message_at_time(user: disnake.User, message: str, date: str):
    # Parse the date string
    target_date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    # Set the target time to noon
    target_time = datetime.today().replace(hour=12, minute=0, second=0, microsecond=0)

    # Combine the target date and time
    target_datetime = datetime.combine(target_date.date(), target_time.time())

    # Calculate the number of seconds until the target datetime
    wait_time = (target_datetime - datetime.now()).total_seconds()
    await asyncio.sleep(wait_time)

    # Send the private message
    await user.send(message)

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


async def write(user:User,money:int):
    try:
        with open(f"./database/{user.id}.json","r",encoding="utf-8'") as f:
            deposits = json.load(f)
    except json.decoder.JSONDecodeError:
            deposits = []
    add_days = int(money) / 200 
    Date_required = date.today() + timedelta(days=add_days)
    date_time_str = Date_required.strftime("%Y-%m-%d")
    deposit_data = {"name": user.name, "money":money, "time": date_time_str}
    deposits.append(deposit_data)
    deposits.remove({"temp_money":money})
    with open(f"./database/{user.id}.json","w",encoding="utf-8'") as f:
            json.dump(deposits,f)

    return user, money, date_time_str
     

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
                    webhook = Webhook.from_url('https://discord.com/api/webhooks/1089207116612513843/o_AB92mdds4IA3soqpcyu5S63dJcpy_vAZ26j57UV_wuj4yWhKgks8uUO24Tv10Qid-R', session=session)
                        #webhook = Webhook.from_url('https://discord.com/api/webhooks/1065564022386204782/DWaGphaPa3qaNCiCwh6jVU4atT75sDCaTzVJSkAnVsNOWoo1erdvv-Ke-iGLi16p74sm', session=session)
                try:
                    message = await webhook.send(f'{contract_text}', username=f'{interaction.user.display_name}',avatar_url=f"{interaction.user.display_avatar.url}",wait=True)
                except RuntimeError:
                    session = aiohttp.ClientSession()
                    webhook = Webhook.from_url('https://discord.com/api/webhooks/1089207116612513843/o_AB92mdds4IA3soqpcyu5S63dJcpy_vAZ26j57UV_wuj4yWhKgks8uUO24Tv10Qid-R', session=session)
                    message = await webhook.send(f'{contract_text}', username=f'{interaction.user.display_name}',avatar_url=f"{interaction.user.display_avatar.url}",wait=True)
                embed = disnake.Embed(title="✅ | 已產生成功!",description=f"已將合約發送，︀請等待銀行方確認 | 你的定存次數目前為:`{len(deposits)}`筆!",colour=disnake.Colour.green())
                embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
                await interaction.response.send_message(embed=embed,ephemeral=True)
                full_date_time = Date_required
                date_time_str = full_date_time.strftime("%Y-%m-%d")
                return date_time_str,message,interaction.user
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
                webhook = Webhook.from_url('https://discord.com/api/webhooks/1089207116612513843/o_AB92mdds4IA3soqpcyu5S63dJcpy_vAZ26j57UV_wuj4yWhKgks8uUO24Tv10Qid-R', session=session)
                #webhook = Webhook.from_url('https://discord.com/api/webhooks/1065564022386204782/DWaGphaPa3qaNCiCwh6jVU4atT75sDCaTzVJSkAnVsNOWoo1erdvv-Ke-iGLi16p74sm', session=session)
            try:
                message = await webhook.send(f'{contract_text}', username=f'{interaction.user.display_name}',avatar_url=f"{interaction.user.display_avatar.url}",wait=True)
            except RuntimeError:
                session = aiohttp.ClientSession()
                webhook = Webhook.from_url('https://discord.com/api/webhooks/1089207116612513843/o_AB92mdds4IA3soqpcyu5S63dJcpy_vAZ26j57UV_wuj4yWhKgks8uUO24Tv10Qid-R', session=session)
            embed = disnake.Embed(title="✅ | 已產生成功!",description=f"已將合約發送，︀請等待銀行方確認 | 你的定存次數目前為:`{len(deposits)}`筆!",colour=disnake.Colour.green())
            embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
            await interaction.response.send_message(embed=embed,ephemeral=True)
            full_date_time = Date_required
            date_time_str = full_date_time.strftime("%Y-%m-%d")
            return date_time_str
