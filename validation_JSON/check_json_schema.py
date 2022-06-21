import json
# from systemd import journal
from LoggerJournal.Logger import Logger


########################################################
#
# Validate JSON string with JSON schema file.
#
# Use function check_in for IN request.
# Use function check_out for OUT request.
#
# Function parametr:
#     uri        - uri like '/meter/data/moment'
#     scriptname - use __file__ as parametr
#     request    - json string for test
#
# Example:
#     If you uri is '/meter/data/moment' and
#     scriptname is 'read_*.py' and
#     you want to check the incoming JSON string (IN):
#     the file with the json schema should be named as
#     meter_data_moment_read_in.schema
#
########################################################
# Здесь расположим функции необходимые для валидации JSON схем
########################################################
# Функция для получения нужного названия API
def get_name_API(API_path):
    """

    Вспомогательная Функция для получения нужного названия API через ее путь
    Необходима для нахождения нужной схемы

    :param API_path: ПУть до API
    :return:
    """
    from uspd_paths import \
        _meter_db_settings_path, \
        _meter_db_data_path, \
        _meter_devices_path, \
        _event_db_settings_path, \
        _messenger_db_api_path, \
        _iec60870_db_api_path, \
        _charge_stations_db_api_path

    # Ищем путь по названию API
    API_dict = {
        _event_db_settings_path: "EventAPI",
        _meter_db_data_path: "MeterDataAPI",
        _meter_devices_path: "MeterDeviceAPI",
        _meter_db_settings_path: "MeterSettingsAPI",
        # ///
        _iec60870_db_api_path: "iec60870",
        _messenger_db_api_path: "Messenger",
        _charge_stations_db_api_path: "Charge",
    }

    name_path = API_dict.get(API_path)

    return name_path


########################################################
# Вспомогательная функция обработки постфикса

def get_postfix(postfix):
    """

    Вспомогательная функция обработки постфикса
    Необходима для нахождения нужной схемы
    :param postfix: Постфикс - это входной/выходной JSON
    :return:
    """

    postfix_dict = \
        {
            'in': 'in',
            'out': 'out',
        }
    name_postfix = postfix_dict.get(postfix)

    return name_postfix


########################################################
# Вспомогательная функция обработки типа запроса

def get_request_type(request_type):
    """
    Вспомогательная функция обработки типа запроса

    Необходима для нахождения нужной схемы

    :param request_type: Тип запроса
    :return:
    """
    request_dict = {
        'GET': 'GET',
        'POST': 'POST',
        'PUT': 'PUT',
        'DELETE': 'DELETE',
        # //   И маленькими буквами если чо
        'get': 'GET',
        'post': 'POST',
        'put': 'PUT',
        'delete': 'DELETE',
    }
    name_request_type = request_dict.get(request_type)

    return name_request_type


########################################################
# Получаем Путь до нашей JSON схемы

def get_name_schema(API, postfix, table_name, request_type):
    """
    Получаем Путь до нашей JSON схемы для API

    :param API: Путь / имя самой API
    :param postfix: Постфикс - это входной/выходной JSON
    :param table_name: Имя таблицы с которой работает API
    :param request_type: Тип запроса
    :return:
    """
    filename = './schema/'
    API_path = 'API/'
    # Итак - сначала определяем путь до АПИ
    API_name = get_name_API(API_path=API)
    # Теперь определяем тип нашего запроса
    request_name = get_request_type(request_type=request_type)
    # Получаем постфикс
    postfix_name = get_postfix(postfix=postfix)

    # Теперь проверяем что точно все точно хорошо
    if (API_name is not None) and (request_name is not None) and (postfix_name is not None):
        # Получаем имя нашей JSON схемы
        # Имя рождается из составляющих - шаблон :
        # Постфикс_запрос_Таблица
        Name_schema = str(postfix_name) + "_" + str(request_name) + "_" + str(table_name) + '.schema'
        # Теперь прописываем и путь
        Name_schema = filename + str(API_path) + str(API_name) + "/" + Name_schema
        # Возвращаем
        return Name_schema
    # Иначе возвращаем пустоту
    else:
        return None


