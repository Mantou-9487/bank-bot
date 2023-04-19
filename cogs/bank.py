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
from core.functions import generate,search,remove,write
from typing import Optional



class Menu(disnake.ui.View):
    def __init__(self) -> None:
          super().__init__(timeout=None)
    
    @disnake.ui.button(label="同意", style=disnake.ButtonStyle.green,custom_id="agree")
    async def agree(self, button: disnake.ui.Button, interaction: ApplicationCommandInteraction):
        pass
             
             
    @disnake.ui.button(label="拒絕", style=disnake.ButtonStyle.red,custom_id="deny")
    async def deny(self, button: disnake.ui.Button, interaction: ApplicationCommandInteraction):
        pass

class Bank(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot 
        self.user_file_paths = glob.glob(f'database/*.json')
        super().__init__()

    @tasks.loop(minutes=1)
    async def check_date(self):
        await self.bot.wait_until_ready()
        now = datetime.now(tz=pytz.timezone("Asia/Taipei"))
        for file_path in self.user_file_paths:
            file_name = os.path.basename(file_path).split('.')[0]
            with open(file_path) as f:
                data = json.load(f)
        try:
            with open(f"./database/{int(file_name)}.json","r",encoding="utf-8") as f:
                deposits = json.load(f)
            join_date_str = data[0]['time']  # 获取日期字符串
            join_date_obj = datetime.strptime(join_date_str, '%Y-%m-%d')
            if now.timestamp() >= join_date_obj.timestamp():
                guild = self.bot.get_guild(978571136050806844)
                role = guild.get_role(1006196207447719986)
                member = guild.get_member(int(file_name))
                print(f"{member.name} 的定存時間到了!")
                boss = guild.get_member(597106331324907520)
                data.pop(0)
                if len(deposits) == 0:
                    embed = Embed(title="來自銀行的通知!",description=f"你的定存時間到了! 因你沒有定存所以已將你的定存身分組移除!",colour=Colour.red())
                    await member.remove_roles(role,reason=f"{member.name} 因時間到而移除了 {role.name} 定存身分組！")
                    await member.send(embed=embed)
                    boss_embed = Embed(title="來自銀行的通知!",description=f"{member.name} 因定存時間到了而被拔掉了身分組!",colour=Colour.random())
                    await boss.send(embed=boss_embed) 
                else:
                    embed = Embed(title="來自銀行的通知!",description=f"你的定存時間到了! 你還剩下 `{len(deposits)}` 筆定存!",colour=Colour.red())
                    await member.send(embed=embed)
                    boss_embed = Embed(title="來自銀行的通知!",description=f"{member.name} 定存時間到了!\n到期的定存:\n到期日期:{now}\n原存入金額:`{data['money']}`$",colour=Colour.random())
                    await boss.send(embed=boss_embed) #給老大的訊息
                with open(file_path, 'w') as f:
                    json.dump(data, f)

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
        match interaction.data.custom_id:
            case "agree":
                if role in interaction.user.roles or interaction.user.id == 549056425943629825:
                    temp_money_list = [int(item['temp_money']) for item in deposits if 'temp_money' in item]
                    temp_date_list = [item['temp_date'] for item in deposits if 'temp_date' in item]
                    user,money,date_time = await write(user=orinigal_user,money=temp_money_list[0],date=temp_date_list[0])
                    embed = Embed(title="<a:check:1043896950484902009> | 交易成功!",description=f"已將 {user.name} 的定存紀錄寫入至資料庫!",colour=disnake.Colour.green())
                    guild = self.bot.get_guild(978571136050806844)
                    role = guild.get_role(1006196207447719986)
                    await orinigal_user.add_roles(role)
                    embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
                    await admin_message.edit(embed=embed,view=None)
                    async with aiohttp.ClientSession() as session:
                        #https://discord.com/api/webhooks/1089207116612513843/o_AB92mdds4IA3soqpcyu5S63dJcpy_vAZ26j57UV_wuj4yWhKgks8uUO24Tv10Qid-R
                        webhook = Webhook.from_url('https://discord.com/api/webhooks/1097144035501678602/yBEZvY8305auz7FJz9oARu08tfi-BAmpig7j7NFZauDPJHr7IQcJrjlXR6LNR3GulEkY', session=session)
                        original = await webhook.fetch_message(message.id)
                        if interaction.user.id == 341556620536578048:
                            contract_edit_text = f"[存款條] 本人 {user.mention} 於NN銀行存入yeecord幣 {int(money)}$, 依協調定存一日利息10$, {date_time}可領取原存入全額與相應利息, 若本人要求早於{date_time}\n領出, 只可領取原存入金額之一半, 利息悉數取消。\n本人簽名 :{user.name} \n銀行方簽名: 🫔"
                        else:
                            contract_edit_text = f"[存款條] 本人 {user.mention} 於NN銀行存入yeecord幣 {int(money)}$, 依協調定存一日利息10$, {date_time}可領取原存入全額與相應利息, 若本人要求早於{date_time}\n領出, 只可領取原存入金額之一半, 利息悉數取消。\n本人簽名 :{user.name} \n銀行方簽名: <:castle_draw:994489310176882738>"
                        await original.edit(content=contract_edit_text)
                    await asyncio.sleep(3)
                    await admin_message.delete()
            case "deny":
                if role in interaction.user.roles:
                    embed = Embed(title="❌ | 已拒絕定存",description=f"",colour=disnake.Colour.red())
                    await interaction.edit_original_message(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=Game(name="管理NN銀行的大小事中.."))
        if not self.check_date.is_running():
            self.bot.loop.create_task(self.check_date.start())
        print("Bank Ready!")

    @commands.slash_command(name=Localized(data={Locale.zh_TW: "產生合約"}), description="透過此指令來一鍵定存!")
    async def contract(self, interaction: ApplicationCommandInteraction, money:int = Param(name=Localized(data={Locale.zh_TW: "金額"}),description=Localized(data={Locale.zh_TW: "定存的金額"}))):
        if isinstance(money, int) and money >= 0 and money % 1 == 0:
            if money >= 1000:
                try:
                    with open(f"./database/{interaction.user.id}.json","r",encoding="utf-8'") as f:
                        deposits = json.load(f)
                except json.decoder.JSONDecodeError:
                        deposits = []
                global message, orinigal_user, admin_message
                channel = self.bot.get_channel(1004299585444917248)
                date_time_str, message, orinigal_user = await generate(bot=self.bot,interaction=interaction,money=money)
                temp_data = {"temp_money":money,"temp_date":date_time_str}
                deposits.append(temp_data)
                with open(f"./database/{interaction.user.id}.json","w",encoding="utf-8'") as f:
                    json.dump(deposits,f)
                admin_embed = Embed(title="<:emoji_107:1067077063246368799> | 定存通知!",description=f"{interaction.user.name} 想要定存!\n金額:`{money}$`\n到期日: {date_time_str}",colour=disnake.Colour.random())
                admin_embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
                view = Menu()
                admin_message = await channel.send(embed=admin_embed,view=view)
            else:
                embed = Embed(title="❌ | 金額不可低於1000$",description=f"",colour=disnake.Colour.red())
                await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            embed = Embed(title="❌ | 請輸入正確的金額!",description=f"",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)

    
    @commands.slash_command(name=Localized(data={Locale.zh_TW: "查看使用者定存狀況"}), description="限銀行方查詢",options=[Option(name="user",description="指定的使用者", type=OptionType.user, required=True)])
    async def search_user(self, interaction: ApplicationCommandInteraction, user:Optional[Member]):
        if interaction.user.id in [341556620536578048,597106331324907520,549056425943629825]:
            await search(interaction=interaction,member=user)
        else:
            embed = disnake.Embed(title="❌ | 你無權執行此指令!",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)
    
    @commands.slash_command(name=Localized(data={Locale.zh_TW: "查看定存狀況"}), description="透過此指令來一目了然自己目前的定存吧!")
    async def search_myself(self, interaction: ApplicationCommandInteraction):
            await search(interaction=interaction,member=interaction.user)
    
    @commands.slash_command(name=Localized(data={Locale.zh_TW: "移除使用者定存"}), description="限銀行方查詢",options=[Option(name="user",description="指定的使用者", type=OptionType.user, required=True),Option(name="order",description="要移除的第幾筆，︀如無指定則全數移除",required=False)])
    async def remove_deposits(self, interaction: ApplicationCommandInteraction, user:Optional[Member], order:int = Param(name=Localized(data={Locale.zh_TW: "第幾筆"}),description=Localized(data={Locale.zh_TW: "要移除的第幾筆，︀如無指定則全數移除"}),default=None)):
        await remove(interaction=interaction, member=user,order=order)

    @commands.slash_command(name="load_extension",guild_ids=[1053616489128808499],options=[Option(name="extension",description="噓",type=OptionType.string,required=True)])
    async def load(self,interaction: ApplicationCommandInteraction, extension:str):
        if interaction.user.id == 549056425943629825:
            for fn in os.listdir("./cogs"):
                if fn.endswith(".py"):
                    self.bot.load_extension(f"cogs.{extension}")
            embed = Embed(title="<:check:1036160202174627840> | 加載成功!",description=f"目標cog:{extension}",colour=Colour.green())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("你不是擁有者!",ephemeral=True)
    
    @commands.slash_command(name="unload_extension",guild_ids=[1053616489128808499],options=[Option(name="extension",description="噓",type=OptionType.string,required=True)])
    async def unload(self,interaction: ApplicationCommandInteraction, extension:str):
        if interaction.user.id == 549056425943629825:
            for fn in os.listdir("./cogs"):
                if fn.endswith(".py"):
                    self.bot.unload_extension(f"cogs.{extension}")
            embed = Embed(title="<:check:1036160202174627840> | 卸載成功!",description=f"目標cog:{extension}",colour=Colour.green())
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("你不是擁有者!",ephemeral=True)
    
    @commands.slash_command(name="reload_extension",guild_ids=[1053616489128808499],options=[Option(name="extension",description="噓",type=OptionType.string,required=True)])
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