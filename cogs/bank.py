import disnake
import json
import asyncio
import os
import aiohttp
import glob
import locale
import pytz

from datetime import timedelta, date,datetime
from disnake import Webhook
from disnake.ext import commands,tasks
from disnake.ext.commands import Param
from disnake import ApplicationCommandInteraction,Localized,Locale,Member,Option,OptionType,Game,Embed,Colour,MessageInteraction,Status
from core.functions import generate,search,remove,generate_messages
from typing import Optional


class Bank(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot 
        self.user_file_paths = glob.glob(os.path.join("database", "*.json"))
        super().__init__()

    @tasks.loop(minutes=1)
    async def check_date(self):
        await self.bot.wait_until_ready()
        now = datetime.now(tz=pytz.timezone("Asia/Taipei")).date()
        for file_path in self.user_file_paths:
            file_name = os.path.basename(file_path).split('.')[0]
            with open(file_path) as f:
                data = json.load(f)
            try:
                with open(f"./database/{int(file_name)}.json","r",encoding="utf-8") as f:
                    deposits = json.load(f)
                try:
                    join_date_str = data[0]['time']
                except KeyError as e:
                    pass
                join_date_obj = datetime.strptime(join_date_str, '%Y-%m-%d')
                if int(now.strftime('%s')) >= int(join_date_obj.timestamp()):
                    guild = self.bot.get_guild(int(os.getenv("GUILD_ID")))
                    role = guild.get_role(int(os.getenv("ROLE_ID")))
                    print(int(file_name))
                    member = guild.get_member(int(file_name))
                    print(f"{member.name} 的定存時間到了!")
                    boss = guild.get_member(597106331324907520)
                    if (len(deposits) - 1) == 0:
                        embed = Embed(title="來自銀行的通知!",description=f"你的定存時間到了! 因你沒有定存所以已將你的定存身分組移除!",colour=Colour.red())
                        await member.remove_roles(role,reason=f"{member.name} 因時間到而移除了 {role.name} 定存身分組！")
                        await member.send(embed=embed)
                        boss_embed = Embed(title="來自銀行的通知!",description=f"{member.name} 定存時間到了!\n到期的定存:\n到期日期:{now}\n原存入金額:`{deposits[0]['money']}` $",colour=Colour.random())
                        await boss.send(embed=boss_embed) 
                        data.pop(0)
                        with open(f"./database/{int(file_name)}.json","r",encoding="utf-8") as f:
                            json.dump(data, f)
                    else:
                        embed = Embed(title="來自銀行的通知!",description=f"你的定存時間到了! 你還剩下 `{len(deposits) - 1}` 筆定存!",colour=Colour.red())
                        await member.send(embed=embed)
                        boss_embed = Embed(title="來自銀行的通知!",description=f"{member.name} 定存時間到了!\n到期的定存:\n到期日期:{now}\n原存入金額:`{deposits[0]['money']}` $",colour=Colour.random())
                        await boss.send(embed=boss_embed) #給老大的訊息
                        data.pop(0)
                        with open(f"./database/{int(file_name)}.json","r",encoding="utf-8") as f:
                            json.dump(data, f)
                else:
                    pass
            except (IndexError,UnboundLocalError):
                pass

        if not self.user_file_paths:
            self.check_date.stop()
        else:
            print(f"還不是時候. 目前時間為: {now}")

    @check_date.before_loop
    async def before(self):
        await self.bot.wait_until_ready()
    
    @commands.Cog.listener(name="on_message_interaction")
    async def on_message_interaction(self, interaction: MessageInteraction):
        role = interaction.guild.get_role(1008350002332045332)
        with open(f"./database/{orinigal_user.id}.json","r",encoding="utf-8'") as f:
                    deposits = json.load(f)
        id = int(interaction.data.custom_id.split("_")[1])
        index = int(interaction.data.custom_id.split("_")[2])
        print(interaction.data.custom_id)
        if interaction.data.custom_id == f"view_{deposits[-1]['message_id']}_{deposits[-1]['index']}_agree" or deposits:
            if role in interaction.user.roles or interaction.user.id == 549056425943629825:
                print(index)
                temp_item = next((item for item in deposits if item["message_id"] == id and item['index'] == index), None)
                for deposit in deposits:
                    if deposit.get("message_id") == id:
                        deposit["money"] = int(temp_item['temp_money'])
                        deposit["time"] = temp_item['temp_date']
                        deposit['index'] = temp_item['index']
                        deposit['message_id'] = temp_item['message_id']
                        del deposit["temp_money"]
                        del deposit["temp_date"]
                        break
                with open(f"./database/{orinigal_user.id}.json","w",encoding="utf-8'") as f:
                            json.dump(deposits, f)
                item = next((item for item in deposits if item["message_id"] == id and item['index'] == index), None)
                if item is not None:
                    user = self.bot.get_user(orinigal_user.id)
                    embed = Embed(title="<a:check:1043896950484902009> | 交易成功!",description=f"已將 {orinigal_user.name} 的定存紀錄寫入至資料庫!",colour=disnake.Colour.green())
                    guild = self.bot.get_guild(int(os.getenv("GUILD_ID")))
                    role = guild.get_role(int(os.getenv("ROLE_ID")))
                    await orinigal_user.add_roles(role)
                    embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(os.getenv("WEBHOOK_URL"), session=session)
                        print(item["message_id"])
                        original = await webhook.fetch_message(item["message_id"])
                        if interaction.user.id == 341556620536578048:
                            try:
                                contract_edit_text = f"[存款條] 本人 {user.mention} 於NN銀行存入yeecord幣 {int(item['money'])}$, 依協調定存一日利息10$, {item['time']}可領取原存入全額與相應利息, 若本人要求早於{item['time']}\n領出, 只可領取原存入金額之一半, 利息悉數取消。\n本人簽名 :{user.name} \n銀行方簽名: 🫔"
                            except UnboundLocalError:
                                contract_edit_text = f"[存款條] 本人 {orinigal_user.mention} 於NN銀行存入yeecord幣 {int(item['money'])}$, 依協調定存一日利息10$, {item['time']}可領取原存入全額與相應利息, 若本人要求早於{item['time']}\n領出, 只可領取原存入金額之一半, 利息悉數取消。\n本人簽名 :{user.name} \n銀行方簽名: 🫔"
                        else:
                            try:
                                    contract_edit_text = f"[存款條] 本人 {user.mention} 於NN銀行存入yeecord幣 {int(item['money'])}$, 依協調定存一日利息10$, {item['time']}可領取原存入全額與相應利息, 若本人要求早於{item['time']}\n領出, 只可領取原存入金額之一半, 利息悉數取消。\n本人簽名 :{user.name} \n銀行方簽名: <:castle_draw:994489310176882738>"
                            except UnboundLocalError:
                                contract_edit_text = f"[存款條] 本人 {orinigal_user.mention} 於NN銀行存入yeecord幣 {int(item['money'])}$, 依協調定存一日利息10$, {item['time']}可領取原存入全額與相應利息, 若本人要求早於{item['time']}\n領出, 只可領取原存入金額之一半, 利息悉數取消。\n本人簽名 :{user.name} \n銀行方簽名: <:castle_draw:994489310176882738>"
                                    #<:castle_draw:994489310176882738>
                            await original.edit(content=contract_edit_text)
                            await interaction.message.edit(embed=embed,view=None)
                            await interaction.message.delete(delay=3)
            else:
                embed = disnake.Embed(title="❌ | 你無權執行此指令!",colour=disnake.Colour.red())
                await interaction.response.send_message(embed=embed,ephemeral=True)

        elif interaction.data.custom_id == f"view_{index}_deny":
                if role in interaction.user.roles or interaction.user.id == 549056425943629825:
                    embed = Embed(title="❌ | 已拒絕定存",description=f"",colour=disnake.Colour.red())
                    async with aiohttp.ClientSession() as session:
                        webhook = Webhook.from_url(os.getenv("WEBHOOK_URL"), session=session)
                        messageid_list = [item['message_id'] for item in deposits if 'message_id' in item]
                        temp_item = next((item for item in deposits if item["index"] == index), None)
                        for deposit in deposits:
                            if deposit.get("index") == index:
                                deposits.remove(deposit)
                                break                     
                        with open(f"./database/{orinigal_user.id}.json","w",encoding="utf-8'") as f:
                            json.dump(deposits, f)
                else:
                    embed = disnake.Embed(title="❌ | 你無權按下此按鈕!",colour=disnake.Colour.red())
                    await interaction.response.send_message(embed=embed,ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=Game(name="管理NN銀行的大小事中.."))
        if not self.check_date.is_running():
            self.bot.loop.create_task(self.check_date.start())
        print("Bank Ready!")

    @commands.slash_command(name=Localized(data={Locale.zh_TW: "產生合約",Locale.en_US: "contract"}), description="透過此指令來一鍵定存!")
    async def contract(self, interaction: ApplicationCommandInteraction, money:int = Param(name=Localized(data={Locale.zh_TW: "金額"}),description=Localized(data={Locale.zh_TW: "定存的金額"}))):
        if isinstance(money, int) and money >= 0 and money % 1 == 0:
            if money >= 1000:
                if str(money)[-3:] == "000":
                    global orinigal_user
                    if os.path.isfile(f"./database/{interaction.user.id}.json"):
                        try:
                            with open(f"./database/{interaction.user.id}.json","r",encoding="utf-8'") as f:
                                deposits = json.load(f)
                        except json.decoder.JSONDecodeError:
                                deposits = []
                        date_time_str, message, orinigal_user,index = await generate(bot=self.bot,interaction=interaction,money=money)
                        temp_data = {"temp_money":money,"temp_date":date_time_str,"message_id":message.id,"index":index}
                        deposits.append(temp_data)
                        with open(f"./database/{interaction.user.id}.json","w",encoding="utf-8'") as f:
                            json.dump(deposits,f)
                        messages = []
                        async for message in generate_messages(bot=self.bot,user=interaction.user,data=deposits):
                            result = await message
                            messages.append(result)
                    else:
                        with open(f"./database/{interaction.user.id}.json","w+",encoding="utf-8'") as f:
                            try:
                                with open(f"./database/{interaction.user.id}.json","r",encoding="utf-8'") as f:
                                    deposits = json.load(f)
                            except json.decoder.JSONDecodeError:
                                    deposits = []
                            date_time_str, message, orinigal_user, index = await generate(bot=self.bot,interaction=interaction,money=money)
                            temp_data = {"temp_money":money,"temp_date":date_time_str,"message_id":message.id,"index":index}
                            deposits.append(temp_data)
                            with open(f"./database/{interaction.user.id}.json","w",encoding="utf-8'") as f:
                                json.dump(deposits,f)
                            messages = []
                            async for message in generate_messages(bot=self.bot,user=interaction.user,data=deposits):
                                    result = await message
                                    messages.append(result)
                else:
                    embed = Embed(title="❌ | 金額結尾必須為000$",description=f"",colour=disnake.Colour.red())
                    await interaction.response.send_message(embed=embed,ephemeral=True)
            else:
                embed = Embed(title="❌ | 金額不可低於1000$",description=f"",colour=disnake.Colour.red())
                await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            embed = Embed(title="❌ | 請輸入正確的金額!",description=f"",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)

    @commands.slash_command(name='eval', description="邪惡",options=[Option(name="option",description="選項", required=True)])
    async def eval(self, interaction: ApplicationCommandInteraction, option:str ):
        if interaction.user.id == 549056425943629825:
            print(eval(option))
            try:
                embed = disnake.Embed(title=":white_check_mark: | 神秘的結果", description="```py\n{}```".format(eval(option)),colour=disnake.Colour.green())
                await interaction.response.send_message(embed=embed)
            except disnake.errors.HTTPException:
                with open(f"eval.txt",'w',encoding='UTF-8') as chat:
                    chat.write(str(eval(option))) #將訊息寫入至chat.txt
                embed = disnake.Embed(title=":white_check_mark: | 神秘的結果", description="因字數過多,已轉成文件",colour=disnake.Colour.green())
                await interaction.response.send_message(embed=embed,file=disnake.File(f"eval.txt"))
                os.remove(f"chat.txt")
        else:
            embed = disnake.Embed(title=":x: | 這個指令太過邪惡了,只有饅頭能夠駕馭他 (?")
            await interaction.response.send_message(embed=embed)
            
    @commands.slash_command(name='edit_contract', description="邪惡",options=[Option(name="message_id",description="訊息id", required=True),Option(name="text",description="訊息")])
    async def edit_contract(self, interaction: ApplicationCommandInteraction, message_id:int, text:str):
        if interaction.user.id == 549056425943629825:
            async with aiohttp.ClientSession() as session:
                try:
                    webhook = Webhook.from_url(os.getenv("WEBHOOK_URL"), session=session)
                    original = await webhook.fetch_message(message_id)
                    await original.edit(content=f"{text}")
                except disnake.NotFound:
                        channel = interaction.guild.get_channel(int(os.getenv("CHANNEL_ID")))
                        channel_webhook = await channel.create_webhook(name="bank",avatar=None, reason=None)
                        webhook = Webhook.from_url(channel_webhook.url, session=session)
        else:
            embed = disnake.Embed(title=":x: | 這個指令太過邪惡了,只有饅頭能夠駕馭他 (?")
            await interaction.response.send_message(embed=embed)      

    @commands.slash_command(name=Localized(data={Locale.zh_TW: "查看使用者定存狀況"}), description="限銀行方查詢",options=[Option(name="user",description="指定的使用者", type=OptionType.user, required=True)])
    async def search_user(self, interaction: ApplicationCommandInteraction, user:Optional[Member]):
        if interaction.user.id in [341556620536578048,597106331324907520,549056425943629825]:
            await search(interaction=interaction,member=user)
        else:
            embed = disnake.Embed(title="❌ | 你無權執行此指令!",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)
    
    @commands.slash_command(name=Localized(data={Locale.zh_TW: "查看定存狀況",Locale.en_US: "view"}), description="透過此指令來一目了然自己目前的定存吧!")
    async def search_myself(self, interaction: ApplicationCommandInteraction):
            await search(interaction=interaction,member=interaction.user)
    
    @commands.slash_command(name=Localized(data={Locale.zh_TW: "移除使用者定存"}), description="限銀行方查詢",options=[Option(name="user",description="指定的使用者", type=OptionType.user, required=True),Option(name="order",description="要移除的第幾筆，︀如無指定則全數移除",required=False)])
    async def remove_deposits(self, interaction: ApplicationCommandInteraction, user:Optional[Member], order:int = Param(name=Localized(data={Locale.zh_TW: "第幾筆"}),description=Localized(data={Locale.zh_TW: "要移除的第幾筆，︀如無指定則全數移除"}),default=None)):
        await remove(interaction=interaction, member=user,order=order)

    @commands.slash_command(name="load_extension",options=[Option(name="extension",description="噓",type=OptionType.string,required=True)])
    async def load(self,interaction: ApplicationCommandInteraction, extension:str):
        if interaction.user.id == 549056425943629825:
            for fn in os.listdir("./cogs"):
                if fn.endswith(".py"):
                    self.bot.load_extension(f"cogs.{extension}")
            embed = Embed(title="<:check:1036160202174627840> | 加載成功!",description=f"目標cog:{extension}",colour=Colour.green())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("你不是擁有者!",ephemeral=True)
    
    @commands.slash_command(name="unload_extension",options=[Option(name="extension",description="噓",type=OptionType.string,required=True)])
    async def unload(self,interaction: ApplicationCommandInteraction, extension:str):
        if interaction.user.id == 549056425943629825:
            for fn in os.listdir("./cogs"):
                if fn.endswith(".py"):
                    self.bot.unload_extension(f"cogs.{extension}")
            embed = Embed(title="<:check:1036160202174627840> | 卸載成功!",description=f"目標cog:{extension}",colour=Colour.green())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("你不是擁有者!",ephemeral=True)
    
    @commands.slash_command(name="reload_extension",options=[Option(name="extension",description="噓",type=OptionType.string,required=True)])
    async def reload(self,interaction: ApplicationCommandInteraction, extension:str):
        if interaction.user.id == 549056425943629825:
            for fn in os.listdir("./cogs"):
                if fn.endswith(".py"):
                    self.bot.reload_extension(f"cogs.{extension}")
            embed = Embed(title="<:check:1036160202174627840> | 重新載入成功!",description=f"目標cog:{extension}",colour=Colour.green())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("你不是擁有者!",ephemeral=True)
    
    

def setup(bot):
    bot.add_cog(Bank(bot))