########################################################
########################################################

########################################################
# УМ-40
# Получаем имя JSON схемы по URL
def get_name_schema_by_url_UM40_SMART(url):
    filename = './schema/'

    url = str(url).replace("/", "_")
    # Необходимо правильно сделать путь - Обрезать URL
    Name_schema = url[1:] + '.schema'
    API_name = "JSON_protocol/"
    UM40 = 'UM40/'
    # Необходимо правильно сделать путь - Обрезать URL +слэш
    url_path = url[1:] + '/'
    # Теперь прописываем и путь
    Name_schema = filename + API_name + UM40 + url_path + Name_schema
    # Возвращаем
    return Name_schema


########################################################
# УМ-31
# Получаем имя JSON схемы по URL
def get_name_schema_by_url_UM31_SMART(url):
    filename = './schema/'

    url = str(url).replace("/", "_")
    # Необходимо правильно сделать путь - Обрезать URL
    Name_schema = url[1:] + '.schema'
    API_name = "JSON_protocol/"
    UM40 = 'UM31/'
    # Необходимо правильно сделать путь - Обрезать URL +слэш
    url_path = url[1:] + '/'
    # Теперь прописываем и путь
    Name_schema = filename + API_name + UM40 + url_path + Name_schema
    # Возвращаем
    return Name_schema


########################################################
# Функция проверки по JSON схеме по протоколу JSON_backend - Нужно ли делать
def check_json_backend_protocol(method, body):
    # Первое - Проверяем нужно ли проверять

    non_body = ['GET', 'get', 'delete', 'DELETE']
    # ЕСЛИ информация пришла
    if bool(body):
        # Не приходит в GET и DELETE
        if method not in non_body:
            return True
        # В остальных случаях - Ошибка
        else:
            return False
    else:
        # Проверяем должно ли -
        # Не приходит в GET и DELETE
        if method not in non_body:
            return True
        # В остальных случаях - Ошибка
        else:
            return False


########################################################
# Открытие JSON схемы по ее пути
def open_JSON_schema(schema_path):
    """
    Здесь Открываем наш файл JSON схемы
    :param schema_path: Путь до нашей JSON схемы
    :return:
    """
    # Проверяем на валидность
    if schema_path is not None:
        try:
            # Открываем
            with open(schema_path, 'r') as file:
                schema = json.loads(file.read())
                return schema

        # Если произошла ошибка - логируем
        except Exception as e:
            Text_error = 'Can not open file: ' + str(schema_path) + " .\n error  :" + str(e)
            Logger(Name="Open JSON schema").ERROR(text=Text_error)
            return False

    # Если У нас ошибка
    else:
        Text_error = 'File not found'
        Logger(Name="Open JSON schema").ERROR(text=Text_error)
        return False


########################################################
# Преобразование JSON

def decode_JSON_value(JSON):
    """
    Преобразование JSON
    :param JSON:
    :return:
    """
    # json_value = False
    # Пытаемся преобразовать JSON
    try:
        # Если это словарь , то сразу пропускаем
        if type(JSON) is dict:
            json_value = JSON
        # Переводим
        else:
            json_value = json.loads(JSON)
    # Если ошибка - то сразу логируем это и возвращаем False
    except Exception as e:

        Text_error = 'Error decode JSON. \n Error :' + str(e)
        Logger(Name="Decode JSON").ERROR(text=Text_error)
        json_value = False

    # finally:
    #     return json_value
    return json_value


