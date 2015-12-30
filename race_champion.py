#
# Race Champion mode
#
# Main game mode (1 of 4)
# Shoot moving shots within time to score jackpot
#

__author__="Steven"
__date__ ="$17 Feb 2013 15:21:12 PM$"

from procgame import *
import locale
import random

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Racechampion(game.Mode):
        def __init__(self, game, priority):
                super(Racechampion, self).__init__(game, priority) #81

                self.game.lampctrl.register_show('mode_jackpot', lampshow_path+"mode_jackpot.lampshow")

                self.total_score_layer = dmd.TextLayer(128/2, 15, self.game.fonts['num_14x10'], "center", opaque=False)
                self.jackpot_score_layer = dmd.TextLayer(70, 10, self.game.fonts['num_14x10'], "center", opaque=False)

                self.shot_sequence = [['bonusholdWL'], ['Ltimelock', 'Llock'], ['Cextraball', 'detourWL'],
                                      ['Ctimelock', 'Clock'], ['Rtimelock', 'Rlock', 'Rextraball']] #[0, 1, 2, 3, 4]  self.shot_sequence[self.position]

                #self.position = 2 #VIA MENU Harder = pos 0/1
                self.position = self.game.user_settings['Gameplay (Feature)']['Race Champion Position']
                #self.timer = 12 #VIA MENU
                self.timer = self.game.user_settings['Gameplay (Feature)']['Race Champion Timer']
                self.timer_out = 5 #number of seconds left in shot before position changes. Used for voice-call and light effects.
                self.jackpot_value = 5000000
                self.shot_score = 250000
                self.racechampion_score = 0

        def mode_started(self):
                print("Debug, Racechampion Mode Started")
                self.game.set_player_stats('game_feature_running',True)
                for lamp in self.game.lamps:
                        lamp.disable()
                self.game.base_game_mode.kickback.raise_kickback()
                self.control_racelamps('on')
                self.start_race_champion()
                self.game.effects.drive_lamp('raceChampion','on')

        def mode_stopped(self):
                print("Debug, Racechampion Mode Stopped")

