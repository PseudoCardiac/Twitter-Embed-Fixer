import json
import re
from typing import TYPE_CHECKING
from utils.get_server_language import getServerLanguage
if TYPE_CHECKING:
    import discord


with open( "data/messages.json", 'r', encoding="UTF8" ) as f:
    MESSAGES: dict[ str, dict [str, str] ] = json.load( f )


# 트위터 URL 포맷
TWITTER_URL = re.compile( r"https:\/\/(x|twitter)\.com\/.+\/status\/\d+" )
# 스포일러 컨텐츠 포맷
SPOILER = re.compile( r"\|\|(.+?)\|\|" )


def formatUrl( msg: "discord.Message", xUrl: str ):
    """
    원본 메시지와 그 메시지에 포함된 트위터 URL을 포매팅된 메시지로 변환한다.

    :param discord.Message msg: 처리할 디스코드 메시지
    :param str xUrl: 메시지에 포함된 트위터 URL

    :return str: 포매팅된 메시지 컨텐츠
    """

    # 스포일러 처리된 내용 찾기
    isSpoilered = re.search( SPOILER, msg.content )

    if isSpoilered:     # 스포일러 처리된 내용이 있음
        spoileredText = str( isSpoilered.group( 1 ) )
    else:               # 스포일러 처리된 내용이 없음
        spoileredText = ""

    # 트위터 URL이 스포일러 처리되어 있는지 판별
    isUrlSpoilered = bool( re.match( TWITTER_URL, spoileredText ) )

    # URL 변환
    converted = re.sub( r"https:\/\/(x|twitter)\.com", "https://fxtwitter.com", xUrl )

    # 언어 설정 취득
    language = getServerLanguage( msg )

    # 유저 아이디 취득
    id = msg.author.id

    if isUrlSpoilered:
        # 스포일러 처리 후 반환
        return f"<@{id}>" + MESSAGES[ "spoileredOutput" ][ language ] + converted + ")||"
    else:
        return f"<@{id}>" + MESSAGES[ "output" ][ language ] + converted + ")"