#
# Control for missions, main modes and wizard mode
#

__author__="Pieter"
__date__ ="$Okt 25, 2012 20:30:27 PM$"

import procgame
import random
from procgame import *

from easy_rider import *
from multiball import *
from kickstart_king import *
from race_champion import *
from roadkings_wizard import *

#all necessary paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"

class MissionsModes(game.Mode):

        def __init__(self, game, priority):
            super(MissionsModes, self).__init__(game, priority)
            self.name_layer = dmd.TextLayer(71, 7, self.game.fonts['num_09Bx7'], "center")
            self.info_layer = dmd.TextLayer(71, 18, self.game.fonts['07x5'], "center")

            self.game.lampctrl.register_show('rk_ramp_ready', lampshow_path+"ramp_ready.lampshow")

            self.mission_lamps = ['bonus1k','bonus2k','bonus3k','bonus4k','bonus5k','bonus6k','bonus7k','bonus8k','bonus9k', 'bonus10k']
            self.mission_list = [0,0,0,0,0,0,0,0,0,0]

            self.modes_lamps = ['raceChampion','kickstartKing','multiBall','easyRider']
            self.rkmodes_list = [0,0,0,0]
            self.current_mode_num = 0
            self.choice_id =0
            self.name_text =''
            self.info_text =''
            self.mode_enabled = False

            #setup game modes
            self.race_champion = Racechampion(self.game, 81)
            self.race_champion.callback = self.mode_callback
            self.kickstart_king = Kickstartking(self.game, 82)
            self.kickstart_king.callback = self.mode_callback
            self.multiball = Multiball(self.game, 83)
            self.multiball.callback = self.mode_callback
            self.easyrider = Easyrider(self.game, 84)
            self.easyrider.callback = self.mode_callback
            self.roadkings = Roadkings(self.game, 99)
            self.roadkings.callback = self.roadkings_callback

            self.reset_lamps()

        def mode_started(self):
            print("Debug, Mission Control Started")
            self.current_mode_num = self.game.get_player_stats('current_mode_num')
            self.rkmodes_list = self.game.get_player_stats('mode_status_tracking')
            self.mode_enabled = self.game.get_player_stats('mode_enabled')
            self.mission_list = self.game.get_player_stats('mission_status_tracking')

            #check rkmode list & missions
            self.unplayed_rkmodes()
            self.check_missions()

        def mode_stopped(self):
            self.game.lampctrl.stop_show()
            self.game.set_player_stats('current_mode_num',self.current_mode_num)
            self.game.set_player_stats('mode_status_tracking',self.rkmodes_list)
            print("Debug, Mission Control Ended")

## lamps & animations

        def reset_lamps(self):
            #loop round and turn off all lamps
            for i in range(len(self.modes_lamps)):
                self.game.effects.drive_lamp(self.modes_lamps[i],'off')

            self.mode_start_lamp(self.mode_enabled)

        def update_lamps(self):
            #current mode
            self.game.effects.drive_lamp(self.modes_lamps[self.current_mode_num],'slow')

            #completed modes
            for i in range(len(self.modes_lamps)):
                if self.rkmodes_list[i]==1:
                    self.game.effects.drive_lamp(self.modes_lamps[i],'on')

            #mode start
            if self.mode_enabled == 'Wizard':
                self.game.lampctrl.play_show('rk_ramp_ready', True, 'None')
                for i in range(len(self.modes_lamps)):
                    #if self.rkmodes_list[i]==1:
                        self.game.effects.drive_lamp(self.modes_lamps[i],'slow')
            else:
                self.mode_start_lamp(self.mode_enabled)

            #update mission lamps on bonus 1k...10k
            self.update_mission_lamps()

        def mode_start_lamp(self,flag):
            if flag and self.game.get_player_stats('ramp_state') == False:
                self.game.effects.drive_lamp('megaScore','medium')
                #current mode
                #self.game.effects.drive_lamp(self.modes_lamps[self.current_mode_num],'slow')
            else:
                self.game.effects.drive_lamp('megaScore','off')
                #current mode
                #self.game.effects.drive_lamp(self.modes_lamps[self.current_mode_num],'off')

        def update_ramp_lamps(self):
            # to update lamp after ramp move (called from effects)
            self.mode_start_lamp(self.mode_enabled)


        def play_animation(self):
             self.name_layer.set_text(self.name_text)
             self.info_layer.set_text(self.info_text)
             anim = dmd.Animation().load(dmd_path+"cup_ani.dmd")
             animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=10)
             fgnd_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'basic_layer.dmd').frames[0])
             fgnd_layer.composite_op = "blacksrc"
             self.layer = dmd.GroupedLayer(128, 32, [animation_layer, fgnd_layer, self.name_layer, self.info_layer])

        def clear_layer(self):
            self.layer=None