## lamps & animations

        def control_racelamps(self, state= 'on'):
                if state == 'on':
                    for i in range(len(self.shot_sequence)):
                        for j in range(len(self.shot_sequence[i])):
                            self.game.effects.drive_lamp(self.shot_sequence[i][j],'medium')
                if state == 'off':
                    for i in range(len(self.shot_sequence)):
                        for j in range(len(self.shot_sequence[i])):
                            self.game.effects.drive_lamp(self.shot_sequence[i][j],'off')

        def update_lamps(self):
                self.control_racelamps('off')
                # activate current position lamps
                for j in range(len(self.shot_sequence[self.position])):
                        #print self.shot_sequence[self.position][j]
                        self.game.effects.drive_lamp(self.shot_sequence[self.position][j],'medium')

        def time_out_lamps(self):
                # fast blink current position lamps, to indicate time's running out
                for j in range(len(self.shot_sequence[self.position])):
                    self.game.effects.drive_lamp(self.shot_sequence[self.position][j],'fast')

        def update_position(self):
                if self.position == 0:
                    self.game.sound.play_music(self.game.assets.music_RCmode60, loops=-1)
                    self.racer_animation.racer_to_5th()
                elif self.position == 1:
                      self.game.sound.play_music(self.game.assets.music_RCmode70, loops=-1)
                      pass
                elif self.position == 2:
                      self.game.sound.play_music(self.game.assets.music_RCmode80, loops=-1)
                      self.racer_animation.racer_to_4th()
                elif self.position == 3:
                      self.game.sound.play_music(self.game.assets.music_RCmode90, loops=-1)
                      self.racer_animation.racer_to_3th()
                elif self.position == 4:
                      self.game.sound.play_music(self.game.assets.music_RCmode100, loops=-1)
                      self.racer_animation.racer_to_2nd()

        def totalscore_animation(self):
                self.total_score_layer.set_text(locale.format("%d", self.racechampion_score, True))
                self.total_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'mode_total.dmd').frames[0])
                self.layer=dmd.GroupedLayer(128,32,[self.total_layer,self.total_score_layer])

        def play_animation_road_side(self):
                anim_flats = dmd.Animation().load(dmd_path+'flats1.dmd')
                anim_road_plane = dmd.Animation().load(dmd_path+'road_plane.dmd')
                if self.position <2: 
                        self.animation_flats_layer = dmd.AnimatedLayer(frames=anim_flats.frames, opaque=False, repeat=False, hold=False, frame_time=6)
                        self.animation_road_layer = dmd.AnimatedLayer(frames=anim_road_plane.frames, opaque=False, repeat=False, hold=False, frame_time=4)
                        self.animation_flats_layer.add_frame_listener(-1,self.play_animation_road_side)
                        self.animation_road_layer.composite_op = "alpha"
                        #self.animation_flats_layer.composite_op = "blacksrc"
                        self.layer = dmd.GroupedLayer(128, 32, [self.animation_flats_layer,self.animation_road_layer])
                elif self.position <3: 
                        self.animation_flats_layer = dmd.AnimatedLayer(frames=anim_flats.frames, opaque=False, repeat=False, hold=False, frame_time=4)
                        self.animation_road_layer = dmd.AnimatedLayer(frames=anim_road_plane.frames, opaque=False, repeat=False, hold=False, frame_time=3)
                        self.animation_flats_layer.add_frame_listener(-1,self.play_animation_road_side)
                        self.animation_road_layer.composite_op = "alpha"
                        #self.animation_flats_layer.composite_op = "blacksrc"
                        self.layer = dmd.GroupedLayer(128, 32, [self.animation_flats_layer,self.animation_road_layer])
                elif self.position <4: 
                        self.animation_flats_layer = dmd.AnimatedLayer(frames=anim_flats.frames, opaque=False, repeat=False, hold=False, frame_time=3)
                        self.animation_road_layer = dmd.AnimatedLayer(frames=anim_road_plane.frames, opaque=False, repeat=False, hold=False, frame_time=2)
                        self.animation_flats_layer.add_frame_listener(-1,self.play_animation_road_side)
                        self.animation_road_layer.composite_op = "alpha"
                        #self.animation_flats_layer.composite_op = "blacksrc"
                        self.layer = dmd.GroupedLayer(128, 32, [self.animation_flats_layer,self.animation_road_layer])
                elif self.position <5: 
                        self.animation_flats_layer = dmd.AnimatedLayer(frames=anim_flats.frames, opaque=False, repeat=False, hold=False, frame_time=2)
                        self.animation_road_layer = dmd.AnimatedLayer(frames=anim_road_plane.frames, opaque=False, repeat=False, hold=False, frame_time=1)
                        self.animation_flats_layer.add_frame_listener(-1,self.play_animation_road_side)
                        self.animation_road_layer.composite_op = "alpha"
                        #self.animation_flats_layer.composite_op = "blacksrc"
                        self.layer = dmd.GroupedLayer(128, 32, [self.animation_flats_layer,self.animation_road_layer])  

        def play_victory_animation(self):
                self.game.modes.remove(self.racer_animation)
                self.game.modes.remove(self.bike3_animation)
                self.game.modes.remove(self.house_animation)
                self.jackpot_score_layer.set_text(locale.format("%d",self.jackpot_value, True), seconds=3, blink_frames=4)
                anim = dmd.Animation().load(dmd_path+'rc_victory.dmd')
                self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=8)
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.jackpot_score_layer])

        def clear_layer(self):
                self.layer = None

