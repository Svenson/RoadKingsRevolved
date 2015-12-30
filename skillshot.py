#
# skillshot
# Control for skillshot and superskillshot
#
__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"


import procgame
import locale
from procgame import *
from random import *
import random

#all necessary paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"


class Skillshot(game.Mode):

        def __init__(self, game, priority):
            super(Skillshot, self).__init__(game, priority)

            self.text_layer = dmd.TextLayer(98, 12, self.game.fonts['num_09Bx7'], "center", opaque=False)
            self.text_layer_superskill1 = dmd.TextLayer(90, 6, self.game.fonts['07x5'], "center", opaque=False)
            self.text_layer_superskill2 = dmd.TextLayer(90, 17, self.game.fonts['num_09Bx7'], "center", opaque=False)

            self.game.lampctrl.register_show('rev_show', lampshow_path+"rev_skill.lampshow")

            self.superskilllamps = ['Ctimelock','Clock']
            self.lanelamps = ['lane1','lane2']
            self.skill_active = True
            self.superskill_active = False
            self.choice = 0
            #self.skill_timer =7 #VIA MENU
            self.skill_timer = self.game.user_settings['Gameplay (Feature)']['Skillshot Timer']
            self.skill_value_start = 100000
            self.skill_value_boost = 100000
            self.super_skill_value_start = 250000
            self.super_skill_value_boost = 250000

        def mode_started(self):
            print("Debug, Skilshot Mode Started")
            #load player specific data
            self.count = self.game.get_player_stats('skillshots')
            # calculate value
            self.skill_value = self.skill_value_boost*self.count +self.skill_value_start
            self.super_skill_value=self.super_skill_value_boost*self.count + self.super_skill_value_start
            self.start_skill()

        def mode_stopped(self):
            #save player specific data
            self.game.set_player_stats('skillshots',self.count)
            self.game.update_lamps()
            print("Debug, Skillshot Mode Ended")

## lamps & animation

        def activate_skill_lamps(self):
             self.game.effects.drive_lamp(self.lanelamps[self.choice],'medium')

        def activate_superskill_lamps(self):
             for i in range(len(self.superskilllamps)):
                self.game.effects.drive_lamp(self.superskilllamps[i],'superfast')
             self.game.effects.drive_flasher('showroomFlash','fast')

        def clear_superskill_lamps(self):
            for i in range(len(self.superskilllamps)):
                self.game.effects.drive_lamp(self.superskilllamps[i],'off')
            self.game.effects.drive_flasher('showroomFlash','off')

        def clear_lamps(self):
            self.game.effects.drive_lamp(self.lanelamps[self.choice],'off')
            self.clear_superskill_lamps()
            self.layer=None

        def update_lamps(self):
            pass

        def super_skill_lampshow(self):
             self.game.sound.play(self.game.assets.sfx_skillRev)
             self.game.lampctrl.play_show('rev_show', False, self.after_rev_lamps)

        def after_rev_lamps(self):
             self.game.base_game_mode.missions_modes.update_lamps()
             self.game.base_game_mode.generalplay.update_miles_lamps()

        def play_animation(self, skill_level):
             #select skill value
             if skill_level == 'normal_skill':
                 self.text_layer.set_text(locale.format("%d",self.skill_value,True),blink_frames=2)
             elif skill_level == 'super_skill':
                 self.text_layer.set_text(locale.format("%d",self.super_skill_value,True),blink_frames=2)
             #set layers for animation
             anim = dmd.Animation().load(dmd_path+'skillshot.dmd')
             self.bgnd_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=7)
             self.layer = dmd.GroupedLayer(128, 32, [self.bgnd_layer, self.text_layer])

        def play_animation_rev(self):
             self.text_layer_superskill1.set_text("SUPER SKILLSHOT")
             self.text_layer_superskill2.set_text("ENABLED")
             #set layers for animation
             anim = dmd.Animation().load(dmd_path+'cylinder_short.dmd')
             self.cylinder_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=3)
             self.layer = dmd.GroupedLayer(128, 32, [self.cylinder_layer, self.text_layer_superskill1,  self.text_layer_superskill2])

