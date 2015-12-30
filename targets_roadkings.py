#
# Roadkings targets
# Control for targethits
#

__author__="Pieter"
__date__ ="$20 Sep 2012 20:36:37 PM$"

import procgame
from procgame import *

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"


class TargetsRoadkings(game.Mode):

        def __init__(self, game, priority):
            super(TargetsRoadkings, self).__init__(game, priority)

            self.text_layer = dmd.TextLayer(128/2, 22, self.game.fonts['07x5'], "center", opaque=False)

            self.road_flag = [False,False,False,False]
            self.kings_flag = [False,False,False,False, False]
            self.roadlamps = ['targetR','targetO','targetA','targetD']
            self.kingslamps = ['targetK','targetI','targetN','targetG','targetS']

            self.target_hit_value = 1000
            self.target_lit_value = 110

            self.road_complete = False
            self.kings_complete = False
            self.roadkings_complete = 0
            #self.set_xball = 2 #VIA MENU
            #self.set_xball = self.game.user_settings['Gameplay (Feature)']['Roadkings Targets Xball']
            self.game.set_player_stats('roadkings_xball', self.game.user_settings['Gameplay (Feature)']['Roadkings Targets Xball'])
            #self.inc_xball = 2 #VIA MENU
            #self.inc_xball = self.game.user_settings['Gameplay (Feature)']['Roadkings Targets Xball Raise']
            self.clear_lamps()

        def mode_started(self):
            print("Debug, Targets Roadkings Mode Started")
            self.road_flag = self.game.get_player_stats('road_targets')
            self.kings_flag = self.game.get_player_stats('kings_targets')
            self.roadkings_complete = self.game.get_player_stats('roadkings_complete')
            self.set_xball = self.game.get_player_stats('roadkings_xball')

        def mode_stopped(self):
            self.clear_lamps()
            self.clear_layer()
            print("Debug, Targets Roadkings Mode Ended")

        def mode_tick(self):
            pass