# Mission control

        def update_missions(self,mission_id):
             self.mission_list = self.game.get_player_stats('mission_status_tracking')
             # mission_id -1 to correspond with list
             self.mission_list[mission_id-1] = 1
             self.game.set_player_stats('mission_status_tracking',self.mission_list)
             print("Mission list: ", self.mission_list)
             self.update_mission_lamps()
             self.check_missions()

        def check_missions(self):
             count_missions = self.count_missions()
             count_modes = self.count_modes()
             if count_missions >= 1 and count_modes == 0:
                 print("1st mode enabled")
                 self.game.set_player_stats('mode_enabled',True)
                 self.activate_rkmode(True)
             elif count_missions >= 3 and count_modes == 1:
                 print("2nd mode enabled")
                 self.game.set_player_stats('mode_enabled',True)
                 self.activate_rkmode(True)
             elif count_missions >= 5 and count_modes == 2:
                 print("3th mode enabled")
                 self.game.set_player_stats('mode_enabled',True)
                 self.activate_rkmode(True)
             elif count_missions >= 7 and count_modes == 3:
                 print("4th mode enabled")
                 self.game.set_player_stats('mode_enabled',True)
                 self.activate_rkmode(True)
             elif count_missions == 10 and count_modes == 4:
                 print("Wizard mode enabled!")
                 self.game.set_player_stats('mode_enabled',True)
                 self.activate_wizardmode()

        def update_mission_lamps(self):
             for i in range(len(self.mission_lamps)):
                if self.mission_list[i]==1:
                    self.game.effects.drive_lamp(self.mission_lamps[i],'on')
                else:
                    self.game.effects.drive_lamp(self.mission_lamps[i],'off')

        def count_missions(self):
             count_rkmissions = 0
             for i in range(len(self.mission_list)):
                if self.mission_list[i]:
                    count_rkmissions +=1
             print("Missions nr: ", count_rkmissions)
             return count_rkmissions

