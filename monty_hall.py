import tkinter as tk
from tkinter import PhotoImage
from PIL import ImageTk,Image
from tkinter import messagebox
import random
import time 
import mysql.connector

#sql connection
conn=mysql.connector.connect(host="localhost",password="oranje57",user="root",database="monty")
cursor=conn.cursor()

query="select games from monty_stats where s_no=1"
cursor.execute(query)
g=cursor.fetchone()
query1="select wins from monty_stats where s_no=1"
cursor.execute(query1)
g1=cursor.fetchone()
query2="select loses from monty_stats where s_no=1"
cursor.execute(query2)
g2=cursor.fetchone()
query3="select switch_counter from monty_stats where s_no=1"
cursor.execute(query3)
g3=cursor.fetchone()
query4="select stay_counter from monty_stats where s_no=1"
cursor.execute(query4)
g4=cursor.fetchone()

query5="select pwin_switch from monty_stats where s_no=1"
cursor.execute(query5)
g5=cursor.fetchone()
query6="select pwin_stay from monty_stats where s_no=1"
cursor.execute(query6)
g6=cursor.fetchone()


user_car = None
car_behind = None
dummy_door = None
game_counter=int(g[0])
win_counter=int(g1[0])
lose_counter=int(g2[0])
switch_win_counter=int(g3[0])
stay_win_counter=int(g4[0])
p_switch= switch_win_counter / game_counter if game_counter > 0 else 0
p_stay = stay_win_counter / game_counter if game_counter > 0 else 0

def setup_game():
    global user_car, car_behind, dummy_door
    user_car = None
    car_behind = None
    dummy_door = None

def user_select(door_number):
    global user_car
    global game_counter
    global switch_win_counter,stay_win_counter,p_switch,p_stay
    user_car = door_number
    result_label1.config(text=f"You chose door {door_number}")
    result_label2.config(text="Monty is choosing a door...")
    root.update_idletasks()
    root.after(1500,monty_select())
    
    result_label2.config(text=f"Monty chose door {dummy_door}")
    root.update_idletasks()
    switch = messagebox.askyesno("Switch Doors", "Do you want to switch doors?")
    #----statistics----
    if(user_car==car_behind):
        stay_win_counter+=1
        value=(stay_win_counter,)
        q1="update monty_stats set stay_counter=%s where s_no=1"
        cursor.execute(q1,value)
        conn.commit()
    else:
        switch_win_counter+=1
        value=(switch_win_counter,)
        q1="update monty_stats set switch_counter=%s where s_no=1"
        cursor.execute(q1,value)
        conn.commit()
    #--------------------   
    if switch:
        switched_car = switch_doors()
        result_label1.config(text=f"You switched to door {switched_car}")     
    else:
        switched_car = user_car 

    announce_result(switched_car)
    game_counter+=1
    value=(game_counter,)
    q1="update monty_stats set games=%s where s_no=1"
    cursor.execute(q1,value)
    conn.commit()
    p_switch=switch_win_counter/game_counter
    value=(p_switch,)
    que1="update monty_stats set pwin_switch=%s where s_no=1"
    cursor.execute(que1,value)
    conn.commit()
    p_stay=stay_win_counter/game_counter
    value=(p_stay,)
    que2="update monty_stats set pwin_stay=%s where s_no=1"
    cursor.execute(que2,value)
    conn.commit()

def monty_select():
    global car_behind
    doors = [1, 2, 3]
    car_behind = random.choice(doors)
    global dummy_door
    doors.remove(car_behind)
    if(user_car in doors):
        doors.remove(user_car)
    dummy_door = doors[0]
    
def switch_doors():
    doors = [1, 2, 3]
    doors.remove(user_car)
    doors.remove(dummy_door)
    return doors[0]

def change_labels():
    if(car_behind==1):
        label2.configure(text="Car")
        label3.configure(text="Goat")
        label4.configure(text="Goat")
    elif(car_behind==2):
        label2.configure(text="Goat")
        label3.configure(text="Car")
        label4.configure(text="Goat")        
    else:
        label2.configure(text="Goat")
        label3.configure(text="Goat")
        label4.configure(text="Car")
        
def announce_result(switched_car):
    global win_counter,lose_counter
    if switched_car == car_behind:
        win_counter+=1
        value=(win_counter,)
        q1="update monty_stats set wins=%s where s_no=1"
        cursor.execute(q1,value)
        conn.commit()
        result_label1.config(text="Congratulations, You won!!!")
        result_label2.config(text=f"Car is in door {car_behind}")
        change_labels()
        
    else:
        lose_counter+=1
        value=(lose_counter,)
        q1="update monty_stats set loses=%s where s_no=1"
        cursor.execute(q1,value)
        conn.commit()
        result_label1.config(text="Sorry, You Lost")
        result_label2.config(text=f"You chose door {switched_car} but Car is in door {car_behind}")
        change_labels()

def play_again():
    setup_game()
    result_label1.config(text="")
    result_label2.config(text="")
    label2.configure(text="Door 1")
    label3.configure(text="Door 2")
    label4.configure(text="Door 3")

def update_welcome_text_position():
    global direction
    canvas.move(welcome_text, direction, 0)
    x, _ = canvas.coords(welcome_text)
    if x<=500 or x>=1000:
        direction=-direction
    root.after(10, update_welcome_text_position)
 

