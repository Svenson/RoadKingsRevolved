#
# Kickstart King mode
#
# Main game mode (1 of 4)
# 2-ball multiball
# Colect slingshotskicks to lite Jackpot
#

__author__="Pieter"
__date__ ="$21 Jan 2013 21:21:21 PM$"

from procgame import *
import locale
from random import *
import random

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Kickstartking(game.Mode):

        def __init__(self, game, priority):
             super(Kickstartking, self).__init__(game, priority)

             self.game.lampctrl.register_show('mode_jackpot', lampshow_path+"mode_jackpot.lampshow")
             self.game.lampctrl.register_show('kk_start', lampshow_path+"succes_short.lampshow")
             self.game.lampctrl.register_show('kk_jackpot_lit', lampshow_path+"kk_jackpot_lit.lampshow")
             self.game.lampctrl.register_show('kk_inform_jackpot', lampshow_path+"kk_inform_jackpot.lampshow")
             self.game.lampctrl.register_show('kk_inform_jackpot', lampshow_path+"kk_inform_jackpot1.lampshow")
             #self.game.lampctrl.register_show('sling_left', lampshow_path+"sling_left.lampshow")
             #self.game.lampctrl.register_show('sling_right', lampshow_path+"sling_right.lampshow")
             self.game.lampctrl.register_show('kk_slings', lampshow_path+"kk_slings.lampshow")

             self.title_layer = dmd.TextLayer(95, 3, self.game.fonts['num_09Bx7'], "center", opaque=False)
             self.kicks_layer = dmd.TextLayer(95, 13, self.game.fonts['num_09Bx7'], "center", opaque=False)
             self.value_layer = dmd.TextLayer(94, 23, self.game.fonts['tiny7'], "center", opaque=False)
             self.score_layer = dmd.TextLayer(128/2, 8, self.game.fonts['num_14x10'], "center", opaque=False)
             self.total_score_layer = dmd.TextLayer(128/2, 15, self.game.fonts['num_14x10'], "center", opaque=False)

             self.roadkingslamps = ['targetR','targetO','targetA','targetD','targetK','targetI','targetN','targetG','targetS']
             self.slingshotlamps = ['bonus2x','bonus3x','bonus4x','bonus5x','bonus20k','bonus40k','bonus60k','bonus80k']

             self.index = len(self.roadkingslamps)
             self.temp_list = []
             #self.target_timer = 4 #VIA MENU
             self.target_timer = self.game.user_settings['Gameplay (Feature)']['Kickstart King Timer']
             self.kicks_raise = 0 #VIA MENU?
             self.kicks_score = 10300
             self.count_kicks = 0
             self.jackpot_value = 3156160
             self.lite_jackpot = False
             self.animation_status='ready'
             self.ballsaver = True
             self.kickstartking_score = 0


        def mode_started(self):
             print("Debug, Kickstartking Mode Started")
             self.game.set_player_stats('game_feature_running',True)
             self.game.base_game_mode.kickback.raise_kickback()
             self.reset_kicks()
             self.game.effects.clear_all_lamps()
             self.kickstart_intro()
             self.game.effects.drive_lamp('kickstartKing','on')

        def mode_stopped(self):
             self.game.coils.Rgate.disable()
             print("Debug, Kickstartking Mode Stopped")

