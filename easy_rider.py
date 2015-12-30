#
# Easy Rider mode
#
# Main game mode (1 of 4)
# Shoot all lit shots within time for jackpot on right ramp
#

__author__="Steven"
__date__ ="$19 Nov 2012 15:21:12 PM$"

from procgame import *
import locale

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Easyrider(game.Mode):
        def __init__(self, game, priority):
                super(Easyrider, self).__init__(game, priority) #84

                self.game.lampctrl.register_show('er_shotmade', lampshow_path+"er_shotmade.lampshow")
                self.game.lampctrl.register_show('mode_jackpot', lampshow_path+"mode_jackpot.lampshow")

                self.title_layer = dmd.TextLayer(128/2, 2, self.game.fonts['num_09Bx7'], "center", opaque=False) #num_09Bx7 num_14x10
                self.score_layer = dmd.TextLayer(128/2, 17, self.game.fonts['num_14x10'], "center", opaque=False)
                self.total_score_layer = dmd.TextLayer(128/2, 15, self.game.fonts['num_14x10'], "center", opaque=False)

                self.lamps_trafficlight = ['stoplight_green','stoplight_yellow','stoplight_red']
                self.lamps_ramp = ['megaScore','Rtimelock','Rlock','Rextraball']

                self.shot_sequence = [0,0,0,0,0,0,0] #[road_targets,spinner,left_eject,center_ramp,center_eject,right_loop,kings_targets]
                self.lamp_sequence = [['targetR','targetO','targetA','targetD'],['bonusholdWL'], ['Ltimelock'], ['detourWL'],
                                      ['Ctimelock'], ['Rtimelock'],['targetK','targetI','targetN', 'targetG','targetS']]
                self.race_done = False
                self.time_left=16
                #self.timer_setting = 15 VIA MENU
                self.timer_setting = self.game.user_settings['Gameplay (Feature)']['Easy Rider Timer']
                self.jackpot_ready = False
                self.shot_value = 500000 #250000
                self.jackpot_value = 5000000 #2500000
                self.easyrider_score = 0
                self.spinner_active=False
                #self.knocker_on = False # VIA MENU
                self.knocker_on = self.game.user_settings['Gameplay (Feature)']['Easy Rider Knocker On']


        def mode_started(self):
                print("Debug, Easyrider Mode Started")
                self.game.set_player_stats('game_feature_running',True)
                for lamp in self.game.lamps:
                        lamp.disable()
                self.game.sound.play_music(self.game.assets.music_ERmode, loops=-1)
                self.game.base_game_mode.rampmove.move_ramp('up')
                self.game.base_game_mode.kickback.raise_kickback()
                self.start_easyrider()
                self.play_animation()
                self.update_lamps()

        def mode_stopped(self):
                print("Debug, Easyrider Mode Stopped")

        def start_easyrider(self):
                self.delay(name='shootlitshotssound', event_type=None, delay=1, handler=self.shootlitshotssound)
                self.game.effects.eject_ball('upperLkicker')
                self.game.ball_save.start(num_balls_to_save=1, time=10, now=True, allow_multiple_saves=True)
                self.countdown()
                #resume playfield multiplier if running
                self.game.base_game_mode.pause_pf_multiplier(set=False)

## lamps & animations

        def update_lamps(self):
                #disable all lamps
                for lamp in self.game.lamps:
                        lamp.disable()
                #update shot lamps
                for i in range(len(self.shot_sequence)):
                    for j in range(len(self.lamp_sequence[i])):
                        if self.shot_sequence[i] == 0:
                            self.game.effects.drive_lamp(self.lamp_sequence[i][j],'medium')
                        else:
                            self.game.effects.drive_lamp(self.lamp_sequence[i][j],'on')
                #update jackpot lamps
                if self.jackpot_ready == True:
                        for i in range(len(self.lamps_ramp)):
                                self.game.effects.drive_lamp(self.lamps_ramp[i],'medium')
                        for i in range(len(self.lamps_trafficlight)):
                                self.game.effects.drive_lamp(self.lamps_trafficlight[i],'fast')
                #update kickback lamp
                self.game.base_game_mode.kickback.update_lamps()
                #update mode lamp
                self.game.effects.drive_lamp('easyRider','on')

        def play_animation(self):
                anim = dmd.Animation().load(dmd_path+'easy_rider.dmd')
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=6) #frame_time=6
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer, self.score_layer])

        def totalscore_animation(self):
                self.total_score_layer.set_text(locale.format("%d", self.easyrider_score, True))
                self.total_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'mode_total.dmd').frames[0])
                self.layer=dmd.GroupedLayer(128,32,[self.total_layer,self.total_score_layer])

        def clear_layer(self):
                self.layer = None

