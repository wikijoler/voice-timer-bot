print("Bot 正在启动中...")

# 导入需要的库
import discord
from discord.ext import commands, tasks
import datetime
import pytz
import os

# 从环境变量中读取 Token 和服务器 ID
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
guild_id_str = os.getenv("DISCORD_GUILD_ID")
if not guild_id_str:
    raise RuntimeError("❌ 环境变量 DISCORD_GUILD_ID 未设置！")
GUILD_ID = int(guild_id_str)

ROLE_NAME = "别当哈基耶了"  # 要操作的角色名
guild = None  # 用于全局缓存服务器对象

# 设置 Intents（必须启用成员列表权限）
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

# 创建 bot 实例
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot 启动后执行
@bot.event
async def on_ready():
    global guild
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        print("❌ 未找到服务器，请检查 GUILD_ID 是否正确 & Bot 是否已加入服务器")
    else:
        print(f"✅ 已获取服务器：{guild.name}")
    print(f"🟢 已上线：{bot.user}")
    check_and_toggle_role.start()

# 判断是否为周一到周五
def is_weekday():
    today = datetime.datetime.now(pytz.timezone("Asia/Shanghai")).weekday()
    return today < 5  # 周一~周五：0~4

# 每分钟检查一次是否应操作角色
@tasks.loop(minutes=1)
async def check_and_toggle_role():
    now = datetime.datetime.now(pytz.timezone("Asia/Shanghai"))
    current_time = now.strftime("%H:%M")

@tasks.loop(minutes=1)
async def check_and_toggle_role():
    now = datetime.datetime.now(pytz.timezone("Asia/Shanghai"))
    print(f"[定时任务] 当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not is_weekday():
        return  # 周六日不处理

    if not guild:
        print("⚠️ 尚未获取服务器，跳过本次检查")
        return

    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    if not role:
        print(f"⚠️ 未找到角色：{ROLE_NAME}")
        return

    # 凌晨 2:30 → 禁语（移除角色）
    if current_time == "02:30":
        for member in guild.members:
            if role in member.roles:
                try:
                    await member.remove_roles(role)
                except Exception as e:
                    print(f"⚠️ 移除失败：{member} | {e}")
        print(f"[{current_time}] ✅ 已移除角色：{ROLE_NAME}")

    # 早上 9:00 → 解禁（添加角色）
    elif current_time == "09:00":
        for member in guild.members:
            if role not in member.roles:
                try:
                    await member.add_roles(role)
                except Exception as e:
                    print(f"⚠️ 添加失败：{member} | {e}")
        print(f"[{current_time}] ✅ 已添加角色：{ROLE_NAME}")

print("准备连接 Discord...")
bot.run(TOKEN)
