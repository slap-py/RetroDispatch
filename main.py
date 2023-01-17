import curses 

screen = curses.initscr() 
#curses.noecho() 
curses.curs_set(0) 
screen.keypad(1) 
curses.mousemask(1)
dispatch_text = r''' ____ ___ ____  ____   _  _____ ____ _   _ 
|  _ \_ _/ ___||  _ \ / \|_   _/ ___| | | |
| | | | |\___ \| |_) / _ \ | || |   | |_| |
| |_| | | ___) |  __/ ___ \| || |___|  _  |
|____/___|____/|_| /_/   \_\_| \____|_| |_|'''

clear_text = r'''  ____ _     _____    _    ____  
 / ___| |   | ____|  / \  |  _ \ 
| |   | |   |  _|   / _ \ | |_) |
| |___| |___| |___ / ___ \|  _ < 
 \____|_____|_____/_/   \_\_| \_'''
units_list = {
    'E191':{'name':'Engine 191','type':'ENG','dept':'Mercer Island Fire Department','station':'91','available':True},
    'A191':{'name':'Aid 191','type':'BLSAMBO','dept':'MIFD','station':'91','available':True},
    'B191':{'name': 'Battalion 191','type':'BC','dept':'MIFD','station':'91','available':True},
    'MIDI191':{'name':'Midi 191','type':'ENGT3','dept':'MIFD','station':'91','available':True},
    'E192':{'name':'Engine 192','type':'ENG','dept':'MIFD','station':'92','available':True},
    'A192':{'name':'Aid 192','type':'BLSAMBO','dept':'MIFD','station':'92','available':True},
    'MIDI192':{'name':'Midi 192','type':'ENGT3','dept':'MIFD','station':'92','available':True},

    'E101':{'name':'Engine 101','type':'ENG','dept':'BVFD','station':'1','available':True},
    'A101':{'name':'Aid 101','type':'BLSAMBO','dept':'BVFD','station':'1','available':True},
    'B101':{'name':'Battalion 101','type':'BC','dept':'BVFD','station':'1','available':True},
    'E102':{'name':'Engine 102','type':'ENG','dept':'BVFD','station':'2','available':True},
    'A102':{'name':'Aid 102','type':'BLSAMBO','dept':'BVFD','station':'2','available':True},
    'M102':{'name':'Medic 102','type':'ALSAMBO','dept':'BVFD','station':'2','available':True},
    'MSO105':{'name':'Medic Staff Officer 105','type':'MSO','dept':'BVFD','station':'2','available':True},
    'E103':{'name':'Engine 103','type':'ENG','dept':'BVFD','station':'3','available':True},
    'L103':{'name':'Ladder 103','type':'LADNP','dept':'BVFD','station':'3','available':True},
    'A103':{'name':'Aid 103','type':'BLSAMBO','dept':'BVFD','station':'3','available':True},
    'E104':{'name':'Engine 104','type':'ENG','dept':'BVFD','station':'4','available':True},
    'E105':{'name':'Engine 105','type':'ENG','dept':'BVFD','station':'5','available':True},
    'E106':{'name':'Engine 106','type':'ENG','dept':'BVFD','station':'6','available':True},
    'A106':{'name':'Aid 106','type':'BLSAMBO','dept':'BVFD','station':'6','available':True},
    'E107':{'name':'Engine 107','type':'ENG','dept':'BVFD','station':'7','available':True},
    'L107':{'name':'Ladder 107','type':'LADNP','dept':'BVFD','station':'7','available':True},
    'AIR101':{'name':'Light & Air 101','type':'AIR','dept':'BVFD','station':'8','available':True},
    'E108':{'name':'Engine 108','type':'ENG','dept':'BVFD','station':'8','available':True},
    'E109':{'name':'Engine 109','type':'ENG','dept':'BVFD','station':'9','available':True},
}


screen.addstr(1,1,'Assignment:',curses.A_UNDERLINE)
screen.addstr(1,13,'No current assignment.')

screen.addstr(2,1,'Command:',curses.A_UNDERLINE)
screen.addstr(2,10,'No active command.')

screen.addstr(3,1,'Command Requests:',curses.A_UNDERLINE)
screen.addstr(3,19,'No active command.')

screen.addstr(1,int(curses.COLS/2.5),'On-scene units:',curses.A_UNDERLINE)

screen.addstr(1,int(curses.COLS/1.25),'Available units:',curses.A_UNDERLINE)


units_list_a = []
units_list_o = []
for x in range(len(list(units_list))):
    unit = units_list[list(units_list.keys())[x]]
    if unit['available'] == True:
        units_list_a.append(unit)
    else:
        units_list_o.append(unit)

#available units list
for x in range(len(units_list_a)):
    screen.addstr(x+2,int(curses.COLS/1.25),str(units_list_a[x]['name']))

#on scene units list
for x in range(len(units_list_o)):
    screen.addstr(x+2,int(curses.COLS/2.5),str(units_list_o[x]['name']))

#'dispatch'
for x in range(len(dispatch_text.split('\n'))):
    linetext = dispatch_text.split('\n')[x]
    screen.addstr(x+10,2,linetext)
#'clear'
for x in range(len(clear_text.split('\n'))):
    linetext = clear_text.split('\n')[x]
    screen.addstr(x+15,2,linetext)
lastButton = None

def redraw_units_lists():
    #available units list
    for x in range(50):
        try:
            screen.addstr(x+2,int(curses.COLS/1.25),'                      ')
            screen.addstr(x+2,int(curses.COLS/2.5),'                      ')
        except curses.error:
            pass
    for x in range(len(units_list_a)):
        screen.addstr(x+2,int(curses.COLS/1.25),str(units_list_a[x]['name']))

    #on scene units list
    for x in range(len(units_list_o)):
        screen.addstr(x+2,int(curses.COLS/2.5),str(units_list_o[x]['name']))

while True:
    event = screen.getch() 
    if event == ord("q"): break 
    if event == curses.KEY_MOUSE:
        _, mx, my, _, _ = curses.getmouse()
        y, x = screen.getyx()
        #screen.addstr(y, x, str(mx)+' '+str(my)+'   ')
        if mx >=2 and mx <=44 and my >=10 and my <=14:
            screen.addstr(22,2,'                            ')
            screen.addstr(22,2,'Dispatch registered')
            lastButton = 'dispatch'
        elif mx >=2 and mx<=33 and my>=15 and my<=19:
            screen.addstr(22,2,'                            ')
            screen.addstr(22,2,'Clear registered')
            lastButton = 'clear'
        elif mx>=96 and mx<=110 and my>=2:
            screen.addstr(22,2,'                            ')
            if lastButton == 'dispatch':
                screen.addstr(22,2,'Dispatch '+str(units_list_a[my-2]['name'])+' registered.')
                #a_list_cache = units_list[list(units_list.keys())[my-2]]
                a_list_cache = units_list_a[my-2]
                idx = units_list_a.index(a_list_cache)
                del units_list_a[idx]
                units_list_o.append(a_list_cache)
                redraw_units_lists()
                #units_list.keys()[my-2]
            elif lastButton == 'clear':
                screen.addstr(22,2,'Clear '+list(units_list.keys())[my-2]+' registered.')
            else:
                screen.addstr(22,2,units_list_a[my-2]['name']+' no command.')

            lastButton = list(units_list.keys())[my-2]

curses.endwin()
