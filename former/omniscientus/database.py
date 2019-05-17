from . import db
from bson.objectid import ObjectId


def get_document_by_id(collection_name, document_id):
    if not check_collection_existence(collection_name):
        return False  # give error info in json format here

    collection = db[collection_name]
    return collection.find_one({'_id': ObjectId(document_id)})  # if not found, return None


def get_many_document(collection_name, query=None, offset=None, number=None):
    if not check_collection_existence(collection_name):
        return False  # give error info in json format here
    collection = db[collection_name]
    if offset is None and number is None:
        return list(collection.find(query))
    elif offset and number:
        return list(collection.find(query).skip(int(offset)).limit(int(number)))
    else:
        return False


def replace_one_document(collection_name, _filter, new_document):
    if not check_collection_existence(collection_name): return False
    collection = db[collection_name]
    return collection.replace_one(_filter, new_document)


def get_one_document(collection_name, _filter=None):
    if not check_collection_existence(collection_name): return False
    collection = db[collection_name]
    return collection.find_one(filter=_filter)


def update_one_document(collection_name, filters, new_document):
    if not check_collection_existence(collection_name):
        return False  # give error info in json format here

    collection = db[collection_name]

    new_document = error_check_for_fields(new_document, collection_name)

    if new_document is False:  # if there is an error in fields from -error_check_for_fields-
        return False
    elif not check_unique_fields(collection_name, new_document):  # if there is any duplication
        return False
    else:  # if one document is given
        collection.update_one(filters, {"$set": new_document})
        return True


def add_one_document(collection_name, document):
    print(document)
    if not check_collection_existence(collection_name):
        return False  # give error info in json format here
    collection = db[collection_name]
    document = error_check_for_fields(document, collection_name)
    if document is False:  # if there is an error in fields from -error_check_for_fields-
        return False
    elif not check_unique_fields(collection_name, document):  # if there is any duplication
        return False
    elif isinstance(document, list):  # if many documents are given
        collection.insert_many(document)
        return document
    elif isinstance(document, dict):  # if one document is given
        collection.insert_one(document)
        return document
    else:
        return False


# for comment and channel_commentator there are
# different situations, fix them later
def check_unique_fields(collection_name, document):
    collection = db[collection_name]
    uniques = {
        "channel": ["channelId"],
        "video": ["videoId"],
        "comment": ["commentId"],
        "channel_commentator": [],
        "statistic": ["statisticId"],
        "request_log": [],
        "response_log": []
    }
    # there is problem here
    # if multiple inputs are given and one of them is exist
    # it returns false, but we need to configure
    # just existence document
    if isinstance(document, list):
        for doc in document:
            for unique in uniques[collection_name]:
                if collection.find_one({unique: doc[unique]}):
                    return False
    elif isinstance(document, dict):
        for unique in uniques[collection_name]:
            if collection.find_one({unique: document[unique]}):
                return False
    return True


