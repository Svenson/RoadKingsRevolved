#
# Trade miles
# Display menu for player to trade miles for awards
#

__author__="Pieter"
__date__ ="$17 juli 2013 20:36:37 PM$"


import procgame
from procgame import *


# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Trademiles(game.Mode):

        def __init__(self, game, priority):
            super(Trademiles, self).__init__(game, priority)

            #register animation layers
            #self.miles_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'mt_miles_trade.dmd').frames[0])
            anim = dmd.Animation().load(dmd_path+'mt_miles_trade.dmd')
            self.miles_bgnd = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=40)
            self.text_layer_miles = dmd.TextLayer(13, 9, self.game.fonts['num_09Bx7'], "center", opaque=False)
            self.text_layer_1 = dmd.TextLayer(28, 2, self.game.fonts['tiny7'], "left", opaque=False)
            self.text_layer_2 = dmd.TextLayer(28, 10, self.game.fonts['tiny7'], "left", opaque=False)
            self.text_layer_3 = dmd.TextLayer(28, 18, self.game.fonts['tiny7'], "left", opaque=False)
            self.trademiles_layer = dmd.GroupedLayer(128, 32, [self.miles_bgnd, self.text_layer_miles, self.text_layer_1, self.text_layer_2, self.text_layer_3])
            self.trademiles_layer.transition = dmd.PushTransition(direction='west')

            self.choice_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'bonus_bgnd.dmd').frames[0])
            self.choice_layer_1 = dmd.TextLayer(128/2, 6, self.game.fonts['tiny7'], "center", opaque=False) #tiny7
            self.choice_layer_2 = dmd.TextLayer(128/2, 10, self.game.fonts['07x5'], "center", opaque=False)
            self.choice_layer_3 = dmd.TextLayer(128/2, 13, self.game.fonts['tiny7'], "center", opaque=False) #tiny7
            self.choice_layer_4 = dmd.TextLayer(128/2, 17, self.game.fonts['07x5'], "center", opaque=False)
            self.choice_layer_5 = dmd.TextLayer(128/2, 20, self.game.fonts['tiny7'], "center", opaque=False) #tiny7

            #register lampshow
            self.game.lampctrl.register_show('select_show', lampshow_path+"rampenter.lampshow")

            self.miles_list = [5,10,15,20,25,30,35] #[4,8,12,16,20,24,28]
            #self.item_list =[['500.000','Light Kickback','Raise spinner value'],['1 Million','Add 3X Bonus','Award Skillshot'],['1,5 Million','Collect right combo','Collect left combo'],
            #     OLD         ['2 Million','X-ramp 250k','Collect ramp combo'],['2,5 Million','Add 10X Bonus','Jumpramp 1 million'],['3 Million','2X playfield 60sec.','Complete mode']]
            self.item_list =[['200.000','Update Kickback','Raise Spinner Value'],['500.000','Spinner Miles Feature','Collect Right Combo'],['1 Million','Award Skillshot','Collect Left Combo'],
                             ['1,75 Million','X-ramp 250k','Collect Ramp Combo'],['3 Million','Add 10X Bonus','Jumpramp Million Plus'],['5X Playfield 20sec','2X Playfield 60sec.','Complete Multiball'],
                             ['Complete Race Champion','Complete Kickstart King','Complete Easy Rider']] #Complete Unfinished Modes Finish All Modes
            # 500k; 1; 1,75; 2,75;  4; 5,5    500, 750, 1m, 1,25m, 1,5m  200k; 500k; 1m; 1,75m; 3m; 4,5m
            self.item_choice = ''
            self.miles_index = 0
            self.item_index = 0
            self.status = False

        def mode_started(self):
             print("Debug, Trademiles Mode Started")
             self.status = 'ask_player'
             self.miles_collected = self.game.get_player_stats('miles_collected')
             # determine max lenght of list
             self.index_max = len(self.miles_list) - 1
             self.ask_player()

        def mode_stopped(self):
             self.game.effects.gi_on()
             print("Debug, Trademiles Mode Ended")

