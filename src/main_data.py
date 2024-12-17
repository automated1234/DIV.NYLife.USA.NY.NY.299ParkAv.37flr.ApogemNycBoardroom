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
    'in1name': 'Table Laptop',  #usb-c for laptop conf
    'in2name': 'blank2',  
    'in3name': 'Table Laptop',  #table laptop1
    'in4name': 'Table Laptop',  #table laptop2


    'out1name': 'Codec Content',  
    'out2name': 'blank',  




    'display1': 'COM1',
    'display1name': 'Display',           #Planar UR9851  OFE



    'poly':'COM3',  
    'polyname':'VTC',


    'onebeyond':'10.239.1.54',      #CRESTRON IV-SAM-VX2-S

    'cam1': '10.239.1.131',               
    'cam1name': 'Camera-1',  
    'cam2': '10.239.1.132',               
    'cam2name': 'Camera-2', 
    'cam3': '10.239.1.133',               
    'cam3name': 'Camera-3', 
    'cam4': '10.239.1.134',               
    'cam4name': 'Camera-4', 
   

      
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

