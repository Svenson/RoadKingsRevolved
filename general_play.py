#
# General play
# all gameplay items that don't belong to a specific mode
#
# To Do: extraball via roadkings-targets
#
__author__="Pieter"
__date__ ="$20 Sep 2012 20:36:37 PM$"

import procgame
import locale
from jumpramp import *
from procgame import *
from mystery import *


# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Generalplay(game.Mode):

        def __init__(self, game, priority):
            super(Generalplay, self).__init__(game, priority)

            self.mystery = Mystery(self.game, 51) # reference to mystery
            self.jumpramp = Jumpramp(self.game, 91) # reference to jumpramp hurryup

            #register animation layers
            self.showroom_text = dmd.TextLayer(70, 22, self.game.fonts['07x5'], "center", opaque=False)
            self.showroom_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'showroom.dmd').frames[0])
            self.showroom_layer = dmd.GroupedLayer(128, 32, [self.showroom_bgnd, self.showroom_text])
            self.showroom_layer.transition = dmd.PushTransition(direction='north')

            self.ramp_text = dmd.TextLayer(70, 23, self.game.fonts['07x5'], "center", opaque=False)
            self.display_miles_layer = dmd.TextLayer(90, 26, self.game.fonts['07x5'], "center", opaque=False)
            self.count_miles_layer = dmd.TextLayer(26, 18, self.game.fonts['tiny7'], "center", opaque=False).set_text('')
            self.millionplus_text = dmd.TextLayer(128/2, 7, self.game.fonts['18x12'], "center", opaque=False)

            self.game.lampctrl.register_show('rampenter_show', lampshow_path+"rampenter.lampshow")
            self.game.lampctrl.register_show('million_plus_show', lampshow_path+"succes_short.lampshow")

            self.lamps_ramp = ['megaScore','Rtimelock','Rlock','Rextraball']

            #self.spinner_count = 1 #VIA MENU #determines the count of each revolution
            self.spinner_count = self.game.user_settings['Gameplay (Feature)']['Spinner Count Per Revolution']
            #self.miles_for_mission = 75 #VIA MENU
            self.miles_for_mission = self.game.user_settings['Gameplay (Feature)']['Miles for mission']
            self.ani_list = ['kk_joker.dmd','lightningDMD.dmd','kk_skeleton.dmd','Gravity.dmd','JordanCurver.dmd','lightning1.dmd','fireworks.dmd','babe3.dmd']
            self.mystery_ready = False
            self.millionplus = False
            #self.millionplus_value = 2000000
            self.spinner_miles = False
            self.spin_miles = 0
            self.animation_status = 'ready'
            self.test_frame = 0
            self.index = 0

        def mode_started(self):
             print("Debug, Generalplay Mode Started")
             self.game.effects.all_flashers_off()
             self.game.effects.check_droptarget()
             self.spinner_value = self.game.get_player_stats('spinner_value')
             self.spinner_turns = self.game.get_player_stats('spinner_turns')
             self.millionplus = self.game.get_player_stats('million_plus')
             self.millionplus_value = self.game.get_player_stats('millionplus_value')

        def mode_stopped(self):
             print("Debug, Generalplay Mode Ended")
             self.game.modes.remove(self.mystery)
             self.game.set_player_stats('spinner_turns',self.spinner_turns)
             #self.game.set_player_stats('million_plus', False)

