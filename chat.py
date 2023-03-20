from tkinter import *
import customtkinter
import openai
import os
import pickle

#TKInter variables
root = customtkinter.CTk()
root.title("ChatGPT Bot Test")
root.geometry("600x600")
root.iconbitmap("ai_lt.ico")

#Set colour scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

#Submit data on click
def speak():
	if chat_entry.get():
		#Define filename
		filename = "api_key"

		try:
			if os.path.isfile(filename):
				#open file
				input_file = open(filename, 'rb')

				#load data into var
				api_key = pickle.load(input_file)

				#Display "Sending Query" Message
				my_text.insert(END, "Sending query...\n\n")

				#Pass API key to ChatGPT
				openai.api_key = api_key

				#Create OpenAI instance
				openai.Model.list()

				#Define query/response
				response = openai.Completion.create(
					model = "text-davinci-003",
					prompt = chat_entry.get(),
					temperature = 0,
					max_tokens =60,
					top_p = 1.0,
					frequency_penalty=0.0,
					presence_penalty=0.0
					)
				
				my_text.insert(END, (response["choices"][0]["text"]).strip())
				my_text.insert(END, "\n\n")

			else:
				#Create file
				input_file = open(filename, 'wb')
				#Close file
				input_file.close()
				#Display error message
				my_text.insert(END, "\n\nPlease add an API key first\n\n")

		except Exception as e:
			my_text.insert(END, f"\n\n There was an error\n\n{e}\n\n")
	else:
		my_text.insert(END, "\n\nPlease insert a chat subject\n\n")

#Clear the screen
def clear():
	#Clear the main text box
	my_text.delete(1.0, END)
	#Clear the query entry widget
	chat_entry.delete(0,END)

#API Key Save/Update
def key():
	#Define filename
	filename = "api_key"

	try:
		if os.path.isfile(filename):
			#open file
			input_file = open(filename, 'rb')

			#load data into var
			api_key = pickle.load(input_file)

			#Get current key value to check whether the key is currently visible 
			api_entry_value = api_entry.get()

			#Avoid duplication of API Key in display
			if api_entry_value == api_key:
				pass
			else:
				#Output API Key to text box
				api_entry.insert(END, api_key)
		else:
			#Create file
			input_file = open(filename, 'wb')
			#Close file
			input_file.close()

	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}\n\n")

	#Resize window
	root.geometry("600x750")
	#Show API Key frame
	api_frame.pack(pady=30)

#Save API Key
def save_key():
	#Define filename
	filename = "api_key"

	try:
		#Open file
		output_file = open(filename, 'wb')

		#Add data to file
		pickle.dump(api_entry.get(), output_file)

		#Close API Key frame
		api_frame.pack_forget()
		#Resize window
		root.geometry("600x600")

		#Delete text from API entry box
		api_entry.delete(0, END)

	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")

#Create text frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

#Add text widget to get responses back from ChatGPT
my_text = Text(text_frame,
	bg="#343638",
	width=65,
	bd=1,
	fg="#d6d6d6",
	relief="flat",
	wrap=WORD,
	selectbackground="#1f538d")
my_text.grid(row=0,column=0)

#Create scrollbar to text widget
text_scroll = customtkinter.CTkScrollbar(text_frame,
	command=my_text.yview)
text_scroll.grid(row=0,column=1, sticky="ns")

#Add scrollbar to text box
my_text.configure(yscrollcommand=text_scroll.set)

#Entry widget to send data to Chat GPT
chat_entry = customtkinter.CTkEntry(root,
	placeholder_text = "Enter a subject to talk about...",
	width=535,
	height=50,
	border_width=1)
chat_entry.pack(pady=10)

#Add button frame
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

#Add submit button
submit_button = customtkinter.CTkButton(button_frame,
	text="Send",
	command=speak)
submit_button.grid(row=0,column=0, padx=25)

#Add clear button
clear_button = customtkinter.CTkButton(button_frame,
	text="Clear Screen",
	command=clear)
clear_button.grid(row=0,column=1, padx=35)

#Add API Key button
api_button = customtkinter.CTkButton(button_frame,
	text="Update API Key",
	command=key)
api_button.grid(row=0,column=2, padx=25)

#Add API Key Frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

#Add API Key Entry Widget
api_entry = customtkinter.CTkEntry(api_frame,
	placeholder_text="Enter API Key",
	width=350,height=50,border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

#Add API key save button
api_save_button = customtkinter.CTkButton(api_frame,
	text="Save Key",
	command=save_key)
api_save_button.grid(row=0, column=1, padx=10)

root.mainloop()
