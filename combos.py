#
# Combo's
#
# Game mode for scoring following combo's:
# - centerramp + leftloop
# - centerramp + rightloop (ramp up!)
# - centerramp + rightramp (ramp down!)
#

__author__="Pieter"
__date__ ="$13 Nov 2012 20:36:37 PM$"


import procgame
from procgame import *

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Combo(game.Mode):

        def __init__(self, game, priority):
            super(Combo, self).__init__(game, priority)

            #register animation layers
            self.combo_text = dmd.TextLayer(128/2, 10, self.game.fonts['num_14x10'], "center", opaque=False) #num_09Bx7 num_14x10
            combo_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'combo_bgnd1.dmd').frames[0])
            anim = dmd.Animation().load(dmd_path+'arrows_ttt.dmd')
            animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=3)
            animation_layer.composite_op = "blacksrc"
            self.anilayer = dmd.GroupedLayer(128, 32, [combo_bgnd, animation_layer])

            #register lampshow
            self.game.lampctrl.register_show('combo_show', lampshow_path+"succes.lampshow")

            #self.combo_flag = [False,False,False]
            self.combo_flag = [0,0,0]
            self.spinner = True
            self.runder = True
            self.combo_value = 500000 #VIA MENU

        def mode_started(self):
             print("Debug, Combo Mode Started")
             self.combo_flag = self.game.get_player_stats('combo_flag')
             print("Combo flag: "+str(self.combo_flag))

        def mode_stopped(self):
             print("Debug, Combo Mode Ended")


## lamps and animations

        def reset_combo_lamps(self):
             self.game.update_lamps()

        def play_animation(self):
             #self.combo_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'combo_bgnd.dmd').frames[0])
             anim = dmd.Animation().load(dmd_path+'arrows_ttt.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=3)
             #self.animation_layer.add_frame_listener(-1, self.clear_layer)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer,self.combo_text, self.info_text])
             self.delay(name='clear_display', event_type=None, delay=3.5, handler=self.clear_layer)

        def play_animation2(self):
             self.layer = dmd.GroupedLayer(128, 32, [self.anilayer, self.combo_text])
             self.delay(name='clear_display', event_type=None, delay=3.5, handler=self.clear_layer)

        def clear_layer(self):
             self.layer = None

## mode functions

        def check_combos(self):
             count = 0
             for i in range(len(self.combo_flag)):
                  if self.combo_flag[i]: # check if all 3 are made
                      count += 1
                  if self.combo_flag[i] == 3: #check if any 3 are made
                      count = 3
             if count >=3:
                 # combos complete
                 self.game.sound.play(self.game.assets.sfx_combos_complete)
                 self.combo_text.set_text("COMPLETED!",3,3)#on for 3 seconds 3 blinks
                 # update missions for achieving Combo's
                 self.game.base_game_mode.missions_modes.update_missions(5)
             return count

        def set_combo(self, id=0):
             #play sound, lightshow and animation
             self.game.sound.play(self.game.assets.sfx_combo_made)
             self.game.lampctrl.play_show('combo_show', False, 'None')
             self.play_animation2()
             #score combo value
             self.game.score(self.combo_value)
             #set flag
             #self.combo_flag[id] = True
             self.combo_flag[id] += 1
             self.game.set_player_stats('combo_flag',self.combo_flag)
             #check for combos completed
             self.check_combos()

        def close_gate(self):
             self.game.coils.Lgate.disable()
             self.game.coils.Rgate.disable()

        def set_spinner(self):
             self.spinner = True

        def set_Runder(self):
             self.runder = True

## Switches Combo's

        def sw_lane4_active(self,sw):
             if self.game.switches.CrampEnter.time_since_change() < 4:
                # update lamps right ramp
                    self.game.lamps.Rtimelock.schedule(schedule=0x0f0f0f0f, cycle_seconds=3, now=True)
                    self.game.lamps.Rlock.schedule(schedule=0xf0f0f0f0, cycle_seconds=3, now=True)
                    self.game.lamps.Rextraball.schedule(schedule=0x0f0f0f0f, cycle_seconds=3, now=True)
                    self.delay(name='reset_combo_lamps', event_type=None, delay=3.5, handler=self.reset_combo_lamps)

        def sw_CrampRexit_active(self, sw):
                self.game.effects.drive_lamp('bonusholdWL','timeout',time=3)
                self.delay(name='reset_combo_lamps', event_type=None, delay=3.5, handler=self.reset_combo_lamps)

        def sw_Lspinner_active(self, sw):
             if self.spinner:
                 if self.game.switches.CrampRexit.time_since_change() < 3:
                     self.spinner = False
                     # open right gate
                     self.game.coils.Rgate.enable()
                     self.combo_text.set_text("TURN LEFT")#on for 3 seconds 4 blinks
                     self.set_combo(id=0)
                     self.delay(name='close_gate', event_type=None, delay=2, handler=self.close_gate)
                     self.delay(name='set_spinner', event_type=None, delay=3, handler=self.set_spinner)

        def sw_RrampExit_active(self,sw):
             if self.game.switches.CrampEnter.time_since_change() < 5 and self.game.switches.lane4.time_since_change() < 3:
                 self.combo_text.set_text("JUMP",3,4)#on for 3 seconds 4 blinks
                 self.set_combo(id=1)

        def sw_Rrollunder_active(self,sw):
             if self.runder:
                 if self.game.switches.CrampEnter.time_since_change() < 4 and self.game.switches.lane4.time_since_change() < 2:
                     self.runder = False
                     # open left gate
                     self.game.coils.Lgate.enable()
                     self.combo_text.set_text("TURN RIGHT")#on for 3 seconds 4 blinks
                     self.set_combo(id=2)
                     self.delay(name='close_gate', event_type=None, delay=2, handler=self.close_gate)
                     self.delay(name='set_runder', event_type=None, delay=3, handler=self.set_Runder)

