default_byte_block = [
    ['AVON\x1c\x00\x00\x00QR\x18\x00\x04\x02\x00\x00\xd6\x01\x00\x00\x00\x00\xe8\x01', '\xd6', '\xe8'],
    ['AVON\r\x00\x00\x00QR\x18\x00\x04\x02\x00\x00\x81\x02\x00\x00\x00\x00\x85\x01', '\x81', '\x85'],
    ['AVON+\x00\x00\x00QR\x18\x00\x04\x02\x00\x00,\x03\x00\x00\x00\x00O\x02', '\x00,', '\x00O'],
    ['AVON\x12\x00\x00\x00QR\x18\x00\x04\x02\x00\x00\xd7\x03\x00\x00\x00\x00\xe1\x01', '\xd7', '\xe1'],
    ['AVON\x17\x00\x00\x00QR\x18\x00\x04\x02\x00\x00\x82\x04\x00\x00\x00\x00\x92\x01', '\x82', '\x92'],
    ['AVON\x1d\x00\x00\x00QR\x18\x00\x04\x02\x00\x00-\x05\x00\x00\x00\x00D\x02', '\x00-', '\x00D'],
    ['AVON\x0f\x00\x00\x00QR\x18\x00\x04\x02\x00\x00\xd8\x05\x00\x00\x00\x00\xe1\x01', '\xd8', '\xe1'],
    ['AVON\x19\x00\x00\x00QR\x18\x00\x04\x02\x00\x00\x83\x06\x00\x00\x00\x00\x97\x01', '\x83', '\x97'],
    ['AVON#\x00\x00\x00QR\x18\x00\x04\x02\x00\x00.\x07\x00\x00\x00\x00M\x02', '\x00.', '\00M'],
    ['AVON.\x00\x00\x00QR\x18\x00\x04\x02\x00\x00\xd9\x07\x00\x00\x00\x00\x03\x02', '\xd9', '\x03']]

auto_bright_array = [['true', '10 0 0', '96'],
                     ['true', '10 0 0', '96'],
                     ['true', '10 0 0', '96'],
                     ['true', '10 0 0', '96']]

list_plat = ["user admin\n", "pass 80005273@novaStar\n", "OPTS utf8 on\n", "PWD\n", "TYPE I\n", "CWD /\n"]
             # "PASV\n",
             # "STOR sdcard/nova/viplex_terminal/program/program_SINAPS-NOUT-32/1/planlist.json\n",
             # "STOR sdcard/nova/viplex_terminal/program/program_SINAPS-NOUT-32/1/playlist0.json\n",
             # "STOR sdcard/nova/viplex_terminal/program/program_SINAPS-NOUT-32/1/",
             # "STOR sdcard/nova/viplex_terminal/media/"]

project_path = 'C:/TOI_prod/tcpimage/'
path_to_table_bright_xlsx = 'C://Users/Гамбоев/Desktop/TOI_prod/TOI_/tcpimage/timetable/tcp_test_z/timing.xlsx'
list_json = ['planlist.json', 'playlist0.json']
colors = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
path = 'C:/TOI/tcpimage'
hostIP = "172.22.1.55"
login_image = '41564f4e0100000051520000000000004e000000000026027b22736e223a2232303230303830353830303035323733222c227' \
              '57365726e616d65223a2261646d696e222c2270617373776f7264223a22313233343536222c226c6f67696e54797065223a337d'
mode = '41564f4e3000000051521800050200001e000000000044027b226973537570706f7274436f6d706c65746543726f6e223a747275657d' \
       '41564f4e2f00000051521800050100000000000000002402'
bright_auto_mode = '41564f4e6500000051521800050100000000000000005a0241564f4e6600000051521800050200001e0000' \
                   '0000007a027b226973537570706f7274436f6d706c65746543726f6e223a747275657d'
