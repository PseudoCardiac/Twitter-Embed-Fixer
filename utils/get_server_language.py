import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import discord


def getServerLanguage( msg: "discord.Message" ):
    """
    디스코드 메시지로부터 서버 ID를 찾아 그 서버의 언어 설정을 반환한다. \\
    언어가 설정되지 않은 경우 영어로 설정한 뒤 `"en"`을 반환한다.

    :param discord.Message msg: 서버 ID를 찾을 메시지

    :return: 언어 설정 (`"ko"`, `"en"`, `"jp"` 중 하나)
    """

    # 예외: 길드를 찾을 수 없음 (웬만하면 일어나지 않을 일이라 예상됨)
    if msg.guild is None:
        print( "====================================" )
        print( "메시지가 보내진 길드를 찾을 수 없음!" )
        print( msg.content )
        print( msg.created_at.strftime( "%Y-%m-%d %H:%M:%S" ) )
        return "en"

    with open( "data/language_config.json", 'r', encoding="UTF8" ) as f:
        LANGUAGE_CONFIG: dict[ str, str ] = json.load( f )

    # 길드 ID와 언어 설정 취득
    ID = msg.guild.id
    language = LANGUAGE_CONFIG.get( str( ID ) )

    # 언어 설정이 없음
    if language is None:
        # 새로운 설정 등록
        LANGUAGE_CONFIG[ str( ID ) ] = "en"
        with open( "data/language_config.json", 'w', encoding="UTF8", ) as f:
            json.dump( LANGUAGE_CONFIG, f, indent=4 )

        language = "en"

    return language