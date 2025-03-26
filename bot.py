print("Bot 正在启动中...")
# 导入需要的库
import discord
from discord.ext import commands, tasks
import datetime
import pytz
import os

# 从环境变量中读取 Token 和服务器 ID
TOKEN = "MTM1NDMwMzMzOTE3NjkyMzI1Ng.GY6yN4.0f8oDYKfbrY5RDID_NwxZs0TGzfC1LzR8gx_cM"
GUILD_ID = 793587230866276362
ROLE_NAME = "别当哈基耶了"  # 要操作的角色名

# 创建 bot 实例，启用成员列表权限
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 当 bot 成功启动时
@bot.event
async def on_ready():
    print(f"已上线：{bot.user}")
    check_and_toggle_role.start()

# 判断是否是周一到周五
def is_weekday():
    today = datetime.datetime.now(pytz.timezone("Asia/Shanghai")).weekday()
    return today < 5  # 0～4 是周一到周五

# 每分钟检查一次当前时间
@tasks.loop(minutes=1)
async def check_and_toggle_role():
    now = datetime.datetime.now(pytz.timezone("Asia/Shanghai"))
    current_time = now.strftime("%H:%M")

    if not is_weekday():
        return  # 周六日不处理

    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    role = discord.utils.get(guild.roles, name=ROLE_NAME)

    if not role:
        print("未找到角色")
        return

    # 凌晨 2:30 移除角色（禁语）
    if current_time == "02:30":
        for member in guild.members:
            if role in member.roles:
                try:
                    await member.remove_roles(role)
                except:
                    pass
        print(f"[{current_time}] 移除了角色 {ROLE_NAME}")

    # 早上 9:00 添加角色（解禁）
    elif current_time == "09:00":
        for member in guild.members:
            if role not in member.roles:
                try:
                    await member.add_roles(role)
                except:
                    pass
        print(f"[{current_time}] 添加了角色 {ROLE_NAME}")
print("准备连接 Discord...")
bot.run(TOKEN)
