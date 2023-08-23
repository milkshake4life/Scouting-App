from kivy.core.text import LabelBase
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivy.metrics import dp
import requests


Window.size = (310, 580)

class MainApp(MDApp):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(Builder.load_file("main.kv"))
        screen_manager.add_widget(Builder.load_file("login.kv"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        screen_manager.add_widget(Builder.load_file("regional.kv"))
        screen_manager.add_widget(Builder.load_file("scout1.kv"))
        screen_manager.add_widget(Builder.load_file("scout2.kv"))
        screen_manager.add_widget(Builder.load_file("s1s.kv"))
        screen_manager.add_widget(Builder.load_file("s1i.kv"))
        screen_manager.add_widget(Builder.load_file("s2s.kv"))
        screen_manager.add_widget(Builder.load_file("s2i.kv"))
        screen_manager.add_widget(Builder.load_file("newAccount.kv"))
        

        return screen_manager

    # def get_qualification_matches(event_key):
    # # Make a request to the Blue Alliance API to fetch the qualification matches for the given event
    #     url = f"https://www.thebluealliance.com/api/v3/event/{event_key}/matches/simple"
    #     headers = {"X-TBA-Auth-Key": api_key}  
    #     response = requests.get(url, headers=headers)

    #     if response.status_code == 200:
    #         matches = response.json()
    #         qualification_matches = {}

    #         # Iterate over the matches and populate the qualification_matches dictionary
    #         for match in matches:
    #             if match["comp_level"] == "qm":
    #                 match_number = match["match_number"]
    #                 team_keys = match["alliances"]["red"]["team_keys"] + match["alliances"]["blue"]["team_keys"]
    #                 team_numbers = [int(team_key[3:]) for team_key in team_keys]
    #                 qualification_matches[match_number] = team_numbers

    #         return qualification_matches
    #     else:
    #         raise Exception("Failed to fetch qualification matches from Blue Alliance API")

    def print_teams_in_match(match_number, qualification_matches):
        if match_number in qualification_matches:
            teams = qualification_matches[match_number]
            for team in teams:
                print(f"Team {team}")
        else:
            print("Invalid match number!")
        
    def sendData(self, team_number_input, password_input):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)

        team_number_text = team_number_input.text
        password_text = password_input.text

        data = {
            'team_number': team_number_text,
            'password': password_text
        }

        firebase.post('https://scouting-app-68229-default-rtdb.firebaseio.com/Users', data)
        
    def verifyData(self, team_number_input, password_input):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)

        team_number_text = team_number_input.text
        password_text = password_input.text

        is_verified = False

        result = firebase.get('https://scouting-app-68229-default-rtdb.firebaseio.com/Users', '')

        for i in result.keys():
            if result[i]['team_number'] == team_number_text:
                if result[i]['password'] == password_text:
                    self.root.get_screen('login').ids.status_label.text = ""
                    is_verified = True
                    self.root.transition.direction = "left"
                    self.root.current = "regional"
                    break
    
        if not is_verified:
            self.root.get_screen('login').ids.status_label.text = "Incorrect team number or password"

if __name__ == "__main__":
    LabelBase.register(name="MPoppins", fn_regular="C:\\Users\\elee9\\Downloads\\Poppins\\Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="C:\\Users\\elee9\\Downloads\\Poppins\\Poppins-SemiBold.ttf")


    app = MainApp()
    app.run()