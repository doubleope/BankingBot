import streamlit as st
import json

if "page" not in st.session_state: 
    st.session_state["page"]="login"

login_info = json.loads(open("login_info.json").read())

def get_user(username, login_info): 
    for user in login_info["users"]: 
        if user["username"]==username: 
            return user
    return None

## login page
if st.session_state["page"]=="login": 
    st.title("Banking Bot Login")
    username_ti = st.text_input("username")
    password_ti = st.text_input("password", type="password")
    if st.button("Log In"): 
        user = get_user(username_ti, login_info)
        if not user: 
            st.write("User not registered")
        elif password_ti != user["password"]: 
            st.write("Incorrect password")
        else: 
            st.session_state["page"] = "bot"
            st.rerun()


##interaction with bot
elif st.session_state["page"]=="bot": 
    ## button to return to login (not sure where to put this)
    if st.button("Return to Log In"): 
        st.session_state["page"]="login"
        st.session_state["chat_history"]=[]
        st.rerun()
    
    st.title("Banking Bot")

    ## class for each utterance of the interaction of the user and the bot. 
    class Utterance(): 
        def __init__(self, speaker="user", text=""): 
            self.speaker = speaker
            self.text = text
        
        def to_string(self): 
            return self.speaker + ": " + self.text

    ## dummy function to get a response from the model
    def get_bot_text(utt): 
        return "I am a robot"

    ##get saved chat history from the session state. 
    if "chat_history" not in st.session_state: 
        st.session_state["chat_history"]=[]

    ##write the chat history
    for utt in st.session_state.chat_history: 
        st.write(utt.to_string())

    ## prompt user
    prompt = st.chat_input("Say something")
    if prompt:
        ##recieve user response
        user_utt = Utterance(speaker = "User", text=prompt)
        ## add user's input to the chat history
        st.session_state.chat_history.append(user_utt)
        ## write user's response to current window
        st.write(user_utt.to_string())

        ## create a bot response to the user. 
        response = get_bot_text(prompt)
        bot_utt = Utterance(speaker = "Bot", text=response)
        st.session_state.chat_history.append(bot_utt)
        ## write bot response to the current window
        st.write(bot_utt.to_string())