## mode functions

        def start_race_champion(self):
                self.delay(name='eject_delay', event_type=None, delay=2, handler=self.game.effects.eject_ball)
                self.delay(name='control_position', event_type=None, delay=2, handler=self.control_position)
                self.game.ball_save.start(num_balls_to_save=1, time=12, now=True, allow_multiple_saves=True)
                self.game.base_game_mode.rampmove.move_ramp('up')
                self.play_animation_road_side()
                self.racer_animation = Racer_animation(self.game, 84)
                self.game.modes.add(self.racer_animation)
                self.bike3_animation = Bike3_animation(self.game, 85)
                self.game.modes.add(self.bike3_animation)
                self.house_animation = House_animation(self.game, 86)
                self.game.modes.add(self.house_animation)
                #resume playfield multiplier if running
                self.game.base_game_mode.pause_pf_multiplier(set=False)

        def cancel_race_champion(self):
                self.cancel_delayed('update_racer_animation')
                self.cancel_delayed('update_bike3_animation')
                self.cancel_delayed('move_back')
                self.cancel_delayed('time_out')
                self.cancel_delayed('eject_delay')
                self.game.modes.remove(self.racer_animation)
                self.game.modes.remove(self.bike3_animation)
                self.game.modes.remove(self.house_animation)

        def end_race_champion(self):
                self.delay(name='stop_race_champion', event_type=None, delay=2.0, handler=self.stop_race_champion)
                self.cancel_race_champion()
                self.totalscore_animation()
                self.game.set_player_stats('game_feature_running',False)
                self.game.set_player_stats('racechampion_total',self.racechampion_score)

        def stop_race_champion(self):
                self.clear_layer()
                #self.game.coils.outhole.pulse(30)
                self.callback('racechampion')

        def time_out(self):
                self.game.sound.play(self.game.assets.sfx_rc_timeOut)
                self.time_out_lamps()

        def move_back(self):
                if self.position == 0:
                    self.race_lost()
                else:
                    if self.position == 4:
                        self.game.base_game_mode.rampmove.move_ramp('up')
                    self.position -=1
                    self.game.sound.play(self.game.assets.sfx_rc_moveBack)
                    self.control_position()

        def move_forward(self):
                self.position +=1
                self.control_position()

        def control_position(self):
                print ("Position: "+str(self.position))
                self.update_position()
                self.update_lamps()
                self.delay(name='move_back', event_type=None, delay=self.timer, handler=self.move_back)
                self.delay(name='time_out', event_type=None, delay=self.timer-self.timer_out, handler=self.time_out)

        def shot_made(self):
                self.cancel_delayed('move_back')
                self.cancel_delayed('time_out')
                if self.position == 4:
                    self.race_won()
                else:
                    self.game.sound.play(self.game.assets.sfx_rc_shotMade)
                    self.game.score(self.shot_score)
                    self.racechampion_score += self.shot_score
                    self.move_forward()

        def race_won(self):
                self.control_racelamps('off')
                self.game.coils.GIrelay.schedule(0x55555555, cycle_seconds=3, now=True)
                self.game.sound.fadeout_music(time_ms=100)
                self.game.sound.play(self.game.assets.sfx_rc_raceWon)
                self.game.lampctrl.play_show('mode_jackpot', False, 'None')
                self.game.coils.flipperEnable.disable()
                self.game.score(self.jackpot_value)
                self.racechampion_score += self.jackpot_value
                self.game.base_game_mode.missions_modes.update_modes_completed(1)
                self.racer_animation.racer_wins()
                self.delay(name='play_victory_animation', event_type=None, delay=2, handler=self.play_victory_animation)
                self.delay(name='end_race_champion', event_type=None, delay=5, handler=self.end_race_champion)

        def race_lost(self):
                self.game.sound.play_music(self.game.assets.music_RCmode00, loops=0)
                self.control_racelamps('off')
                self.game.coils.GIrelay.schedule(0xffffffff, cycle_seconds=3, now=True)
                self.game.coils.flipperEnable.disable()
                self.game.ball_save.start(num_balls_to_save=1, time=15, now=True, allow_multiple_saves=False)
                self.delay(name='end_race_champion', event_type=None, delay=0.5, handler=self.end_race_champion)

        def frenzy_score(self):
                self.game.score(110)
                return True

## switches

        def sw_upperLkicker_active(self, sw):
                return True

        def sw_Lspinner_active(self,sw):
                if self.position == 0:
                    self.shot_made()
                    self.game.sound.play(self.game.assets.sfx_rc_justInTime)
                self.game.coils.Rgate.schedule(0xffffffff, cycle_seconds=1, now=True)
                return True

        def sw_Leject_active(self,sw):
                if self.position == 1:
                    self.shot_made()
                self.delay(name='eject_delay', event_type=None, delay=0.4, handler=self.game.effects.eject_ball)
                return True

        def sw_CrampEnter_active(self,sw):
                if self.position == 2:
                    self.shot_made()
                return True

        def sw_Ceject_active(self,sw):
                if self.position == 3:
                    self.shot_made()
                    self.game.base_game_mode.rampmove.move_ramp('down')
                self.delay(name='eject_delay', event_type=None, delay=0.4, handler=self.game.effects.eject_ball)
                return True

        def sw_RrampExit_active(self,sw):
                if self.position == 4:
                    self.shot_made()
                return True

        def sw_outhole_active(self,sw):
             if self.game.ball_save.timer == 0: #Don't end mode if ball_save is still running
                self.end_race_champion()
             else:
                 self.game.coils.outhole.pulse(30)
             return True

        def sw_bumperL_active(self,sw):
                self.frenzy_score()
                return True
        def sw_bumperU_active(self,sw):
                self.frenzy_score()
                return True
        def sw_bumperR_active(self,sw):
                self.frenzy_score()
                return True
        def sw_bumperD_active(self,sw):
                self.frenzy_score()
                return True

