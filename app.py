import Subnetz as net
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
import ipaddress

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename='darkly')
        self.title('Network Tool')
        self.geometry('300x350')
        self.resizable(False, False)

        self.entry_ip = Entry(self, 'XXX', 'normal', 'Ip-Adress', entry_cidr=True)
        self.entry_sub = Entry(self, 'XXX', 'readonly', 'Subnetmask')
        self.radio_buttons = Toggle(self, self.entry_sub, self.entry_ip)

        self.button_submit = ttk.Button(self, text='Submit', command=self.show_network)
        self.button_submit.pack(pady=(10, 10))

        self.result_frame = FrameResult(self)
        self.result_frame.pack(expand=True, fill='x', padx=20)

        self.entry_ip.cidr_field.bind('<Return>', self.update_subnetmask)

        self.mainloop()

    def show_network(self):
        ip = self.validate_ip()
        subnetmask = self.get_mask()
        try:
            network = ipaddress.ip_network((ip + '/' + subnetmask), strict=False)
            self.result_frame.update_labels(
                network_id=network.network_address,
                first_host=net.first_host_get(network),
                last_host=net.last_host_get(network),
                broadcast=network.broadcast_address,
                max_hosts=network.num_addresses - 2
            )
            self.update_subnetmask(subnetmask.split('.'))
        except ValueError as e:
            messagebox.showerror(title='Invalid Network', message=f'Something went wrong. Check IP and Subnetmask. Error: {e}')


    def validate_ip(self):
        ip_lst = self.entry_ip.get_values()
        ip = f"{ip_lst[0]}.{ip_lst[1]}.{ip_lst[2]}.{ip_lst[3]}"
        try:
            net.ipaddress.ip_address(ip)
            return ip
        except:
            messagebox.showwarning(title='Invalid IP', message='Invalid IP-Address. Please enter a valid IP')
            for octet in self.entry_ip.octet_list:
                octet.delete(0, tk.END)
                octet.insert(0,'0')

    def get_mask(self):
        if not self.entry_ip.cidr_field.instate(['readonly']):
            cidr_value = self.entry_ip.get_cidr_value()
            subnetmask = net.cidr_to_sub(cidr_value)
        else:
            sub_lst = self.entry_sub.get_values()
            subnetmask = f'{sub_lst[0]}.{sub_lst[1]}.{sub_lst[2]}.{sub_lst[3]}'
            if subnetmask not in net.cidr_to_subnet.values():
                messagebox.showwarning(title='Invalid Mask', message='Invalid Subnetmask. Please enter a valid mask')
                subnetmask = '0.0.0.0'
                for octet in self.entry_sub.octet_list:
                    octet.delete(0, tk.END)
                    octet.insert(0,'0')
        return subnetmask

    def update_subnetmask(self, subnetmask):
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

        image_url = './icons/copy_alt.png'
        self.image = tk.PhotoImage(file=image_url)

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

        self.Label_netid_result.grid(row=0, column=1, columnspan=3, sticky='w')
        self.Label_first_host_result.grid(row=1, column=1, columnspan=3, sticky='w')
        self.Label_last_host_result.grid(row=2, column=1, columnspan=3, sticky='w')
        self.Label_broadcast_result.grid(row=3, column=1, columnspan=3, sticky='w')
        self.Label_max_hosts_result.grid(row=4, column=1, columnspan=3, sticky='w')

        self.button_netid = tk.Button(
            self, 
            text='Copy', 
            image=self.image, 
            command=lambda: self.copy_to_clipboard(self.Label_netid_result.cget('text')))
        self.button_first_host = tk.Button(
            self, 
            text='Copy', 
            image=self.image, 
            command=lambda: self.copy_to_clipboard(self.Label_first_host_result.cget('text')))
        self.button_last_host = tk.Button(
            self, 
            text='Copy', 
            image=self.image, 
            command=lambda: self.copy_to_clipboard(self.Label_last_host_result.cget('text')))
        self.button_broadcast = tk.Button(
            self, 
            text='Copy', 
            image=self.image, 
            command=lambda: self.copy_to_clipboard(self.Label_broadcast_result.cget('text')))
        self.button_max_hosts = tk.Button(
            self, 
            text='Copy', 
            image=self.image, 
            command=lambda: self.copy_to_clipboard(self.Label_max_hosts_result.cget('text')))

        self.button_netid.grid(row=0, column=4, sticky='e', ipady=0, ipadx=0)
        self.button_first_host.grid(row=1, column=4, sticky='e')
        self.button_last_host.grid(row=2, column=4, sticky='e')
        self.button_broadcast.grid(row=3, column=4, sticky='e')
        self.button_max_hosts.grid(row=4, column=4, sticky='e')

    def update_labels(self, network_id, first_host, last_host, broadcast, max_hosts):
        self.Label_netid_result.config(text=network_id)
        self.Label_first_host_result.config(text=first_host)
        self.Label_last_host_result.config(text=last_host)
        self.Label_broadcast_result.config(text=broadcast)
        self.Label_max_hosts_result.config(text=max_hosts)

    def copy_to_clipboard(self, label):
        self.clipboard_clear()
        self.clipboard_append(label)
        self.update()

# run
App()