#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install SpeechRecognition


# In[2]:


pip install pyttsx3


# In[3]:


pip install transformers


# In[4]:


pip install torch


# In[5]:


pip install pyaudio


# In[6]:


pip install keras


# In[7]:


pip install --upgrade transformers tensorflow keras


# In[8]:


pip install torch transformers


# In[9]:


pip install opencv-python


# In[10]:


import speech_recognition as sr
import pyttsx3
from transformers import pipeline
import tkinter as tk
from tkinter import messagebox
import threading
import cv2
from PIL import Image, ImageTk

# Initialize the speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# Load the language model (using PyTorch backend)
chatbot = pipeline('text-generation', model='gpt2', framework='pt')

# Initialize OpenCV for webcam
cap = cv2.VideoCapture(0)

def update_frame():
    global cap
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to Image
            img = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(image=img)
            # Update the image in the label
            video_label.imgtk = img
            video_label.configure(image=img)
    video_label.after(10, update_frame)  # Update every 10ms

def speech_to_speech():
    global running
    print("Starting the speech-to-speech interaction. Say 'exit' to quit.")
    
    while running:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

            try:
                # Recognize speech using Google Speech Recognition
                user_input = recognizer.recognize_google(audio)
                print(f"You said: {user_input}")

                if user_input.lower() == 'exit':
                    print("Exiting...")
                    break

                # Update the query text widget
                query_text_widget.delete(1.0, tk.END)
                query_text_widget.insert(tk.END, user_input)

                # Generate a response using the LLM
                response = chatbot(user_input, max_length=50, temperature=0.5, top_k=30)[0]['generated_text']
                print(f"Bot response: {response}")

                # Update the response text widget
                response_text_widget.delete(1.0, tk.END)
                response_text_widget.insert(tk.END, response)

                # Convert the response back to speech
                tts_engine.say(response)
                tts_engine.runAndWait()

            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                # Handle errors gracefully
                response_text_widget.delete(1.0, tk.END)
                response_text_widget.insert(tk.END, "Sorry, I could not understand the audio.")
            except sr.RequestError:
                print("Sorry, my speech service is down.")
                # Handle errors gracefully
                response_text_widget.delete(1.0, tk.END)
                response_text_widget.insert(tk.END, "Sorry, my speech service is down.")

def start_interaction():
    global running
    running = True
    threading.Thread(target=speech_to_speech, daemon=True).start()
    status_label.config(text="Status: Listening")

def stop_interaction():
    global running
    running = False
    status_label.config(text="Status: Stopped")

def close_application():
    global cap
    cap.release()  # Release the webcam
    root.destroy()

# Create the GUI
root = tk.Tk()
root.title("Speech-to-Speech Interface")

# Start button
start_button = tk.Button(root, text="Start", command=start_interaction)
start_button.pack(pady=10)

# Stop button
stop_button = tk.Button(root, text="Stop", command=stop_interaction)
stop_button.pack(pady=10)

# Status label
status_label = tk.Label(root, text="Status: Idle")
status_label.pack(pady=10)

# Query text widget
query_label = tk.Label(root, text="User Query:")
query_label.pack(pady=5)
query_text_widget = tk.Text(root, height=5, width=50)
query_text_widget.pack(pady=5)

# Response text widget
response_label = tk.Label(root, text="Bot Response:")
response_label.pack(pady=5)
response_text_widget = tk.Text(root, height=5, width=50)
response_text_widget.pack(pady=5)

# Webcam video label
video_label = tk.Label(root)
video_label.pack(pady=10)

# Start the video capture
update_frame()

# Bind the close event
root.protocol("WM_DELETE_WINDOW", close_application)

# Run the GUI main loop
root.mainloop()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




