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
    #'E191':{'name':'Engine 191','type':'ENG','dept':'Mercer Island Fire Department','station':'91'},
    'A191':{'name':'Aid 191','type':'BLSAMBO','dept':'Mercer Island Fire Department','station':'91'},
    'MIDI191':{'name':'Midi 191','type':'ENGT3','dept':'Mercer Island Fire Department','station':'91'},
    'E192':{'name':'Engine 192','type':'ENG','dept':'Mercer Island Fire Department','station':'92'},
    'A192':{'name':'Aid 192','type':'BLSAMBO','dept':'Mercer Island Fire Department','station':'92'},
}


screen.addstr(1,1,'Assignment:',curses.A_UNDERLINE)
screen.addstr(1,13,'Residential Smoke Investigation')

screen.addstr(2,1,'Command:',curses.A_UNDERLINE)
screen.addstr(2,10,'30th Avenue CMD')

screen.addstr(3,1,'Command Requests:',curses.A_UNDERLINE)
screen.addstr(3,19,'Engine Company')

screen.addstr(1,int(curses.COLS/2.5),'On-scene units:',curses.A_UNDERLINE)
screen.addstr(2,int(curses.COLS/2.5),'E191')

screen.addstr(1,int(curses.COLS/1.25),'Available units:',curses.A_UNDERLINE)
for x in range(len(list(units_list.keys()))):
    screen.addstr(x+2,int(curses.COLS/1.25),list(units_list.keys())[x]+' - STA'+units_list[list(units_list.keys())[x]]['station'])
for x in range(len(dispatch_text.split('\n'))):
    linetext = dispatch_text.split('\n')[x]
    screen.addstr(x+10,2,linetext)
for x in range(len(clear_text.split('\n'))):
    linetext = clear_text.split('\n')[x]
    screen.addstr(x+15,2,linetext)
while True:
    event = screen.getch() 
    if event == ord("q"): break 
    if event == curses.KEY_MOUSE:
        _, mx, my, _, _ = curses.getmouse()
        y, x = screen.getyx()
        screen.addstr(y, x, str(mx)+' '+str(my)+'   ')
        if mx >=2 and mx <=44 and my >=10 and my <=14:
            screen.addstr(22,2,'Dispatch registered')

curses.endwin()
