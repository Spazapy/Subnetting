import Subnetz as net
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

def entry_focus_out(event):
    if event.widget.get() == '':
        event.widget.insert(0, 'XXX')

def entry_focus_out_cidr(event):
    cidr = event.widget.get()
    if event.widget.get() == '':
        event.widget.insert(0, 'XXX')
    elif cidr.isdigit():
        subnet_mask = net.cidr_to_sub(cidr)
        sub_octetts = subnet_mask.split('.')
        entry_sub_1.delete(0, tk.END)
        entry_sub_2.delete(0, tk.END)
        entry_sub_3.delete(0, tk.END)
        entry_sub_4.delete(0, tk.END)
        entry_sub_1.insert(0, sub_octetts[0])
        entry_sub_2.insert(0, sub_octetts[1])
        entry_sub_3.insert(0, sub_octetts[2])
        entry_sub_4.insert(0, sub_octetts[3])
        
def entry_focus_in(event):
    if event.widget.get() != '':
        event.widget.delete(0, tk.END)

def get_net_data():
    ip_oct_1 = entry_ip_1.get()
    ip_oct_2 = entry_ip_2.get()
    ip_oct_3 = entry_ip_3.get()
    ip_oct_4 = entry_ip_4.get()
    sub_oct_1 = entry_sub_1.get()
    sub_oct_2 = entry_sub_2.get()
    sub_oct_3 = entry_sub_3.get()
    sub_oct_4 = entry_sub_4.get()
    ip_string = f'{ip_oct_1}.{ip_oct_2}.{ip_oct_3}.{ip_oct_4}'
    sub_string = f'{sub_oct_1}.{sub_oct_2}.{sub_oct_3}.{sub_oct_4}'
    network = net.get_network(ip_string, sub_string)
    print(network)
    
def disable_sub():
    pass

def disable_cidr():
    pass

# window
window = ttk.Window(themename='darkly')
window.title('Netzwerk Tool')
window.geometry('600x400')

# entry IP Adress and Prefix
label_title_ip = ttk.Label(window, text='IP Adress', font=('Arial', 12))
frame_ip = ttk.Frame(window)

entry_ip_1 = ttk.Entry(frame_ip, justify='center', width='5', foreground='lightgrey')
entry_ip_1.insert(0,'XXX')
entry_ip_2 = ttk.Entry(frame_ip, justify='center', width='5', foreground='lightgrey')
entry_ip_2.insert(0,'XXX')
entry_ip_3 = ttk.Entry(frame_ip, justify='center', width='5', foreground='lightgrey')
entry_ip_3.insert(0,'XXX')
entry_ip_4 = ttk.Entry(frame_ip, justify='center', width='5', foreground='lightgrey')
entry_ip_4.insert(0,'XXX')
entry_cidr = ttk.Entry(frame_ip, justify='center', width='3', foreground='lightgrey')
entry_cidr.insert(0,'XX')

label_ip_12 = ttk.Label(frame_ip, text='.')
label_ip_23 = ttk.Label(frame_ip, text='.')
label_ip_34 = ttk.Label(frame_ip, text='.')
label_ip_cidr = ttk.Label(frame_ip, text='/')

label_title_ip.pack(pady=(10,6))
frame_ip.pack()
entry_ip_1.grid(row=0, column=0)
label_ip_12.grid(row=0, column=1)
entry_ip_2.grid(row=0, column=2)
label_ip_23.grid(row=0, column=3)
entry_ip_3.grid(row=0, column=4)
label_ip_34.grid(row=0, column=5)
entry_ip_4.grid(row=0, column=6)
label_ip_cidr.grid(row=0, column=7, padx=5)
entry_cidr.grid(row=0, column=8)

# Entry Subnetmask
label_title_sub = ttk.Label(window, text='Subnetmask', font=('Arial', 12))
frame_sub = ttk.Frame(window)

entry_sub_1 = ttk.Entry(frame_sub, justify='center', width='5', foreground='lightgrey')
entry_sub_1.insert(0,'XXX')
entry_sub_2 = ttk.Entry(frame_sub, justify='center', width='5', foreground='lightgrey')
entry_sub_2.insert(0,'XXX')
entry_sub_3 = ttk.Entry(frame_sub, justify='center', width='5', foreground='lightgrey')
entry_sub_3.insert(0,'XXX')
entry_sub_4 = ttk.Entry(frame_sub, justify='center', width='5', foreground='lightgrey')
entry_sub_4.insert(0,'XXX')

radio = tk.StringVar(value='cidr')

# label_radio_sub = ttk.Label(window, text='Use Subnetmask')
# label_radio_cidr = ttk.Label(window, text='Use CIDR Prefix')

radio_sub = ttk.Radiobutton(window, text='Use Subnetmask', value='sub', variable=radio, command=disable_cidr)
radio_cidr = ttk.Radiobutton(window, text='Use CIDR Prefix', value='cidr', variable=radio, command=disable_sub)
radio_sub.pack()
radio_cidr.pack()

label_sub_12 = ttk.Label(frame_sub, text='.')
label_sub_23 = ttk.Label(frame_sub, text='.')
label_sub_34 = ttk.Label(frame_sub, text='.')

label_title_sub.pack(pady=(10,6))
frame_sub.pack(expand=True, fill='y')
entry_sub_1.grid(row=0, column=0)
label_sub_12.grid(row=0, column=1)
entry_sub_2.grid(row=0, column=2)
label_sub_23.grid(row=0, column=3)
entry_sub_3.grid(row=0, column=4)
label_sub_34.grid(row=0, column=5)
entry_sub_4.grid(row=0, column=6)

button_submit = ttk.Button(frame_sub, text='Submit', command=get_net_data)
button_submit.grid(row=1, column=0, rowspan=2, pady=10)

frame_result = ttk.Frame(window)
label_net_ip = ttk.Label(frame_result)
label_broadcast = ttk.Label(frame_result)
label_first_host = ttk.Label(frame_result)
label_last_host = ttk.Label(frame_result)
label_possible_hosts = ttk.Label(frame_result)

frame_result.pack()
label_net_ip.pack()
label_broadcast.pack()
label_first_host.pack()
label_last_host.pack()
label_possible_hosts.pack()

frame_result.pack()

# events
entry_ip_1.bind('<FocusIn>', entry_focus_in)
entry_ip_1.bind('<FocusOut>', entry_focus_out)
entry_ip_2.bind('<FocusIn>', entry_focus_in)
entry_ip_2.bind('<FocusOut>', entry_focus_out)
entry_ip_3.bind('<FocusIn>', entry_focus_in)
entry_ip_3.bind('<FocusOut>', entry_focus_out)
entry_ip_4.bind('<FocusIn>', entry_focus_in)
entry_ip_4.bind('<FocusOut>', entry_focus_out)
entry_cidr.bind('<FocusIn>', entry_focus_in)
entry_cidr.bind('<FocusOut>', entry_focus_out_cidr)

entry_sub_1.bind('<FocusIn>', entry_focus_in)
entry_sub_1.bind('<FocusOut>', entry_focus_out)
entry_sub_2.bind('<FocusIn>', entry_focus_in)
entry_sub_2.bind('<FocusOut>', entry_focus_out)
entry_sub_3.bind('<FocusIn>', entry_focus_in)
entry_sub_3.bind('<FocusOut>', entry_focus_out)
entry_sub_4.bind('<FocusIn>', entry_focus_in)
entry_sub_4.bind('<FocusOut>', entry_focus_out)

# run
window.mainloop()