# ones and zeros determines necessity of field.
# if value of key is one that means the field is field necessary
def get_fields_of_collection(collection_name):
    fields = {
        'channel': {
            'channelId': 1, 'channelName': 0, 'channelTitle': 1, 'nameAbbr': 1, 'publishedAt': 1, 'statistics': 1,
            'topicDetails': 0, 'thumbnails': 0, 'activation': 0, 'activationDate': 0, 'email': 0, 'phone': 0,
            'majorSentimentClass': 0, 'score': 0, 'videoPriceFactor': 0, 'responseEtag': 0, 'itemEtag': 0,
            'commentators': 1, 'numCommentators': 1, "fans": 1, "numFans": 1, "commentsOther": 1, "commentsSelf": 1,
            'numCommentsOther': 1, "numCommentsSelf": 1
        },
        'video': {
            "responseEtag": 0, "itemEtag": 0, "videoId": 1, "categoryId": 0, "channelId": 1, "description": 0,
            "tags": 0,  "thumbnails": 0, "title": 1, "statistics": 1
        },
        'comment': {
            'commentId': 1, 'authorProfileImageUrl': 0, 'authorChannelId': 1, 'videoId': 1, 'channelId': 1,
            'textDisplay': 1, 'textOriginal': 1, 'likeCount': 0, 'publishedAt': 1, 'updatedAt': 1,
            'totalReplyCount': 0, 'commentEtag': 0, 'itemEtag': 0, 'pageInfo': 1, 'replied': 1
        },
        'channel_commentator': {
            'channelId': 1, 'commentatorId': 1, 'videoId': 1, 'commentId': 1, 'date': 1
        },
        'channel_fan': {
            'channelId': 1, 'fanId': 1, 'date': 1
        },
        'statistic': {
            'statisticId': 1, 'type': 1, 'recordDate': 1, 'opinion': 1, 'feedback': 1, 'abusive': 1,
            'request': 1, 'supportive': 1, 'didactic': 1, 'question': 1, 'criticism': 1, 'admiration': 1,
            'advice': 1, 'trash': 1
        },
        "request_log": {
            'path': 1, 'full_path': 1, 'script_root': 1, 'base_url': 1, 'url': 1, 'url_root': 1, 'accept_charsets': 1,
            'accept_encodings': 1, 'accept_languages': 1, 'accept_mimetypes': 1, 'access_route': 1, 'args': 1,
            'authorization': 1, 'blueprint': 1, 'cache_control': 1, 'content_encoding': 1, 'content_length': 1,
            'content_md5': 1, 'content_type': 1, 'cookies': 1, 'data': 1, 'date': 1, 'endpoint': 1, 'files': 1,
            'form': 1, 'headers': 1, 'host': 1, 'host_url': 1, 'if_match': 1, 'if_modified_since': 1,
            'if_none_match': 1, 'if_range': 1, 'if_unmodified_since': 1, 'is_json': 1, 'is_multiprocess': 1,
            'is_multithread': 1, 'is_run_once': 1, 'is_secure': 1, 'is_xhr': 1, 'max_content_length': 1,
            'max_forwards': 1, 'method': 1, 'mimetype': 1, 'mimetype_params': 1, 'pragma': 1, 'query_string': 1,
            'range': 1, 'referrer': 1, 'remote_user': 1, 'routing_exception': 1, 'scheme': 1, 'stream': 1,
            'charset_of_url': 1, 'url_rule': 1
        },
        "response_log": {
            'headers': 1, 'status': 1, 'status_code': 1, 'data': 1, 'json': 1, 'is_json': 1, 'max_cookie_size': 1,
            'mimetype': 1
        }
    }
    return fields.get(collection_name, None)


def error_check_for_fields(document, collection_name):
    fields = get_fields_of_collection(collection_name)  # general fields for comment
    if isinstance(document, dict):
        diff_fields = get_missing_fields(fields, document)  # missing fields in given documents
        # check keys for some cases explained into above method
        result = check_document_fields(document, fields, diff_fields)
        if result:
            return document
    elif isinstance(document, list):
        for doc in document:
            diff_fields = get_missing_fields(fields, doc)
            result = check_document_fields(doc, fields, diff_fields)
            if not result:
                return False
        return document


def check_document_fields(document, fields, diff_fields):
    # case for unexpected field(s)
    if any([key not in fields for key in document.keys()]):
        return False
    # case for missing necessary field(s)
    for key in diff_fields:
        if fields[key] == 1:
            return False
    return True


# compare keys of fields of document and given document
# return missing fields
def get_missing_fields(fields, document):
    result = list()
    document_keys = document.keys()
    for key, value in fields.items():
        if key not in document_keys:
            result.append(key)
    return result


def check_collection_existence(collection_name):
    try:
        result = get_fields_of_collection(collection_name)
        if result:
            return True
    except KeyError:
        return False
