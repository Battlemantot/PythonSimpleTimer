import customtkinter
import datetime
import threading

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simple Timer")
        #self.geometry("320x320")

        self.entry_Hours = customtkinter.CTkEntry(self, placeholder_text="Hours")
        self.entry_Hours.grid(row=0, column=0, padx=20, pady=20)
        self.entry_Minutes = customtkinter.CTkEntry(self, placeholder_text="Minutes")
        self.entry_Minutes.grid(row=0, column=1, padx=20, pady=20)
        self.entry_Seconds = customtkinter.CTkEntry(self, placeholder_text="Seconds")
        self.entry_Seconds.grid(row=0, column=2, padx=20, pady=20)

        self.label_Time = customtkinter.CTkLabel(self, text="Time remaining:", fg_color="transparent")
        self.label_Time.grid(row=1, column=1, padx=20, pady=20)

        self.button_start = customtkinter.CTkButton(self, text="Start Timer", command=self.start_timer)
        self.button_start.grid(row=2, column=0, padx=20, pady=20)

        self.button_stop = customtkinter.CTkButton(self, text="Pause Timer", command=self.stop_countdown)
        self.button_stop.grid(row=2, column=1, padx=20, pady=20)

        self.button_reset = customtkinter.CTkButton(self, text="Reset Timer", command=lambda : self.reset_countdown())
        self.button_reset.grid(row=2, column=2, padx=20, pady=20)

        # create an event object, that's needed later for pause functionality
        self.event = threading.Event()
        # create a thread object, so program doesn't hang on countdown
        self.thread = threading.Thread(target=self.countdown)

    # Timer start function
    def start_timer(self):
        # get the user input values
        h = int(self.entry_Hours.get())
        m = int(self.entry_Minutes.get())
        s = int(self.entry_Seconds.get())
        # calculate and store the total seconds as a class attribute
        self.total_seconds = h * 3600 + m * 60 + s
        # clear the event flag if it was set
        self.event.clear()
        # start the thread if it is not alive
        if not self.thread.is_alive():
            self.thread.start()
    
    # Timer pause function
    def stop_countdown(self):
        # check if the event flag is set or not
        if self.event.is_set():
            # clear the event flag
            self.event.clear()
            # schedule the countdown function to run again
            self.after(1, self.countdown)
        else:
            # set the event flag
            self.event.set()
            # get the current time
            timer = datetime.timedelta(seconds=self.total_seconds)
            # update the label with the time and the word "Paused"
            self.label_Time.configure(text="Time remaining: " + str(timer) + " PAUSED")
            self.button_stop.configure(text="Resume Timer")

    # Timer countdown function    
    def countdown(self):
        # check if the total seconds are zero
        if self.total_seconds == 0:
            # update the label with the final message
            self.label_Time.configure(text="Time remaining: Timer done!")
            return
        # Needed so the "PAUSED" text is displayed correctly
        elif self.event.is_set():
            pass
        else:
            self.button_stop.configure(text="Pause Timer")
            # update the label with the remaining time
            timer = datetime.timedelta(seconds=self.total_seconds)
            self.label_Time.configure(text="Time remaining: " + str(timer))
            # decrement the total seconds by one
            self.total_seconds -= 1
            # schedule this function to run again after one second using self.after()
            self.after(1000, self.countdown)
        
    # Timer reset function
    def reset_countdown(self):
        self.total_seconds = 0

app = App()
app.mainloop()