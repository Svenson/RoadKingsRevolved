#
# Quick multiball (Spinner millions)
# Control for countdown and quick multiball mode
#

__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"


import procgame
import locale
from procgame import *

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"


class Quickmb(game.Mode):

        def __init__(self, game, priority):
            super(Quickmb, self).__init__(game, priority)

            self.title_layer = dmd.TextLayer(90, 4, self.game.fonts['07x5'], "center", opaque=False)
            self.value_layer = dmd.TextLayer(90, 16, self.game.fonts['num_14x10'], "center", opaque=False)
            self.spinner_layer = dmd.TextLayer(90, 16, self.game.fonts['num_14x10'], "center", opaque=False)

            self.game.lampctrl.register_show('leftloop', lampshow_path+"leftloop.lampshow")

            self.counter = 0
            #self.spinner_value = 200000 #VIA MENU
            self.spinner_value = self.game.user_settings['Gameplay (Feature)']['Quick Mball Spinner Value']
            self.spinner_turns = 0
            self.quickmb_running = False
            self.animation_status = 'ready'


        def mode_started(self):
            print("Debug, Quickmb Mode Started")
            self.quickmb_running = False
            self.counter = 10
            self.game.set_player_stats('game_feature_running',True)
            self.update_lamps()
            self.game.effects.gi_off()
            self.game.sound.play(self.game.assets.sfx_qm_clockTick)
            self.display_countdown()
            # start when ball is out of bumpers
            self.bumper()

        def mode_stopped(self):
            self.game.set_player_stats('game_feature_running',False)
            self.clear_lamps()
            self.clear_layer()
            # close both gates
            self.game.coils.Lgate.disable()
            self.game.coils.Rgate.disable()
            # turn gi on and update game lamps
            self.game.effects.gi_on()
            self.game.update_lamps()
            # restart main theme music
            self.game.assets.rk_play_music()
            print("Debug, Quickmb Mode Ended")