class Racer_animation(game.Mode):
        def __init__(self, game, priority):
                super(Racer_animation, self).__init__(game, priority)
        def mode_started(self):
                self.racer_x=50
                self.racer_animation_update()

        def racer_animation_update(self):
                anim = dmd.Animation().load(dmd_path+'bike3.dmd') #bike3
                self.animation_racer_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False)
                self.animation_racer_layer.set_target_position(self.racer_x, 12)
                self.layer = self.animation_racer_layer
                self.layer.composite_op = "alpha"
        def racer_wins(self):
                if self.racer_x<140:
                        self.racer_x+=1
                        self.delay(name='racer_wins', event_type=None, delay=0.02, handler=self.racer_wins)
                self.racer_animation_update()
        def racer_to_2nd(self):
                if self.racer_x<95:
                        self.racer_x+=1
                        self.delay(name='racer_to_2nd', event_type=None, delay=0.02, handler=self.racer_to_2nd)
                elif self.racer_x>95:
                        self.racer_x-=1
                        self.delay(name='racer_to_2nd', event_type=None, delay=0.02, handler=self.racer_to_2nd)
                self.racer_animation_update()
        def racer_to_3th(self):
                if self.racer_x<60:
                        self.racer_x+=1
                        self.delay(name='racer_to_3th', event_type=None, delay=0.02, handler=self.racer_to_3th)
                elif self.racer_x>60:
                        self.racer_x-=1
                        self.delay(name='racer_to_3th', event_type=None, delay=0.02, handler=self.racer_to_3th)
                self.racer_animation_update()
        def racer_to_4th(self):
                if self.racer_x<30:
                        self.racer_x+=1
                        self.delay(name='racer_to_4th', event_type=None, delay=0.02, handler=self.racer_to_4th)
                elif self.racer_x>30:
                        self.racer_x-=1
                        self.delay(name='racer_to_4th', event_type=None, delay=0.02, handler=self.racer_to_4th)
                self.racer_animation_update()
        def racer_to_5th(self):
                if self.racer_x<10:
                        self.racer_x+=1
                        self.delay(name='racer_to_5th', event_type=None, delay=0.02, handler=self.racer_to_5th)
                elif self.racer_x>10:
                        self.racer_x-=1
                        self.delay(name='racer_to_5th', event_type=None, delay=0.02, handler=self.racer_to_5th)
                self.racer_animation_update()

class Bike3_animation(game.Mode):
        def __init__(self, game, priority):
                super(Bike3_animation, self).__init__(game, priority)
        def mode_started(self):
                self.bike3_x=20
                self.bike4_x=-10
                self.bike5_x=56
                self.bike6_x=92
                self.changedirection=1
                self.bike3_animation_update()

        def bike3_animation_update(self):
                if self.changedirection>=0:
                        self.bike3_x+=1
                        self.bike4_x+=1
                        self.bike5_x+=1
                        self.bike6_x+=1
                        self.changedirection+=1
                        if self.changedirection>=20:
                                self.changedirection=-1
                else:
                        self.bike3_x-=1
                        self.bike4_x-=1
                        self.bike5_x-=1
                        self.bike6_x-=1
                        self.changedirection-=1
                        if self.changedirection<=-20:
                                self.changedirection=0
                anim = dmd.Animation().load(dmd_path+'bike1.dmd')
                self.animation_bike_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False)
                self.animation_bike3_layer = self.animation_bike_layer
                self.animation_bike3_layer.set_target_position(self.bike3_x, 01)
                self.animation_bike4_layer = self.animation_bike_layer
                self.animation_bike4_layer.set_target_position(self.bike4_x, 03)
                self.animation_bike5_layer = self.animation_bike_layer
                self.animation_bike5_layer.set_target_position(self.bike5_x, 04)
                self.animation_bike6_layer = self.animation_bike_layer
                self.animation_bike6_layer.set_target_position(self.bike6_x, 02)
                self.layer = dmd.GroupedLayer(128, 32, [self.animation_bike3_layer,self.animation_bike4_layer, self.animation_bike5_layer, self.animation_bike6_layer])
                self.layer.composite_op = "alpha"
                self.delay(name='update_bike3_animation', event_type=None, delay=0.1, handler=self.bike3_animation_update)

class House_animation(game.Mode):
        def __init__(self, game, priority):
                super(House_animation, self).__init__(game, priority)
        def mode_started(self):
                self.delay(name='update_house_animation', event_type=None, delay=8, handler=self.house_animation_update)

        def house_animation_update(self):
                anim = dmd.Animation().load(dmd_path+'house_small.dmd')
                self.animation_house_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=2)
                self.layer = self.animation_house_layer
                self.layer.composite_op = "alpha"
                self.delay(name='update_house_animation', event_type=None, delay=13, handler=self.house_animation_update)
