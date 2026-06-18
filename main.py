import discord
from utils.convert_url import convertUrl


INTENTS = discord.Intents.all()
CLIENT = discord.Client( intents=INTENTS )
TREE = discord.app_commands.CommandTree( CLIENT )


@CLIENT.event
async def on_ready():
    print( "===== TWITTER EMBEDDER READY =====" )
    # TODO: 참여 중인 길드 목록 표시


@CLIENT.event
async def on_message( msg: discord.Message ):
    # 봇에 의해 보내진 메시지에는 반응하지 않음
    if msg.author.bot: return

    if convertUrl( msg ):
        # TODO: 버튼 열을 포함 메시지 전송
        pass