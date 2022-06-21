
from UM40_SMART_JSON_API_Framework import SSH

JSON = {"job": "ElMomentEnergy", "meters": [{"iface": "Iface1", "deviceidx": 1, "type": 36, "address": "88", "password": "2222222222222222", "password2": "2222222222222222"}]}

JSON = {'table': 'Reboot', 'method': 'get'}
IP_address = "192.168.202.197"
IP_port = "22"
user_login = "root"
user_password = "7CLcCt95"

JSON_list = [
{"method":"post","table":"TimeCorrectionsJournal","record":{"before":41,"diff":5}},
{"method":"post","table":"TimeCorrectionsJournal","record":{"before":41123,"diff":235}},
{"method":"post","table":"TimeSetJournal","record":{"before":41,"after":42}},
{"method":"post","table":"TimeSetJournal","record":{"before":41231,"after":42}},
{"method":"post","table":"MeterStateJournal","record":{"idx":41,"time":4242,"state":True}},
{"method":"post","table":"MeterStateJournal","record":{"idx":42,"time":42123242,"state":False}},
{"method":"post","table":"ActionJournal","record":{"time":123456789,"event":{"id":42,"type":"Scheduler"},"action":{"id":7,"type":"Poller"}}},
{"method":"post","table":"ActionJournal","record":{"time":123426789,"event":{"id":1,"type":"Scheduler"},"action":{"id":7,"type":"Poller"}}}
]


JSON_list = [
# {'table': 'ActionJournal', 'method': 'get'},
# {"method":"get","table":"ActionJournal"}
]
# for JSON in JSON_list :
#     answer = SSH(IP_address=IP_address,
#                  IP_port=IP_port,
#                  user_login=user_login,
#                  user_password=user_password).Journals_database(JSON=JSON)
#
#     print(answer)

JSON = {"job": "ElMomentEnergy", "meters": [{"iface": "Ethernet", "deviceidx": 4, "type": 94, "address": "192.168.202.241:5555"}, {"iface": "Iface1", "deviceidx": 1, "type": 5, "address": "141227285", "password": "373737373737", "password2": "373737373737"}]}


answer = SSH(IP_address=IP_address,
                 IP_port=IP_port,
                 user_login=user_login,
                 user_password=user_password).Meter_dev(JSON=JSON)

print(answer)