## lamps & animations

        def update_lamps(self):
             #play lampshow
             self.game.lampctrl.play_show('kk_slings', True, 'None')
             #for i in range(len(self.slingshotlamps)):
             #    self.game.effects.drive_lamp(self.slingshotlamps[i],'superfast')
             #update kickback lamp
             self.game.base_game_mode.kickback.update_lamps()

        def clear_lamps(self):
             for i in range(len(self.roadkingslamps)):
                 self.game.effects.drive_lamp(self.roadkingslamps[i],'off')
             for i in range(len(self.slingshotlamps)):
                 self.game.effects.drive_lamp(self.slingshotlamps[i],'off')

        def bgnd_animation(self):
             self.bgnd_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'kicks_bgnd.dmd').frames[0])
             self.bgnd = dmd.GroupedLayer(128, 32, [self.bgnd_layer, self.title_layer, self.kicks_layer, self.value_layer])
             self.layer = self.bgnd

        def kick_animation(self):
             print(self.animation_status)
             if self.animation_status=='ready':
               anim = dmd.Animation().load(dmd_path+'kickstarting.dmd')
               self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=2)
               self.animation_layer.add_frame_listener(-1, self.animation_ended)
               self.bgnd.composite_op = "blacksrc"
               self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.bgnd])
               self.animation_status = 'running'

        def animation_ended(self):
             self.animation_status = 'ready'

        def jackpot_animation(self):
             self.cancel_delayed('end_jpmissed')
             self.score_layer.set_text(locale.format("%d", self.jackpot_value, True))
             anim = dmd.Animation().load(dmd_path+"nf_jackpot.dmd")
             self.jackpot_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False,frame_time=4)
             self.layer=dmd.GroupedLayer(128,32,[self.jackpot_layer, self.score_layer])

        def jackpot_missed_animation(self):
             choice = random.randint(0,1)
             if choice:
                 anim = dmd.Animation().load(dmd_path+"kk_joker.dmd")
                 self.jpmissed_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False,frame_time=1)
             else:
                 anim = dmd.Animation().load(dmd_path+"kk_skeleton.dmd")
                 self.jpmissed_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False,frame_time=4)
             self.jpmissed_layer.composite_op = "blacksrc" #"blacksrc"
             self.layer=dmd.GroupedLayer(128,32,[self.jackpot_lit_layer, self.jpmissed_layer])
             self.delay(name='end_jpmissed', event_type=None, delay=1.7, handler=self.jackpot_lit_animation)

        def jackpot_lit_animation(self):
             # determine current lit lamp for frame_nr in animation
             for i in range(len(self.roadkingslamps)):
                  if self.roadkingslamps[i] == self.temp_list[self.index]:
                       frame_nr = i
                       break
             # play proper frame_nr from animation
             self.jackpot_lit_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'kk_jackpot_lit.dmd').frames[frame_nr])
             self.layer = self.jackpot_lit_layer

        def inform_player_jp(self):
             self.game.lampctrl.play_show('kk_inform_jackpot', False, 'None')
             anim = dmd.Animation().load(dmd_path+'kk_jackpot_info.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=20)
             self.layer = self.animation_layer

        def inform_player(self):
             anim = dmd.Animation().load(dmd_path+'kk_makekicks.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=5)
             self.layer = self.animation_layer

        def totalscore_animation(self):
             self.total_score_layer.set_text(locale.format("%d", self.kickstartking_score, True))
             self.total_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'mode_total.dmd').frames[0])
             self.layer=dmd.GroupedLayer(128,32,[self.total_layer,self.total_score_layer])

        def clear_layer(self):
             self.layer = None

        def lamp_off(self):
             self.game.effects.drive_lamp(self.temp_list[self.index],'off')

