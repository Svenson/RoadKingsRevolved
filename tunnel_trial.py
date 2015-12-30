#
# Tunnel Trial
#
# Make (x) shots trough tunnel within (x) seconds.
# Each shot scores 1Mil. last shot is time remaining * time_value.
#

__author__="Pieter"
__date__ ="$03 dec 2012 20:36:37 PM$"


import procgame
import locale
from procgame import *

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"


class Tunneltrial(game.Mode):

        def __init__(self, game, priority):
            super(Tunneltrial, self).__init__(game, priority)

            self.title_layer = dmd.TextLayer(128/2, 4, self.game.fonts['07x5'], "center", opaque=False)
            self.time_layer = dmd.TextLayer(128/2, 16, self.game.fonts['num_14x10'], "center", opaque=False)
            self.hit_layer = dmd.TextLayer(128/2, 20, self.game.fonts['num_09Bx7'], "center", opaque=False)

            self.game.lampctrl.register_show('rightloop', lampshow_path+"tunneltrial.lampshow")

            self.hit_value = 1000000 #VIA MENU
            self.time_value = 500000 #VIA MENU
            self.tunneltrial_time = 40 #VIA MENU
            self.shots_togo = 3 #VIA MENU
            self.hit_spinner = True

            self.animation_status = 'ready'

        def reset(self):
            pass

        def mode_started(self):
            print("Debug, Tunneltrial Mode Started")
            #stop current music
            self.game.assets.rk_play_music('stop')
            #stackable or not??
            self.game.set_player_stats('game_feature_running',True)
            self.tunneltrial_time = self.game.user_settings['Gameplay (Feature)']['Tunnel Trial Timer']
            self.shots_togo = self.game.user_settings['Gameplay (Feature)']['Tunnel Trial Shots']
            self.game.base_game_mode.rampmove.move_ramp('up')
            self.game.coils.Lgate.enable()
            self.update_lamps()
            self.game.effects.gi_off()
            self.game.sound.play_music(self.game.assets.music_hurryupTheme, loops=-1)
            self.start_countdown()
            self.play_countdown()

        def mode_stopped(self):
            self.game.set_player_stats('game_feature_running',False)
            self.game.base_game_mode.rampmove.move_ramp('down')
            # close gate
            self.game.coils.Lgate.disable()
            # restart main theme music
            self.game.assets.rk_play_music()
            # turn gi and lamps on
            self.game.effects.gi_on()
            self.game.update_lamps()
            print("Debug, Tunneltrial Mode Ended")

        def mode_tick(self):
            pass

## lamps & animations

        def update_lamps(self):
             self.game.effects.drive_lamp('megaScore','medium')

        def clear_lamps(self):
             self.game.effects.drive_lamp('megaScore','off')

        def clear_layer(self):
             self.layer = None

        def play_countdown(self):
            if self.animation_status=='ready':
              self.title_layer.set_text('TUNNEL TRIAL')
              anim = dmd.Animation().load(dmd_path+'tunneltrial_bgnd.dmd')
              self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=5)
              self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer, self.time_layer])

        def play_tunnel(self):
            if self.animation_status=='ready':
                anim = dmd.Animation().load(dmd_path+'tunneltrial_hit.dmd')
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=8)
                self.animation_layer.add_frame_listener(-1, self.animation_ended)
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer, self.hit_layer])
                self.animation_status = 'running'

        def animation_ended(self):
            self.animation_status = 'ready'
            # No countdown if shots is 0
            if self.shots_togo > 1:
                self.play_countdown()

## mode functions

        def start_countdown(self):
            #Countdown via repeated call to itself with delaytime 1sec,
            if self.tunneltrial_time == 0:
                self.game.sound.play(self.game.assets.sfx_hurryupMissed)
                self.clear_countdown()
            else:
                self.delay(name='start_countdown', event_type=None, delay=1, handler=self.start_countdown)
                self.game.lampctrl.play_show('rightloop', False, 'None')
                self.game.coils.rearFlash_upLeftkicker.schedule(0x00FF00FF, cycle_seconds=1, now=False) #bikesFlash_dropTarget / rearFlash_upLeftkicker

            # set counter value on textlayer
            self.time_layer.set_text(str(self.tunneltrial_time))

            # decrease counter
            self.tunneltrial_time -=1

        def clear_countdown(self):
             self.game.effects.gi_blinking(schedule=33333333, cycle_seconds=2)
             self.cancel_delayed('start_countdown')
             self.clear_layer()
             self.game.sound.stop_music()
             self.game.modes.remove(self)

        def reset_spinner(self):
             self.hit_spinner = True
             self.hit_layer.set_text('')

## switches

        def sw_Rrollunder_active(self,sw):
             if self.shots_togo == 1:
                 #play sound
                 self.game.sound.play(self.game.assets.sfx_hurryupScored)
                 self.game.coils.midBikeFlash_rampDown.schedule(0x00FF00FF, cycle_seconds=2, now=False)
                 #stop spinner score
                 self.hit_spinner = False
                 #count shots to 0
                 self.shots_togo -= 1
                 #calculate value
                 trial_value = self.time_value*self.tunneltrial_time
                 #set display text for animation
                 self.title_layer.set_text('TRIAL COMPLETED')
                 self.hit_layer.set_text(locale.format("%d", trial_value, True))
                 #add value to score
                 self.game.score(trial_value)
                 #play animation
                 self.play_tunnel()
                 #clear after delay
                 self.delay(name='clear_countdown', event_type=None, delay=3, handler=self.clear_countdown)
             else:
                 self.game.sound.play(self.game.assets.sfx_tunnelHit)
                 #play animation
                 self.play_tunnel()


        def sw_Lspinner_active(self, sw):
            if self.game.switches.Rrollunder.time_since_change() < 1:
              if self.hit_spinner:
                  self.hit_spinner = False
                  #score spinner value
                  self.game.score(self.hit_value)
                  #count shots
                  self.shots_togo -= 1
                  #set display text for animation
                  self.hit_layer.set_text(locale.format("%d", self.hit_value, True))
                  self.title_layer.set_text(" "+str(self.shots_togo)+" shots to go ")
                  self.game.coils.midBikeFlash_rampDown.pulse(30)
                  self.game.coils.Llightningbolt.pulse(20)
                  #return procgame.game.SwitchStop
                  self.delay(name='reset_spinner', event_type=None, delay=2, handler=self.reset_spinner)


        # end mode when a ball drains
        def sw_outhole_active(self,sw):
             self.clear_countdown()

        def sw_bumperL_active(self,sw):
             self.game.score(110)
             return True
        def sw_bumperU_active(self,sw):
             self.game.score(110)
             return True
        def sw_bumperR_active(self,sw):
             self.game.score(110)
             return True
        def sw_bumperD_active(self,sw):
             self.game.score(110)
             return True

        # Prevent ramp_move during Tunnel Trial
        def sw_Leject_active(self, sw):
             self.delay(name='ejectball', event_type=None, delay=0.2, handler=self.game.effects.eject_ball)
             return procgame.game.SwitchStop

        def sw_Ceject_active(self, sw):
             self.delay(name='ejectball', event_type=None, delay=0.2, handler=self.game.effects.eject_ball)
             return procgame.game.SwitchStop