## lamps & animations

        def update_lamps(self):
             if self.quickmb_running == False:
                 self.game.effects.drive_lamp('Llock','medium')
                 self.game.effects.drive_flasher('workshopFlash','medium',seconds_on=10)
                 self.game.effects.drive_lamp('Clock','medium')
                 self.game.effects.drive_flasher('showroomFlash','medium',seconds_on=10)
                 if self.game.get_player_stats('ramp_state') == False:
                     self.game.effects.drive_lamp('Rlock','medium')
             else:
                 self.game.effects.all_flashers_off()
                 self.game.effects.drive_lamp('bonusholdWL','medium')
                 self.game.effects.drive_lamp('megaScore','medium')

        def clear_lamps(self):
             self.game.effects.all_flashers_off()
             self.game.effects.drive_lamp('Llock','off')
             self.game.effects.drive_lamp('Clock','off')
             self.game.effects.drive_lamp('Rlock','off')
             self.game.effects.drive_lamp('bonusholdWL','off')
             self.game.effects.drive_lamp('megaScore','off')

        def clear_layer(self):
             self.layer = None

        def display_countdown(self):
             self.title_layer.set_text('QUICK M-BALL')
             self.value_layer.set_text('10')
             self.display_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'timer.dmd').frames[0])
             self.layer = dmd.GroupedLayer(128, 32, [self.display_layer, self.title_layer, self.value_layer])

        def play_countdown(self):
             self.title_layer.set_text('QUICK M-BALL')
             anim = dmd.Animation().load(dmd_path+'timer.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=13)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer, self.value_layer])

        def play_spinner(self,opaque=False, repeat=False, hold=False, frame_time=8):
            if self.animation_status=='ready':
                anim = dmd.Animation().load(dmd_path+'spinning.dmd')
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=5)
                self.animation_layer.add_frame_listener(-1, self.animation_ended)
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.spinner_layer])
                self.animation_status = 'running'

        def animation_ended(self):
            self.animation_status = 'ready'
            self.layer = None

        def inform_player(self):
             anim = dmd.Animation().load(dmd_path+'shoot_spinner.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=20)
             self.layer = self.animation_layer

## mode functions

        def start_countdown(self):
            #Countdown via repeated call to itself with delaytime 1sec,
            #if time is up, start grace period before stop and remove mode (end_countdown)
            if self.counter == 0:
                #start grace period
                self.delay(name='grace_period', event_type=None, delay=2, handler=self.end_countdown)
            else:
                self.delay(name='start_countdown', event_type=None, delay=1, handler=self.start_countdown)
                self.game.coils.rearFlash_upLeftkicker.schedule(0x00FF00FF, cycle_seconds=1, now=False)
                # set counter value on textlayer
                self.value_layer.set_text(str(self.counter))
                # decrease counter
                self.counter -=1

        def end_countdown(self):
             self.counter = 10 # reset counter
             self.game.modes.remove(self)

        def clear_countdown(self):
             print("Call clear countdown")
             self.cancel_delayed('start_countdown')
             self.cancel_delayed('grace_period')
             self.clear_layer()
             self.clear_lamps()
             self.game.sound.stop_music()
             self.game.effects.gi_blinking(schedule=33333333, cycle_seconds=2)
             self.delay(name='start_quickmb', event_type=None, delay=2, handler=self.start_quickmb)

        def start_quickmb(self):
             #setup quick multiball
             self.quickmb_running = True
             #self.game.coils.Lgate.pulse(0)
             self.game.coils.Rgate.pulse(0)
             self.inform_player()
             #launch ball
             self.game.trough.launch_balls(1)
             #self.game.effects.gi_on()
             #play music
             self.game.sound.play_music(self.game.assets.music_quickMultiball, loops=-1)
             #play lightshow
             self.game.lampctrl.play_show('leftloop', False, 'None')

        def bumper(self):
             # start countdown after ball is out of bumper area (for 1s)
             if self.quickmb_running == False:
                 self.cancel_delayed('bumper_time')
                 self.quickmb_running = 'bumpers_stopped'
                 self.delay(name='bumper_time', event_type=None, delay=1.5, handler=self.bumpers_stopped)
             else:
                 pass

        def bumpers_stopped(self):
             print("Call bumpers stopped")
             self.game.sound.stop(self.game.assets.sfx_qm_clockTick, fade_ms=100)
             self.game.sound.play_music(self.game.assets.music_qm_clockTickAlarm, loops=0)
             self.start_countdown()
             self.play_countdown()

## switches

        def sw_Leject_active(self, sw):
            # Start quick multiball, block switchevents to other modes during multiball intro
            if self.quickmb_running != True:
                self.clear_countdown()
                return procgame.game.SwitchStop

        def sw_Ceject_active(self, sw):
            if self.quickmb_running != True:
                self.clear_countdown()
                return procgame.game.SwitchStop

        def sw_upperLkicker_active(self, sw):
            if self.quickmb_running != True:
                return procgame.game.SwitchStop

        def sw_RrampExit_active(self, sw):
            if self.quickmb_running != True:
                self.clear_countdown()
                return procgame.game.SwitchStop

        # make sure ball is plunged before starting multiball
        def sw_shooterLane_open_for_1s(self,sw):
             #self.clear_layer()
             self.game.effects.eject_ball(location='all', ball_save=True)
             self.game.coils.Lgate.pulse(0)
             self.update_lamps()

        def sw_Lspinner_active(self, sw):
            if self.quickmb_running == True:
                self.game.sound.play(self.game.assets.sfx_qm_spinner)
                #score spinner value
                self.game.score(self.spinner_value)
                #count spinner turns
                self.spinner_turns += 1
                #calculate score to display
                self.display_score = self.spinner_turns * self.spinner_value
                #set display text for animation
                self.spinner_layer.set_text(locale.format("%d", self.display_score, True))
                #play animation
                self.play_spinner()
                self.game.coils.midBikeFlash_rampDown.pulse(30)
                self.game.coils.Llightningbolt.pulse(25)
                self.game.coils.workshopFlash.pulse(30)
                #return procgame.game.SwitchStop

        # reset spinner counter after 500ms
        def sw_Lspinner_open_for_500ms(self,sw):
             self.spinner_turns = 0
             return procgame.game.SwitchStop

        # end mode when a ball drains
        def sw_outhole_active(self,sw):
             self.quickmb_running = False
             self.game.sound.stop(self.game.assets.sfx_qm_clockTick, fade_ms=100)
             self.game.sound.stop_music()
             self.game.modes.remove(self)

        def sw_bumperL_active(self,sw):
             self.bumper()
             #return True

        def sw_bumperU_active(self,sw):
             self.bumper()
             #return True

        def sw_bumperR_active(self,sw):
             self.bumper()
             #return True

        def sw_bumperD_active(self,sw):
             self.bumper()
             #return True

        def sw_lane1_active(self, sw):
             self.bumper()
             #return True

        def sw_lane2_active(self, sw):
             self.bumper()
             #return True