## mode functions

        def kickstart_intro(self):
            self.game.sound.play(self.game.assets.sfx_KKintro)
            self.game.effects.gi_blinking(cycle_seconds=4)
            # delay animation to synchronise with sound
            self.delay(name='start_kickstart', event_type=None, delay=5, handler=self.start_kickstart)
            #play lightshow
            self.game.lampctrl.play_show('kk_start', False, 'None')

        def start_kickstart(self):
             #stop lightshow
             self.game.lampctrl.stop_show()
             #put ramp up
             self.game.base_game_mode.rampmove.move_ramp('up')
             # raise droptarget
             self.game.effects.raise_droptarget()
             # open right gate
             self.game.coils.Rgate.enable()
             #play music
             self.game.sound.play_music(self.game.assets.music_KKmode, loops=-1)
             #Kick slings to inform player
             self.inform_player()
             # set jackpot status 'kick_slings' to prevent intro kicks count to build jackpot
             self.lite_jackpot = 'kick_slings'
             self.delay(name='kick_sling', event_type=None, delay=0.2, handler=self.kick_slingR)
             self.delay(name='kick_sling', event_type=None, delay=0.4, handler=self.kick_slingL)
             #update lamps after lampshow
             self.update_lamps()
             #launch ball
             self.game.trough.launch_balls(1)
             #resume playfield multiplier if running
             self.game.base_game_mode.pause_pf_multiplier(set=False)

        def kick_slingR(self):
             self.game.coils.slingR.schedule(schedule=0x00010001, cycle_seconds=1, now=True)
        def kick_slingL(self):
             self.game.coils.slingL.schedule(schedule=0x00010001, cycle_seconds=1, now=True)

        def reset_kicks(self):
             # reset to starting point
             self.lite_jackpot = False
             self.animation_status = 'ready'
             self.kicks_raise += 5
             self.kicks_setting = self.kicks_raise
             # set display values
             self.title_layer.set_text('KICKS')
             self.kicks_layer.set_text(str(self.kicks_setting))
             self.value_layer.set_text(" value: "+str(locale.format("%d", self.kicks_score, True)))
             # shuffle for next jackpot order
             self.shuffle_jackpot()
             # reset index
             self.index = len(self.roadkingslamps)
             # set background animation
             self.bgnd_animation()
             # update lightning
             self.update_lamps()
             self.game.effects.gi_on()

        def shuffle_jackpot(self):
             # make copy of list to shuffle list for random jackpot target
             self.temp_list = list(self.roadkingslamps)
             shuffle(self.temp_list)
             print(self.temp_list)

        def lit_jackpot(self):
             # repeat call to itself to lite random jackpot
             if self.index > 0:
                 self.index -= 1
                 print("self.index :"+str(self.index))
                 self.game.sound.play(self.game.assets.sfx_spark)
                 self.jackpot_lit_animation()
                 self.game.lampctrl.play_show('kk_jackpot_lit', False, 'None')
                 # light jackpot lamp
                 self.game.effects.drive_lamp(self.temp_list[self.index],'medium')
                 self.delay(name='lit_jackpot', event_type=None, delay=self.target_timer, handler=self.lit_jackpot)
                 # jackpot lamp off after delay
                 self.delay(name='lamp_off', event_type=None, delay=self.target_timer-0.5, handler=self.lamp_off)
                 if self.index == 3:
                      self.game.sound.play(self.game.assets.sfx_HurryUp)
             else:
                 # cancel repeated call
                 self.cancel_delayed('lit_jackpot')
                 # reset
                 self.delay(name='reset_kicks', event_type=None, delay=2, handler=self.reset_kicks)

        def kicks_hit(self):
             self.count_kicks += 1
             self.game.sound.play(self.game.assets.sfx_kk_kick)
             self.game.score(self.kicks_score)
             self.kickstartking_score += self.kicks_score
             if self.lite_jackpot == False:
                 # decrease kicks
                 self.kicks_setting -= 1
                 self.kicks_layer.set_text(str(self.kicks_setting))
                 self.kick_animation()
                 if self.kicks_setting == 0: # Jackpot ready
                     #stop current lightshow
                     self.game.lampctrl.stop_show()
                     #self.game.effects.gi_off()
                     self.lite_jackpot = True
                     # inform player before start jackpot sequence
                     self.inform_player_jp()
                     self.game.sound.play(self.game.assets.sfx_kk_jackpotLit)
                     # start jackpot sequence after 3 seconds
                     self.delay(name='lit_jackpot', event_type=None, delay=3, handler=self.lit_jackpot)
                     #self.lit_jackpot()

        def raise_kicks(self):
             self.kicks_score += 5000
             self.value_layer.set_text(" value: "+ str(locale.format("%d", self.kicks_score, True)))

        def target_hit(self,id):
             if self.lite_jackpot == True and self.index < 9: # prevent index out of range error for temp_list[]
                 # check if hit-target == jackpot-target
                 if self.roadkingslamps[id] == self.temp_list[self.index]:
                    if self.game.switches.shooterLane.is_active(): # only award jackpot if both balls are in play
                        self.game.sound.play(self.game.assets.sfx_kk_gotGuts)
                    else: # Jackpot!
                        self.lite_jackpot = False
                        self.cancel_delayed('lit_jackpot')
                        #play sounds
                        self.game.sound.play(self.game.assets.sfx_kk_Jackpot)
                        # lampshow
                        self.game.lampctrl.play_show('mode_jackpot', False, 'None')
                        self.jackpot_animation()
                        # score jackpot
                        self.game.score(self.jackpot_value)
                        self.kickstartking_score += self.jackpot_value
                        self.game.base_game_mode.missions_modes.update_modes_completed(2)
                        # reset
                        self.delay(name='reset_kicks', event_type=None, delay=4, handler=self.reset_kicks)
                 else:
                     self.game.effects.drive_lamp_schedule(self.roadkingslamps[id], schedule=0x99999999, cycle_seconds=1, now=True)
                     self.game.sound.play(self.game.assets.sfx_kk_jackpotMissed)
                     self.jackpot_missed_animation()

        def end_kickstartking(self):
             self.delay(name='stop_kickstartking', event_type=None, delay=2.0, handler=self.stop_kickstartking)
             self.lite_jackpot = False
             if self.kickstartking_score > 5000000:
                 self.game.sound.play(self.game.assets.sfx_kk_gotGuts)
             self.totalscore_animation()
             print("Total Kicks: "+str(self.count_kicks))
             self.game.set_player_stats('kicks_made',self.count_kicks)
             self.game.set_player_stats('game_feature_running',False)
             self.game.set_player_stats('kickstartking_total',self.kickstartking_score)

        def stop_kickstartking(self):
             self.clear_layer()
             self.callback('kickstartking')

        def bumper(self):
             self.game.score(10)
             self.game.sound.play(self.game.assets.sfx_bumper)
             # raise kick_value
             self.raise_kicks()

