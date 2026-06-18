import json


def setServerLanguage( id: int, language: str ):
    """
    서버의 언어 설정을 변경하고 반환한다.
    잘못된 키워드가 주어질 경우 False를 반환한다.

    :param int id: 서버의 ID.
    :param str language: (검사되지 않은) 언어 키워드
    """

    language = language.strip()
    
    if language not in ( "ko", "en", "jp" ):
        return False

    with open( "data/language_config.json", 'r', encoding="UTF8" ) as f:
        LANGUAGE_CONFIG: dict[ str, str ] = json.load( f )

    LANGUAGE_CONFIG[ str( id ) ] = language

    with open( "data/language_config.json", 'w', encoding="UTF8" ) as f:
        json.dump( LANGUAGE_CONFIG, f, indent=4 )

    return language 