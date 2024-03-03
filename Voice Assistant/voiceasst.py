import tkinter as tk
from tkinter import messagebox, PhotoImage, scrolledtext
import threading, sys, io, pyttsx3, datetime, webbrowser, smtplib, requests
import speech_recognition as sr

class VoiceAssistantApp:
    def __init__(self, master):
        self.master = master
        master.title("Voice Assistant")

        # Set a larger window size
        window_width = 740 
        window_height = 462 
        master.geometry(f"{window_width}x{window_height}")
        master.resizable(False, False)
        
        # Load background image
        try:
            self.background_image = PhotoImage(file="bgimage.png")
        except tk.TclError as e:
            messagebox.showerror("Error", f"Couldn't recognize data in image file: {e}")

        # Set up a label to display the background image
        background_label = tk.Label(master, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Set a label on top of the canvas for the title
        self.label = tk.Label(master, text="Voice Assistant", font=("Helvetica", 24), bg="black", fg="white")
        self.label.place(relx=0.5, rely=0.1, anchor="center")

        # Create a scrolled text widget for the output
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=20, bg="lightblue")
        self.output_text.place(relx=0.5, rely=0.5, anchor="center")

        # Create a button to start the assistant
        self.button = tk.Button(master, text="Start Assistant", bg="goldenrod1" ,command=self.start_assistant)
        self.button.place(relx=0.5, rely=0.9, anchor="center")

        self.assistant_thread = None

    def start_assistant(self):
        self.button['state'] = 'disabled'  # Disable button during assistant execution
        sys.stdout = io.StringIO()  # Redirect standard output to capture print statements
        sys.stderr = io.StringIO()  # Redirect standard error to capture error messages

        self.assistant_thread = threading.Thread(target=self.run_assistant)
        self.assistant_thread.start()

    def run_assistant(self):
        speak("Hello! How can I help you today?")
        self.update_output("Hello! How can I help you today?")

        while True:
            query = recognize_speech()

            if "hello" in query:
                speak("Hello there!")
                self.update_output("Hello there!")

            elif "time" in query:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The current time is {current_time}")
                self.update_output(f"The current time is {current_time}")

            elif "date" in query:
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                speak(f"Today's date is {current_date}")
                self.update_output(f"Today's date is {current_date}")

            elif "search" in query:
                speak("What do you want to search for?")
                self.update_output("What do you want to search for?")
                search_query = recognize_speech()

                # Specify the chrome browser command
                chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe --new-window %s"

                # Form the search URL
                url = f"https://www.google.com/search?q={search_query}"

                # Open the URL in a new Chrome window
                webbrowser.get(chrome_path).open(url)

                speak(f"Here are the search results for {search_query}")
                self.update_output(f"Here are the search results for {search_query}")

            elif "send email" in query:
                speak("To whom do you want to send the email?")
                self.update_output("To whom do you want to send the email?")
                recipient = recognize_speech()
                recipient_email = " ".join(recipient.split())
                speak("What should be the subject of the email?")
                self.update_output("What should be the subject of the email?")
                email_subject = recognize_speech()
                speak("What should be the body of the email?")
                self.update_output("What should be the body of the email?")
                email_body = recognize_speech()

                send_email(recipient_email, email_subject, email_body)
                self.update_output("Email sent successfully.")

            elif "weather" in query:
                speak("Which city's weather would you like to know?")
                self.update_output("Which city's weather would you like to know?")
                city = recognize_speech()
                get_weather(city)

            elif "exit" in query:
                speak("Goodbye!")
                self.update_output("Goodbye!")
                break

        # Get captured standard output
        output_text = sys.stdout.getvalue()  
        # Get captured standard error
        error_text = sys.stderr.getvalue()  

        # Reset standard output
        sys.stdout = sys.__stdout__  
        # Reset standard error
        sys.stderr = sys.__stderr__ 

        # Enable button after assistant execution
        self.button['state'] = 'normal'

    def update_output(self, text):
        self.output_text.insert(tk.END, text + '\n')
        # Scroll to the end
        self.output_text.see(tk.END)
        # Update the GUI immediately
        self.master.update_idletasks()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        # Print to GUI
        print_to_gui("Listening...")  
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            # Print to GUI
            print_to_gui("Recognizing...")  
            query = recognizer.recognize_google(audio)
            # Print to GUI
            print_to_gui(f"User: {query}")  
            return query.lower()

        except sr.UnknownValueError:
            # Print to GUI
            speak("Sorry, I couldn't understand. Can you repeat that?")
            print_to_gui("Sorry, I couldn't understand. Can you repeat that?")  
            return ""

def print_to_gui(message):
    # Function to print messages to the GUI
    app.update_output(message)

def print_to_gui(message):
    # Function to print messages to the GUI
    app.update_output(message)
    
def send_email(to, subject, body):
    # Email credentials
    email_address = "user1@gmail.com"
    email_password = "password1"

    # SMTP server details
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_address, email_password)

            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(email_address, to, message)

        speak("Email sent successfully.")
        print_to_gui("Email sent successfully.")

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the email.")
        print_to_gui("Sorry, I couldn't send the email.")

def get_weather(city):
    # Use a weather API to get current weather information
    api_key = '3d705e4b300169bfd78d4a6cb34b03eb'
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': api_key, 'units': 'metric'}

    try:
        response = requests.get(base_url, params=params)
        weather_data = response.json()

        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']

        speak(f"The current temperature in {city} is {temperature} degrees Celsius with {description}.")
        print_to_gui(f"The current temperature in {city} is {temperature} degrees Celsius with {description}.")

    except Exception as e:
        print(e)
        speak("Sorry, I couldn't fetch the weather information.")
        print_to_gui("Sorry, I couldn't fetch the weather information.")

def main():
    root = tk.Tk()
    global app
    app = VoiceAssistantApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
