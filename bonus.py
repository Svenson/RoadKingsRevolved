#
# Bonus
#
# Calculates end-of-ball bonus
#
__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"


import procgame
import locale
from procgame import *

#all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"


class Bonus(game.Mode):
    """docstring for Bonus"""

    def __init__(self, game, priority):
        super(Bonus, self).__init__(game, priority)

        self.bonus_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'bonus_bgnd.dmd').frames[0])
        self.title_layer = dmd.TextLayer(128/2, 4, self.game.fonts['num_09Bx7'], "center")
        self.value_layer = dmd.TextLayer(128/2, 15, self.game.fonts['num_14x10'], "center")
        self.bonus_layer = dmd.GroupedLayer(128, 32, [self.bonus_bgnd, self.title_layer, self.value_layer])

        self.game.lampctrl.register_show('bonus_show', lampshow_path+"bonus.lampshow")

        self.delay_time = 2.5
        self.bonus_x = 1
        self.x_display = ''


    def mode_started(self):
        print("Debug, Bonus Mode Started")
        # check for flippersbuttons pressed at start for faster bonuscount
        if self.game.switches.flipperLwR.is_active() and self.game.switches.flipperLwL.is_active():
                self.delay_time = 0.250
                self.game.coils.flipperEnable.disable()
        else:
                self.delay_time = 2.5

    def mode_stopped(self):
        self.game.coils.flipperEnable.enable()
        print("Debug, Bonus Mode Ended")

    def mode_tick(self):
        ## Hit both flippers for faster bonuscount
        if self.game.switches.flipperLwR.is_active() and self.game.switches.flipperLwL.is_active():
            self.delay_time = 0.250
            # disable flippers
            self.game.coils.flipperEnable.disable()

## mode functions
    def bonus_effects(self):
            self.game.lampctrl.play_show('bonus_show', False, 'None')

    def get_bonus_miles(self):
            miles = self.game.get_player_stats('miles_collected') * 10000
            return miles

    def get_bonus_crossramps(self):
            crossramps =  self.game.get_player_stats('crossramps_made') * 10000
            return crossramps

    def get_bonus_jumpramps(self):
            jumpramps =  self.game.get_player_stats('ramps_made') * 50000
            return jumpramps

    def get_bonus_x(self):
            bonus_x = self.game.get_player_stats('bonus_x')
            return bonus_x

    def calculate(self,callback):
            self.callback = callback
            self.base()

    def base(self):

            self.game.sound.play_music(self.game.assets.music_bonusTune, loops=1)
            self.bonus_x = self.get_bonus_x()
            self.total_base = self.get_bonus_miles()

            if self.bonus_x > 1:
                self.x_display = ' X'+str(self.bonus_x)
            else:
                self.x_display=''

            self.title_layer.set_text('BONUS MILES'+ self.x_display)
            self.value_layer.set_text(locale.format("%d", self.total_base, True))
            self.layer = self.bonus_layer

            # only play lighteffects if bonuscount is not 'pressed away'.
            if self.delay_time == 2.5:
                self.bonus_effects()
            self.delay(name='bonus_jumpramps', event_type=None, delay=self.delay_time, handler=self.crossramps)

    def crossramps(self):

          self.total_crossramps = self.get_bonus_crossramps()
          if self.total_crossramps > 0:

            self.title_layer.set_text('CROSSRAMPS'+ self.x_display)
            self.value_layer.set_text(locale.format("%d", self.total_crossramps, True))
            self.layer = self.bonus_layer

            # only play lighteffects if bonuscount is not 'pressed away'.
            if self.delay_time == 2.5:
                self.bonus_effects()
            self.delay(name='bonus_total', event_type=None, delay=self.delay_time, handler=self.jumpramps)

          else:
              self.jumpramps()

    def jumpramps(self):

          self.total_jumpramps = self.get_bonus_jumpramps()
          if self.total_jumpramps > 0:

            self.title_layer.set_text('JUMPRAMPS'+ self.x_display)
            self.value_layer.set_text(locale.format("%d", self.total_jumpramps, True))
            self.layer = self.bonus_layer

            # only play lighteffects if bonuscount is not 'pressed away'.
            if self.delay_time == 2.5:
                self.bonus_effects()
            self.delay(name='bonus_total', event_type=None, delay=self.delay_time, handler=self.total)

          else:
              self.total()

    def total(self):

            total_bonus = (self.total_base * self.bonus_x) + (self.total_jumpramps * self.bonus_x)
            self.title_layer.set_text('TOTAL BONUS')
            self.value_layer.set_text(locale.format("%d", total_bonus, True))
            self.layer = self.bonus_layer

            self.game.score(total_bonus)
            self.bonus_effects()

            # Repeat bonuscount if bonushold on last ball
            if self.game.get_player_stats('hold_bonusx') and (self.game.ball == self.game.balls_per_game):
                # reset hold_bonusx
                self.game.set_player_stats('hold_bonusx',False)
                self.delay(name='bonus_hold', event_type=None, delay=self.delay_time, handler=self.hold_bonusx)
            else:
                self.game.sound.fadeout_music(250)
                self.delay(name='bonus_callback', event_type=None, delay=self.delay_time, handler=self.callback)

    def hold_bonusx(self):

            self.game.sound.fadeout_music(500)
            self.title_layer.set_text('HOLD BONUS X')
            self.value_layer.set_text(self.x_display)
            self.layer = self.bonus_layer

            self.delay(name='bonus_hold', event_type=None, delay=1, handler=self.base)
## switches
   ## Hit both flippers for faster bonuscount in mode_tick

