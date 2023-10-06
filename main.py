from kivy.core.text import LabelBase
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.spinner import MDSpinner
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
import requests


Window.size = (310, 580)

class MainApp(MDApp):
    team_number_text = ''
    qualification_match_text = ''
    team_data = ''

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
        screen_manager.add_widget(Builder.load_file("teleop.kv"))
        screen_manager.add_widget(Builder.load_file("submitted.kv"))
        screen_manager.add_widget(Builder.load_file("autoData.kv"))

        return screen_manager
    
        
    def sendQualificationMatch(self, team_number_input, qualification_match_input):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)

        global team_number_text
        global qualification_match_text
        team_number_text = team_number_input.text.strip()
        qualification_match_text = qualification_match_input.text.strip()

        if team_number_text and qualification_match_text:
            # Both inputs have non-empty values
            self.root.get_screen('s1s').ids.status_label.text = ""

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
        
    def verify_team_number(self, team_number_input):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)

        team_number_text = team_number_input.text
        is_verified = False

        result = firebase.get('https://scouting-app-68229-default-rtdb.firebaseio.com/tidal_tumble', '')
        if result is not None:
            for i in result.keys():
                if i == team_number_text:
                    self.root.get_screen('login').ids.status_label.text = ""
                    is_verified = True
                    self.root.transition.direction = "left"
                    self.root.current = "autoData"
                    self.root.get_screen('autoData').ids.data_team.text = team_number_text
                    global team_data
                    team_data = team_number_text
                    break
    
        if not is_verified:
            self.root.get_screen('s1i').ids.status_label.text = "Team number not found in database"

    def change_cone(self, page, square):


        if self.root.get_screen(page).ids[square].icon == "square-rounded-outline":
            self.root.get_screen(page).ids[square].icon = "cone"
        else:
            self.root.get_screen(page).ids[square].icon = "square-rounded-outline"
    
    def change_cube(self, page, square):


        if self.root.get_screen(page).ids[square].icon == "square-rounded-outline":
            self.root.get_screen(page).ids[square].icon = "cube-outline"
        else:
            self.root.get_screen(page).ids[square].icon = "square-rounded-outline"
    
    def change_bot(self, page, square):

        if self.root.get_screen(page).ids[square].icon == "square-rounded-outline":
            self.root.get_screen(page).ids[square].icon = "cube-outline"
        elif self.root.get_screen(page).ids[square].icon == "cube-outline":
            self.root.get_screen(page).ids[square].icon = "cone"
        else:
            self.root.get_screen(page).ids[square].icon = "square-rounded-outline"
    
    def change_two_check_mark(self, page, box1, box2):

        if (self.root.get_screen(page).ids[box1].icon == "square-rounded-outline")  and (self.root.get_screen('auto').ids[box2].icon == "square-rounded-outline"):
            self.root.get_screen(page).ids[box1].icon = "checkbox-marked"

        elif (self.root.get_screen(page).ids[box1].icon == "square-rounded-outline") and (self.root.get_screen('auto').ids[box2].icon == "checkbox-marked"):
            self.root.get_screen(page).ids[box1].icon = "checkbox-marked"
            self.root.get_screen(page).ids[box2].icon = "square-rounded-outline"
        
        elif (self.root.get_screen(page).ids[box1].icon == "checkbox-marked"):
            self.root.get_screen(page).ids[box1].icon = "square-rounded-outline"
    
    def change_three_check_mark(self, page, box1, box2, box3):

        if (self.root.get_screen(page).ids[box1].icon == "square-rounded-outline")  and (self.root.get_screen('auto').ids[box2].icon == "square-rounded-outline") and (self.root.get_screen('auto').ids[box3].icon == "square-rounded-outline"):
            self.root.get_screen(page).ids[box1].icon = "checkbox-marked"

        elif (self.root.get_screen(page).ids[box1].icon == "square-rounded-outline") and (self.root.get_screen('auto').ids[box2].icon == "checkbox-marked"):
            self.root.get_screen(page).ids[box1].icon = "checkbox-marked"
            self.root.get_screen(page).ids[box2].icon = "square-rounded-outline"
        
        elif (self.root.get_screen(page).ids[box1].icon == "square-rounded-outline") and (self.root.get_screen('auto').ids[box3].icon == "checkbox-marked"):
            self.root.get_screen(page).ids[box1].icon = "checkbox-marked"
            self.root.get_screen(page).ids[box3].icon = "square-rounded-outline"
        
        elif (self.root.get_screen(page).ids[box1].icon == "checkbox-marked"):
            self.root.get_screen(page).ids[box1].icon = "square-rounded-outline"

    def send_auto_info(self, grid):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)

        auto_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        if(self.root.get_screen('auto').ids.wire.icon == "checkbox-marked"):
           placement = "wire"
        elif(self.root.get_screen('auto').ids.middle.icon == "checkbox-marked"):
            placement = "middle"
        else:
            placement = "short"
        taxi = "false"
        balanced = "false"
        docked = "false"

        if((self.root.get_screen('auto').ids.check1.icon == "checkbox-marked")):
            taxi = "true"
        if((self.root.get_screen('auto').ids.check3.icon == "checkbox-marked")):
            balanced = "true"
        if((self.root.get_screen('auto').ids.check5.icon == "checkbox-marked")):
            docked = "true"


        three = [0, 1, 2]

        for row in three:
            for cols in three:
                button = self.root.get_screen('auto').ids[grid].children[8-(row * 3 + cols)]
                if (button.icon != "square-rounded-outline"):
                    auto_grid[row][cols] = 1
        

        
        data = {
            'grid': auto_grid,
            'auto placement': placement,
            'taxi': taxi,
            'balanced': balanced,
            'docked': docked
        }
        
        firebase.post('https://scouting-app-68229-default-rtdb.firebaseio.com/tidal_tumble/' + team_number_text + '/' + qualification_match_text + '/auto', data)
        
    def send_teleop_info(self, left_grid, middle_grid, right_grid):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)

        teleop_grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        defense = "false"
        balance = "false"
        docked = "false"

        if((self.root.get_screen('teleop').ids.check1.icon == "checkbox-marked")):
            defense = "true"
        if((self.root.get_screen('teleop').ids.check3.icon == "checkbox-marked")):
            balanced = "true"
        if((self.root.get_screen('teleop').ids.check5.icon == "checkbox-marked")):
            docked = "true"

        #fix this
        three = [0, 1, 2]

        for row in three:
            for cols in three:
                leftButton = self.root.get_screen('teleop').ids[left_grid].children[8-(row * 3 + cols)]
                if (leftButton.icon != "square-rounded-outline"):
                    teleop_grid[row][cols] = 1
                middleButton = self.root.get_screen('teleop').ids[middle_grid].children[8-(row * 3 + cols)]
                if (middleButton.icon != "square-rounded-outline"):
                    teleop_grid[row][cols + 3] = 1
                rightButton = self.root.get_screen('teleop').ids[right_grid].children[8-(row * 3 + cols)]
                if (rightButton.icon != "square-rounded-outline"):
                    teleop_grid[row][cols + 6] = 1
        

        
        data = {
            'grid': teleop_grid,
            'defense bot': defense,
            'balanced': balance,
            'docked': docked
        }
        
        firebase.post('https://scouting-app-68229-default-rtdb.firebaseio.com/tidal_tumble/' + team_number_text + '/' + qualification_match_text + '/teleop', data)

    def get_auto_balanced_percentage(self):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)


        yesCounter = 0
        total = 0
        result = firebase.get('https://scouting-app-68229-default-rtdb.firebaseio.com/tidal_tumble/' + team_data, '')

        if result is not None:
            for i in result.items():
                if i['auto']['balanced'] == 'true':
                    yesCounter = yesCounter + 1
                total = total + 1
        
        return (yesCounter / total)
    

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