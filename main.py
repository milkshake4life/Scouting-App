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
    current_auto_grid_percentage = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    current_teleop_grid_percentage = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]


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
        screen_manager.add_widget(Builder.load_file("teleopData.kv"))

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
                    self.root.get_screen('autoData').ids.data_team.text = "Team " + team_number_text
                    self.root.get_screen('teleopData').ids.data_team.text = "Team " + team_number_text
                    global team_data
                    team_data = team_number_text
                    self.root.get_screen('s1i').ids.teamNumber.text = ""
                    self.root.get_screen('s1i').ids.status_label.text = ""
                    break
    
        if not is_verified:
            self.root.get_screen('s1i').ids.status_label.text = ""
            self.root.get_screen('s1i').ids.status_label.text = "Team number not found in database"
            return is_verified
        else:
            return is_verified

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
           self.root.get_screen('auto').ids.wire.icon = "square-rounded-outline"
        elif(self.root.get_screen('auto').ids.middle.icon == "checkbox-marked"):
            placement = "middle"
            self.root.get_screen('auto').ids.middle.icon = "square-rounded-outline"
        else:
            placement = "short"
            self.root.get_screen('auto').ids.short.icon = "square-rounded-outline"
        taxi = "false"
        balanced = "false"
        docked = "false"

        if((self.root.get_screen('auto').ids.check1.icon == "checkbox-marked")):
            taxi = "true"
            self.root.get_screen('auto').ids.check1.icon = "square-rounded-outline"
        self.root.get_screen('auto').ids.check2.icon = "square-rounded-outline"
        if((self.root.get_screen('auto').ids.check3.icon == "checkbox-marked")):
            balanced = "true"
            self.root.get_screen('auto').ids.check3.icon = "square-rounded-outline"
        self.root.get_screen('auto').ids.check4.icon = "square-rounded-outline"
        if((self.root.get_screen('auto').ids.check5.icon == "checkbox-marked")):
            docked = "true"
            self.root.get_screen('auto').ids.check5.icon = "square-rounded-outline"
        self.root.get_screen('auto').ids.check6.icon = "square-rounded-outline"


        three = [0, 1, 2]

        for row in three:
            for cols in three:
                button = self.root.get_screen('auto').ids[grid].children[8-(row * 3 + cols)]
                if (button.icon != "square-rounded-outline"):
                    auto_grid[row][cols] = 1
                    button.icon = "square-rounded-outline"
        

        
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
            self.root.get_screen('teleop').ids.check1.icon = "square-rounded-outline"
        self.root.get_screen('teleop').ids.check2.icon = "square-rounded-outline"
        if((self.root.get_screen('teleop').ids.check3.icon == "checkbox-marked")):
            balance = "true"
            self.root.get_screen('teleop').ids.check3.icon = "square-rounded-outline"
        self.root.get_screen('teleop').ids.check4.icon = "square-rounded-outline"
        if((self.root.get_screen('teleop').ids.check5.icon == "checkbox-marked")):
            docked = "true"
            self.root.get_screen('teleop').ids.check5.icon = "square-rounded-outline"
        self.root.get_screen('teleop').ids.check6.icon = "square-rounded-outline"

        #fix this
        three = [0, 1, 2]

        for row in three:
            for cols in three:
                leftButton = self.root.get_screen('teleop').ids[left_grid].children[8-(row * 3 + cols)]
                if (leftButton.icon != "square-rounded-outline"):
                    teleop_grid[row][cols] = 1
                    leftButton.icon = "square-rounded-outline"
                middleButton = self.root.get_screen('teleop').ids[middle_grid].children[8-(row * 3 + cols)]
                if (middleButton.icon != "square-rounded-outline"):
                    teleop_grid[row][cols + 3] = 1
                    middleButton.icon = "square-rounded-outline"
                rightButton = self.root.get_screen('teleop').ids[right_grid].children[8-(row * 3 + cols)]
                if (rightButton.icon != "square-rounded-outline"):
                    teleop_grid[row][cols + 6] = 1
                    rightButton.icon = "square-rounded-outline"
        

        
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
        results = firebase.get('https://scouting-app-68229-default-rtdb.firebaseio.com/tidal_tumble/' + team_data, '')

        balanced_true_count = 0
        total_count = 0

        for item in results:
            if item and "auto" in item:
                auto_data = item["auto"]
                for entry in auto_data.values():
                    if entry.get("balanced") == "true":
                        balanced_true_count += 1
                    total_count += 1

        if total_count == 0:
            return 0  # Avoid division by zero

        percentage = round((balanced_true_count / total_count) * 100)
        self.root.get_screen('autoData').ids.balanced_percentage.text = str(percentage)
        return round(percentage, 2)
    
    def get_auto_docked_percentage(self):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)
        results = firebase.get('https://scouting-app-68229-default-rtdb.firebaseio.com/tidal_tumble/' + team_data, '')

        docked_true_count = 0
        total_count = 0

        for item in results:
            if item and "auto" in item:
                auto_data = item["auto"]
                for entry in auto_data.values():
                    if entry.get("docked") == "true":
                        docked_true_count += 1
                    total_count += 1

        if total_count == 0:
            return 0  # Avoid division by zero

        percentage = round((docked_true_count / total_count) * 100)
        self.root.get_screen('autoData').ids.docked_percentage.text = str(percentage)
        return round(percentage, 2)

    def get_auto_taxi_percentage(self):
            from firebase import firebase
            firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)
            results = firebase.get('https://scouting-app-68229-default-rtdb.firebaseio.com/tidal_tumble/' + team_data, '')

            taxi_true_count = 0
            total_count = 0

            for item in results:
                if item and "auto" in item:
                    auto_data = item["auto"]
                    for entry in auto_data.values():
                        if entry.get("taxi") == "true":
                            taxi_true_count += 1
                        total_count += 1

            if total_count == 0:
                return 0  # Avoid division by zero

            percentage = round((taxi_true_count / total_count) * 100)
            self.root.get_screen('autoData').ids.taxi_percentage.text = str(percentage)
            return round(percentage, 2)
    
    def get_auto_grid_percentage(self):
        from firebase import firebase
        firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)      
        results = firebase.get('https://scouting-app-68229-default-rtdb.firebaseio.com/tidal_tumble/' + team_data, '')
        autoGridPercentage = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
        three = [0, 1, 2]
        total_count = 0

        for item in results: 
            if item and "auto" in item:
                auto_data = item["auto"]
                for item2 in auto_data.values():
                    if 'grid' in item2:
                        auto_grid_data = item2["grid"]
                        for x in three:
                            for y in three:
                                if auto_grid_data[x][y] == 1:
                                    autoGridPercentage[x][y] = autoGridPercentage[x][y] + 1
                                    total_count = total_count + 1

        
        if total_count == 0:
            pass
        else:    
            for x in three:
                for y in three:
                    autoGridPercentage[x][y] = autoGridPercentage[x][y] / total_count
        global current_auto_grid_percentage
        current_auto_grid_percentage = autoGridPercentage
        
    def all_auto_functions(self, getData):   
        if getData:
            from firebase import firebase
            firebase = firebase.FirebaseApplication('https://scouting-app-68229-default-rtdb.firebaseio.com/', None)
            results = firebase.get('https://scouting-app-68229-default-rtdb.firebaseio.com/tidal_tumble/' + team_data, '')

            balanced_true_count = 0
            docked_true_count = 0
            taxi_true_count = 0
            autoGridPercentage = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
            three = [0, 1, 2]
            total_count = 0

            #print(results)
            for item in results:
                #print(item)
                if item and "auto" in item:
                    auto_data = item["auto"]
                    for entry in auto_data.values():
                        if entry.get("docked") == "true":
                            docked_true_count += 1
                        if entry.get("balanced") == "true":
                            balanced_true_count += 1
                        if entry.get("taxi") == "true":
                            taxi_true_count += 1
                        if 'grid' in entry:
                            auto_grid_data = entry["grid"]
                            for x in three:
                                for y in three:
                                    if auto_grid_data[x][y] == 1:
                                        autoGridPercentage[x][y] = autoGridPercentage[x][y] + 1
                        total_count += 1

            balanced_percentage = round((balanced_true_count / total_count) * 100)
            self.root.get_screen('autoData').ids.balanced_percentage.text = str(balanced_percentage)
            docked_percentage = round((docked_true_count / total_count) * 100)
            self.root.get_screen('autoData').ids.docked_percentage.text = str(docked_percentage)
            taxi_percentage = round((taxi_true_count / total_count) * 100)
            self.root.get_screen('autoData').ids.taxi_percentage.text = str(taxi_percentage)
            
            if total_count == 0:
                pass
            else:    
                for x in three:
                    for y in three:
                        autoGridPercentage[x][y] = autoGridPercentage[x][y] / total_count
            
            global current_auto_grid_percentage
            current_auto_grid_percentage = autoGridPercentage

            self.update_auto_button_color('auto_grid_layout')
            self.all_teleop_functions(results)

    def update_auto_button_color(self, grid):
        three = [0, 1, 2]
        for row in three:
            for cols in three:
                # Calculate Opacity factor values for the gradient based on the percentage
                percentage = round(current_auto_grid_percentage[row][cols]*10)/10

                button = self.root.get_screen('autoData').ids[grid].children[8-(row * 3 + cols)]
                button.md_bg_color = (46/255, 143/255, 72/255, 1*percentage)

    def all_teleop_functions(self, data):
        results = data

        balanced_true_count = 0
        docked_true_count = 0
        taxi_true_count = 0
        teleopGridPercentage = [[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0]]
        three = [0, 1, 2]
        nine = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        total_count = 0

        #print(results)
        for item in results:
            #print(item)
            if item and "teleop" in item:
                teleop_data = item["teleop"]
                for entry in teleop_data.values():
                    if entry.get("docked") == "true":
                        docked_true_count += 1
                    if entry.get("balanced") == "true":
                        balanced_true_count += 1
                    if entry.get("taxi") == "true":
                        taxi_true_count += 1
                    if 'grid' in entry:
                        teleop_grid_data = entry["grid"]
                        for x in three:
                            for y in nine:
                                if teleop_grid_data[x][y] == 1:
                                    teleopGridPercentage[x][y] = teleopGridPercentage[x][y] + 1
                    total_count += 1

        balanced_percentage = round((balanced_true_count / total_count) * 100)
        self.root.get_screen('teleopData').ids.balanced_percentage.text = str(balanced_percentage)
        docked_percentage = round((docked_true_count / total_count) * 100)
        self.root.get_screen('teleopData').ids.docked_percentage.text = str(docked_percentage)
            
        if total_count == 0:
            pass
        else:    
            for x in three:
                for y in three:
                    teleopGridPercentage[x][y] = teleopGridPercentage[x][y] / total_count
            
        global current_teleop_grid_percentage
        current_teleop_grid_percentage = teleopGridPercentage
        self.update_teleop_button_color('teleop_grid_layout')
    
    def update_teleop_button_color(self, grid):
        three = [0, 1, 2]
        nine = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        for row in three:
            for cols in nine:
                # Calculate Opacity factor values for the gradient based on the percentage
                percentage = round(current_teleop_grid_percentage[row][cols]*10)/10

                button = self.root.get_screen('teleopData').ids[grid].children[26-(row * 9 + cols)]
                #print(26-(row*3 + cols))
                button.md_bg_color = (46/255, 143/255, 72/255, 1*percentage)
        
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