########################################################
# Проверка согласно JSON схеме
def validate_JSON_to_schema(JSON: dict, schema_path: str):
    """

    Проверка согласно JSON схеме

    :param JSON: JSON запрос
    :param schema_path: путь до схемы
    :return:
    """

    from jsonschema import validate

    # Сначала получаем СХЕМУ по ее пути
    schema = open_JSON_schema(schema_path=schema_path)
    # Теперь смотрим на свой JSON - Если он коректный - переводим в словарь
    JSON_dict = decode_JSON_value(JSON=JSON)

    if (not schema) or (not JSON_dict):
        # Логируем это
        Text_error = "Not JSON schema and not validate JSON string request"
        Logger(Name="check JSON schema").ERROR(text=Text_error)
        # и возвращаем фалсе
        return False

    else:
        try:
            validate(instance=JSON_dict, schema=schema)

        except Exception as e:
            # Формируем Лог
            Text_error = 'Can not validate JSON string request.\n JSON :' + str(JSON) + \
                         "\n with JSON schema:  " + str(schema_path) + \
                         "\n Error : " + str(e)
            Logger(Name="check JSON schema").ERROR(text=Text_error)

            return False
        return True


########################################################
# Проверка json для API
########################################################
def check(
        # САМ JSON
        JSON,
        # Тип запроса GET-POST-PUT-DELETE
        request_type,
        # ПОСТФИКС - in - out
        postfix,
        # ПУТЬ ДО АПИ
        API,
        # ИМЯ ТАБЛИЦЫ
        table_name
):
    """
    Функция сравнения для JSON  что летят в API
    :param JSON: САМ JSON
    :param request_type: Тип запроса GET-POST-PUT-DELETE
    :param postfix: ПОСТФИКС - in - out - валидируем на входе или на выходе из API
    :param API: ПУТЬ ДО АПИ
    :param table_name: ИМЯ ТАБЛИЦЫ
    :return:
    """

    # для начала - получаем путь до JSON схемы
    schema_path = get_name_schema(API=API, postfix=postfix, table_name=table_name, request_type=request_type)

    # Теперь опускаем все это в валидатор

    result = validate_JSON_to_schema(JSON=JSON, schema_path=schema_path)

    return result


########################################################
# Проверка json для Протокола JSON-Backend-SMART-40
########################################################

def check_UM40(url, method, JSON):
    """
    Проверка json для Протокола JSON-Backend-SMART-40

    :param url:
    :param method:
    :param JSON:
    :return:
    """
    # Выравниваем сам метод
    method = get_request_type(request_type=method)

    # Продолжаем только в том случае - если такой метод есть
    if method is not None:
        # Сначала проверяем - Нужно ли лидировать
        if check_json_backend_protocol(method=method, body=JSON):
            # Теперь получаем путь до схемы
            schema_path = get_name_schema_by_url_UM40_SMART(url=url)
            # И валидируем
            result = validate_JSON_to_schema(JSON=JSON, schema_path=schema_path)
            return result

        # Иначе - Отправляем что все ок
        else:
            return True
    # Если нет такого метода
    else:
        # Логируем что такого метода нет
        Logger("Request").ERROR(text="Method Not Allowed")
        return False


########################################################
# Проверка json для Протокола JSON-Backend-SMART-31
########################################################

def check_UM31(url, method, JSON):
    """
    Проверка json для Протокола JSON-Backend-SMART-40

    :param url:
    :param method:
    :param JSON:
    :return:
    """
    # Выравниваем сам метод
    method = get_request_type(request_type=method)

    # Продолжаем только в том случае - если такой метод есть
    if method is not None:
        # Сначала проверяем - Нужно ли лидировать
        if check_json_backend_protocol(method=method, body=JSON):
            # Теперь получаем путь до схемы
            schema_path = get_name_schema_by_url_UM31_SMART(url=url)
            # И валидируем
            result = validate_JSON_to_schema(JSON=JSON, schema_path=schema_path)
            return result

        # Иначе - Отправляем что все ок
        else:
            return True
    # Если нет такого метода
    else:
        # Логируем что такого метода нет
        Logger("Request").ERROR(text="Method Not Allowed")
        return False