def stats_page():
    global game_counter,k1,k2,k3,k4,k5,stats,p_switch,p_stay
    stats=tk.Tk()
    stats.title("statistics")
    stats.state("zoomed")
    stats.configure(bg="purple")
    
    l1=tk.Label(stats,text="Total No of games played:",font=("italic_iv50",15),fg="white",bg="indigo",width=30,height=2)
    l1.place(x=100,y=100)
    k1=tk.Label(stats,text=game_counter,font=("italic_iv50",15),fg="indigo",bg="orange",width=5,height=2)
    k1.place(x=600,y=100)
    l2=tk.Label(stats,text="Total No of games Won:",font=("italic_iv50",15),fg="white",bg="indigo",width=30,height=2)
    l2.place(x=100,y=200)
    k2=tk.Label(stats,text=win_counter,font=("italic_iv50",15),fg="indigo",bg="orange",width=5,height=2)
    k2.place(x=600,y=200)
    l3=tk.Label(stats,text="Total No of games Lost:",font=("italic_iv50",15),fg="white",bg="indigo",width=30,height=2)
    l3.place(x=100,y=300)
    k3=tk.Label(stats,text=lose_counter,font=("italic_iv50",15),fg="indigo",bg="orange",width=5,height=2)
    k3.place(x=600,y=300)
    l4=tk.Label(stats,text="P(win|we switch):",font=("italic_iv50",15),fg="white",bg="indigo",width=30,height=2)
    l4.place(x=100,y=400)
    k4=tk.Label(stats,text=p_switch,font=("italic_iv50",15),fg="indigo",bg="orange",width=20,height=2)
    k4.place(x=600,y=400)
    l5=tk.Label(stats,text="P(win|we stay):",font=("italic_iv50",15),fg="white",bg="indigo",width=30,height=2)
    l5.place(x=100,y=500)
    k5=tk.Label(stats,text=p_stay,font=("italic_iv50",15),fg="indigo",bg="orange",width=20,height=2)
    k5.place(x=600,y=500)
    b1=tk.Button(stats,text="Reset stats",font=("italic_iv50",16),fg="orange",bg="indigo",width=10,height=1,command=reset_counters)
    b1.place(x=1015,y=200)
    b2=tk.Button(stats,text="Back to game",font=("italic_iv50",15),fg="orange",bg="indigo",width=13,height=1,command=stats.destroy)
    b2.place(x=1000,y=300)
    
    stats.mainloop()

def reset_counters():
    global k1, k2, k3, k4, k5, game_counter, win_counter, lose_counter, switch_win_counter, stay_win_counter,p_switch, p_stay

    values = ('0','0','0','0','0','0.0','0.0')
    que = "UPDATE monty_stats SET games=%s, wins=%s, loses=%s, switch_counter=%s,stay_counter=%s,pwin_switch=%s, pwin_stay=%s WHERE s_no=1"
    cursor.execute(que, values)
    conn.commit()

    game_counter = 0
    win_counter = 0
    lose_counter = 0
    switch_win_counter = 0
    stay_win_counter = 0
    p_switch=0
    p_stay=0

    k1.config(text=game_counter)
    k2.config(text=win_counter)
    k3.config(text=lose_counter)
    k4.config(text=p_switch)
    k5.config(text=p_stay)

    stats.mainloop()

def rootclose():
    if messagebox.askyesno('Quit','Do you want to quit the Game?'):
        root.destroy()
        quit()

root=tk.Tk()
root.title("Monty Hall")
root.configure(bg="purple")
root.state('zoomed')
root.protocol('WM_DELETE_WINDOW',rootclose)

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=40,bg="indigo")
canvas.pack()
welcome_text = canvas.create_text(500, 25,text="Monty hall", font=("Italic_iv50", 17),fill="orange")  
direction=1
update_welcome_text_position()

label=tk.Label(text="Click the door number u want",font=("italic_iv50",15),fg="white",bg="indigo",width=30,height=2)
label.place(x=100,y=670)
label2=tk.Label(text="Door 1",font=("italic_iv50",20),bg="orange",fg="indigo",width=20,height=10)
label2.place(x=50,y=70)
label3=tk.Label(text="Door 2",font=("italic_iv50",20),fg="white",bg="indigo",width=20,height=10)
label3.place(x=560,y=70)
label4=tk.Label(text="Door 3",font=("italic_iv50",20),bg="orange",fg="indigo",width=20,height=10)
label4.place(x=1070,y=70)

b1=tk.Button(text="1",font=("italic_iv50",16),fg="indigo",bg="orange",width=5,height=2,command=lambda:user_select(1))
b1.place(x=600,y=650)
b2=tk.Button(text="2",font=("italic_iv50",16),fg="indigo",bg="orange",width=5,height=2,command=lambda:user_select(2))
b2.place(x=800,y=650)
b3=tk.Button(text="3",font=("italic_iv50",16),fg="indigo",bg="orange",width=5,height=2,command=lambda:user_select(3))
b3.place(x=1000,y=650)

result_label1 = tk.Label(text="", font=("italic_iv50", 15), bg="orange", fg="indigo", width=40, height=2)
result_label1.place(x=100, y=500)
result_label2 = tk.Label(text="", font=("italic_iv50", 15), bg="orange", fg="indigo", width=40, height=2)
result_label2.place(x=800, y=500)

play_again_button = tk.Button(text="Play Again",font=("italic_iv50",12),bg="indigo",fg="white",width=10,height=2 , command=play_again)
play_again_button.place(x=1150, y=665)

view_stats_button = tk.Button(text="View stats",font=("italic_iv50",12),bg="indigo",fg="white",width=10,height=2 , command=stats_page)
view_stats_button.place(x=1350, y=665)
root.mainloop()