## lamps and animations

        def update_lamps(self):
             self.update_miles_lamps()
             self.update_xball_lamp()
             self.update_mystery_lamps()
             self.update_ramp_lamps()

        def update_mystery_lamps(self):
             if self.mystery_ready and self.game.get_player_stats('game_feature_running')==False:
                #self.game.effects.drive_lamp('Ctimelock','slow')
                self.game.effects.drive_lamp('bonusholdWL','off')
             else:
                self.game.effects.drive_lamp('bonusholdWL','slow')

        def update_miles_lamps(self):
             # update lamps for collected miles
             miles = self.game.get_player_stats('miles_collected')
             if miles >= 10:
                  self.game.effects.drive_lamp('bonus20k','slow')
             if miles >= 20:
                  self.game.effects.drive_lamp('bonus20k','on')
             if miles >= 30:
                  self.game.effects.drive_lamp('bonus40k','slow')
             if miles >= 40:
                  self.game.effects.drive_lamp('bonus40k','on')
             if miles >= 50:
                  self.game.effects.drive_lamp('bonus60k','slow')
             if miles >= 60:
                  self.game.effects.drive_lamp('bonus60k','on')
             if miles >= 70:
                  self.game.effects.drive_lamp('bonus80k','slow')
             if miles >= 80:
                  self.game.effects.drive_lamp('bonus80k','on')

        def update_xball_lamp(self):
             # update extraball lamp if player has extra ball
             if self.game.current_player().extra_balls:
                  self.game.effects.drive_lamp('cruiseAgain','on')
             else:
                  self.game.effects.drive_lamp('cruiseAgain','off')

        def update_ramp_lamps(self):
            # to update lamp after ramp move (called from effects)
             if self.game.get_player_stats('game_feature_running')==False: # only when no feature running
                if self.game.get_player_stats('ramp_state') == True: # ramp up
                    self.game.effects.drive_lamp('Rtimelock','off')
                else:
                    self.game.effects.drive_lamp('Rtimelock','slow')

        def play_showroom_ani(self):
            script = list()
            script.append({'seconds':2.0, 'layer':self.showroom_layer})
            self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)
            self.delay(name='clear_display', event_type=None, delay=2, handler=self.clear_layer)

        def play_spinner(self):
             # use spinner_turns to select frame, divide with // operator to increase needed turns
             anim = dmd.Animation().load(dmd_path+'mystery.dmd')
             self.animation_layer = dmd.FrameLayer(opaque=False, frame=anim.frames[self.spinner_turns//2])
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.count_miles_layer])
             self.delay(name='clear_display', event_type=None, delay=2, handler=self.clear_layer)

        def play_mystery_ready(self):
            if self.animation_status=='ready':
                anim = dmd.Animation().load(dmd_path+'mystery_ready.dmd')
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=10)
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.count_miles_layer])
                self.animation_status = 'running'
                self.delay(name='clear_display', event_type=None, delay=2, handler=self.clear_layer)

        def play_millionplus(self):
             anim = dmd.Animation().load(dmd_path+'million_plus.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=5)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer,self.millionplus_text])
             #self.animation_layer.add_frame_listener(-1, self.clear_layer)
             self.delay(name='clear_display', event_type=None, delay=2, handler=self.clear_layer)

        def clear_layer(self):
             self.layer = None
             self.animation_status = 'ready'

        def clear_sound(self):
             self.game.sound.stop(self.game.assets.sfx_jumpApplause)

## mode functions
        def check_ball_in_shooter_delay(self):
             self.delay(name='ball_check', event_type=None, delay=1, handler=self.check_ball_in_shooter)
        def check_ball_in_shooter(self):
             print ("Delay balls in play: ", self.game.trough.num_balls_in_play)
             if self.game.switches.trough1.is_active():
                print("trough1 active")
             if self.game.switches.trough2.is_active():
                print("trough2 active")
             if self.game.switches.trough3.is_active():
                print("trough3 active")
             if self.game.switches.trough1.is_active() and self.game.switches.trough2.is_active() and self.game.switches.trough3.is_active():
                 self.game.coils.trough.pulse(25)
                 self.game.coils.Rlightningbolt.pulse(40)
                 print ("Eject ball; balls in play: ", self.game.trough.num_balls_in_play)

        def check_spinner_counter(self):
             if self.spinner_turns == 40:
                 self.spinner_turns = 0
                 self.light_mystery()

        def light_mystery(self):
             self.mystery_ready = True
             # update mystery lamps
             self.update_mystery_lamps()
             # add mystery mode
             self.game.modes.add(self.mystery)

        def raise_spinner_value(self):
             # raises the spinner value times 3 and saves it to player stats
             self.spinner_value *= 3
             self.game.set_player_stats('spinner_value',self.spinner_value)

        def spinner_reset(self):
             self.mystery_ready = False

        def check_extra_ball(self):
             if self.game.get_player_stats('extraball_on'):
                 # collect extra ball
                 self.game.extra_ball.collect()
                 # update missions
                 self.game.base_game_mode.missions_modes.update_missions(6)

        def check_ramps(self):
             if self.game.get_player_stats('jumpramps_count') == self.game.user_settings['Gameplay (Feature)']['Jumpramps For Hurryup']:
                 # start hurry up
                 self.game.modes.add(self.jumpramp)
                 self.game.set_player_stats('game_feature_running',True)
                 # update missions (MOVED TO JUMPRAMP MODESTOP)
                 # reset jumpramps_count
                 self.game.set_player_stats('jumpramps_count', 0)

        def check_miles(self):
             if self.game.get_player_stats('miles_collected') >= self.miles_for_mission:
                 # update missions
                 self.game.base_game_mode.missions_modes.update_missions(8)

        def close_gate(self):
             self.game.coils.Lgate.disable()

        def add_miles(self, number, display=True):
             self.game.add_player_stats('miles_collected',number)
             self.check_miles()
             if display:
                 self.layer = self.display_miles_layer.set_text(" add "+str(number)+" mile ")
                 self.delay(name='clear_display', event_type=None, delay=1, handler=self.clear_layer)

        def set_millionplus(self):
             # Sets the million plus feature
             self.millionplus = True
             self.game.set_player_stats('million_plus', True)

        def score_millionplus(self):
             # Scores millionplus
             self.game.sound.play(self.game.assets.speech_million)
             self.millionplus_text.set_text(str(self.millionplus_value))
             self.play_millionplus()
             self.game.lampctrl.play_show('million_plus_show', False, 'None')
             self.game.score(self.millionplus_value*1000000)
             self.millionplus_value +=1

        def set_spinner_miles(self):
             # Sets the spinner miles feature
             self.spinner_miles = True
             print("Spinner miles:")
             print(self.spinner_miles)

## Switches regular gameplay

        def sw_outhole_active_for_500ms(self, sw):
             self.game.coils.outhole.pulse(40)

        def sw_Rtenpoint_active(self,sw):
             self.game.score(1000)
             self.game.sound.play(self.game.assets.sfx_bark)
             self.add_miles(1)

        def sw_Ltenpoint_active(self,sw):
             self.game.score(1000)

        def sw_Rrollunder_active(self,sw):
             self.game.score(1000)
             if self.game.switches.flipperLwR.is_active():
                 self.game.coils.Lgate.enable()
                 self.delay(name='close_gate', event_type=None, delay=2, handler=self.close_gate)

        def sw_Leject_active_for_750ms(self, sw):
             #self.game.coils.Leject.pulse(20)
             self.add_miles(2)
             self.update_miles_lamps()

        def sw_Ceject_active_for_250ms(self, sw):
             if self.mystery_ready == True:
                 self.showroom_text.set_text("MYSTERY", blink_frames=10)
             else:
                 self.showroom_text.set_text("2 Miles", blink_frames=10)
             self.game.sound.play(self.game.assets.sfx_showroom)
             self.play_showroom_ani()

        def sw_Ceject_active_for_1s(self, sw):
             if self.mystery_ready==True and self.game.get_player_stats('game_feature_running')==False:
                 # start mystery
                 self.delay(name='start_feature', event_type=None, delay=1, handler=self.mystery.start_feature)
             else:
                 self.game.effects.eject_ball('Ceject')
                 self.add_miles(2)
                 self.update_miles_lamps()

        def sw_slingL_active(self,sw):
             self.game.sound.play(self.game.assets.sfx_slingShot)
             self.game.score(110)

        def sw_slingR_active(self,sw):
             self.game.sound.play(self.game.assets.sfx_slingShot)
             self.game.score(110)

        def sw_outlaneR_active(self,sw):
             self.game.sound.play(self.game.assets.sfx_crash)
             self.game.score(25000)
             if self.game.trough.num_balls_in_play==1 and self.game.ball_save.timer==0:
                 anim = dmd.Animation().load(dmd_path+'crash.dmd')
                 self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=7)
                 self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer])
                 self.delay(name='clear_layer', event_type=None, delay=3, handler=self.clear_layer)

        def sw_upperLkicker_active_for_1s(self,sw):
             self.game.add_player_stats('ramps_made',1)
             self.check_ramps()
             # eject ball
             self.delay(name='ulkicker', event_type=None, delay=0.5, handler=self.game.effects.eject_ball, param='upperLkicker')
             # raise droptarget with delay to avoid AC-select conflict
             self.delay(name='raise_droptarget', event_type=None, delay=0.2, handler=self.game.effects.raise_droptarget)

        def sw_RrampEnter_active(self,sw):
             self.game.lampctrl.play_show('rampenter_show', False, 'None')
             # Only when no mode_enabled
             if not self.game.get_player_stats('mode_enabled'):
                 self.game.sound.play(self.game.assets.sfx_jumpApplause)
                 # play animation
                 self.ramp_text.set_text("") # clear text on rampenter
                 counter = self.game.user_settings['Gameplay (Feature)']['Jumpramps For Hurryup'] - self.game.get_player_stats('jumpramps_count')
                 self.ramp_text.set_text(" "+str(counter)+" jumps for hurry-up ") # set text on rampexit
                 anim = dmd.Animation().load(dmd_path+'nf_wheely.dmd')
                 self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=5)
                 self.animation_layer.add_frame_listener(-1, self.clear_layer)
                 self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer,self.ramp_text])
                 # clear animation and sound after 1sec if ball doesn't make it to rampexit switch
                 self.delay(name='clear_layer', event_type=None, delay=1.5, handler=self.clear_layer)
                 self.delay(name='clear_sound', event_type=None, delay=1.5, handler=self.clear_sound)

        def sw_RrampExit_active(self, sw):
             if self.millionplus:
                 self.score_millionplus()
             # Only when no mode_enabled
             if not self.game.get_player_stats('mode_enabled'):
                 self.game.effects.gi_blinking(schedule=0x0F0F0F0F, cycle_seconds=1)
                 self.game.add_player_stats('jumpramps_count',1)
                 self.game.score(50000)
                 counter = self.game.user_settings['Gameplay (Feature)']['Jumpramps For Hurryup'] - self.game.get_player_stats('jumpramps_count')
                 self.ramp_text.set_text(" "+str(counter)+" jumps for hurry-up ") # set text on rampexit
                 #if self.millionplus:
                 #    self.score_millionplus()
                 # cancel delay if ball hits rampexit switch (see sw_RrampEnter_active)
                 self.cancel_delayed('clear_layer')
                 self.cancel_delayed('clear_sound')
             # Always on rampexit
             self.add_miles(3,display=False)
             self.check_extra_ball()

        def sw_Rrollunder_active(self,sw):
             self.check_extra_ball()

        def sw_Lspinner_active(self, sw):
             #if self.game.switches.upperLkicker.time_since_change() > 3:
                 if self.spinner_miles:
                     self.spin_miles += 1
                     #set display text for animation
                     self.count_miles_layer.set_text('+'+str(self.spin_miles)+' mile')
                     self.add_miles(1,display=False)
                 self.game.sound.play(self.game.assets.sfx_spinner)
                 #score spinner value
                 self.game.score(self.spinner_value)
                 #count spinner turns
                 if self.mystery_ready == False:
                     self.spinner_turns += self.spinner_count
                     #play animation
                     self.play_spinner()
                     self.game.coils.Llightningbolt.pulse(25)
                     #check number of spinner turns
                     self.check_spinner_counter()
                 else:
                     self.game.coils.Rgate.schedule(0xffffffff, cycle_seconds=2, now=True)
                     self.play_mystery_ready()

        def sw_Lspinner_open_for_500ms(self,sw):
             self.spin_miles = 0
             return procgame.game.SwitchStop

###  TEST for animations. Use flipper to scroll to animations while ball is in shooterlane.

#        def sw_flipperLwR_active_for_500mss(self,sw):
#             if self.game.switches.shooterLane.is_active():
#                 animation = self.ani_list[self.index]
#                 self.cancel_delayed('clear_display')
#                 anim = dmd.Animation().load(dmd_path+animation)
#                 self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=7)
#                 self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.count_miles_layer])
#                 self.index += 1
#                 if self.index == 8:
#                     self.index = 0
#                 anim = dmd.Animation().load(dmd_path+'colortest.dmd')
#                 self.animation_layer = dmd.FrameLayer(opaque=False, frame=anim.frames[self.test_frame])
#                 self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer])
#                 self.test_frame +=1
#                 if self.test_frame == 6:
#                     self.test_frame = 0
#                 self.delay(name='clear_display', event_type=None, delay=4, handler=self.clear_layer)
