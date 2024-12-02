# "author": "ted.cygan"

# AV4KENIL-0017205 Apogem NYC Boardroom
#STATUS:
# gui approved  
# programmed    
# lab tested    
# site tested   


data = {
    'biamp': '10.239.1.232',   


    'switcher': '10.239.1.62',            #ATLONA AT-OME-MS42
    'switcher_inscount': 4,
    'switcher_outscount': 2,

   
    'in0name': 'Blank',  
    'in1name': 'Table Laptop-1',  #usbc for laptop conf
    'in2name': 'blank2',  
    'in3name': 'Table Laptop-1',  #soft codec laptop
    'in4name': 'Table Laptop-2',  


    'out1name': 'Codec Content',  
    'out2name': 'blank',  




    'display1': 'COM1',
    'display1name': 'Display',           #SAMSUNG QN85Q60CAF  //ofe, need to verify make and model



    'poly':'COM3',  
    'polyname':'VTC',


    'onebeyond':'172.22.0.55',      #CRESTRON IV-SAM-VX2-S

    'cam1': '10.239.1.131',               
    'cam1name': 'Camera-1',  
    'cam2': '10.239.1.132',               
    'cam2name': 'Camera-2', 
    'cam3': '10.239.1.133',               
    'cam3name': 'Camera-3', 
    'cam4': '10.239.1.134',               
    'cam4name': 'Camera-4', 
   

    'lights':'COM2',  

    "lights_id": "11", 
    "lights_name1": "Meeting Hi",
    "lights_name2": "Meeting Lo",
    "lights_name3": "AV Present",
    "lights_name4": "Video Conf.",
    "lights_name5": "Off",
    "lights_name6": "not used",
    "lights_name7": "not used",
    "lights_name8": "not used",
    "lights_name9": "not used",
    "lights_name10": "not used",

    "shades_id1":"191",   
    "shades_name1": "Open", 
    "shades_name2": "Close",
    "shades_name3": "Open",
    "shades_name4": "Close",
    "shades_name5": "Open",   
    "shades_name6": "Close",
    "shades_name7": "not used",
    "shades_name8": "not used",
    "shades_name9": "not used",
    "shades_name10": "not used",

    
    'warmup':8,
    'cooldown':8,


    'roomname':'Apogem NYC Boardroom', 
    'password':'1234',
    'enable_nightlyshutdown':False,
    'nightlyshutdown':'19:00:00',
    'enable_incomingcalls':False,
    'touchpanel_count':1,


    'labtest':False
}


todo = [
    '<< TODO >>',
    'ips',
    'dsp tags'
]

