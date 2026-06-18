import re
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import discord


# 트위터 URL 포맷
TWITTER_URL = re.compile( r"https:\/\/(x|twitter)\.com\/.+\/status\/\d+" )


def extractUrl( msg: "discord.Message" ):
    """
    디스코드 메시지에서 트위터 URL을 찾아, 트위터 URL로 변환한다.

    :param discord.Message msg: 처리할 디스코드 메시지

    :return str: 트위터 URL이 포함된 경우 트위터 URL을 반환
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

    return xUrl