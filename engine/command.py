import sqlite3
import pyttsx3
import speech_recognition as sr
import eel
import time
import datetime
import wikipedia
import webbrowser

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

#voice input and converting to text
def speak(text):
    text=str(text)
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate',120)
    eel.DisplayMessage(text)
    #print(voices)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():
    r =sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening.....')
        eel.DisplayMessage('Listening.....')
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source, timeout=20, phrase_time_limit=10)

    try:
        print('recognize')
        eel.DisplayMessage('recognize.....')
        query = r.recognize_google(audio,language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        # speak(query)

    except Exception as e:
        return ""
    
    return query.lower()


# text = takecommand()
# speak(text)


#wish user
def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your voice assistant. How can I help you today?")

#wish_user()

@eel.expose
def allCommands(message=1):

    try:
        if message == 1 : 
            query=takecommand()
            print(query)

        else:
            query = message
            
        eel.senderText(query)

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                speak(result)
            except:
                speak("Sorry, I couldn't find anything.")

        elif 'open youtube' in query:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")

        elif 'time now' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a nice day!")

        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)
        
        elif 'open google' in query:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com")

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                if "send message" in query:
                    message = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    message = 'call'
                else:
                    message = 'video call'
                    
                whatsApp(contact_no, query, message, name)

        else:
            print("statement in else")
            from engine.features import chatBot
            chatBot(query)
            speak("thank you")

    except Exception as e:
        print(e)
        print("error")
    eel.ShowHood()

# Add to command.py

def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS web_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sys_command (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL
        )
    """)
    con.commit()
    print("Database initialized")

# Call this when your application starts
#init_db()

@eel.expose
def add_website(name, url):
    try:
        url = validate_url(url)
        
        # Check if website already exists
        cursor.execute("SELECT 1 FROM web_commands WHERE url=?", (url,))
        if cursor.fetchone():
            print(f"Website already exists: {url}")
            return False
            
        # Rest of your add logic
        cursor.execute("INSERT INTO web_commands VALUES (null, ?, ?)", (name, url))
        con.commit()
        print(f"Added website: {name} - {url}")
        return True
    except Exception as e:
        print(f"Error adding website: {e}")
        return False

@eel.expose
def add_application(name, path):
    try:
        # Basic validation
        if not name or not path:
            print("Error: Name and path cannot be empty")
            return False
            
        # Check if path exists (optional)
        import os
        if not os.path.exists(path):
            print(f"Error: Path does not exist - {path}")
            return False
            
        cursor.execute("INSERT INTO sys_command VALUES (null, ?, ?)", (name, path))
        con.commit()
        print(f"Added application: {name} - {path}")  # Debug print
        return True
    except Exception as e:
        print(f"Error adding application: {e}")
        return False

def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def validate_path(path):
    # Add any path validation logic here
    return path.strip()

@eel.expose
def delete_website(id):
    try:
        # Validate ID is numeric
        if not str(id).isdigit():
            print(f"Error: Invalid website ID - {id}")
            return False
            
        cursor.execute("DELETE FROM web_commands WHERE id=?", (id,))
        con.commit()
        print(f"Deleted website with ID: {id}")  # Debug print
        return True
    except Exception as e:
        print(f"Error deleting website: {e}")
        return False

@eel.expose
def delete_application(id):
    try:
        # Validate ID is numeric
        if not str(id).isdigit():
            print(f"Error: Invalid application ID - {id}")
            return False
            
        cursor.execute("DELETE FROM sys_command WHERE id=?", (id,))
        con.commit()
        print(f"Deleted application with ID: {id}")  # Debug print
        return True
    except Exception as e:
        print(f"Error deleting application: {e}")
        return False

@eel.expose
def get_websites():
    try:
        cursor.execute("SELECT * FROM web_commands ORDER BY name")
        websites = cursor.fetchall()
        print(f"Retrieved {len(websites)} websites")  # Debug print
        return websites
    except Exception as e:
        print(f"Error getting websites: {e}")
        return []

@eel.expose
def get_applications():
    try:
        cursor.execute("SELECT * FROM sys_command ORDER BY name")
        apps = cursor.fetchall()
        print(f"Retrieved {len(apps)} applications")  # Debug print
        return apps
    except Exception as e:
        print(f"Error getting applications: {e}")
        return []