# login = '41564f4e0100000051520000000000005200000000002a027b22736e223a22425a524136394230365730303330303032323437222c' \
#         '22757365726e616d65223a2261646d696e222c2270617373776f7264223a22313233343536222c226c6f67696e54797065223a307d'
login = '41564f4e0100000051520000000000004e000000000026027b22736e223a2232303230303830353830303035323733222c2275736572' \
        '6e616d65223a2261646d696e222c2270617373776f7264223a22313233343536222c226c6f67696e54797065223a337d'
change_to_auto = '41564f4e5500000051521800040300004b000000000096027b22736f75726365223a7b2274797065223a312c22706c6174' \
                 '666f726d223a327d2c2274797065223a2253435245454e5f4252494748544e455353222c226d6f6465223a224155544f227d'

change_to_manual = '41564f4e2a01000051521800040300004f000000000070027b22736f75726365223a7b2274797065223a312c22706c61' \
                   '74666f726d223a327d2c2274797065223a2253435245454e5f4252494748544e455353222c226d6f6465223a224d414e' \
                   '55414c4c59227d'

check_manual_bright = '41564f4e3000000050521800000005004f000000000072027b226d6f6465223a224d414e55414c4c59222c22736f7' \
                      '5726365223a7b22706c6174666f726d223a312c2274797065223a317d2c2274797065223a2253435245454e5f4252' \
                      '494748544e455353227d'

check_manual_bright1 = '41564f4e310000005152180005010000000000000000260241564f4e3200000051521800050200001e0000000000' \
                       '46027b226973537570706f7274436f6d706c65746543726f6e223a747275657d'

update1 = '41564f4e1500000051521e000b02000031000000000048027b226964656e746966696572223a22666637383865386338616662343' \
          '1663766613031396230653263623462303463227d'

update2 = '41564f4e1600000051521e000902000031000000000047027b226964656e746966696572223a22666637383865386338616662343' \
          '1663766613031396230653263623462303463227d'

temperature_bright = '41564f4e520000005152990000000000ad00000000006f017b22736f75726365223a7b2274797065223a312c22706c' \
                     '6174666f726d223a327d2c227461736b4172726179223a5b7b2274797065223a22535550504f52545f53454e534f52' \
                     '5f494e464f222c22616374696f6e223a352c22737461747573223a302c226572726f72436f6465223a302c22646174' \
                     '61223a7b2269735570677261646553656e736f7250726f6772616d223a747275652c2273656e736f72496e666f7322' \
                     '3a6e756c6c7d7d5d7d'

init = '41564f4e1900000051521e0009030000a90000000000c3017b226465766963654964656e746966696572223a2253494e4150532d4e4f55542d3234222c22746f74616c53697a65223a313032342c2274797065223a2244454641554c54222c226c6f63616c223a66616c73652c22736f75726365223a302c22736f6c7574696f6e73223a7b226e616d65223a2231222c226964656e746966696572223a223332313163653735633662343031366137623538636433343735663365316638227d7d'
run_hard = '41564f4e1a00000051521e000d030000bc0100000000dc017b22636f6e6669726d6564496e666f73223a7b226964656e746966696572223a223332313163653735633662343031366137623538636433343735663365316638222c226e616d65223a2231222c22706c616e4c69737455726c223a227364636172642f6e6f76612f7669706c65785f7465726d696e616c2f70726f6772616d2f70726f6772616d5f53494e4150532d4e4f55542d32342f312f706c616e6c6973742e6a736f6e222c227468756d626e61696c55726c223a227364636172642f6e6f76612f7669706c65785f7465726d696e616c2f70726f6772616d2f70726f6772616d5f53494e4150532d4e4f55542d32342f312f38343233376363322d353266622d343732352d623834332d3731626661313437666134622e706e67227d2c22736f75726365223a7b2274797065223a312c22706c6174666f726d223a327d2c2273706f747354797065223a6e756c6c2c226e6f726d616c50726f6772616d537461747573223a6e756c6c2c2264656c617954696d65223a302c22706c617954696d65223a302c22706c6179496d6d6564696174656c79223a747275652c226973537570706f72744d6435436865636b6f7574223a747275657d'