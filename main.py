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
        screen_manager.add_widget(Builder.load_file("auto.kv"))
        screen_manager.add_widget(Builder.load_file("newAccount.kv"))
        

        return screen_manager
        
    def sendQualificationMatch(self, team_number_input, qualification_match_input):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)

        team_number_text = team_number_input.text.strip()
        team_qualification_text = qualification_match_input.text.strip()

        if team_number_text and team_qualification_text:
            # Both inputs have non-empty values
            self.root.get_screen('s1s').ids.status_label.text = ""

            # Send data to Firebase
            firebase.post('https://scouting-app-68229-default-rtdb.firebaseio.com/' + team_number_text, team_qualification_text)
            self.root.transition.direction = "left"
            self.root.current = "auto"

            team_number_input.text = ""
            qualification_match_input.text = ""
        else:
            # At least one input is empty
            self.root.get_screen('s1s').ids.status_label.text = "Empty Inputs"

    def sendTeamNumber(self, team_number_input):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)

        team_number_text = team_number_input.text

        data = {
            'team_number': team_number_text
        }

        firebase.post('https://scouting-app-68229-default-rtdb.firebaseio.com/', data)
        
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

    def change_cone(self, square):


        if self.root.get_screen('auto').ids[square].icon == "square-rounded-outline":
            self.root.get_screen('auto').ids[square].icon = "cone"
        else:
            self.root.get_screen('auto').ids[square].icon = "square-rounded-outline"
    
    def change_cube(self, square):


        if self.root.get_screen('auto').ids[square].icon == "square-rounded-outline":
            self.root.get_screen('auto').ids[square].icon = "cube-outline"
        else:
            self.root.get_screen('auto').ids[square].icon = "square-rounded-outline"
    
    def change_bot(self, square):

        if self.root.get_screen('auto').ids[square].icon == "square-rounded-outline":
            self.root.get_screen('auto').ids[square].icon = "cube-outline"
        elif self.root.get_screen('auto').ids[square].icon == "cube-outline":
            self.root.get_screen('auto').ids[square].icon = "cone"
        else:
            self.root.get_screen('auto').ids[square].icon = "square-rounded-outline"
    
    def change_check_mark(self, box1, box2):

        if (self.root.get_screen('auto').ids[box1].icon == "square-rounded-outline") and (self.root.get_screen('auto').ids[box2].icon == "square-rounded-outline"):
            self.root.get_screen('auto').ids[box1].icon = "checkbox-marked"

        elif (self.root.get_screen('auto').ids[box1].icon == "square-rounded-outline") and (self.root.get_screen('auto').ids[box2].icon == "checkbox-marked"):
            self.root.get_screen('auto').ids[box1].icon = "checkbox-marked"
            self.root.get_screen('auto').ids[box2].icon = "square-rounded-outline"
        
        elif (self.root.get_screen('auto').ids[box1].icon == "checkbox-marked"):
            self.root.get_screen('auto').ids[box1].icon = "square-rounded-outline"

    def send_auto_info(self, grid):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)

        auto_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        three = [0, 1, 2]

        for row in three:
            for cols in three:
                button = self.root.get_screen('auto').ids[grid].children[row * 3 + cols]
                if (button.icon != "square-rounded-outline"):
                    auto_grid[row][cols] = 1

        for row in three:
            for cols in three:
                print(auto_grid[row][cols])
        

if __name__ == "__main__":
    LabelBase.register(name="MPoppins", fn_regular="C:\\Users\\elee9\\Downloads\\Poppins\\Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins", fn_regular="C:\\Users\\elee9\\Downloads\\Poppins\\Poppins-SemiBold.ttf")


    app = MainApp()
    app.run()


    # Below is lines of code for main.kv, this is for the second regional.
    # 
    # Button:
    #         text: "San Diego"
    #         font_name: "BPoppins"
    #         size_hint: .66, .065
    #         pos_hint: {"center_x": .5, "center_y": .09}
    #         background_color: 0, 0, 0, 0
    #         color: rgba(0, 130, 190, 255)
    #         on_release:
    #             root.manager.transition.direction = "left"
    #             root.manager.current = "scout2"
    #         canvas.before:
    #             Color:
    #                 rgb: rgba(0, 130, 190, 255)
    #             Line:
    #                 width: 1.2
    #                 rounded_rectangle: self.x, self.y, self.width, self.height, 5, 5, 5, 5, 100