## mode functions

        def start_timer(self):
             # start timer
             self.delay(name='grace_time', event_type=None, delay=self.skill_timer, handler=self.grace_time)

        def start_skill(self):
             #generate random lamp from list
             #self.choice = random.randrange(0, len(self.lanelamps),1)
             self.choice = random.randint(0, len(self.lanelamps)-1)
             print("lamp_keuze: "+self.lanelamps[self.choice])
             self.activate_skill_lamps()

        def lanes(self,id):
            if self.skill_active == True:
               # skillshot is only once active (to prevent from double hit via bumpers)
               self.skill_active = False
               if id == self.choice:
                  # skillshot scored
                  self.game.sound.play(self.game.assets.sfx_skillshotMade)
                  self.play_animation('normal_skill')
                  self.game.score(self.skill_value)
                  # raise counter
                  self.count+=1
                  # update missions
                  self.game.base_game_mode.missions_modes.update_missions(1)
                  # clear mode after delay
                  self.delay(name='clear', event_type=None, delay=2, handler=self.clear)
                  # Add bonus X
                  self.game.add_player_stats('bonus_x',1)
               else:
                  #self.game.sound.play('skillshot_missed')
                  self.clear()

        def activate_superskill(self):
             print("Super skilshot activated")
             self.play_animation_rev()
             self.super_skill_lampshow()
             self.activate_superskill_lamps()
             self.superskill_active = True

        def deactivate_superskill(self):
             print("Super skilshot deactivated")
             self.clear_superskill_lamps()
             self.superskill_active = False
             self.layer=None

        def start_superskill(self):
             self.game.coils.Lgate.pulse(0)

        def super_skill(self):
            # cancel delays
            self.cancel_delayed('grace_time')
            self.cancel_delayed('clear')
            self.skill_active = False

            # play sound & animation
            self.game.sound.play(self.game.assets.sfx_superskillMade)
            self.play_animation('super_skill')
            self.clear_superskill_lamps()

            # clear mode after delay (call drain_save first)
            self.delay(name='drain_save', event_type=None, delay=2, handler=self.drain_save)

            # raise counter
            self.count+=1

            # add score
            self.game.score(self.super_skill_value)

            # update missions
            self.game.base_game_mode.missions_modes.update_missions(1)

            # raise 2 crossramps for superskillshot
            self.game.base_game_mode.crossramp.raise_crossramps(2)

        def drain_save(self):
             # add time to ballsaver in case of SDTM from Ceject
             #self.game.ball_save.add(add_time=3, allow_multiple_saves=False)
             #self.game.ball_save.start(num_balls_to_save=1, time=10, now=True, allow_multiple_saves=False)
             self.clear()

        def grace_time(self):
             self.clear_lamps()
             self.delay(name='clear', event_type=None, delay=1.5, handler=self.clear)

        def clear(self):
             self.clear_lamps()
             self.layer = None
             self.superskill_active = False
             self.game.coils.Lgate.disable()
             self.game.effects.eject_ball(location='Ceject', ball_save=True)
             self.callback()

## switches

        def sw_lane1_active(self, sw):
             self.lanes(0)
             return procgame.game.SwitchStop

        def sw_lane2_active(self, sw):
             self.lanes(1)
             return procgame.game.SwitchStop

        def sw_Ceject_active(self,sw):
             return procgame.game.SwitchStop

        def sw_Ceject_active_for_250ms(self,sw):
             if self.superskill_active == True:
                 self.super_skill()

        def sw_CrampEnter_active(self,sw):
             self.clear()

        def sw_shooterLane_open_for_20ms(self,sw):
             if self.game.ball_starting:
                  # start timer
                  self.start_timer()
                  # check for superskillshot
                  if self.superskill_active == True:
                       self.start_superskill()

        # end mode when a ball drains
        def sw_outhole_active(self,sw):
             self.clear()