## switches

        # make sure ball is plunged before starting multiball
        def sw_shooterLane_open_for_1s(self,sw):
             self.game.effects.eject_ball(location='upperLkicker')
             self.lite_jackpot = False
             if self.ballsaver == True:
                 self.game.ball_save.start(num_balls_to_save=2, time=15, now=True, allow_multiple_saves=True)
                 self.ballsaver = False
             self.update_lamps()
             return True

        def sw_outhole_active(self,sw):
             if self.game.ball_save.timer==0: #Don't end mode if ball_save is still running
                 self.delay(name='end_kickstartking', event_type=None, delay=1.0, handler=self.end_kickstartking)
                 self.cancel_delayed('lit_jackpot')
                 self.clear_lamps()
             else:
                 self.game.coils.outhole.pulse(30)
             return True

        def sw_CrampEnter_active(self,sw):
             self.game.sound.play(self.game.assets.sfx_kk_gotGuts)
             self.game.score(500000)
             return True

        def sw_Lspinner_active(self,sw):
             return True

        def sw_Leject_active(self,sw):
             return True

        def sw_Leject_active_for_2s(self,sw):
             self.game.effects.eject_ball('Leject')
             return True

        def sw_Ceject_active(self,sw):
             return True

        def sw_Ceject_active_for_2s(self,sw):
             self.game.effects.eject_ball('Ceject')
             return True

        def sw_slingL_active(self,sw):
             self.game.coils.Llightningbolt.pulse(30)
             #self.game.lampctrl.play_show('sling_left', False, 'None')
             if self.lite_jackpot != 'kick_slings':
                 self.kicks_hit()
             return True

        def sw_slingR_active(self,sw):
             self.game.coils.Rlightningbolt.pulse(30)
             #self.game.lampctrl.play_show('sling_right', False, 'None')
             if self.lite_jackpot != 'kick_slings':
                 self.kicks_hit()
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

        def sw_dropTarget_active_for_500ms(self,sw):
             self.game.effects.raise_droptarget()
             return True

        def sw_targetR_active(self,sw):
             self.target_hit(0)
             return True

        def sw_targetO_active(self,sw):
             self.target_hit(1)
             return True

        def sw_targetA_active(self,sw):
             self.target_hit(2)
             return True

        def sw_targetD_active(self,sw):
             self.target_hit(3)
             return True

        def sw_targetK_active(self,sw):
             self.target_hit(4)
             return True

        def sw_targetI_active(self,sw):
             self.target_hit(5)
             return True

        def sw_targetN_active(self,sw):
             self.target_hit(6)
             return True

        def sw_targetG_active(self,sw):
             self.target_hit(7)
             return True

        def sw_targetS_active(self,sw):
             self.target_hit(8)
             return True
