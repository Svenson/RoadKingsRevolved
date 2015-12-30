#
# Jumpramp
#
# Hurry-up mode for right ramp
#
__author__="Pieter"
__date__ ="$32 Jan 2013 20:36:37 PM$"

import procgame
import locale
from procgame import *

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"


class Jumpramp(game.Mode):

        def __init__(self, game, priority):
            super(Jumpramp, self).__init__(game, priority)

            self.hurryup_layer = dmd.TextLayer(128/2, 12, self.game.fonts['num_14x10'], "center", opaque=False)

            self.game.lampctrl.register_show('hurryup_show', lampshow_path+"succes.lampshow")

            self.lamps_ramp = ['megaScore','Rtimelock','Rlock','Rextraball']

            self.hurryup_running = False
            #self.hurryup_value = 30000000 #VIA MENU
            self.hurryup_value = self.game.user_settings['Gameplay (Feature)']['Jumpramp Hurryup Value']

        def mode_started(self):
            print("Debug, Jumpramp Mode Started")
            self.prepare_hurryup()

        def mode_stopped(self):
            self.game.set_player_stats('game_feature_running',False)
            # close right gate
            self.game.coils.Rgate.disable()
            # restore all lamps
            self.game.update_lamps()
            # update missions
            self.game.base_game_mode.missions_modes.update_missions(10)
            print("Debug, Jumpramp Mode Ended")

        def mode_tick(self):
            pass

## lamps & animations

        def clear_lamps(self):
             # clear lamps right ramp
            for i in range(len(self.lamps_ramp)):
                  self.game.effects.drive_lamp(self.lamps_ramp[i],'off')

        def hurryup_lamps(self):
            # update lamps right ramp
            for i in range(len(self.lamps_ramp)):
                  self.game.effects.drive_lamp(self.lamps_ramp[i],'fast')

        def hurryup_animation(self):
             anim = dmd.Animation().load(dmd_path+'crossramp_hurryup.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=7)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.hurryup_layer])

        def inform_player(self):
             anim = dmd.Animation().load(dmd_path+'inform_ramp_hurryup.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=20)
             self.layer = self.animation_layer

        def hurryup_scored_ani(self):
             anim = dmd.Animation().load(dmd_path+'crossramp_hurryup_scored.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=10)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.hurryup_layer])

        def clear_layer(self):
             self.layer = None

## mode functions

        def prepare_hurryup(self):
             print ("prepare hurryup!")
             #stop music, play sound
             self.game.sound.fadeout_music(time_ms=250)
             self.game.sound.play(self.game.assets.sfx_hurryupStart)
             # open right gate
             self.game.coils.Rgate.enable()
             #play lampshow
             self.game.effects.gi_blinking(schedule=33003300, cycle_seconds=2)
             #play animation
             self.inform_player()
             #light lamps
             self.hurryup_lamps()
             # set hurryup status True
             self.hurryup_running = True
             # start after (delay) seconds
             self.delay(name='start_hurryup', event_type=None, delay=4, handler=self.start_hurryup)

        def start_hurryup(self):
             print ("start hurryup!")
             self.cancel_delayed('start_hurryup')
             #play music
             self.game.sound.play_music(self.game.assets.music_hurryupjumpRamp, loops=-1)
             #play animation
             self.hurryup_animation()
             #start countdown
             self.hurryup_countdown()

        def hurryup_countdown(self):
             # repeat call to itself to countdown hurryup value
             if self.hurryup_value > 500000:
                 self.hurryup_value -= 21700
                 self.delay(name='hurryup_countdown', event_type=None, delay=0.04, handler=self.hurryup_countdown)
                 self.hurryup_layer.set_text(locale.format("%d", self.hurryup_value, True))
             else:
                 self.game.sound.play(self.game.assets.sfx_hurryupMissed)
                 self.clear_hurryup()

        def score_hurryup(self):
             print ("score hurryup!")
             self.hurryup_running = False
             #stop hurryup music and play sound
             self.game.sound.stop_music()
             self.game.sound.play(self.game.assets.sfx_hurryupScored)
             #cancel hurryup countdown
             self.cancel_delayed('hurryup_countdown')
             #play lampshow
             self.game.lampctrl.play_show('hurryup_show', False, 'None')
             #play animation
             self.hurryup_scored_ani()
             #add score
             self.game.score(self.hurryup_value)
             # eject ball after delay
             self.delay(name='eject_ball', event_type=None, delay=2, handler=self.game.effects.eject_ball)
             # clear hurryup after delay
             self.delay(name='clear_hurryup', event_type=None, delay=3, handler=self.clear_hurryup)

        def clear_hurryup(self):
             print ("clear hurryup!")
             self.hurryup_running = False
             # stop hurryup music
             self.game.sound.stop_music()
             # cancel delays in case its running
             self.cancel_delayed('start_hurryup')
             self.cancel_delayed('hurryup_countdown')
             # restart main theme music
             self.game.assets.rk_play_music()
             # clear items
             self.clear_layer()
             self.clear_lamps()
             # remove from mode qeue
             self.game.modes.remove(self)

        def check_extra_ball(self):
             if self.game.get_player_stats('extraball_on'):
                 # collect extra ball
                 self.game.extra_ball.collect()

## switches

        def sw_outhole_active(self, sw):
             if self.hurryup_running == True:
                 self.clear_hurryup()

        def sw_RrampExit_active(self, sw):
             self.game.effects.gi_blinking(schedule=0x0F0F0F0F, cycle_seconds=1)
             if self.hurryup_running == True:
                 self.score_hurryup()
             if self.game.get_player_stats('million_plus'): #million plus is stackable
                 self.game.base_game_mode.generalplay.score_millionplus()
             # check for possible extra ball
             self.game.base_game_mode.generalplay.check_extra_ball()
             return procgame.game.SwitchStop

        def sw_upperLkicker_active(self,sw):
             # raise droptarget with delay to avoid AC-select conflict
             self.delay(name='raise_droptarget', event_type=None, delay=1, handler=self.game.effects.raise_droptarget)
             return procgame.game.SwitchStop

        def sw_Leject_active_for_100ms(self,sw):
             self.game.effects.eject_ball('Leject')
             return procgame.game.SwitchStop