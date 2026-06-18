import json


def setServerLanguage( id: int, language: str ):
    language = language.strip()

    if language not in ( "ko", "en", "jp" ):
        return False

    with open( "data/language_config.json", 'r', encoding="UTF8" ) as f:
        LANGUAGE_CONFIG: dict[ str, str ] = json.load( f )

    LANGUAGE_CONFIG[ str( id ) ] = language

    with open( "data/language_config.json", 'w', encoding="UTF8" ) as f:
        json.dump( LANGUAGE_CONFIG, f )

    return language 