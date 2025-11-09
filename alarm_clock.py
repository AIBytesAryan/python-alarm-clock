import tkinter as tk
from tkinter import ttk, messagebox
import time
import datetime
import winsound
import threading

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Alarm Clock")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#2C3E50')
        
        self.alarm_running = False
        self.current_alarm_time = None
        
        self.create_widgets()
        self.update_time()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="⏰ SMART ALARM CLOCK", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2C3E50')
        title_label.pack(pady=20)
        
        # Current Time Display
        self.time_label = tk.Label(self.root, text="", 
                                  font=('Digital-7', 35, 'bold'), 
                                  fg='#00FF00', bg='black', 
                                  relief=tk.SUNKEN, bd=3)
        self.time_label.pack(pady=10, padx=20, fill=tk.X)
        
        # Date Display
        self.date_label = tk.Label(self.root, text="", 
                                  font=('Arial', 14), 
                                  fg='white', bg='#2C3E50')
        self.date_label.pack(pady=5)
        
        # Alarm Frame
        alarm_frame = tk.LabelFrame(self.root, text=" Set Alarm ", 
                                   font=('Arial', 12, 'bold'),
                                   fg='white', bg='#34495E', bd=3)
        alarm_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # Time Selection
        time_frame = tk.Frame(alarm_frame, bg='#34495E')
        time_frame.pack(pady=15)
        
        # Hour
        tk.Label(time_frame, text="Hour:", font=('Arial', 11), 
                fg='white', bg='#34495E').grid(row=0, column=0, padx=5)
        self.hour_var = tk.StringVar(value="12")
        hour_spinbox = tk.Spinbox(time_frame, from_=1, to=12, width=5,
                                 textvariable=self.hour_var, font=('Arial', 11))
        hour_spinbox.grid(row=0, column=1, padx=5)
        
        # Minute
        tk.Label(time_frame, text="Minute:", font=('Arial', 11), 
                fg='white', bg='#34495E').grid(row=0, column=2, padx=5)
        self.minute_var = tk.StringVar(value="00")
        minute_spinbox = tk.Spinbox(time_frame, from_=0, to=59, width=5,
                                   textvariable=self.minute_var, format="%02.0f")
        minute_spinbox.grid(row=0, column=3, padx=5)
        
        # AM/PM
        self.ampm_var = tk.StringVar(value="PM")
        ampm_combobox = ttk.Combobox(time_frame, textvariable=self.ampm_var,
                                    values=["AM", "PM"], width=5, state="readonly")
        ampm_combobox.grid(row=0, column=4, padx=5)
        
        # Alarm Message
        tk.Label(alarm_frame, text="Alarm Message:", font=('Arial', 11), 
                fg='white', bg='#34495E').pack(pady=(10,5))
        self.message_var = tk.StringVar(value="Wake Up! Time's up!")
        message_entry = tk.Entry(alarm_frame, textvariable=self.message_var, 
                                font=('Arial', 11), width=30)
        message_entry.pack(pady=5)
        
        # Buttons Frame
        button_frame = tk.Frame(alarm_frame, bg='#34495E')
        button_frame.pack(pady=15)
        
        self.set_btn = tk.Button(button_frame, text="🔔 Set Alarm", 
                                font=('Arial', 11, 'bold'),
                                bg='#27AE60', fg='white',
                                command=self.set_alarm, width=12)
        self.set_btn.grid(row=0, column=0, padx=10)
        
        self.cancel_btn = tk.Button(button_frame, text="❌ Cancel Alarm", 
                                   font=('Arial', 11, 'bold'),
                                   bg='#E74C3C', fg='white',
                                   command=self.cancel_alarm, width=12)
        self.cancel_btn.grid(row=0, column=1, padx=10)
        
        # Snooze Button
        self.snooze_btn = tk.Button(button_frame, text="⏰ Snooze (5 min)", 
                                   font=('Arial', 11, 'bold'),
                                   bg='#F39C12', fg='white',
                                   command=self.snooze_alarm, width=15)
        self.snooze_btn.grid(row=1, column=0, columnspan=2, pady=10)
        self.snooze_btn.config(state=tk.DISABLED)
        
        # Alarm Status
        self.status_label = tk.Label(self.root, text="No alarm set", 
                                    font=('Arial', 12, 'bold'), 
                                    fg='yellow', bg='#2C3E50')
        self.status_label.pack(pady=10)
        
        # Next Alarm Display
        self.next_alarm_label = tk.Label(self.root, text="", 
                                        font=('Arial', 10), 
                                        fg='#AED6F1', bg='#2C3E50')
        self.next_alarm_label.pack(pady=5)
    
    def update_time(self):
        """Update current time every second"""
        current_time = time.strftime("%I:%M:%S %p")
        current_date = time.strftime("%A, %B %d, %Y")
        
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        
        # Check alarm every second
        if self.alarm_running and self.current_alarm_time:
            self.check_alarm()
        
        # Update every 1000ms (1 second)
        self.root.after(1000, self.update_time)
    
    def set_alarm(self):
        """Set the alarm for specified time"""
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            ampm = self.ampm_var.get()
            
            if hour < 1 or hour > 12:
                messagebox.showerror("Error", "Hour must be between 1 and 12")
                return
            if minute < 0 or minute > 59:
                messagebox.showerror("Error", "Minute must be between 0 and 59")
                return
            
            # Convert to 24-hour format for comparison
            if ampm == "PM" and hour != 12:
                hour_24 = hour + 12
            elif ampm == "AM" and hour == 12:
                hour_24 = 0
            else:
                hour_24 = hour
            
            self.current_alarm_time = f"{hour_24:02d}:{minute:02d}"
            self.alarm_running = True
            
            # Update status
            display_time = f"{hour:02d}:{minute:02d} {ampm}"
            self.status_label.config(text=f"Alarm set for: {display_time}", fg='#00FF00')
            self.next_alarm_label.config(text=f"Next: {display_time} - {self.message_var.get()}")
            
            messagebox.showinfo("Alarm Set", f"Alarm set for {display_time}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for hour and minute")
    
    def cancel_alarm(self):
        """Cancel the current alarm"""
        self.alarm_running = False
        self.current_alarm_time = None
        self.status_label.config(text="Alarm cancelled", fg='red')
        self.next_alarm_label.config(text="")
        self.snooze_btn.config(state=tk.DISABLED)
        messagebox.showinfo("Alarm Cancelled", "Alarm has been cancelled")
    
    def snooze_alarm(self):
        """Snooze alarm for 5 minutes"""
        if self.alarm_running:
            # Add 5 minutes to current alarm time
            hour_24, minute = map(int, self.current_alarm_time.split(':'))
            minute += 5
            if minute >= 60:
                minute -= 60
                hour_24 = (hour_24 + 1) % 24
            
            self.current_alarm_time = f"{hour_24:02d}:{minute:02d}"
            
            # Convert back to 12-hour format for display
            if hour_24 == 0:
                display_hour = 12
                ampm = "AM"
            elif hour_24 < 12:
                display_hour = hour_24
                ampm = "AM"
            elif hour_24 == 12:
                display_hour = 12
                ampm = "PM"
            else:
                display_hour = hour_24 - 12
                ampm = "PM"
            
            display_time = f"{display_hour:02d}:{minute:02d} {ampm}"
            self.status_label.config(text=f"Snoozed until: {display_time}", fg='orange')
            self.snooze_btn.config(state=tk.DISABLED)
    
    def check_alarm(self):
        """Check if current time matches alarm time"""
        if not self.alarm_running or not self.current_alarm_time:
            return
        
        current_time_24 = time.strftime("%H:%M")
        
        if current_time_24 == self.current_alarm_time:
            self.trigger_alarm()
    
    def trigger_alarm(self):
        """Trigger the alarm sound and notification"""
        self.alarm_running = False
        self.snooze_btn.config(state=tk.NORMAL)
        
        # Show alarm message
        message = self.message_var.get()
        messagebox.showwarning("ALARM!", f"{message}\n\nClick OK to stop alarm")
        
        # Play sound (Windows - you can change this for other OS)
        try:
            # Play beep sound repeatedly
            for _ in range(5):
                winsound.Beep(1000, 1000)  # Frequency 1000Hz, duration 1000ms
                time.sleep(0.5)
        except:
            # If winsound not available, just show message
            pass
        
        self.status_label.config(text="Alarm triggered!", fg='red')

def main():
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()