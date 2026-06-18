import json
import re
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import discord

with open( "../data/language_config.json", 'r', encoding="UTF8" ) as f:
    LANGUAGE_CONFIG: dict[ str, str ] = json.load( f )

with open( "../data/messages.json", 'r', encoding="UTF8" ) as f:
    MESSAGES: dict[ str, str ] = json.load( f )

# 트위터 URL
TWITTER_URL = re.compile( r"https:\/\/(x|twitter)\.com\/.+\/status\/\d+" )
# 스포일러 컨텐츠
SPOILER = re.compile( r"\|\|(.+?)\|\|" )


def convertUrl( msg: discord.Message ):
    """
    디스코드 메시지에서 트위터 URL을 찾아, 포매팅된 메시지 컨텐츠로 반환한다.

    :param discord.Message msg: 처리할 디스코드 메시지

    :return: 트위터 URL이 포함된 경우 포매팅된 메시지 컨텐츠를 반환
    :return: 트위터 URL이 포함되지 않은 경우 `False` 반환
    """
    
    # 메시지나 메시지 내용이 없으면 리턴
    if not ( msg and msg.content ) :
        return False

    # 정규식 매치
    xUrlMatch = re.match( TWITTER_URL, msg.content )

    # 메시지에 트위터 URL이 포함되지 않으면 리턴
    if not xUrlMatch:
        return False

    # 메시지에서 추출한 트위터 URL (여러 개일 경우 그 중 첫 번째)
    xUrl = xUrlMatch.group()

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

    if isUrlSpoilered:
        # 스포일러 처리 후 반환
        return MESSAGES[ "spoileredOutput" ] + converted + ")||"
    else:
        return MESSAGES[ "output" ] + converted + ")"