## mode functions

        def check_shot(self, id=0):
                if self.shot_sequence[id] == 0:
                    self.shot_sequence[id] = 1
                    self.update_status()

        def check_shots_made(self):
                shots_made = self.shot_sequence.count(1)
                print ("Shots made: " +str(shots_made))
                self.shot_made(shots_made)
                if shots_made == 7 and self.jackpot_ready == False: # Jackpot ready
                       self.game.base_game_mode.rampmove.move_ramp('down')
                       self.jackpot_ready = True
                       self.delay(name='shootrampsound', event_type=None, delay=3, handler=self.shootrampsound)

        def shot_made(self, knocks=1):
                self.game.sound.play(self.game.assets.speech_er_shotMade)
                self.game.lampctrl.play_show('er_shotmade', False, 'None')
                self.game.score(self.shot_value)
                self.score_layer.set_text(locale.format("%d",self.shot_value, True), seconds=2, blink_frames=2)
                self.easyrider_score += self.shot_value
                self.knock_times(knocks)

        def update_status(self):
                # reset timer
                if self.jackpot_ready:
                    self.time_left = self.timer_setting + 5
                else:
                    self.time_left = self.timer_setting
                # check for shots made
                self.check_shots_made()
                if self.race_done==True:
                        # If countdown runs out while shot is already made but not yet registered, continue if shot is registered
                        self.cancel_delayed('end_easyrider')
                        self.race_done=False
                        self.game.coils.flipperEnable.enable()
                        self.game.effects.gi_on()
                        self.title_layer.set_text('BACK ON TRACK..')
                        self.delay(name='countdown', event_type=None, delay=2, handler=self.countdown)
                        self.game.ball_save.start(num_balls_to_save=1, time=8, now=True, allow_multiple_saves=False)
                self.update_lamps()

        def countdown(self):
                self.title_layer.set_text('TIME: '+str(self.time_left),True)
                self.time_left-=1
                self.delay(name='countdown', event_type=None, delay=1, handler=self.countdown)
                if self.time_left<0:
                        self.game.effects.gi_off()
                        self.race_done=True
                        self.cancel_delayed('countdown')
                        self.title_layer.set_text('RACE OVER...',4,4)
                        #self.game.coils.flipperEnable.disable()
                        #self.game.ball_save.start(num_balls_to_save=1, time=8, now=True, allow_multiple_saves=False)
                        self.delay(name='end_easyrider', event_type=None, delay=2.0, handler=self.end_easyrider)
                elif self.time_left==7:
                        self.game.sound.play(self.game.assets.sfx_siren)
                elif self.time_left>6:
                        self.game.sound.stop(self.game.assets.sfx_siren)

        def knock_times(self, param=1):
               if self.knocker_on:
                  for i in range(1,param+1): # param+1 because range starts always at 0
                       self.delay(name='knocker'+str(param), event_type=None, delay=0.4*i, handler=self.knocker)
        def knocker(self):
                self.game.coils.knocker_rampUp.pulse(9)

        def score_jackpot(self):
                self.game.sound.play(self.game.assets.sfx_er_Jackpot)
                self.title_layer.set_text('THATS EASY RIDING') #EASY GOING RIDER, THATS EASY RIDING, YOU R EASY RIDING
                self.score_layer.set_text(locale.format("%d",self.jackpot_value, True), seconds=3, blink_frames=2)
                self.game.score(self.jackpot_value)
                self.easyrider_score += self.jackpot_value
                self.game.sound.play(self.game.assets.speech_er_thatsEasy)
                self.knock_times(7)
                self.game.effects.gi_off()
                for lamp in self.game.lamps:
                       lamp.disable()
                self.game.lampctrl.play_show('mode_jackpot', False, 'None')
                self.game.base_game_mode.missions_modes.update_modes_completed(4)
                self.delay(name='end_easyrider', event_type=None, delay=2.0, handler=self.end_easyrider)

        def shootrampsound(self):
                self.game.sound.play(self.game.assets.speech_shootRightRamp)

        def shootlitshotssound(self):
                self.game.sound.play(self.game.assets.speech_er_shootLitShots)
                self.steer = Steer(self.game, 85)
                self.game.modes.add(self.steer)

        def bumper(self):
                self.game.score(110)
                self.game.sound.play(self.game.assets.sfx_bumper)

        def check_road(self):
                self.check_shot(0)

        def check_kings(self):
                self.check_shot(6)

        def spinreset(self):
                self.spinner_active=True #reset to prevent counting multiple spinner hits

        def end_easyrider(self):
                self.delay(name='stop_easyrider', event_type=None, delay=2.0, handler=self.stop_easyrider)
                self.game.modes.remove(self.steer)
                if self.easyrider_score > 3000000:
                    self.game.sound.play(self.game.assets.speech_er_bornToBeWild)
                self.totalscore_animation()
                self.game.set_player_stats('game_feature_running',False)
                self.game.set_player_stats('easyrider_total',self.easyrider_score)

        def stop_easyrider(self):
                self.clear_layer()
                self.callback('easyrider')

