import curses
import json
import random
import time

screen = curses.initscr() 
#curses.noecho() 
curses.curs_set(0) 
screen.keypad(1) 
curses.mousemask(1)
screen.nodelay(True)
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

sort_text = r''' ____   ___  ____ _____ 
/ ___| / _ \|  _ \_   _|
\___ \| | | | |_) || |  
 ___) | |_| |  _ < | |  
|____/ \___/|_| \_\|_|  '''
code_to_pt = {'ENG':'Engine','BLSAMBO':'Aid','BC':'Battalion','ENGT3':'Brush','ALSAMBO':'Medic','LADNP':'Ladder N/P','AIR':'Air'}
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
    'MSO105':{'name':'Medic Sup. 105','type':'MSO','dept':'BVFD','station':'2','available':True},
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
'''when terminating a call:
return all units available
make call=None, minimums=None, bcchance=None, commandDone=None'''
def generate_requirement(text):
    screen.addstr(3,19,'                             ')
    screen.addstr(3,19,text)
def clear_requirement():
    screen.addstr(3,19,'                             ')
    screen.addstr(3,19,'No active requests from cmd.')
def generate_street_name():
    suffix = ""
    street_number = str(random.randint(24, 96))
    if street_number.endswith("11") or street_number.endswith("12") or street_number.endswith("13"):
        suffix = "th"
    elif street_number.endswith("1"):
        suffix = "st"
    elif street_number.endswith("2"):
        suffix = "nd"
    elif street_number.endswith("3"):
        suffix = "rd"
    else:
        suffix = "th"
    street_number+=suffix
    street_suffix = random.choice(["St", "Ave", "Blvd", "Dr", "Rd"])
    street_direction = random.choice(["N", "E", "S", "W", "NE", "NW", "SE", "SW",""])
    
    
    return [street_number,street_suffix,street_direction]
commandDone = False
call = None
minimums = [None,1500]
bcchance = 0
length = None
startTime = None
rtc = False
points = 0 
minimum_stop = False
def set_points(total):
    screen.addstr(5,1,"Total Points:",curses.A_UNDERLINE)
    screen.addstr(5,16,str(total))
set_points(0)
def update_command(unit,street_info = generate_street_name()):
    global commandDone
    #8th Avenue W cmd (Engine 191)
    street_number,street_suffix,street_direction = street_info
    screen.addstr(2,10,f"{street_number} {street_suffix} {street_direction} CMD ({unit})")
    screen.addstr(3,19,'No active requests from cmd.')
    commandDone = True
def create_call():
    global call
    global minimums
    global bcchance
    global length

    f = open('situations.json')
    data = f.read()
    f.close()
    data = json.loads(data)
    data = random.choice(data)
    call = data['title']
    minimums = [data['minimum_type'],data['minimum_count']]
    bcchance = data['b/c']
    if random.randint(0,100)<=bcchance:
        bcchance=True
    else:bcchance=False
    length = random.randint(data['time_min'],data['time_max'])
    screen.addstr(1,1,'Assignment:',curses.A_UNDERLINE)
    screen.addstr(1,13,data['title'])

    screen.addstr(2,1,'Command:',curses.A_UNDERLINE)
    screen.addstr(2,10,'No active command.')

    screen.addstr(3,1,'Command Requests:',curses.A_UNDERLINE)
    screen.addstr(3,19,'No active command.')

    screen.addstr(4,1,'Situation:',curses.A_UNDERLINE)
    screen.addstr(4,12,random.choice(data['situation']))
create_call()

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
    if minimums[1] == 0 and minimum_stop == False:
        startTime = time.time()
        screen.addstr(23,2,'                                      ')
        screen.addstr(23,2,'Time started.')
        minimum_stop = True
        clear_requirement()
    if startTime !=None:
        if time.time()-startTime>=length:
            generate_requirement('Call complete. Clear units.')
            rtc=True
    if rtc == True and units_list_o == []:
        if bcchance == "Complete" or bcchance == False:
            points+=500
            set_points(points)
        else:
            points+=250
            set_points(points)
        commandDone = False
        call = None
        minimums = [None,1500]
        bcchance = 0
        length = None
        startTime = None
        rtc = False
        minimum_stop = False
        clear_requirement()
        screen.addstr(4,12,'                               ')
        screen.addstr(4,12,'No active call.')
        screen.addstr(3,19,'                               ')
        screen.addstr(3,19,'No active call.')
        screen.addstr(2,10,'                               ')
        screen.addstr(2,10,'No active call.')
        screen.addstr(1,13,'                               ')
        screen.addstr(1,13,'No active call.')


    event = screen.getch() 
    if event == curses.KEY_MOUSE:
        _, mx, my, _, _ = curses.getmouse()
        y, x = screen.getyx()
        #screen.addstr(y, x, str(mx)+' '+str(my)+'   ')
        if mx >=2 and mx <=44 and my >=10 and my <=14:
            screen.addstr(22,2,'                                             ')
            screen.addstr(22,2,'Dispatch registered')
            lastButton = 'dispatch'
        elif mx >=2 and mx<=33 and my>=15 and my<=19:
            screen.addstr(22,2,'                                            ')
            screen.addstr(22,2,'Clear registered')
            lastButton = 'clear'
        elif mx>=96 and mx<=110 and my>=2:
            screen.addstr(22,2,'                                     ')
            if lastButton == 'dispatch':

                screen.addstr(22,2,'Dispatch '+str(units_list_a[my-2]['name'])+' registered.')
                #a_list_cache = units_list[list(units_list.keys())[my-2]]
                a_list_cache = units_list_a[my-2]
                idx = units_list_a.index(a_list_cache)
                if a_list_cache['type'] == minimums[0]:
                    minimums[1] -=1
                    screen.addstr(23,2,'                                      ')
                    screen.addstr(23,2,str(str(commandDone)+' '+str(bcchance)))
                if minimums[1] == 1 and bcchance == False or bcchance == 'Complete' and minimum_stop == False:
                    generate_requirement('1 {} company requested.'.format(code_to_pt[minimums[0]]))
                elif minimums[1] > 1 and bcchance == False or bcchance == 'Complete' and minimum_stop == False:
                    generate_requirement ('{} {} companies requested.'.format(minimums[1],code_to_pt[minimums[0]]))
                elif bcchance == True:
                    #wait until BC on scene
                    pass
                if commandDone==False:
                    existing_street_name = generate_street_name()
                    update_command(units_list_a[my-2]['name'],street_info=existing_street_name)

                if units_list_a[my-2]['type'] == "BC" and commandDone == False:
                    update_command(units_list_a[my-2]['name'],street_info=existing_street_name)
                    if bcchance==True:
                        clear_requirement()
                if bcchance == True:
                    generate_requirement('A command unit is requested.')
                    bcchance='Complete'

                del units_list_a[idx]
                units_list_o.append(a_list_cache)
                redraw_units_lists()
                #units_list.keys()[my-2]
            else:
                screen.addstr(22,2,units_list_a[my-2]['name']+' no command.')
                
            lastButton = None
        elif mx>=48 and mx<=66 and my >=2:
            if lastButton == 'clear':
                screen.addstr(22,2,'                                      ')
                screen.addstr(22,2,'Clear '+units_list_o[my-2]['name']+' registered.')
                o_list_cache = units_list_o[my-2]
                idx = units_list_o.index(o_list_cache)
                del units_list_o[idx]
                units_list_a.append(o_list_cache)
                redraw_units_lists()
            else:
                screen.addstr(22,2,units_list_o[my-2]['name']+' no command.')
            

curses.endwin()
