#
# Roadkings mode
#
# Wizard Mode (end game)
# 2-ball multiball
# Collect Jackpots
#

__author__="Pieter"
__date__ ="$27 Feb 2013 21:21:21 PM$"

from procgame import *
import locale
from random import *
import random

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Roadkings(game.Mode):

        def __init__(self, game, priority):
             super(Roadkings, self).__init__(game, priority)

             #self.info_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'sterren.dmd').frames[0])
             anim = dmd.Animation().load(dmd_path+'lightningDMD.dmd') #lightning_dmd, sterren.dmd
             self.info_bgnd = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=8)
             self.item_layer = dmd.TextLayer(128/2, 4, self.game.fonts['num_09Bx7'], "center", opaque=False)
             self.value_layer = dmd.TextLayer(128/2, 15, self.game.fonts['num_09Bx7'], "center", opaque=False)
             self.award_layer = dmd.TextLayer(128/2, 24, self.game.fonts['tiny7'], "center", opaque=False) #.set_text('')
             self.info_layer = dmd.GroupedLayer(128, 32, [self.info_bgnd, self.item_layer, self.value_layer, self.award_layer])
             self.info_layer.transition = dmd.PushTransition(direction='south')

             self.title_layer = dmd.TextLayer(128/2, 4, self.game.fonts['num_09Bx7'], "center", opaque=False) #num_09Bx7 num_14x10 07x5
             self.score_layer = dmd.TextLayer(128/2, 15, self.game.fonts['num_14x10'], "center", opaque=False)
             self.jackpot_layer = dmd.GroupedLayer(128, 32, [self.info_bgnd,self.title_layer,self.score_layer])
             self.total_score_layer = dmd.TextLayer(128/2, 15, self.game.fonts['num_14x10'], "center", opaque=False)

             self.game.lampctrl.register_show('rk_mode_jackpot', lampshow_path+"mode_jackpot.lampshow")
             self.game.lampctrl.register_show('rk_slamlights', lampshow_path+"rk_slamlights.lampshow")
             self.game.lampctrl.register_show('rk_rklamps', lampshow_path+"kk_inform_jackpot1.lampshow")
             self.game.lampctrl.register_show('rk_ramp_ready', lampshow_path+"ramp_ready.lampshow")

             self.roadkingslamps = ['targetR','targetO','targetA','targetD','targetK','targetI','targetN','targetG','targetS']
             self.ramplamps = ['megaScore','Rtimelock','Rlock','Rextraball']
             self.mode_jp_lamps = [['bonusholdWL'], ['Ltimelock','Llock'], ['bonus10k','detourWL'],['Ctimelock','Clock']]

             # dubbel tijd Jackpot lit, all scores double, dubbel Road King Jackpot, tijd ballsave dubbel, unlimited powerkick, dubbel tijd mode-jackpots lit
             self.mode_items = ['racechampion_total','kickstartking_total','multiball_total','easyrider_total']
             self.mode_awards = ['All scores double','Double time Road jackpots','Ballsave extended','Unlimited kickback']
             self.info_items = list() # e.g.({"name":racechampion,"value":2344450})

             self.modes_completed = [False,False,False,False]
             self.index = 0
             self.spinner_active = False
             self.mode_jp_timer = 15 #VIA MENU
             self.ballsave_timer = 10 #VIA MENU
             self.ballsaver = True
             self.kings_jackpot_value = 20000000
             self.road_jackpot_value = 0
             self.lite_jackpot = False
             self.unlimited_kickback = False
             self.roadkings_score = 0

        def mode_started(self):
             print("Debug, Roadkings Mode Started")
             self.game.set_player_stats('game_feature_running',True)
             self.modes_completed = self.game.get_player_stats('modes_completed')
             # start roadkings intro only once
             self.lite_jackpot = 'intro'

        def mode_stopped(self):
             self.game.set_player_stats('game_feature_running',False)
             self.game.coils.Rgate.disable()
             self.game.update_lamps()
             print("Debug, Roadkings Mode Stopped")

