from typing import Optional
from disnake.ext import commands
from disnake import ApplicationCommandInteraction, Embed, Colour, SelectOption, MessageInteraction
from disnake.ui import StringSelect, View
import disnake

class Dropdown(StringSelect):
    def __init__(self):
        super().__init__(placeholder="📖指令教學",max_values=1,min_values=1,custom_id="help_menu",options=[
                        SelectOption(label="定存教學",description="不會使用點這",emoji="🔍",value="1"),
                        SelectOption(label="工作人員名單",description="我需要新鮮的肝",emoji="<:936168862045597726:1068505975809638470>",value="2")
                    ])
        
    async def callback(self, interaction: disnake.MessageInteraction):
        print(self.values[0])
        match self.values[0]:
            case "1":
                embed = Embed(
                        title="🔍| 定存教學",
                        description="",
                        colour=Colour.random())
                embed.add_field(name="如何定存？",value="""你可以輸入 </contract:1088833824391168152> 這個指令來產生一個定存合約
                再輸入定存金額並發送指令後 ，你的合約會位於 <#1004299585444917248>
                一但銀行方通過了你的申請，你的定存便會正式生效。""")
                embed.add_field(name="如何查詢定存？",value="""你可以使用 </view:1089185491632537652>，來一目了然你目前定存了幾筆、到期日、存入金額
                如果你遇到了問題或是想提出建議，可以 <@549056425943629825> 以尋求支援""",inline=False)
                await interaction.response.send_message(
                    embed=embed, ephemeral=True
                )
            case "2": #工作人員名單
                embed = Embed(
                        title="<:936168862045597726:1068505975809638470> 工作人員名單",
                        description="",
                        colour=Colour.random())
                
                embed.add_field(name="主要開發人員 & 指令設計 & 架構設計",value="∙ Man頭(´・ω・)#8870")
                embed.add_field(name="特別感謝",value="∙ NN#3093 & 蛋餅#9168 (銀行創始人&經理)\n∙ Nat1an#0001 (技術支持)",inline=False)
                embed.set_footer(text="Made by 肝 & ❤️")

                await interaction.response.send_message(
                    embed = embed, ephemeral=True
                )               


class View(View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.add_item(Dropdown())

class Help(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot 
        super().__init__()
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(View())

    @commands.slash_command(name="help",description="指令幫助")
    async def help(self, interaction:ApplicationCommandInteraction):
        view = View()
        await interaction.response.send_message(
            embed = Embed(
                title="",
                description="如何使用這台ㄐ器人？\n你可以透過底下的選單來查看你需要的幫助類型喔<:emoji_112:1100426140130218127>\n有任何問題都可以 <@549056425943629825> 來尋求幫助，祝使用順利！",
                colour=Colour.random()
            ).set_author(name="嘿! 歡迎使用定存小幫手",icon_url=self.bot.user.avatar.url),
            view=view
        )

def setup(bot):
    bot.add_cog(Help(bot))