# "author": "ted.cygan"

data = [
    {
        "name":'Room Volume',
        "nameID": 9999,
        "upID": 601,
        "downID": 602,
        "levelID": 604,
        "minRange": -45,
        "maxRange": 0,
        "instanceTag": 'RM1_PRG',
        "channel":"1",
        'subscription':'LevelControl'
    },
    {
        "name":'Program Mute',
        "nameID": 9999,
        "muteID": 603,
        "instanceTag": "RM1_PRG",
        "channel":"1",
        'subscription':'MuteControl'
    },
    {
        "name":'atc Call Volume',
        "nameID": 9999,
        "upID": 611,
        "downID": 612,
        "levelID": 614,
        "minRange": -20,
        "maxRange": 0,
        "instanceTag": "RM1_ATC_RX",
        "channel":"1",
        'subscription':'LevelControl'
    },
    {
        "name":'atc Call Mute',
        "nameID": 9999,
        "muteID": 613,
        "instanceTag": "RM1_ATC_RX",
        "channel":"1",
        'subscription':'MuteControl'
    },
    # {
    #     "name":'All Mics',
    #     "nameID": 620,
    #     "upID": 616,
    #     "downID": 617,
    #     "levelID": 619,
    #     "minRange": -40,
    #     "maxRange": 12,
    #     "instanceTag": "MICS_ALL",
    #     "channel":"1",
    #     'subscription':'LevelControl'
    # },
    {
        "name":'RM1_VOICELIFT',
        "nameID": 9999,
        "onID": 617,
        "offID": 616,
        "instanceTag": "RM1_VOICELIFT",
        "channel":"1",
        'subscription':'MuteControlDiscrete'
    },
    {
        "name":'mic mute',
        "nameID": 9999,
        "muteID": 618,
        "instanceTag": "RM1_MIC_MUTE",
        "channel":"1",
        'subscription':'MuteControl'
    },
    # {
    #     "name":'RM1_VTC_CONTENT_AUDIO',
    #     "nameID": 9999,
    #     "onID": 619,
    #     "offID": 620,
    #     "instanceTag": "RM1_VTC_CONTENT_AUDIO",
    #     "channel":"1",
    #     'subscription':'LogicState'
    # },
    # {
    #     "name":'vtc Call Volume',
    #     "nameID": 9999,
    #     "upID": 621,
    #     "downID": 622,
    #     "levelID": 624,
    #     "minRange": -20,
    #     "maxRange": 0,
    #     "instanceTag": "RM1_VTC_RX",
    #     "channel":"1",
    #     'subscription':'LevelControl'
    # },
    {
        "name":'vtc Call Mute',
        "nameID": 9999,
        "muteID": 623,
        "instanceTag": "RM1_VTC_RX",
        "channel":"1",
        'subscription':'MuteControl'
    },
    # {
    #     "name":'vtc far end',
    #     "nameID": 9999,
    #     "muteID": 628,
    #     "instanceTag": "RM1_VTC_FAR_END",
    #     "channel":"1",
    #     'subscription':'MuteControl'
    # },
    # {
    #     "name":'Table Mics',
    #     "nameID": 705,
    #     "upID": 701,
    #     "downID": 702,
    #     "levelID": 704,
    #     "minRange": -6,
    #     "maxRange": 6,
    #     "instanceTag": "RM1_TABLE_MICS",
    #     "channel":"1",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 703,
    #     "instanceTag": "RM1_TABLE_MICS",
    #     "channel":"1",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Speaker 1',
    #     "nameID": 710,
    #     "upID": 706,
    #     "downID": 707,
    #     "levelID": 709,
    #     "minRange": -45,
    #     "maxRange": 6,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"1",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 708,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"1",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Speaker 2',
    #     "nameID": 715,
    #     "upID": 711,
    #     "downID": 712,
    #     "levelID": 714,
    #     "minRange": -45,
    #     "maxRange": 6,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"2",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 713,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"2",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Speaker 3',
    #     "nameID": 720,
    #     "upID": 716,
    #     "downID": 717,
    #     "levelID": 719,
    #     "minRange": -45,
    #     "maxRange": 6,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"3",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 718,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"3",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Speaker 4',
    #     "nameID": 725,
    #     "upID": 721,
    #     "downID": 722,
    #     "levelID": 724,
    #     "minRange": -45,
    #     "maxRange": 6,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"4",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 723,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"4",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Speaker 5',
    #     "nameID": 730,
    #     "upID": 726,
    #     "downID": 727,
    #     "levelID": 729,
    #     "minRange": -45,
    #     "maxRange": 6,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"5",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 728,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"5",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Speaker 6',
    #     "nameID": 735,
    #     "upID": 731,
    #     "downID": 732,
    #     "levelID": 734,
    #     "minRange": -45,
    #     "maxRange": 6,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"6",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 733,
    #     "instanceTag": "RM1_SPK",
    #     "channel":"6",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Call Volume',
    #     "nameID": 740,
    #     "upID": 736,
    #     "downID": 737,
    #     "levelID": 739,
    #     "minRange": -40,
    #     "maxRange": 12,
    #     "instanceTag": "RM2_CALL_VOL",
    #     "channel":"1",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 738,
    #     "instanceTag": "RM2_CALL_VOL",
    #     "channel":"1",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Call Volume',
    #     "nameID": 745,
    #     "upID": 741,
    #     "downID": 742,
    #     "levelID": 744,
    #     "minRange": -40,
    #     "maxRange": 12,
    #     "instanceTag": "RM3_CALL_VOL",
    #     "channel":"1",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 743,
    #     "instanceTag": "RM3_CALL_VOL",
    #     "channel":"1",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Call Volume',
    #     "nameID": 750,
    #     "upID": 746,
    #     "downID": 747,
    #     "levelID": 749,
    #     "minRange": -40,
    #     "maxRange": 12,
    #     "instanceTag": "RM4_CALL_VOL",
    #     "channel":"1",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 748,
    #     "instanceTag": "RM4_CALL_VOL",
    #     "channel":"1",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Call Volume',
    #     "nameID": 755,
    #     "upID": 751,
    #     "downID": 752,
    #     "levelID": 754,
    #     "minRange": -40,
    #     "maxRange": 12,
    #     "instanceTag": "RM5_CALL_VOL",
    #     "channel":"1",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 753,
    #     "instanceTag": "RM5_CALL_VOL",
    #     "channel":"1",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Call Volume',
    #     "nameID": 760,
    #     "upID": 756,
    #     "downID": 757,
    #     "levelID": 759,
    #     "minRange": -40,
    #     "maxRange": 12,
    #     "instanceTag": "RM6_CALL_VOL",
    #     "channel":"1",
    #     'subscription':'LevelControl'
    # },
    # {
    #     "nameID": 9999,
    #     "muteID": 758,
    #     "instanceTag": "RM6_CALL_VOL",
    #     "channel":"1",
    #     'subscription':'MuteControl'
    # },
    #    {
    #     "name":'Mic-13',
    #     "nameID": 765,
    #     "upID": 761,
    #     "downID": 762,
    #     "levelID": 764,
    #     "minRange": -40,
    #     "maxRange": 12,
    #     "instanceTag": "MICS",
    #     "channel":"13",
    #     'subscription':'LevelControl'
    # },
    {
        "name":'phone',
        "nameID": 650,
        "num1ID": 651,
        "num2ID": 652,
        "num3ID": 653,
        "num4ID": 654,
        "num5ID": 655,
        "num6ID": 656,
        "num7ID": 657,
        "num8ID": 658,
        "num9ID": 659,
        "num0ID": 660,
        "numStarID": 661,
        "numHashID": 662,
        "numBackID": 663,
        "numClearID": 664,
        "numDialID": 665,
        "numHangupID": 666,
        "numAnswerCallID": 667,
        "numRejectCallID": 668,
        "labelDialStringID": 670,
        "labelCallerID": 671,
        "labelStatusID": 672,
        "instanceTag": "RM1_ATC_DIALER",
        "statusInstanceTag": "RM1_ATC_DIALER_STATUS",
        # "subscription":'TICallStatus',
        # "subscription2":'TICallerID',
        # "subscription3":'TILineInUse',
        "line":"1",
        "subscription":'VoIPCallStatus',
        "subscription2":'VoIPCallerID',
        "subscription3":'VoIPLineInUse'
    }
    # {
    #     "name":'ON',
    #     "nameID": 9999,
    #     "presetID": 551,
    #     "instanceTag": "VOICELIFT_ON",
    #     'subscription':'presettbd'
    # },
    # {
    #     "name":'OFF',
    #     "nameID": 9999,
    #     "presetID": 552,
    #     "instanceTag": "VOICELIFT_OFF",
    #     'subscription':'presettbd'
    # }
]
