#
# kickback
#
# Game mode that controls the kickback
#
__author__="Steven"
__date__ ="$Sep 11, 2012 16:36:37 PM$"


import procgame
import locale
from procgame import *
import random

game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"


class Kickback(game.Mode):

        def __init__(self, game, priority):
            super(Kickback, self).__init__(game, priority)

            anim_kb = dmd.Animation().load(dmd_path+"kickback.dmd")
            self.kb_layer = dmd.AnimatedLayer(frames=anim_kb.frames, opaque=False, repeat=False, hold=True,frame_time=1)
            anim_pk = dmd.Animation().load(dmd_path+"powerkick.dmd")
            self.pk_layer = dmd.AnimatedLayer(frames=anim_pk.frames, opaque=False, repeat=False, hold=True,frame_time=2)
            anim_crash = dmd.Animation().load(dmd_path+'crash.dmd')
            self.crash_layer = dmd.AnimatedLayer(frames=anim_crash.frames, opaque=False, repeat=False, hold=True, frame_time=5)

            self.title_layer = dmd.TextLayer(128/2, 12, self.game.fonts['num_09Bx7'], "center", opaque=True)

            self.kickback_state = 'normal'
            self.kickback_ready = True
            self.grace_time = 3

        def mode_started(self):
            print("Debug, Kickback Mode Started")
            self.update_kickback()

        def mode_stopped(self):
            # substract superkickback if ball is lost
            if self.kickback_state=='super':
                self.game.set_player_stats('kickback','normal')
            self.clear_lamps()
            print("Debug, Kickback Mode Ended")

## lamps & Animations

        def update_lamps(self, effect='on'):
            if self.kickback_state=='normal':
                    self.game.effects.drive_lamp('kickback',effect)
            elif self.kickback_state=='super':
                    self.game.lamps.kickback.schedule(schedule=0xfffffff0)
            else:
                    self.game.effects.drive_lamp('kickback','off')

        def clear_lamps(self):
             self.game.effects.drive_lamp('kickback','off')

        def play_animation_kickback(self):
            self.layer = self.kb_layer
            self.delay(name='clear_layer', event_type=None, delay=2.5, handler=self.clear_layer)

        def play_animation_powerkick(self):
            self.layer = self.pk_layer
            self.delay(name='clear_layer', event_type=None, delay=2.5, handler=self.clear_layer)

        def clear_layer(self):
            self.layer = None

## mode functions

        def play_sound(self):
            if self.kickback_state=='super':
                self.game.sound.play(self.game.assets.sfx_powerkick)
            elif self.kickback_state=='normal':
                self.game.sound.play(self.game.assets.sfx_kickback)
            else:
                self.game.sound.play(self.game.assets.sfx_crash)

        def update_kickback(self):
             self.kickback_state = self.game.get_player_stats('kickback')
             self.update_lamps()

        def raise_kickback(self): # called from other modes to raise kickback
             self.kickback_state = self.game.get_player_stats('kickback')
             if self.kickback_state == False:
                 self.kickback_state = 'normal'
             elif self.kickback_state == 'normal':
                   self.kickback_state = 'super'
             else:
                   self.kickback_state = 'super'
             self.game.set_player_stats('kickback',self.kickback_state)
             self.update_lamps('smarton')

        def lower_kickback(self): # called from other modes to lower kickback
             if self.kickback_state == 'super':
                 self.kickback_state = 'normal'
             elif self.kickback_state == 'normal':
                   self.kickback_state = False
             else:
                   self.kickback_state = False
             self.game.set_player_stats('kickback',self.kickback_state)
             self.update_lamps()

        def kick_back(self):

            # super kickback
            if self.kickback_state == 'super':
                self.game.coils.kickback.pulse(60)
                self.game.score(100000)
                # play animation
                self.delay(name='play_animation_powerkick', event_type=None, delay=0.2, handler=self.play_animation_powerkick)
                if not self.game.get_player_stats('game_feature_running'):
                    self.game.ball_save.start(num_balls_to_save=1, time=3, now=True, allow_multiple_saves=False) # Activate ball save if kickback doesn't work (not during multiball)

            # regular kickback
            elif self.kickback_state == 'normal':
                self.game.coils.kickback.pulse(30)
                self.game.score(10000)
                # play animation
                self.delay(name='play_animation_kickback', event_type=None, delay=0.2, handler=self.play_animation_kickback)
                if not self.game.get_player_stats('game_feature_running'):
                    self.game.ball_save.start(num_balls_to_save=1, time=2, now=True, allow_multiple_saves=False)  # Activate ball save if kickback doesn't work (not during multiball)

            # no kickback
            else:
                 self.game.score(1000)

        def kickback_reset(self):
             self.kickback_ready = True

        def grace_period(self):
             self.game.effects.drive_lamp('kickback','medium')
             self.delay(name='lower_kickback', event_type=None, delay=self.grace_time, handler=self.lower_kickback)

## switches

        def sw_outlaneL_active(self, sw):
             # Check for kickback
             if self.kickback_ready:
                 self.kick_back()
                 self.kickback_ready = False
                 self.delay(name='kickback_reset', event_type=None, delay=0.2, handler=self.kickback_reset)
                 if self.kickback_state:
                     self.grace_period()

             # Display animation if ball is lost (e.g. no kickback, no ball_save, no balls in play)
             if self.game.trough.num_balls_in_play==1 and self.kickback_state== False and self.game.ball_save.timer==0:
                 self.layer = self.crash_layer
                 self.delay(name='clear_layer', event_type=None, delay=2, handler=self.clear_layer)

             self.play_sound()

