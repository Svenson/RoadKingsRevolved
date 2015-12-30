#
# Mystery
# Select random mystery award from mysterylist
# In tournament mode awards are in fixed order
#
__author__="Pieter"
__date__ ="$18 Sep 2012 20:36:37 PM$"

import procgame
from procgame import *
from random import *
import random

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Mystery(game.Mode):

        def __init__(self, game, priority):
             super(Mystery, self).__init__(game, priority)

             self.text_layer = dmd.TextLayer(85, 18, self.game.fonts['tiny7'], "center", opaque=False) #tiny7, 07x5

             self.game.lampctrl.register_show('mystery_show', lampshow_path+"mystery.lampshow")

             #self.mysterylist =['Complete ROAD','Complete KINGS','500.000','1 Million','Light Kickback','20 Miles','Hold BonusX','1,5 Million','Bonus add 5X','Light Extra Ball','Quick MultiBall']
             self.mysterylist =['Complete ROAD','Complete KINGS','500.000','1 Million','Light Kickback','20 Miles','Hold BonusX','Award left combo','Bonus add 5X','Light Extra Ball','X-ramp 250k']
             self.temp_list =[]

             self.tournament_mode = False # VIA MENU
             self.choice = 0
             self.index = len(self.mysterylist)


        def mode_started(self):
             print("Debug, Mystery Mode Started")
             self.tournament_mode = self.game.user_settings['Gameplay (Feature)']['Tournament Mode']
             self.lit()

        def mode_stopped(self):
            self.game.effects.drive_flasher('showroomFlash','off')
            self.game.update_lamps()
            print("Debug, Mystery Mode Stopped")

