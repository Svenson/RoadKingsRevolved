#
# Extra Ball
#
# Control of extra ball
#
__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"

import procgame
from procgame import *

game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"


class Extra_Ball(game.Mode):

        def __init__(self, game):
            super(Extra_Ball, self).__init__(game, 90)

            self.game.lampctrl.register_show('succes', lampshow_path+"succes.lampshow")
            self.game.lampctrl.register_show('shoot_again_show', lampshow_path+"shoot_again.lampshow")

            #self.extraball_award = True # VIA MENU
            self.extraball_award = self.game.user_settings['Gameplay (Feature)']['Extraball Awarded']
            self.set_xball = self.game.user_settings['Gameplay (Feature)']['Roadkings Targets Xball']
            # Set roadkings targets extraball settings

        def clear_layer(self):
            self.layer = None

        def set_rk_xball(self):
            self.game.set_player_stats('roadkings_xball',self.set_xball)

        def reset_xball(self):
            self.game.set_player_stats('extraball_on', False)

        def collect(self, location='Rextraball'):
            self.cancel_delayed('reset_xball')
            anim = dmd.Animation().load(game_path+"dmd/jd_extra_ball.dmd")
            self.layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True,frame_time=4)
            self.game.sound.play(self.game.assets.sfx_extraBallCollected)
            #self.game.sound.play_voice('extra_ball_speech')
            self.game.effects.drive_lamp(location,'off')
            self.game.lampctrl.play_show('succes', False, 'None')
            if self.extraball_award:  # Menu instelling voor extraball of score
                self.game.effects.drive_lamp('cruiseAgain','smarton')
                self.game.extra_ball_count()
            else:
                self.game.score(5000000)
            self.reset_xball()
            self.delay(name='clear_layer', event_type=None, delay=4, handler=self.clear_layer)

        def lit(self, location='Rextraball'):
            self.game.sound.play(self.game.assets.sfx_extraBallLit)
            self.game.set_player_stats('extraball_on', True)
            self.game.effects.drive_lamp(location,'smarton')

        def hurryup(self, location='Rextraball'):
            self.game.sound.play(self.game.assets.sfx_extraBallLit)
            self.game.set_player_stats('extraball_on', True)
            self.game.effects.drive_lamp(location,'timeout',time=30)
            self.delay(name='reset_xball', event_type=None, delay=31, handler=self.reset_xball)
            self.game.sound.play_voice(self.game.assets.sfx_HurryUp)

        def shoot_again(self):
            self.game.sound.play(self.game.assets.sfx_shootAgain)
            self.game.lampctrl.play_show('shoot_again_show', False, 'None')
            anim = dmd.Animation().load(dmd_path+'shoot_again.dmd')
            self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=25)
            self.layer = self.animation_layer
            self.delay(name='clear_layer', event_type=None, delay=4, handler=self.clear_layer)
            self.delay(name='shoot_again', event_type=None, delay=2, handler=self.game.ball_starting)
            #self.game.ball_starting()