## lamps & animations

        def update_lamps(self):
             for i in range(len(self.roadkingslamps)):
                 self.game.effects.drive_lamp(self.roadkingslamps[i],'normal')

             #update kickback lamp
             self.game.base_game_mode.kickback.update_lamps()

        def update_mode_jp_lamps(self):
             for i in range(len(self.modes_completed)):
                 for j in range(len(self.mode_jp_lamps[i])):
                     if self.modes_completed[i] == True:
                         self.game.effects.drive_lamp(self.mode_jp_lamps[i][j],'fast')
                     else:
                         self.game.effects.drive_lamp(self.mode_jp_lamps[i][j],'off')

        def clear_lamps(self):
             for i in range(len(self.roadkingslamps)):
                 self.game.effects.drive_lamp(self.roadkingslamps[i],'off')

        def animate_layer(self):
             script = list()
             script.append({'seconds':3.0, 'layer':self.info_layer})
             self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)

        def totalscore_animation(self):
             self.total_score_layer.set_text(locale.format("%d", self.roadkings_score, True))
             self.total_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'mode_total.dmd').frames[0])
             self.layer=dmd.GroupedLayer(128,32,[self.total_layer,self.total_score_layer])

        def play_animation(self):
             anim = dmd.Animation().load(dmd_path+'road_jd.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=6) #frame_time=6
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer, self.score_layer])

        def jackpot_animation(self):
             jp_anim = dmd.Animation().load(dmd_path+'fireworks.dmd')
             self.jackpot_layer = dmd.AnimatedLayer(frames=jp_anim.frames, opaque=False, repeat=True, hold=False, frame_time=3) #frame_time=6
             self.layer = dmd.GroupedLayer(128, 32, [self.jackpot_layer, self.title_layer, self.score_layer])

        def clear_layer(self):
             self.layer = None

## mode functions

        def check_completed_modes(self):
             if self.modes_completed[0]: #all scores double for Race Champion completed
                 self.game.set_pf_multiplier(value=2)
             if self.modes_completed[1]: #double time mode-jackpots lit for Kickstart King completed
                 self.mode_jp_timer *= 2
             if self.modes_completed[2]: #ballsave extended for Multiball completed
                 self.ballsave_timer = 20
             if self.modes_completed[3]: #unlimited kickback for Easy Rider completed
                  self.unlimited_kickback = True
                  self.game.base_game_mode.kickback.raise_kickback()

        def slam_letter(self):
             # repeat call to itself to spot letters on display
             if self.index < 9:
                 self.index += 1
                 self.game.sound.play(self.game.assets.sfx_rk_slam)
                 self.game.lampctrl.play_show('rk_slamlights', False, 'None')
                 self.layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'rk_letters.dmd').frames[self.index])
                 # light letter lamp
                 self.game.effects.drive_lamp(self.roadkingslamps[self.index-1],'on')
                 self.delay(name='slam_letter', event_type=None, delay=0.7, handler=self.slam_letter)
             else:
                 # cancel repeated call
                 self.index = 0
                 self.cancel_delayed('slam_letter')
                 self.slam_end()

        def mode_jp_countdown(self):
             # repeated call to itself for mode_jp_timer
             self.title_layer.set_text('TIME: '+str(self.mode_jp_timer),True)
             self.score_layer.set_text('')
             if self.mode_jp_timer > 0:
                 self.mode_jp_timer -= 1
                 self.delay(name='mode_jp_countdown', event_type=None, delay=1, handler=self.mode_jp_countdown)
             else:
                 # cancel repeated call and start next phase (rkwizard)
                 self.mode_jp_timer = 0
                 # clear completed modes
                 self.modes_completed = [False,False,False,False]
                 self.cancel_delayed('mode_jp_countdown')
                 self.start_rkwizard()

        def slam_end(self):
             self.game.sound.play(self.game.assets.sfx_rk_slamEnd)
             self.game.effects.gi_blinking(schedule=0x33333333, cycle_seconds=5)
             self.game.lampctrl.play_show('rk_rklamps', False, 'None')
             anim = dmd.Animation().load(dmd_path+'rk_slam_end.dmd')
             self.layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=4)
             self.delay(name='slam_reset', event_type=None, delay=5, handler=self.start_mode_info)

        def reset_roadkings(self):
             # reset to starting point
             self.lite_jackpot = True
             self.clear_layer()
             self.game.effects.gi_on()
             self.game.coils.flipperEnable.enable()
             self.check_completed_modes()
             # start
             self.start_jp_countdown()

        def start_jp_countdown(self):
             #launch ball
             self.game.trough.launch_balls(1)
             self.game.coils.Rgate.enable()
             self.play_animation()
             #stop lightshow
             self.game.lampctrl.stop_show()
             #update lamps after lampshow
             self.update_mode_jp_lamps()
             self.update_lamps()
             #put ramp up
             self.game.base_game_mode.rampmove.move_ramp('up')
             self.mode_jp_countdown()

        def start_rkwizard(self):
             #launch ball
             self.game.trough.launch_balls(1)
             self.game.effects.raise_droptarget()
             self.game.sound.play(self.game.assets.speech_shootRightRamp)
             #stop lightshow
             self.game.lampctrl.stop_show()
             #update lamps after lampshow
             self.update_lamps()
             self.update_mode_jp_lamps()
             self.game.lampctrl.play_show('rk_ramp_ready', True, 'None')
             #put ramp down
             self.game.base_game_mode.rampmove.move_ramp('down')

        def wizard_jackpot_scored(self):
             self.lite_jackpot = False
             self.game.sound.stop_music()
             self.game.sound.play(self.game.assets.sfx_rk_slamEnd)
             self.game.effects.gi_off()
             self.game.coils.flipperEnable.disable()
             self.game.ball_save.start(num_balls_to_save=1, time=20, now=True, allow_multiple_saves=False)
             self.game.lampctrl.play_show('mode_jackpot', True, 'None')
             self.title_layer.set_text('YOU ARE ROADKING!', seconds=5)
             self.score_layer.set_text(locale.format("%d",self.kings_jackpot_value, True), seconds=5, blink_frames=2)
             self.jackpot_animation()
             self.game.score(self.kings_jackpot_value)
             self.roadkings_score += self.kings_jackpot_value
             self.delay(name='end_roadkings', event_type=None, delay=8.0, handler=self.end_roadkings)

        def score_modejp(self, mode=0):
             self.game.sound.play(self.game.assets.sfx_kk_Jackpot)
             self.title_layer.set_text('ROAD JACKPOT', seconds=3)
             self.score_layer.set_text(locale.format("%d",self.road_jackpot_value, True), seconds=3, blink_frames=2)
             # add to jackpot value
             self.kings_jackpot_value += self.road_jackpot_value
             # register scored modes
             self.modes_completed[mode] = False
             self.update_mode_jp_lamps()
             self.delay(name='check_modejp', event_type=None, delay=2.0, handler=self.check_modejp)
             #self.check_modejp()

        def check_modejp(self):
            # if all jackpots are scored
             print("* modes completed *")
             print(self.modes_completed)
             if sum(self.modes_completed) == 0:
                 self.cancel_delayed('mode_jp_countdown')
                 self.title_layer.set_text('KINGS JACKPOT', seconds=5, blink_frames=16)
                 self.score_layer.set_text(locale.format("%d",self.kings_jackpot_value, True), seconds=5, blink_frames=2)
                 self.delay(name='start_rkwizard', event_type=None, delay=3.0, handler=self.start_rkwizard)

        def bumper(self):
             self.game.score(10000)

        def target_hit(self):
             self.game.sound.play(self.game.assets.sfx_kk_kick)
             self.kings_jackpot_value += 100000

        def end_roadkings(self):
             self.game.effects.gi_on()
             self.game.set_pf_multiplier(value=1)
             self.totalscore_animation()
             self.delay(name='stop_roadkings', event_type=None, delay=2.0, handler=self.stop_roadkings)

        def stop_roadkings(self):
             self.clear_layer()
             self.callback()