## mode functions

        def count_modes(self):
             count_rkmodes = 0
             for i in range(len(self.rkmodes_list)):
                if self.rkmodes_list[i]:
                    count_rkmodes +=1
             print("Modes nr: ", count_rkmodes)
             return count_rkmodes

        def update_modes_completed(self,mode_id):
             modes_list = self.game.get_player_stats('modes_completed')
             # mode_id -1 to correspond with list
             modes_list[mode_id-1] = True
             self.game.set_player_stats('modes_completed',modes_list)
             print("Completed Modes list: ", modes_list)

        def activate_rkmode(self, flag=False):
             self.mode_enabled = flag
             self.mode_start_lamp(flag)

        def activate_wizardmode(self):
             self.game.sound.play(self.game.assets.sfx_wziardModeReady)
             self.mode_enabled = 'Wizard'
             self.game.lampctrl.play_show('rk_ramp_ready', True, 'None')

        def mode_callback(self,mode_name):
             #remove the active rkmode
             print("Ending Mode: "+mode_name)
             if mode_name == 'multiball':
                  self.game.modes.remove(self.multiball)
             if mode_name == 'easyrider':
                  self.game.modes.remove(self.easyrider)
             if mode_name == 'kickstartking':
                  self.game.modes.remove(self.kickstart_king)
             if mode_name == 'racechampion':
                  self.game.modes.remove(self.race_champion)

             #setup new rkmode list
             self.unplayed_rkmodes()

             # reset all
             self.reset_after_mode()

        def reset_after_mode(self):
             self.game.coils.flipperEnable.enable()
             self.game.lampctrl.stop_show()
             self.game.effects.clear_all_lamps()
             self.game.assets.rk_play_music()
             self.game.base_game_mode.rampmove.move_ramp('down')
             self.game.effects.gi_on()
             self.game.update_lamps()
             self.game.effects.release_stuck_balls()

        def roadkings_callback(self):
             # remove roadkings wizard mode
             self.game.modes.remove(self.roadkings)

             # reset game
             self.mission_list = [0,0,0,0,0,0,0,0,0,0]
             self.rkmodes_list = [0,0,0,0]
             self.current_mode_num = 0
             self.mode_enabled = False

             # update player stats
             self.game.set_player_stats('current_mode_num',self.current_mode_num)
             self.game.set_player_stats('mode_status_tracking',self.rkmodes_list)
             self.game.set_player_stats('mission_status_tracking',self.mission_list)
             self.game.set_player_stats('mode_enabled',False)

             # setup new rkmode list
             self.unplayed_rkmodes()

             # reset all
             self.reset_after_mode()

        def unplayed_rkmodes(self,dirn=None):

            #turn off current mode lamp
            self.game.effects.drive_lamp(self.modes_lamps[self.current_mode_num],'off')

            #create list of unplayed rkmode numbers
            choice_list=[]
            for i in range(len(self.rkmodes_list)):
                if self.rkmodes_list[i]==0:
                    choice_list.append(i)

            if choice_list: # if list has items
                #adjust choice number
                if dirn=='left':
                    self.choice_id -=1
                elif dirn=='right':
                    self.choice_id +=1
                else:
                    self.choice_id = random.randint(0, len(choice_list)-1)

                #create wrap around
                if self.choice_id>len(choice_list)-1:
                    self.choice_id=0
                elif self.choice_id<0:
                    self.choice_id=len(choice_list)-1

                #set new mode number
                self.current_mode_num = choice_list[self.choice_id]
            else:
                print("All modes played, wizard mode left")

            #update lamps
            self.update_lamps()

        def start_rkmode(self):
            if self.mode_enabled:

                print("Starting Mode: "+str(self.modes_lamps[self.current_mode_num]))

                # pause timer for playfield multiplier if running
                self.game.base_game_mode.pause_pf_multiplier(set=True)

                # select mode
                if self.current_mode_num==0:
                    self.name_text = 'RACE CHAMPION'
                    self.info_text = 'SHOOT MOVING SHOT'
                    self.game.sound.play(self.game.assets.sfx_RCstart)

                elif self.current_mode_num==1:
                    self.name_text = 'KICKSTART KING'
                    self.info_text = 'MAKE KICKS FOR JACKPOTS'
                    self.game.sound.play(self.game.assets.sfx_KKstart)

                elif self.current_mode_num==2:
                    self.name_text = 'MULTIBALL'
                    self.info_text = 'SHOOT JACKPOTS'
                    self.game.sound.play(self.game.assets.sfx_MBstart)

                elif self.current_mode_num==3:
                    self.name_text = 'EASY RIDER'
                    self.info_text = 'SHOOT ALL LIT SHOTS'
                    self.game.sound.play(self.game.assets.sfx_ERstart)

                #update mode completed status tracking
                self.rkmodes_list[self.current_mode_num] = 1

                #play animation
                self.play_animation()

                # reset mode enable
                self.mode_enabled=False
                self.game.set_player_stats('mode_enabled',False)

                # start mode
                self.delay(name='rkmode_delay', event_type=None, delay=5, handler=self.add_selected_rkmode)
                self.delay(name='clear_delay', event_type=None, delay=6, handler=self.clear_layer)

                #self.update_lamps()
                self.game.effects.all_flashers_off()

            else:
                self.delay(name='eject_delay', event_type=None, delay=0.5, handler=self.eject_ball)

        def add_selected_rkmode(self):
            if self.current_mode_num==0:
                self.game.modes.add(self.race_champion)
            elif self.current_mode_num==1:
                  self.game.modes.add(self.kickstart_king)
            elif self.current_mode_num==2:
                  self.game.modes.add(self.multiball)
            elif self.current_mode_num==3:
                  self.game.modes.add(self.easyrider)

        def start_wizardmode(self):
             # SHUT DOWN
             print("Wizzzzard!")
             # stop music
             self.game.assets.rk_play_music('stop')
             # disable flippers
             self.game.coils.flipperEnable.disable()
             # clear all lamps + gi
             self.game.lampctrl.stop_show()
             self.game.effects.all_flashers_off()
             for lamp in self.game.lamps:
                    lamp.disable()
             self.game.effects.gi_off()
             # make layer black (i.e. empty layer)
             self.layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'rk_black.dmd').frames[0])
             # clear layer after delay
             self.delay(name='clear_delay', event_type=None, delay=8, handler=self.clear_layer)
             # play sound
             self.game.sound.play(self.game.assets.sfx_wizardShutdown)
             # add wizard mode
             self.game.modes.add(self.roadkings)

        def move_left(self):
            self.unplayed_rkmodes('left')

        def move_right(self):
            self.unplayed_rkmodes('right')

        def eject_ball(self):
            self.game.effects.eject_ball(location='upperLkicker')

## switches

        def sw_upperLkicker_active_for_500ms(self,sw):
             if self.mode_enabled and self.game.get_player_stats('game_feature_running')==False:
                 self.game.add_player_stats('ramps_made',1)
                 self.start_rkmode()
                 return True

        def sw_RrampExit_active(self, sw):
             # Check for Wizard mode active
             if self.mode_enabled == 'Wizard':
                 self.start_wizardmode()
                 return procgame.game.SwitchStop
             # Else check for mode active
             elif self.mode_enabled and self.game.get_player_stats('game_feature_running')==False:
                 print("Ramp gehaald, mode gestart")
                 self.game.effects.gi_blinking(schedule=0x0F0F0F0F, cycle_seconds=1)
                 #play sound
                 self.game.assets.rk_play_music('stop')
                 self.game.sound.play(self.game.assets.sfx_rkmodeStarted)

        def sw_upperLkicker_active(self,sw):
             if self.mode_enabled and self.game.get_player_stats('game_feature_running')==False:
                 return procgame.game.SwitchStop

        def sw_slingL_active(self,sw):
             self.move_right()

        def sw_slingR_active(self,sw):
             self.move_left()

        def sw_Lspinner_active(self, sw):
             self.move_right()