## switches

        def sw_RrampExit_active(self,sw):
                if self.jackpot_ready == True:   # Jackpot scored!
                        self.jackpot_ready = False
                        self.cancel_delayed('countdown')
                        self.score_jackpot()
                        self.game.coils.flipperEnable.disable()
                return True

        def sw_Lspinner_active(self,sw):
                self.game.coils.Rgate.schedule(0xffffffff, cycle_seconds=1, now=True)
                if not self.game.switches.Rrollunder.time_since_change() < 1.5 and self.spinner_active==True:  # left loop trough spinner
                        self.check_shot(1)
                if self.game.switches.Rrollunder.time_since_change() < 1.5: # right loop under ramp
                        self.check_shot(5)
                self.spinner_active=False
                self.delay(name='spinreset', event_type=None, delay=2, handler=self.spinreset)
                return True

        def sw_Rrollunder_active(self,sw):
                self.game.coils.Lgate.schedule(0xffffffff, cycle_seconds=1, now=True)
                return True

        def sw_Leject_active(self,sw):
                return True

        def sw_Leject_active_for_600ms(self,sw):
                self.check_shot(2)
                self.delay(name='kickout_Lejecthole', event_type=None, delay=0.5, handler=self.game.effects.eject_ball)
                return True

        def sw_CrampEnter_active(self,sw):
                self.check_shot(3)
                return True

        def sw_CrampRexit_active(self,sw):
                return True

        def sw_Ceject_active(self,sw):
                return True

        def sw_Ceject_active_for_600ms(self,sw):
                self.check_shot(4)
                self.delay(name='kickout_Cejecthole', event_type=None, delay=0.5, handler=self.game.effects.eject_ball)
                return True

        def sw_outhole_active(self,sw):
             if self.game.ball_save.timer==0: #Don't end mode if ball_save is still running
                self.end_easyrider()
             else:
                 self.game.coils.outhole.pulse(30)
             return True

        def sw_targetR_active(self,sw):
                self.check_road()
                return True
        def sw_targetO_active(self,sw):
                self.check_road()
                return True
        def sw_targetA_active(self,sw):
                self.check_road()
                return True
        def sw_targetD_active(self,sw):
                self.check_road()
                return True
        def sw_targetK_active(self,sw):
                self.check_kings()
                return True
        def sw_targetI_active(self,sw):
                self.check_kings()
                return True
        def sw_targetN_active(self,sw):
                self.check_kings()
                return True
        def sw_targetG_active(self,sw):
                self.check_kings()
                return True
        def sw_targetS_active(self,sw):
                self.check_kings()
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
        def sw_slingL_active(self,sw):
                self.bumper()
                return True
        def sw_slingR_active(self,sw):
                self.bumper()
                return True

class Steer(game.Mode):
        def __init__(self, game, priority):
                super(Steer, self).__init__(game, priority)
        def mode_started(self):
                print("Debug, Steer Mode Started")
                self.show_steer()
        def show_steer(self):
                anim = dmd.Animation().load(dmd_path+'er_steer_gm.dmd')
                self.steer_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True)
                self.layer = self.steer_layer
                self.layer.composite_op = "alpha" #"blacksrc" #"alpha"