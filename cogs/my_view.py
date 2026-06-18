import json, discord
from discord import ButtonStyle
from discord.ui import View, Button


with open( "data/messages.json", 'r', encoding="UTF8" ) as f:
    MESSAGES: dict[ str, dict [str, str] ] = json.load( f )


def myView( xUrl: str, language: str ):
    """
    변환된 디스코드 메시지에 첨부할 버튼 열을 반환합니다.

    :param string xUrl: 원본 트위터 URL
    :param language str: 메시지 언어 설정

    :return: 디스코드 UI 뷰 (`discord.ui.View`)
    """

    # 메시지 삭제 버튼 설정
    deleteButton = Button()
    deleteButton.style = ButtonStyle.danger
    deleteButton.custom_id = "deleteButton"
    deleteButton.label = MESSAGES[ "deleteLabel" ][ language ]
    deleteButton.emoji = "<:trash_bin:1516779355471352049>"

    # 원본 트윗 보기 버튼 설정
    urlButton = Button()
    urlButton.style = ButtonStyle.link
    urlButton.url = xUrl
    urlButton.custom_id = None
    urlButton.label = MESSAGES[ "urlLabel" ][ language ]
    urlButton.emoji = "<:twitter:1516779340338040883>"

    # 버튼 두 개가 포함된 뷰
    myView = View()
    myView.add_item( deleteButton )
    myView.add_item( urlButton )

    return myView


# class DeleteButton( Button ):
#     def __init__( self, language ):
#         super().__init__(
#             style = ButtonStyle.danger,
#             label = MESSAGES[ "deleteLabel" ][ language ],
#             emoji = "<:trash_bin:1516779355471352049>"
#         )

#     async def callback( self, interaction: discord.Interaction ):
#         self.parent