## lamps & animations

        def update_lamps(self):
             if self.game.get_player_stats('game_feature_running')==False:
                 self.game.effects.drive_lamp('Ctimelock','slow')
                 self.game.effects.drive_flasher('showroomFlash','slow')

        def clear_lamps(self):
             self.game.effects.drive_lamp('Ctimelock','off')
             #self.game.effects.drive_lamp('Showroom','off')

        def inform_player(self):
             anim = dmd.Animation().load(dmd_path+'mystery_inform.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=20)
             self.layer = self.animation_layer
             self.delay(name='clear_layer', event_type=None, delay=2, handler=self.clear_layer)

        def mystery_animation(self):
             anim = dmd.Animation().load(dmd_path+'mystery_ani.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=5)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer,self.text_layer])
             # Award at end of animation (after 4s)
             self.delay(name='award_award', event_type=None, delay=4, handler=self.award_award)

        def scroll_list(self):
             # repeat call to itself to scroll to mysterylist
             if self.index > 0:
                 self.index -= 1
                 self.game.sound.play(self.game.assets.sfx_spark)
                 # set display text
                 self.text_layer.set_text(self.temp_list[self.index])
                 self.delay(name='scroll_list', event_type=None, delay=0.3, handler=self.scroll_list)
             else:
                 self.cancel_delayed('scroll_list')
                 # set display text for final award
                 self.text_layer.set_text(self.mysterylist[self.choice], blink_frames=10)
                 # reset counter index
                 self.index = len(self.mysterylist)

        def clear_layer(self):
            self.layer = None

## mode functions

        def lit(self):
            self.update_lamps()
            self.inform_player()

        def start_feature(self):
             # Mystery feature started from general_play.py

             #stop music, play sound and light
             self.game.sound.fadeout_music(time_ms=100)
             self.game.sound.play(self.game.assets.sfx_mystery)
             # turn off all lamps and GI
             for lamp in self.game.lamps:
                  lamp.disable()
             self.game.effects.drive_flasher('showroomFlash','off')
             self.game.effects.gi_off()
             #play lampshow
             self.game.lampctrl.play_show('mystery_show', False, 'None')

             # get award for tournament mode
             if self.tournament_mode:
                 next_award = self.game.get_player_stats('mystery_award')
                 # Create wrap around if end is reached
                 if next_award == 10:
                     next_award = 3
                 self.choice = next_award

             # get award for normal mode
             else:
                 last_award = self.game.get_player_stats('mystery_award')
                 # Generate random award from listitems
                 # If award equals last_award try again, so you won't get the same item twice in a row
                 repeat = True
                 while repeat:
                         self.choice = random.randrange(0, len(self.mysterylist),1)
                         if self.choice != last_award:
                             repeat = False
             #self.choice = 6 # TEST
             print("mystery_keuze: "+str(self.choice)+" , "+self.mysterylist[self.choice])

             # make copy of list to shuffle scrolling list in animation
             self.temp_list = list(self.mysterylist)
             shuffle(self.temp_list)

             #play animation with textscrolling
             self.mystery_animation()
             self.scroll_list()

        def award_award(self):
             #award logic
             self.award(self.mysterylist[self.choice])

        def award(self,option):
            self.cancel_delayed('scroll_list')
            self.delay(name='mystery_end', event_type=None, delay=1, handler=self.mystery_end)

            # assignment off the awards
            if option==self.mysterylist[0]: # complete ROAD
                print("Mystery award: Complete ROAD")
                road_flag = [True,True,True,True]
                self.game.set_player_stats('road_targets',road_flag)
                self.game.base_game_mode.targets_roadkings.spell_road()
            elif option==self.mysterylist[1]: # complete KINGS
                print("Mystery award: Complete KINGS")
                kings_flag = [True,True,True,True,True]
                self.game.set_player_stats('kings_targets',kings_flag)
                self.game.base_game_mode.targets_roadkings.spell_kings()
            elif option==self.mysterylist[2]: #500.000
                print("Mystery award: 500.000")
                self.game.score(500000)
            elif option==self.mysterylist[3]: #1 million
                print("Mystery award: 1 Million")
                self.game.score(1000000)
            elif option==self.mysterylist[4]: # Lite Kickback
                print("Mystery award: Lite Kickback")
                self.game.base_game_mode.kickback.raise_kickback()
            elif option==self.mysterylist[5]: # 20 Miles
                print("Mystery award: 20 Miles")
                self.game.base_game_mode.generalplay.add_miles(20)
            elif option==self.mysterylist[6]: # Bonus Hold
                print("Mystery award: Bonus Hold")
                self.game.set_player_stats('hold_bonusx',True)
                self.game.base_game_mode.lanes1234.update_lamps()
            elif option==self.mysterylist[7]: #1,5 million / Left Combo
                #print("Mystery award: 1,5 Million")
                #self.game.score(1500000)
                print("award: Collect left combo")
                self.game.base_game_mode.combo.set_combo(id=0)
            elif option==self.mysterylist[8]: # Bonus +5x
                print("Mystery award: Bonus +5X")
                self.game.add_player_stats('bonus_x',5)
            elif option==self.mysterylist[9]: # lite extra ball
                print("Mystery award: Lite Extra Ball")
                self.game.extra_ball.hurryup('Rextraball')
            #elif option==self.mysterylist[10]: # Quick Multiball
            #    print("Mystery award: Quick Multi-Ball")
            #    self.game.base_game_mode.bumpers.start_quickmball()
            elif option==self.mysterylist[10]: # X-ramp 250k
                print("Mystery award: X-ramp 250k")
                self.game.base_game_mode.crossramp.set_crossramp_values(value=250000)

        def mystery_end(self):
             self.clear_layer()
             self.clear_lamps()
             self.game.effects.gi_on()
             self.game.effects.eject_ball('Ceject')

             # restart main theme music (not for listnr. 10)
             #if self.mysterylist[self.choice]!=self.mysterylist[10]:
             self.game.assets.rk_play_music()

             # raise choice nr. and save for next mystery in tournament mode
             if self.tournament_mode:
                 self.game.set_player_stats('mystery_award',self.choice+1)
             else: # save for last mystery in normal mode
                 self.game.set_player_stats('mystery_award',self.choice)

             # reset spinner for mystery
             self.game.base_game_mode.generalplay.spinner_reset()
             # update missions
             self.game.base_game_mode.missions_modes.update_missions(7)
             # remove mystery mode
             self.game.modes.remove(self)

## switches

# Mystery feature started from Ceject in general_play.py



