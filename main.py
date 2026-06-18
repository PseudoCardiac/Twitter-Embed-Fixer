import discord, os, json
from dotenv import load_dotenv
from utils import formatUrl, getServerLanguage, extractUrl, getServerLanguage, setServerLanguage
from cogs import myView


INTENTS = discord.Intents.all()
CLIENT = discord.Client( intents=INTENTS )
TREE = discord.app_commands.CommandTree( CLIENT )


with open( "data/messages.json", 'r', encoding="UTF8" ) as f:
    MESSAGES: dict[ str, dict [str, str] ] = json.load( f )


@CLIENT.event
async def on_ready():
    print( "===== TWITTER EMBEDDER READY =====" )
    # TODO: 참여 중인 길드 목록 표시


@CLIENT.event
async def on_message( msg: discord.Message ):
    # 봇에 의해 보내진 메시지에는 반응하지 않음
    if msg.author.bot:
        return

    # 멘션 + 언어 키워드 -> 언어 설정 변경
    if msg.content.startswith( "<@1516141205530874007>" ):
        originalLanguage = getServerLanguage( msg )
        language = setServerLanguage( msg.guild.id, msg.content.partition( "<@1516141205530874007>" )[2] )    # type: ignore

        if language:
            await msg.reply( MESSAGES[ "languageChanged" ][ language ] )
        else:
            await msg.reply( MESSAGES[ "languageNotChanged" ][ originalLanguage ] )

        return

    # 메시지에 포함된 트위터 URL 또는 False
    xUrl = extractUrl( msg )

    # 메시지에 트위터 URL이 포함되지 않은 경우 리턴
    if not xUrl:
        return

    content = formatUrl( msg, xUrl )
    language = getServerLanguage( msg )
    view = myView( xUrl, language )

    try:
        await msg.delete()
    except:
        print( f"메시지를 삭제할 수 없었음! ({ msg.created_at.strftime( "%d/%m/%Y %H:%M:%S" ) })" )

    try:
        await msg.channel.send( content=content, view=view, silent=True )
    except:
        print( f"메시지를 전송할 수 없었음! ({ msg.created_at.strftime( "%d/%m/%Y %H:%M:%S" ) })" )


@CLIENT.event
async def on_interaction( interaction: discord.Interaction ):
    # 임베드 삭제 버튼이 눌렸을 때에만 반응
    if interaction.type == discord.InteractionType.component and interaction.custom_id == "deleteButton":
        msg = interaction.message

        # 일어나서는 안 되는 일
        if msg is None:
            print( "삭제할 메시지를 찾을 수 없었음!" )
            print( interaction.created_at.strftime( "%Y-%m-%d %H:%M:%S" ) )
            return

        LANGUAGE = getServerLanguage( msg )

        # 버튼을 누른 유저와 메시지에 멘션된 유저가 서로 다름
        if ( interaction.user != msg.mentions[0] ):
            # 메시지 삭제 거부
            await interaction.response.send_message( content=MESSAGES[ "notYourMessage" ][ LANGUAGE ], ephemeral=True )
        # 버튼을 누른 유저와 메시지에 멘션된 유저가 서로 일치
        else:
            try:
                await msg.delete()
                await interaction.response.send_message( content=MESSAGES[ "messageDeleted" ][ LANGUAGE ], ephemeral=True )
            except:
                print( "메시지를 삭제할 수 없었음!" )
                print( interaction.created_at.strftime( "%Y-%m-%d %H:%M:%S" ) )
                await interaction.response.send_message( content=MESSAGES[ "messageDeleteError" ][ LANGUAGE ], ephemeral=True )


load_dotenv("../.env")
CLIENT.run( os.environ.get( "FIX_TWITTER_TOKEN" ) ) # type: ignore