## lamps and animations

        def update_lamps(self):
             pass


        def explain_player(self):
             self.ask_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'bonus_bgnd.dmd').frames[0])
             self.choice_layer_1.set_text("Right flipper = Next page")
             self.choice_layer_3.set_text("Left flipper = Select award")
             self.choice_layer_5.set_text("Start button = Confirm")
             self.layer = dmd.GroupedLayer(128, 32, [self.ask_bgnd, self.choice_layer_1, self.choice_layer_3, self.choice_layer_5])

        def ask_player(self):
             self.ask_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'mt_ask_player.dmd').frames[0])
             self.choice_layer_1.set_text("You have "+str(self.miles_collected)+" miles")
             self.choice_layer_3.set_text("Do you want to trade")
             self.choice_layer_5.set_text("for award?")
             self.layer = dmd.GroupedLayer(128, 32, [self.ask_bgnd, self.choice_layer_1, self.choice_layer_3, self.choice_layer_5])

        def no_miles(self):
             self.nomiles_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'mt_nomiles.dmd').frames[0])
             self.choice_layer_2.set_text("Not enough miles...")
             self.choice_layer_4.set_text("You have "+str(self.miles_collected)+" miles")
             self.layer = dmd.GroupedLayer(128, 32, [self.nomiles_bgnd, self.choice_layer_2, self.choice_layer_4])
             self.delay(name='no_miles', event_type=None, delay=3, handler=self.update_mileslist)

        def display_choice(self):
             self.choice_layer_2.set_text("You traded "+str(self.miles_list[self.miles_index])+" miles for")
             self.choice_layer_4.set_text(str(self.item_choice),blink_frames=16)
             self.layer = dmd.GroupedLayer(128, 32, [self.choice_bgnd, self.choice_layer_2, self.choice_layer_4])

        def animate_layer(self):
             # get new data first
             self.get_mileslist(self.miles_index)
             # animate script
             script = list()
             script.append({'seconds':20.0, 'layer':self.trademiles_layer})
             self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)

        def clear_layer(self):
             self.layer = None

