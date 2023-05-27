from disnake.ext import commands
from disnake import ApplicationCommandInteraction, Option, OptionType,Embed,Colour
import disnake

class ExceptionHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Error_Handle Ready!")

    @commands.Cog.listener()
    async def on_slash_command_error(self, interaction: ApplicationCommandInteraction, error) -> None:
        print(error)
        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(title="<:x_mark:1033955039615664199> 無法執行此指令", description=f"請確認您是否有 `{error}` 的權限",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)
        elif isinstance(error, commands.ChannelNotFound):
            embed = disnake.Embed(title="<:x_mark:1033955039615664199> 找不到此頻道",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)
        elif isinstance(error, commands.RoleNotFound):
            embed = disnake.Embed(title="<:x_mark:1033955039615664199> 找不到此身分組",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)
        elif isinstance(error, disnake.NotFound):
            embed = disnake.Embed(title=f"<:x_mark:1033955039615664199> 找不到 {error}",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = disnake.Embed(title=f"<:x_mark:1033955039615664199> 機器人沒有 {error} 的權限",colour=disnake.Colour.red())
            await interaction.response.send_message(embed=embed,ephemeral=True)
        elif isinstance(error, commands.CommandOnCooldown):
            pass
        else:
            embed = disnake.Embed(title=":x: 阿喔，看來你用神奇魔法發現了一個漏洞 <:hahahaha:1038449572915187763>", description=f"```{error}```\n <a:853174934670540811:1038449712359022643> 已自動回報給作者! Bug反饋可以聯繫Man頭(´・ω・)#8870",colour=disnake.Colour.red())
            embed.set_footer(text="機器人作者by 鰻頭", icon_url="https://cdn.discordapp.com/avatars/949535524652216350/f1e7eb9ffd7d225971468d24748b1ba0.png?size=512")
            await interaction.response.send_message(embed=embed)
def setup(bot):
    bot.add_cog(ExceptionHandler(bot))