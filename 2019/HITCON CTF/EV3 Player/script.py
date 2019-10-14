import json

f = ''
of = 0
jq=json.loads(open("btout.json","r").read())
for i in jq:
    if i["_source"]["layers"]["bthci_acl"]["bthci_acl.dst.name"] != "EV3":
        continue
    try: 
        data = i["_source"]["layers"]["data"]["data.data"].replace(':','')
        datalen = i["_source"]["layers"]["data"]["data.len"]
        if bytes.fromhex(data).find(b'fl.rsf') != -1:
            f = open("fl.rsf","wb")
            of = 1
            continue
        if bytes.fromhex(data).find(b'ag.rsf') != -1:
            f = open("ag.rsf","wb")
            of = 1
            continue
        if of == 1:
            f.write(bytes.fromhex(data[14:]))
            if datalen != "907": 
                of = 0
    except:
        pass
        