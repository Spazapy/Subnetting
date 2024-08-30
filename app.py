import Subnetz as net
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        self.title('Network Tool')
        self.geometry('300x350')
        self.resizable(False, False)

        self.entry_ip = Entry(self, 'XXX', 'normal', 'Ip-Adress', entry_cidr=True)
        self.entry_sub = Entry(self, 'XXX', 'readonly', 'Subnetmask')
        self.radio_buttons = Toggle(self, self.entry_sub, self.entry_ip)

        self.button_submit = ttk.Button(self, text='Submit', command=self.get_cidr_value)
        self.button_submit.pack(pady=(10, 10))

        self.result = FrameResult(self).pack(expand=True, fill='x', padx=20)

        self.entry_ip.cidr_field.bind('<Return>', self.get_cidr_value)

        self.mainloop()

    def get_cidr_value(self,event=None):
        cidr_value = self.entry_ip.get_cidr_value()
        subnetmask = net.cidr_to_sub(cidr_value).split('.')
        self.entry_sub.toggle_state('normal')
        counter = 0
        for octet in self.entry_sub.octet_list:
            octet.delete(0, tk.END)
            octet.insert(0,subnetmask[counter])
            counter += 1
        self.entry_sub.toggle_state('readonly')

class Toggle(ttk.Frame):
    def __init__(self, parent, entry_sub, entry_ip):
        super().__init__(parent)
        self.pack()
        self.radio = tk.StringVar(value='cidr')

        self.entry_sub = entry_sub
        self.entry_ip = entry_ip

        self.radio_sub = ttk.Radiobutton(
            self, 
            text='Use Subnetmask', 
            value='sub', 
            variable=self.radio, 
            command=self.toggle_entries)
        self.radio_cidr = ttk.Radiobutton(
            self, 
            text='Use CIDR Prefix', 
            value='cidr', 
            variable=self.radio, 
            command=self.toggle_entries)
        
        self.radio_sub.pack(side='left', padx=(0,10), pady=10)
        self.radio_cidr.pack(side='left')

    def toggle_entries(self):
        if self.radio.get() == 'sub':
            self.entry_sub.toggle_state('normal')
            self.entry_ip.toggle_cidr_state('readonly')
        else:
            self.entry_sub.toggle_state('readonly')
            self.entry_ip.toggle_cidr_state('normal')
        
class Entry(ttk.Frame):
    def __init__(self, parent, text, state, entry_title, entry_cidr=False):
        super().__init__(parent)
        self.pack()

        self.octet_list = []
        self.cidr_field = None
        self.entry_label = ttk.Label(self, text=entry_title, font=('Arial', 14))
        self.entry_label.pack(pady=8)

        oct_1 = Octett(self, text, state)
        ttk.Label(self, text='.').pack(side='left')
        oct_2 = Octett(self, text, state)
        ttk.Label(self, text='.').pack(side='left')
        oct_3 = Octett(self, text, state)
        ttk.Label(self, text='.').pack(side='left')
        oct_4 = Octett(self, text, state)

        self.octet_list.append(oct_1)
        self.octet_list.append(oct_2)
        self.octet_list.append(oct_3)
        self.octet_list.append(oct_4)

        if entry_cidr:
            ttk.Label(self, text='/').pack(side='left', padx=6)
            self.cidr_field = Octett(self, text, state)
            self.cidr_field.pack(side='left')

    def get_values(self):
        return [octet.get_value() for octet in self.octet_list]
    
    def get_cidr_value(self):
        if self.cidr_field:
            return self.cidr_field.get_value()
        return None
    
    def toggle_state(self, new_state):
        for octet in self.octet_list:
            octet.config(state=new_state)

    def toggle_cidr_state(self, new_state):
        if self.cidr_field:
            self.cidr_field.config(state=new_state)

class Octett(ttk.Entry):
    def __init__(self, parent, text, state):
        super().__init__(
            parent, 
            justify='center', 
            width='5', 
            foreground='lightgrey', 
            state=state)
        
        self.pack(side='left')
        self.insert(0,text)

        def entry_focus_in(event):
            if event.widget.get() != '':
                event.widget.delete(0, tk.END)

        def entry_focus_out(event):
            if event.widget.get() == '':
                event.widget.insert(0, 'XXX')

        self.bind('<FocusIn>', entry_focus_in)
        self.bind('<FocusOut>', entry_focus_out)

    def get_value(self):
        return self.get()
    
class FrameResult(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.rowconfigure((1,2,3,4,5), weight=1, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.columnconfigure(2, weight=4, uniform='a')

        self.Label_netid = ttk.Label(self, text='Network Adress: ', font=('Arial', 10))
        self.Label_first_host = ttk.Label(self, text='First Host IP: ', font=('Arial', 10))
        self.Label_last_host = ttk.Label(self, text='Last Host IP: ', font=('Arial', 10))
        self.Label_broadcast = ttk.Label(self, text='Broadcast Adress: ', font=('Arial', 10))
        self.Label_max_hosts = ttk.Label(self, text='Max. # of Hosts: ', font=('Arial', 10))

        self.Label_netid.grid(row=0, column=0, sticky='e')
        self.Label_first_host.grid(row=1, column=0, sticky='e')
        self.Label_last_host.grid(row=2, column=0, sticky='e')
        self.Label_broadcast.grid(row=3, column=0, sticky='e')
        self.Label_max_hosts.grid(row=4, column=0, sticky='e')

        
        self.Label_netid_result = ttk.Label(self, text='0.0.0.0', font=('Arial', 10))
        self.Label_first_host_result = ttk.Label(self, text='0.0.0.0', font=('Arial', 10))
        self.Label_last_host_result = ttk.Label(self, text='0.0.0.0', font=('Arial', 10))
        self.Label_broadcast_result = ttk.Label(self, text='0.0.0.0', font=('Arial', 10))
        self.Label_max_hosts_result = ttk.Label(self, text='0', font=('Arial', 10))

        self.Label_netid_result.grid(row=0, column=1, columnspan=4, sticky='w')
        self.Label_first_host_result.grid(row=1, column=1, columnspan=4, sticky='w')
        self.Label_last_host_result.grid(row=2, column=1, columnspan=4, sticky='w')
        self.Label_broadcast_result.grid(row=3, column=1, columnspan=4, sticky='w')
        self.Label_max_hosts_result.grid(row=4, column=1, columnspan=4, sticky='w')

# run
App()