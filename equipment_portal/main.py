from fastapi import FastAPI
from pymongo import MongoClient
import os
import logging
import asyncio

from db.models import Equipment,Room


MONGO_DATABASE_URI = os.environ.get('MONGO_DATABASE_URI')

#Для подключения к внешней БД:
client = MongoClient(MONGO_DATABASE_URI)

#Доступ к БД через pymongo
db = client['Equipment']

# функция логгера
def create_logger(mode='INFO'):
    logs = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG}

    logger = logging.getLogger('equipment_portal')
    logger.setLevel(logs[mode])

    handler = logging.StreamHandler()
    handler.setLevel(logs[mode])

    formatter = logging.Formatter(
        '%(levelname)-8s  %(asctime)s    %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

    handler.setFormatter(formatter)

    logger.addHandler(handler)


create_logger()  # Создание логгера
logger = logging.getLogger('equipment_portal')  # инициализация логгера

app = FastAPI()

@app.get('/equipment')
async def list_equipments():
    equipmentss = []
    for equipment in db.equipment.find():
        equipmentss.append(Equipment(**equipment))
    logger.info(f"Equipment in the database: {equipmentss}")
    return {'equipment': equipmentss}

@app.get('/room')
async def list_rooms():
    rooms_list = [] 
    for room in db.rooms.find():
        rooms_list.append(room)
    logger.info(f"All rooms in the database: {rooms_list}")
    return (rooms_list)

@app.get('/room/{room_id}')
async def list_room_equipments(room_id: int):
    equipments_list = []
    for equipment in db.equipment.find({ 'room_id': room_id }):
        equipments_list.append(equipment)
    logger.info(f"Equipment in the room {room_id}: {equipments_list}")
    return (equipments_list)

@app.post('/equipment')
async def create_equipment(equipment: Equipment):
    try:
        db.equipment.insert_one(equipment.dict(by_alias=True))
        logger.info(f"Equipment with id: {equipment.id}  -  added to the database")
    except:
        logger.warning(f"Equipment with id: {equipment.id}  -  already exists in the database")
    return {'equipment': equipment}

"""
Проверка функции create_equipment:
    newequipment = Equipment(_id = 150, ip = "172.18.191.21", name = "Презентация", room_id = 1, audio = "main", merge = 'backup2-left', port = 80, rtsp = "rtsp://172.18.191.21/0", tracking = "backup", time_editing = "2020-10-27 10:05:07.820582", external_id = "16682899584")
    asyncio.gather(create_equipment(newequipment))
"""

@app.post('/room')
async def create_room(room: Room):
    try:
        db.rooms.insert_one(room.dict(by_alias=True))
        logger.info(f"Room with id: {room.id}  -  added to the database")
    except:
        logger.warning(f"Room with id: {room.id}  -  already exists in the database")
    return {'room': room}

"""
Проверка функции create_room:
    newroom = Room(_id = 1, name = 504, drive = "https://drive.google.com/drive/u/5/folders/1k-ZqejYgxd3t6BfIprGKCU4wV9LolT9e", calendar = "c_f1hdjmh3q22jnccfrrola0fun0@group.calendar.google.com", tracking_state = 'f', main_source = '172.18.191.24', screen_source = "172.18.191.21", sound_source = "172.18.191.21", tracking_source = "172.18.191.23", auto_control = "f", stream_url = '', ruz_id = 3360)
    asyncio.gather(create_room(newroom))
"""

@app.delete('/room/{room_id}')
async def delete_room(room_id:int):
    db.rooms.remove( {'_id': room_id})
    logger.info(f"Room with id: {room_id}  -  deleted from the database")

"""
Проверка функции delete_room:
    asyncio.gather(delete_room(1))
"""

@app.delete('/equipment/{equipment_id}')
async def delete_equipment(equipment_id:int):
    db.equipment.remove( {'_id': equipment_id})
    logger.info(f"Equipment with id: {equipment_id}  -  deleted from the database")

"""
Проверка функции delete_equipment:
    asyncio.gather(delete_equipment(150))
"""

@app.put('/room/{room_id}')
async def update_room(room_id:int,new_values_dict:dict):
    db.rooms.update_one( {'_id': room_id},{'$set': new_values_dict  } )
    logger.info(f"Room with id: {room_id}  -  updated")#Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту

"""
Проверка функции update_room:
    new_name = { "name": 696 }
    asyncio.gather(update_room(1,new_name))
"""

@app.put('/equipment/{equipment_id}')
async def update_equipment(equipment_id:int,new_values_dict:dict):
    db.equipment.update_one( {'_id': equipment_id},{'$set': new_values_dict  } )
    logger.info(f"Equipment with id: {equipment_id}  -  updated")#Если ключа нет в обьекте, то будет добавлена новая пара ключ-значение к этому обьекту

"""
Проверка функции update_equipment:
    new_name = { "name": 696 }
    asyncio.gather(update_equipment(150,new_name))
"""
