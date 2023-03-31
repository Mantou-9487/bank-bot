import disnake
import json
import asyncio
import os
import aiohttp

from datetime import timedelta, date,datetime
from disnake import Webhook
from disnake.ext import commands,tasks
from disnake.ext.commands import Param
from disnake import ApplicationCommandInteraction,Localized,Locale,Member,Option,OptionType,Game,Embed,Colour,MessageInteraction,Status
from core.functions import generate,search,remove,write
from typing import Optional
from variables import Mode

class Mode:
    def __init__(self):
        self.current_mode = "normal"



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
        super().__init__()
    
    @commands.Cog.listener(name="on_message_interaction")
    async def on_message_interaction(self, interaction: MessageInteraction):
        role = interaction.guild.get_role(1008350002332045332)
        with open(f"./database/{orinigal_user.id}.json","r",encoding="utf-8'") as f:
                deposits = json.load(f)
        match interaction.data.custom_id:
            case "agree":
                if role in interaction.user.roles or interaction.user.id == 549056425943629825:
                    temp_money_list = [int(item['temp_money']) for item in deposits if 'temp_money' in item]
                    user,money,date_time = await write(user=orinigal_user,money=temp_money_list[0])
                    embed = Embed(title="✅ | 執行成功!",description=f"已將 {user.name} 的定存紀錄寫入至資料庫",colour=disnake.Colour.green())
                    await admin_message.edit(embed=embed,view=None)
                    async with aiohttp.ClientSession() as session:
                        #https://discord.com/api/webhooks/1089207116612513843/o_AB92mdds4IA3soqpcyu5S63dJcpy_vAZ26j57UV_wuj4yWhKgks8uUO24Tv10Qid-R
                        webhook = Webhook.from_url('https://discord.com/api/webhooks/1089207116612513843/o_AB92mdds4IA3soqpcyu5S63dJcpy_vAZ26j57UV_wuj4yWhKgks8uUO24Tv10Qid-R', session=session)
                        original = await webhook.fetch_message(message.id)
                        if interaction.user.id == 341556620536578048:
                            contract_edit_text = f"[存款條] 本人 {user.mention} 於NN銀行存入yeecord幣 {int(money)}$, 依協調定存一日利息10$, {date_time}可領取原存入全額與相應利息, 若本人要求早於{date_time}\n領出, 只可領取原存入金額之一半, 利息悉數取消。\n本人簽名 :{user.name} \n銀行方簽名: 🫔"
                        else:
                            contract_edit_text = f"[存款條] 本人 {user.mention} 於NN銀行存入yeecord幣 {int(money)}$, 依協調定存一日利息10$, {date_time}可領取原存入全額與相應利息, 若本人要求早於{date_time}\n領出, 只可領取原存入金額之一半, 利息悉數取消。\n本人簽名 :{user.name} \n銀行方簽名: <:castle_draw:994489310176882738>"
                        await original.edit(content=contract_edit_text)

            case "deny":
                if role in interaction.user.roles:
                    embed = Embed(title="❌ | 已拒絕定存",description=f"",colour=disnake.Colour.red())
                    await interaction.edit_original_message(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=Game(name="管理NN銀行的大小事中.."))
        print("Bank Ready!")

    Mode = commands.option_enum({"開發模式":"dev","一般模式":"normal"})
    @commands.slash_command(name="change",description="切換開發/正式模式")
    async def change_mode(self, interaction: ApplicationCommandInteraction,mode:Mode):
        if Mode.current_mode == "normal":
            Mode.current_mode = "developer"
            await interaction.response.send_message(f"已切換至 {Mode.current_mode} 模式")
            await self.bot.change_presence(activity=Game(name="正在開發模式中..可能無法使用一些服務"),status=Status.dnd)
        else:
            Mode.current_mode = "normal"
            await interaction.response.send_message(f"已切換至 {Mode.current_mode} 模式")
            await self.bot.change_presence(activity=Game(name="管理NN銀行的大小事中.."))
        

    @commands.slash_command(name=Localized(data={Locale.zh_TW: "產生合約"}), description="透過此指令來一鍵定存!")
    async def contract(self, interaction: ApplicationCommandInteraction, money:int = Param(name=Localized(data={Locale.zh_TW: "金額"}),description=Localized(data={Locale.zh_TW: "定存的金額"}))):
        if isinstance(money, int) and money >= 0 and money % 1 == 0:
            try:
                with open(f"./database/{interaction.user.id}.json","r",encoding="utf-8'") as f:
                    deposits = json.load(f)
            except json.decoder.JSONDecodeError:
                    deposits = []
            temp_data = {"temp_money":money}
            deposits.append(temp_data)
            with open(f"./database/{interaction.user.id}.json","w",encoding="utf-8'") as f:
                json.dump(deposits,f)
            global message, orinigal_user, admin_message
            if Mode.current_mode == "normal":
                channel = self.bot.get_channel(1089209730360160306)
            else:
                channel = self.bot.get_channel(1053616489128808502)
            date_time_str, message, orinigal_user = await generate(bot=self.bot,interaction=interaction,money=money)
            admin_embed = Embed(title="<:emoji_107:1067077063246368799> | 定存通知!",description=f"{interaction.user.name} 想要定存!\n金額:`{money}$`\n到期日: {date_time_str}",colour=disnake.Colour.random())
            admin_embed.set_footer(text="Made by 鰻頭",icon_url="https://cdn.discordapp.com/avatars/549056425943629825/21fb28bb033154120ef885e116934aab.png?size=1024")
            view = Menu()
            admin_message = await channel.send(embed=admin_embed,view=view)
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