## lamps & animations

        def update_lamps(self):
            # ROAD lamps
            for i in range(len(self.roadlamps)):
                if self.road_flag[i]: # steady on if target already hit
                    self.game.effects.drive_lamp(self.roadlamps[i],'on')
                else: # blinking if target is lit
                    self.game.effects.drive_lamp(self.roadlamps[i],'medium')
            # KINGS lamps
            for i in range(len(self.kingslamps)):
                if self.kings_flag[i]:
                    self.game.effects.drive_lamp(self.kingslamps[i],'on')
                else:
                    self.game.effects.drive_lamp(self.kingslamps[i],'medium')

        def clear_lamps(self):
             for i in range(len(self.roadlamps)):
                 self.game.effects.drive_lamp(self.roadlamps[i],'off')
             for i in range(len(self.kingslamps)):
                 self.game.effects.drive_lamp(self.kingslamps[i],'off')

        def clear_layer(self):
             self.layer = None

        def play_animation(self, targets='road'):
             if targets == 'road':
                 anim = dmd.Animation().load(dmd_path+'road.dmd')
             elif targets == 'kings':
                 anim = dmd.Animation().load(dmd_path+'kings.dmd')
             elif targets == 'roadkings':
                 anim = dmd.Animation().load(dmd_path+'roadkings.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=True, frame_time=10)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.text_layer])

## mode functions

        def hit_road(self,id):

            if self.road_flag[id] == False:
                #play sounds
                self.game.sound.play(self.game.assets.sfx_targetHit)
                # turn lamp on
                self.game.effects.drive_lamp(self.roadlamps[id],'smarton')
                # set flag
                self.road_flag[id] = True
                # score value
                self.game.score(self.target_hit_value)
                #update player stats var
                self.game.set_player_stats('road_targets',self.road_flag)
                # check for road complete
                self.spell_road()
                #print(self.road_flag)
            else:
                self.game.score(self.target_lit_value)
                self.game.sound.play(self.game.assets.sfx_targetLit)

        def spell_road(self):

            count_road = 0
            self.road_flag = self.game.get_player_stats('road_targets')

            # Count for letters (ROAD) to be True
            for i in range(len(self.road_flag)):
                if self.road_flag[i]:
                    count_road +=1

            if count_road == 4:
                self.road_complete = True
                self.game.sound.play(self.game.assets.sfx_targetsComplete)
                # play animation
                self.text_layer.set_text("lites Kickback", blink_frames=20)
                self.play_animation('road')
                # award kickback
                self.game.base_game_mode.kickback.raise_kickback()
                # update missions
                self.game.base_game_mode.missions_modes.update_missions(2)
                # check for roadkings complete
                self.check_roadkings()
                # reset flag and lamps after delay
                self.delay(name='reset_road', event_type=None, delay=2, handler=self.reset_road)

        def reset_road(self):
            for i in range(len(self.road_flag)):
                self.road_flag[i] = False
            self.update_lamps()
            self.clear_layer()


        def hit_kings(self,id):

            if self.kings_flag[id] == False:
                #play sounds
                self.game.sound.play(self.game.assets.sfx_targetHit)
                # turn lamp on
                self.game.effects.drive_lamp(self.kingslamps[id],'smarton')
                # set flag
                self.kings_flag[id] = True
                # score value
                self.game.score(self.target_hit_value)
                #update player stats var
                self.game.set_player_stats('kings_targets',self.kings_flag)
                # check for kings complete
                self.spell_kings()
                #print(self.kings_flag)
            else:
                self.game.score(self.target_lit_value)
                self.game.sound.play(self.game.assets.sfx_targetLit)

        def spell_kings(self):

            count_kings = 0
            self.kings_flag = self.game.get_player_stats('kings_targets')

            # Count for letters (KINGS) to be True
            for i in range(len(self.kings_flag)):
                if self.kings_flag[i]:
                    count_kings +=1

            if count_kings == 5:
                self.kings_complete = True
                self.game.sound.play(self.game.assets.sfx_targetsComplete)
                # play animation
                self.text_layer.set_text("raises spinner", blink_frames=20)
                self.play_animation('kings')
                # award raise spinner value
                self.game.base_game_mode.generalplay.raise_spinner_value()
                # update missions
                self.game.base_game_mode.missions_modes.update_missions(3)
                # check for roadkings complete
                self.check_roadkings()
                # reset flag and lamps after delay
                self.delay(name='reset_kings', event_type=None, delay=2, handler=self.reset_kings)

        def reset_kings(self):
            for i in range(len(self.kings_flag)):
                self.kings_flag[i] = False
            self.update_lamps()
            self.clear_layer()

        def check_roadkings(self):
             if self.road_complete and self.kings_complete:
                 self.roadkings_complete += 1
                 self.game.add_player_stats('roadkings_complete',1)
                 # determine xball award
                 counter = self.set_xball - self.roadkings_complete
                 print(self.set_xball)
                 print("-")
                 print(self.roadkings_complete)
                 print("=")
                 print(counter)
                 # check for extraball award
                 if counter == 0:
                     self.game.extra_ball.lit('Rextraball')
                     self.game.add_player_stats('roadkings_xball', self.game.user_settings['Gameplay (Feature)']['Roadkings Targets Xball Raise'])
                     self.set_xball = self.game.get_player_stats('roadkings_xball')
                     # update missions
                     self.game.base_game_mode.missions_modes.update_missions(6)
                 else:
                    # play animation
                    self.text_layer.set_text(str(counter)+" more to lite Xball")
                    self.play_animation('roadkings')
                 # reset flags
                 self.road_complete = False
                 self.kings_complete = False

        def add_letter(self):
             # add letter to KINGS, or ROAD
             if self.game.switches.flipperLwR.is_active():
                # count kings_flag till first False
                for i in range(len(self.kings_flag)):
                    if self.kings_flag[i] == False:
                        self.hit_kings(i)
                        break
             else:
                # count road_flag till first False
                for i in range(len(self.road_flag)):
                    if self.road_flag[i] == False:
                        self.hit_road(i)
                        break

## switches

        def sw_dropTarget_active_for_250ms(self,sw):
             self.add_letter()
             self.game.effects.drive_lamp('spotLetter','smartoff')

        def sw_targetR_active(self,sw):
             self.hit_road(0)

        def sw_targetO_active(self,sw):
             self.hit_road(1)

        def sw_targetA_active(self,sw):
             self.hit_road(2)

        def sw_targetD_active(self,sw):
             self.hit_road(3)


        def sw_targetK_active(self,sw):
             self.hit_kings(0)

        def sw_targetI_active(self,sw):
             self.hit_kings(1)

        def sw_targetN_active(self,sw):
             self.hit_kings(2)

        def sw_targetG_active(self,sw):
             self.hit_kings(3)

        def sw_targetS_active(self,sw):
             self.hit_kings(4)