### functions display mode jackpots
        def start_mode_info(self):
             self.game.sound.play_music(self.game.assets.music_RKmode, loops=-1)
             self.create_info_items()
             self.update_display()

        def create_info_items(self):
             #self.info_items.append({'name':'BASE JACKPOT', 'value':str(self.kings_jackpot_value)})
             self.info_items.append({'name':'ROAD', 'value':'JACKPOTS'})

             # create modes total
             for i in range(len(self.mode_items)):
                   # get items
                   mode_item = self.mode_items[i]
                   item_value = str(self.game.get_player_stats(self.mode_items[i]))
                   # convert text to uppercase without underscore
                   mode_item = mode_item.replace("_total", "").upper()
                   # append data to list
                   self.info_items.append({'name':mode_item,'value':item_value})
                   # add to jackpot value
                   self.road_jackpot_value += int(item_value)

             # create total jackpot value
             self.info_items.append({'name':'TOTAL ROAD JACKPOT','value':str(self.road_jackpot_value)})
             self.info_items.append({'name':'SHOOT LIT SHOTS', 'value':'FOR ROAD JACKPOT'})
             self.info_items.append({'name':'EACH JACKPOT ADDS', 'value':'TO KINGS JACKPOT'})

             # print complete list of items with values
             for x in self.info_items:
                 print x["name"], x["value"]

             # determine max lenght of list
             self.index_max = len(self.info_items) - 1

        def exit(self):
            self.cancel_delayed('delayed_progression')
            self.clear_layer()
            self.reset_roadkings()

        def get_info(self,i):
            self.item_layer.set_text(self.info_items[i]['name'])
            if i == 0 or i > 5: # display text
                self.value_layer.set_text(self.info_items[i]['value'])
            else: # display value
                self.value_layer.set_text(locale.format("%d", int(self.info_items[i]['value']), True),blink_frames=2)
            self.award_layer.set_text('')
            if 0 < i < 5:
                if self.modes_completed[i-1]: # i-1 to sync, first info_item is text 'mode jackpots'
                    self.award_layer.set_text(self.mode_awards[i-1])

        def progress(self):
            if self.index == self.index_max:
                self.exit()
            else:
                self.index += 1
                # update display with new index
                self.update_display()

        def update_display(self):
            self.game.sound.play(self.game.assets.sfx_rk_wizardBoom)
            self.get_info(self.index)
            self.animate_layer()
            self.delay(name='delayed_progression', event_type=None, delay=3.0, handler=self.progress)
