# -*- coding: utf-8 -*-
# change width in /usr/share/cinnamon-screensaver/clock.py 
from gi.repository import Gio
mongo = True
if mongo:
    from pymongo import MongoClient

    # initialize the record server
    mongo_url = 'mongodb://localhost:27015'
    client = MongoClient(mongo_url)
    db_name = 'poetry'
    collection_for_record = 'chinese'
    records = client[db_name][collection_for_record]

    def update_msg():
        try:
            content = records.aggregate([{'$sample': {'size':1}}])
            for i in content:
                text = ''
                text += f'{i["title"]}\n{i["author"]}'
                for j in i['paragraphs']:
                    text += f'\n{j}'
        except Exception:
            text = 'error in mongodb'

        schema = "org.cinnamon.desktop.screensaver"
        Gio.Settings(schema).set_string('default-message', text)
    
else:
    import random
    import json
    import io
    with io.open('lunyu.json', encoding="utf-8") as f:
        lunyu = json.load(f)
    rand_idx = random.randint(0, len(lunyu)-1)
    text = lunyu[rand_idx]["paragraphs"]
    schema = "org.cinnamon.desktop.screensaver"
    Gio.Settings(schema).set_string('default-message', text)