## mode functions

        def player_yes(self):
             self.explain_player()
             self.delay(name='explain_player', event_type=None, delay=10, handler=self.update_mileslist)
             self.status = 'trade_miles'
             #self.update_mileslist()
             #change music
             self.game.sound.fadeout_music(time_ms=200)
             self.game.sound.play_music(self.game.assets.music_tmBackground, loops=-1)

        def player_no(self):
             self.clear_layer()
             self.game.effects.eject_ball('Leject')
             self.game.modes.remove(self)

        def end_trading(self):
             self.game.base_game_mode.generalplay.update_miles_lamps()
             self.clear_layer()
             self.game.assets.rk_play_music()
             self.game.effects.eject_ball('Leject')
             self.game.modes.remove(self)

        def check_miles(self):
             self.status = 'select' # prevent multiple hits on startbutton
             if self.miles_collected < self.miles_list[self.miles_index]:
                 self.game.sound.play(self.game.assets.sfx_noMiles)
                 self.no_miles()
             else:
                 self.select_item()

        def select_item(self):
             self.game.sound.play(self.game.assets.sfx_selectItem)
             self.game.effects.gi_off()
             self.game.coils.rearFlash_upLeftkicker.schedule(schedule=0xaaaaaaaa, cycle_seconds=1, now=True)
             self.item_choice = self.item_list[self.miles_index][self.item_index]
             self.display_choice()
             self.game.subtract_player_stats('miles_collected',self.miles_list[self.miles_index])
             self.award_choice()
             self.delay(name='end_trading', event_type=None, delay=3, handler=self.end_trading)

        def award_choice(self):
           # assignment off the awards
            # 5 miles
            if self.item_choice == self.item_list[0][0]:
                print("award: 200k")
                self.game.score(200000)
            elif self.item_choice == self.item_list[0][1]:
                print("award: Update Kickback")
                self.game.base_game_mode.kickback.raise_kickback()
            elif self.item_choice == self.item_list[0][2]:
                print("award: Raise spinner value")
                self.game.base_game_mode.generalplay.raise_spinner_value()
            # 10 miles
            elif self.item_choice == self.item_list[1][0]:
                print("award: 500k")
                self.game.score(500000)
            elif self.item_choice == self.item_list[1][1]:
                print("award: Spinner miles")
                self.game.base_game_mode.generalplay.set_spinner_miles()
            elif self.item_choice == self.item_list[1][2]:
                print("award: Collect right combo")
                self.game.base_game_mode.combo.set_combo(id=2)
            # 15 miles
            elif self.item_choice== self.item_list[2][0]:
                print("award: 1 Million")
                self.game.score(1000000)
            elif self.item_choice== self.item_list[2][1]:
                print("award: Award Skillshot")
                self.game.score(500000)
                self.game.base_game_mode.missions_modes.update_missions(1)
            elif self.item_choice== self.item_list[2][2]:
                print("award: Collect left combo")
                self.game.base_game_mode.combo.set_combo(id=0)
            # 20 miles
            elif self.item_choice== self.item_list[3][0]:
                print("award: 1.75 Million")
                self.game.score(1750000)
            elif self.item_choice== self.item_list[3][1]:
                print("award: X-ramp = 250k")
                self.game.base_game_mode.crossramp.set_crossramp_values(value=250000)
            elif self.item_choice== self.item_list[3][2]:
                print("award: Collect ramp combo")
                self.game.base_game_mode.combo.set_combo(id=1)
             # 25 miles
            elif self.item_choice== self.item_list[4][0]:
                print("award: 3 Million")
                self.game.score(3000000)
            elif self.item_choice== self.item_list[4][1]:
                print("award: Bonus +10X")
                self.game.add_player_stats('bonus_x',10)
            elif self.item_choice== self.item_list[4][2]:
                print("award: Jumpramp million Plus")
                self.game.base_game_mode.generalplay.set_millionplus()
            # 30 miles
            elif self.item_choice== self.item_list[5][0]:
                print("award: 5x playfield 20sec")
                self.game.set_pf_multiplier(value=5, time=23)
            elif self.item_choice== self.item_list[5][1]:
                print("award: 2X playfield 60sec.")
                self.game.set_pf_multiplier(value=2, time=63)
            elif self.item_choice== self.item_list[5][2]:
                self.game.base_game_mode.missions_modes.update_modes_completed(3)
                print("award: Complete Multiball")
            # 35 miles
            elif self.item_choice== self.item_list[6][0]:
                print("award: Complete Race Champion")
                self.game.base_game_mode.missions_modes.update_modes_completed(1)
            elif self.item_choice== self.item_list[6][1]:
                print("award: Complete Kickstart King")
                self.game.base_game_mode.missions_modes.update_modes_completed(2)
            elif self.item_choice== self.item_list[6][2]:
                self.game.base_game_mode.missions_modes.update_modes_completed(4)
                print("award: Complete Easy Rider")
            else:
                print("award not in list")
                self.game.score(1)

        def next_item(self):
             if self.item_index == 2:
                 self.item_index = 0
             else:
                 self.item_index += 1
             self.update_itemlist()

        def update_itemlist(self):
             self.game.sound.play(self.game.assets.sfx_moveItem)
             if self.item_index == 0:
                 self.text_layer_1.set_text(self.item_list[self.miles_index][0],blink_frames=8)
                 self.text_layer_2.set_text(self.item_list[self.miles_index][1],None)
                 self.text_layer_3.set_text(self.item_list[self.miles_index][2],None)

             if self.item_index == 1:
                 self.text_layer_1.set_text(self.item_list[self.miles_index][0],None)
                 self.text_layer_2.set_text(self.item_list[self.miles_index][1],blink_frames=8)
                 self.text_layer_3.set_text(self.item_list[self.miles_index][2],None)

             if self.item_index == 2:
                 self.text_layer_1.set_text(self.item_list[self.miles_index][0],None)
                 self.text_layer_2.set_text(self.item_list[self.miles_index][1],None)
                 self.text_layer_3.set_text(self.item_list[self.miles_index][2],blink_frames=8)
             self.layer = dmd.GroupedLayer(128, 32, [self.miles_bgnd, self.text_layer_miles, self.text_layer_1, self.text_layer_2, self.text_layer_3])

        def next_mileslist(self):
             if self.miles_index == self.index_max:
                 self.miles_index = 0
             else:
                 self.miles_index += 1
             # reset item_index for next mileslist
             self.item_index = 0
             self.update_mileslist()

        def get_mileslist(self,i):
             self.text_layer_miles.set_text(str(self.miles_list[i]))
             #if self.miles_collected < self.miles_list[self.miles_index]:
             #    self.text_layer_1.set_text(self.item_list[i][0],blink_frames=None)
             #else:
             self.text_layer_1.set_text(self.item_list[i][0],blink_frames=8)
             self.text_layer_2.set_text(self.item_list[i][1],blink_frames=None)
             self.text_layer_3.set_text(self.item_list[i][2],blink_frames=None)

        def update_mileslist(self):
             self.status = 'trade_miles' # reset status for active startbutton
             self.game.sound.play(self.game.assets.sfx_moveMiles)
             # Delay to synchronise with sound
             self.delay(name='animate_layer', event_type=None, delay=0.4, handler=self.animate_layer)
             #self.get_mileslist(self.miles_index)
             #self.animate_layer()

## Switches

        def sw_flipperLwL_active(self,sw):
             if self.status == 'trade_miles':
                 #self.next_mileslist();
                 self.next_item();
             elif self.status == 'ask_player':
                 self.player_no()
             return True

        def sw_flipperLwR_active(self,sw):
             if self.status == 'trade_miles':
                 #self.next_item();
                 self.next_mileslist();
             elif self.status == 'ask_player':
                 self.player_yes()
             return True

        def sw_startButton_active(self, sw):
             if not self.status == 'select': # prevent multiple hits on startbutton
                 self.check_miles()
             return True