### End functions display mode jackpots

        def spinreset(self):
             self.spinner_active = True #reset to prevent counting multiple spinner hits
## switches

        # make sure ball is plunged before starting multiball
        def sw_shooterLane_open_for_1s(self,sw):
             self.game.effects.eject_ball(location='upperLkicker')
             if self.game.trough.num_balls_in_play==2: # ballsave only on 2-ball multiball
                 if self.ballsaver == True:
                     self.game.ball_save.start(num_balls_to_save=2, time=self.ballsave_timer, now=True, allow_multiple_saves=True)
                     self.ballsaver = False
             return True

        def sw_outhole_active(self,sw):
             print('number balls in play=', self.game.trough.num_balls_in_play)
             if self.game.trough.num_balls_in_play==3:
                 self.game.coils.outhole.pulse(30)
             elif self.game.trough.num_balls_in_play==2:
                  if self.game.ball_save.timer > 0:  #Don't end mode if ball_save is still running
                      self.game.coils.outhole.pulse(30)
                  else:
                      self.delay(name='end_roadkings', event_type=None, delay=1.0, handler=self.end_roadkings)
             return True

        def sw_RrampExit_active(self,sw):
             if self.lite_jackpot:   # Jackpot scored!
                 self.wizard_jackpot_scored()
             return True

        def sw_upperLkicker_active(self,sw):
             return True

        def sw_upperLkicker_active_for_500ms(self,sw):
             #start intro only once
             if self.lite_jackpot == 'intro':
                 self.delay(name='rk_intro', event_type=None, delay=6, handler=self.slam_letter)
             else:
                 self.delay(name='kickoutupperLkicker', event_type=None, delay=1, handler=self.game.effects.eject_ball)

        def sw_CrampEnter_active(self,sw):
             # check for active mode-jackpot Multiball
             if self.modes_completed[2]:
                self.score_modejp(mode=2)
             else:
                self.game.sound.play(self.game.assets.sfx_kk_gotGuts)
             return True

        def sw_Lspinner_active(self,sw):
             # check for active mode-jackpot RaceChampion
             if self.spinner_active == True:  # prevent multiple hits from spinner
                 if self.modes_completed[0]:
                     self.score_modejp(mode=0)
             self.spinner_active = False
             self.delay(name='spinreset', event_type=None, delay=2, handler=self.spinreset)
             return True

        def sw_Leject_active(self,sw):
             # check for active mode-jackpot KickstartKing
             if self.modes_completed[1]:
                self.score_modejp(mode=1)
             return True

        def sw_Leject_active_for_1s(self,sw):
             self.game.effects.eject_ball('Leject')
             return True

        def sw_Ceject_active(self,sw):
             # check for active mode-jackpot EasyRider
             if self.modes_completed[3]:
                self.score_modejp(mode=3)
             return True

        def sw_Ceject_active_for_1s(self,sw):
             self.game.effects.eject_ball('Ceject')

        def sw_outlaneL_active(self, sw):
             if self.unlimited_kickback:
              self.game.base_game_mode.kickback.raise_kickback()

        def sw_slingL_active(self,sw):
             return True

        def sw_slingR_active(self,sw):
             return True

        def sw_bumperL_active(self,sw):
             self.bumper()
             return True

        def sw_bumperU_active(self,sw):
             self.bumper()
             return True

        def sw_bumperR_active(self,sw):
             self.bumper()
             return True

        def sw_bumperD_active(self,sw):
             self.bumper()
             return True

        def sw_dropTarget_active(self,sw):
             return True

        def sw_dropTarget_active_for_3s(self,sw):
             self.game.effects.raise_droptarget()
             return True

        def sw_targetR_active(self,sw):
             self.target_hit()
             return True

        def sw_targetO_active(self,sw):
             self.target_hit()
             return True

        def sw_targetA_active(self,sw):
             self.target_hit()
             return True

        def sw_targetD_active(self,sw):
             self.target_hit()
             return True

        def sw_targetK_active(self,sw):
             self.target_hit()
             return True

        def sw_targetI_active(self,sw):
             self.target_hit()
             return True

        def sw_targetN_active(self,sw):
             self.target_hit()
             return True

        def sw_targetG_active(self,sw):
             self.target_hit()
             return True

        def sw_targetS_active(self,sw):
             self.target_hit()
             return True
