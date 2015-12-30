#
# Regular multiball
#
# Main game mode (1 of 4)
# 2 ball Multiball, lock balls for 3-ball multiball
# Jackpot on centerramp, superjackpot on rightramp
#
__author__="Steven"
__date__ ="$16 Oct 2012 14:24:37 PM$"

import procgame
import locale
from procgame import *

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Multiball(game.Mode):
        def __init__(self, game, priority):
            super(Multiball, self).__init__(game, priority)

            multi_anim = dmd.Animation().load(dmd_path+'mb_layer.dmd')
            self.mb_layer = dmd.AnimatedLayer(frames=multi_anim.frames, opaque=False, repeat=True, hold=False, frame_time=2)
            self.score_layer = dmd.TextLayer(125, 6, self.game.fonts['num_14x10'], "right", opaque=False)
            self.total_score_layer = dmd.TextLayer(128/2, 15, self.game.fonts['num_14x10'], "center", opaque=False) #num_09Bx7 num_14x10
            self.value_layer = dmd.TextLayer(126, 22, self.game.fonts['tiny7'], "right", opaque=False) #07x5
            self.text_layer1 = dmd.TextLayer(84, 8, self.game.fonts['07x5'], "center", opaque=False) #07x5
            self.text_layer2 = dmd.TextLayer(84, 18, self.game.fonts['07x5'], "center", opaque=False) #07x5

            self.game.lampctrl.register_show('multiball_start', lampshow_path +"attract/wiekensnel.lampshow")
            self.game.lampctrl.register_show('jackpot_show', lampshow_path +"attract/rightleft.lampshow")
            self.game.lampctrl.register_show('jackpot_ready', lampshow_path +"mb_jackpot_ready.lampshow")
            self.game.lampctrl.register_show('superjackpot_ready', lampshow_path +"mb_superjackpot_ready.lampshow")

            self.lamps_trafficlight = ['stoplight_green','stoplight_yellow','stoplight_red']
            self.lamps_ramp = ['megaScore','Rtimelock','Rlock','Rextraball']
            self.lamps_center = ['detourWL','Cextraball']

            self.jackpot_status='jackpot_lit'
            self.timelock='on'
            self.jackpot_setting = 1000000 # VIA MENU
            self.superjackpot_setting = 2500000 # VIA MENU
##            self.ballsaver = True
            self.multiball_score = 0
            self.multiball_status = 'restart_enabled'

        def mode_started(self):
            print("Debug, Multiball Mode Started")
            self.game.set_player_stats('game_feature_running',True)
            self.game.effects.clear_all_lamps()
            self.game.effects.drive_lamp('multiBall','on')
            # start multiball intro
            self.multiball_intro()


        def mode_stopped(self):
            print("Debug, Multiball Mode Stopped")

## lamps & animations

        def update_lamps(self):
            # stop current lightshow
            self.game.lampctrl.stop_show()

            # update lamps for jackpot
            if self.jackpot_status=='jackpot_lit':
                self.game.lamps.Llock.disable()
                # update lamps right ramp
                for i in range(len(self.lamps_ramp)):
                     self.game.effects.drive_lamp(self.lamps_ramp[i],'off')
                # update lamps trafficlights
                for i in range(len(self.lamps_trafficlight)):
                     self.game.effects.drive_lamp(self.lamps_trafficlight[i],'off')
                # update lamps center ramp
                self.game.lampctrl.play_show('jackpot_ready', True, 'None')
                #for i in range(len(self.lamps_center)):
                #     self.game.effects.drive_lamp(self.lamps_center[i],'medium')

            # update lamps for superjackpot
            elif self.jackpot_status=='superjackpot_lit':
                self.game.lamps.Clock.disable()
                self.game.lamps.Llock.disable()
                # update lamps right ramp
                self.game.lampctrl.play_show('superjackpot_ready', True, 'None')
                #for i in range(len(self.lamps_ramp)):
                #     self.game.effects.drive_lamp(self.lamps_ramp[i],'medium')
                # update trafficlights
                for i in range(len(self.lamps_trafficlight)):
                     self.game.effects.drive_lamp(self.lamps_trafficlight[i],'medium')
                # update lamps center
                for i in range(len(self.lamps_center)):
                     self.game.effects.drive_lamp(self.lamps_center[i],'off')

            # update lamps for after jackpot or superjackpot
            elif self.jackpot_status=='jackpot_done' or self.jackpot_status=='superjackpot_done':
                # update lamps right ramp
                for i in range(len(self.lamps_ramp)):
                     self.game.effects.drive_lamp(self.lamps_ramp[i],'off')
                # update lamps center
                for i in range(len(self.lamps_center)):
                     self.game.effects.drive_lamp(self.lamps_center[i],'off')
                # update trafficlights
                for i in range(len(self.lamps_trafficlight)):
                     self.game.effects.drive_lamp(self.lamps_trafficlight[i],'off')
                # update next jackpot
                if self.jackpot_status=='jackpot_done':
                    self.game.effects.drive_lamp('detourWL','medium')
                else: # superjackpot_done
                    self.game.effects.drive_lamp('Llock','medium')

            # update lamps for timelocks
            if self.multiball_status != 'restart_active':
                if self.timelock=='on':
                    self.game.effects.drive_lamp('Ltimelock','medium')
                    self.game.effects.drive_lamp('Ctimelock','medium')
                elif self.timelock=='off':
                    self.game.effects.drive_lamp('Ltimelock','off')
                    self.game.effects.drive_lamp('Ctimelock','off')
            else:
                    self.game.effects.drive_lamp('Ltimelock','superfast')
                    self.game.effects.drive_lamp('Ctimelock','off')
                    self.game.coils.GIrelay.schedule(schedule=0x0000000f, cycle_seconds=9, now=True)

            # update lamps for double scores
            if self.game.trough.num_balls_in_play==3:
                self.game.effects.drive_lamp('allScoresDouble','medium')
            else:
                self.game.effects.drive_lamp('allScoresDouble','off')

            # Update lamp kickback
            self.game.base_game_mode.kickback.update_lamps()

        def multiball_animation(self):
             anim = dmd.Animation().load(dmd_path+"rk_mball_start.dmd")
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True,frame_time=4)
             self.layer=self.animation_layer

        def jackpot_animation(self, award):
             self.cancel_delayed('display_multiball_layer')
             if award == 'jackpot':
                  anim = dmd.Animation().load(dmd_path+"nf_jackpot.dmd")
             elif award == 'superjackpot':
                  anim = dmd.Animation().load(dmd_path+"nf_superjackpot.dmd")
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False,frame_time=4)
             #self.animation_layer.add_frame_listener(-1, self.show_jackpot_value)
             self.animation_layer.add_frame_listener(-1, self.display_multiball_layer)
             self.layer=dmd.GroupedLayer(128,32,[self.animation_layer])

        def show_jackpot_value(self):
             if self.jackpot_status=='superjackpot_lit':
                    self.value_layer.set_text("  SUPERJACKPOT: "+str(locale.format("%d", self.superjackpot_value, True))+"  ")
             else: #begin en end with withspaces to overwrite 'Ball 1 free play' line
                    self.value_layer.set_text("   JACKPOT: "+str(locale.format("%d", self.jackpot_value, True))+"   ")
             self.layer = self.value_layer

        def display_multiball_layer(self):
             p = self.game.current_player()
             scoreString = locale.format("%d",p.score, True)
             self.score_layer.set_text(scoreString,blink_frames=4)
             if self.jackpot_status=='superjackpot_lit':
                 self.value_layer.set_text(" Superjackpot: "+str(locale.format("%d", self.superjackpot_value, True)))
             else:
                 self.value_layer.set_text(" Jackpot: "+str(locale.format("%d", self.jackpot_value, True)))
             self.layer = dmd.GroupedLayer(128, 32, [self.mb_layer, self.value_layer, self.score_layer])
             self.delay(name='display_multiball_layer', event_type=None, delay=0.3, handler=self.display_multiball_layer)

        def display_lock_layer(self):
             self.text_layer1.set_text("Lock balls", blink_frames=8)
             self.text_layer2.set_text("in ejectholes", blink_frames=8)
             self.layer = dmd.GroupedLayer(128, 32, [self.mb_layer, self.text_layer1, self.text_layer2])

        def display_restart_layer(self):
             self.cancel_delayed('display_multiball_layer')
             self.text_layer1.set_text("Restart multiball", blink_frames=2)
             self.text_layer2.set_text("shoot workshop", blink_frames=2)
             self.layer = dmd.GroupedLayer(128, 32, [self.mb_layer, self.text_layer1, self.text_layer2])

        def totalscore_animation(self):
             self.total_score_layer.set_text(locale.format("%d", self.multiball_score, True))
             self.animation_layer = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'mode_total.dmd').frames[0])
             self.layer=dmd.GroupedLayer(128,32,[self.animation_layer, self.total_score_layer])

        def clear_layer(self):
            self.layer = None

        def gi_blink(self):
            self.game.effects.gi_blinking(schedule=33333333, cycle_seconds=2)

## mode functions

        def multiball_intro(self):
            self.game.sound.play(self.game.assets.speech_mb_start)
            self.game.effects.gi_blinking(cycle_seconds=2)
            # delay animation to synchronise with sound
            self.delay(name='multiball_animation', event_type=None, delay=1, handler=self.multiball_animation)
            #play lightshow
            self.game.lampctrl.play_show('multiball_start', True, 'None')
            # delay gi to synchronise with animation
            self.delay(name='gi_blink', event_type=None, delay=7, handler=self.gi_blink)
            self.delay(name='setup_multiball', event_type=None, delay=8, handler=self.setup_multiball)

        def setup_multiball(self):
             #setup  multiball
             self.jackpot_status='jackpot_lit'
             #launch ball
             self.game.trough.launch_balls(1)
             #play music
             self.game.sound.play_music(self.game.assets.music_MBmode, loops=-1)
             #move ramp up
             self.game.base_game_mode.rampmove.move_ramp('up')
             #stop lightshow
             self.game.lampctrl.stop_show()
             #update lamps for entire game after lampshow
             self.game.base_game_mode.kickback.raise_kickback()
             self.delay(name='update_lamps', event_type=None, delay=1, handler=self.update_lamps)
             self.update_jackpot()
             #self.display_multiball_layer()
             self.display_lock_layer()
             self.game.base_game_mode.pause_pf_multiplier(set=False)
             self.delay(name='start_multiball', event_type=None, delay=10, handler=self.start_multiball)

        def end_multiball(self):
             self.cancel_delayed('display_multiball_layer')
             self.delay(name='stop_multiball', event_type=None, delay=2, handler=self.stop_multiball)
             self.jackpot_status=False
             self.totalscore_animation()
             self.game.set_player_stats('game_feature_running',False)
             self.game.set_player_stats('multiball_total',self.multiball_score)
             print('number balls in play = ', self.game.trough.num_balls_in_play)

        def stop_multiball(self):
             self.clear_layer()
             #self.game.coils.outhole.pulse(30)
             self.callback('multiball')

        def update_jackpot(self):
             if self.game.trough.num_balls_in_play == 3:
                  self.jackpot_value = self.jackpot_setting * 2
                  self.superjackpot_value = self.superjackpot_setting * 2
             else:
                  self.jackpot_value = self.jackpot_setting
                  self.superjackpot_value = self.superjackpot_setting
             #print("jackpotvalue = ", self.jackpot_value)
             #print("superjackpotvalue = ", self.superjackpot_value)
             self.update_lamps()
             #self.show_jackpot_value()

        def score_jackpot(self):
            # play sound, animation and lightshow
            self.multiball_status = 'restart_disabled'
            self.game.sound.play(self.game.assets.speech_mb_jackpot)
            self.jackpot_animation('jackpot')
            self.game.lampctrl.play_show('jackpot_show', False, 'None')
            # set jackpot status
            self.jackpot_status='jackpot_done'
            # calculate score
            self.game.score(self.jackpot_value)
            self.multiball_score+=self.jackpot_value
            # update lamps after lightshow
            self.delay(name='update_lamps', event_type=None, delay=3, handler=self.update_lamps)
            # raise droptarget after delay
            self.delay(name='raise_droptarget', event_type=None, delay=2, handler=self.game.effects.raise_droptarget)

        def score_superjackpot(self):
            # play sound, animation and lightshow
            self.game.sound.play(self.game.assets.speech_mb_superJackpot)
            self.jackpot_animation('superjackpot')
            self.game.lampctrl.play_show('jackpot_show', False, 'None')
            # set jackpot status
            self.jackpot_status='superjackpot_done'
            # calculate score
            self.game.score(self.superjackpot_value)
            self.multiball_score+=self.superjackpot_value
            self.game.base_game_mode.missions_modes.update_modes_completed(3)
            # update lamps after lightshow
            self.delay(name='update_lamps', event_type=None, delay=3, handler=self.update_lamps) #self.game.update_lamps

        def raise_jackpot(self):
             if self.jackpot_status=='superjackpot_lit':
                 self.superjackpot_setting += 10000
             else:
                 self.jackpot_setting += 5000
             self.update_jackpot()

        def eject_active(self, ejecthole):
            if self.timelock=='on' and self.multiball_status != 'restart_active':
                self.delay(name='kickout_'+ejecthole, event_type=None, delay=8, handler=self.kickout_eject, param=ejecthole)
                self.timelock='ball_captured'
                self.game.sound.play(self.game.assets.speech_mb_lock1)
                if ejecthole == 'Ceject':
                   self.game.lamps.Ctimelock.enable()
                else:
                   self.game.lamps.Ltimelock.enable()
            elif self.timelock=='ball_captured':
                if ejecthole == 'Ceject':
                   self.cancel_delayed('kickout_Leject')
                else:
                   self.cancel_delayed('kickout_Ceject')
                self.game.sound.play(self.game.assets.speech_mb_lock2)
                self.game.score(50000)
                self.game.trough.launch_balls(1)
                self.timelock='off'
            else:
                self.game.effects.eject_ball(location=ejecthole)
            self.update_jackpot()
            self.update_lamps()

        def kickout_eject(self, ejecthole):
            #self.game.coils[ejecthole].pulse(18)
            self.game.effects.eject_ball(location=ejecthole)
            self.timelock='on'
            self.update_lamps()

        def start_multiball(self):
             self.cancel_delayed('start_multiball')
             self.game.effects.eject_ball(location='all', ball_save=True)
             self.display_multiball_layer()
             self.update_lamps()

        def bumper(self):
             self.game.score(10)
             self.game.sound.play(self.game.assets.sfx_bumper)
             self.raise_jackpot()

## switches

        def sw_Ceject_active(self, sw):
             return procgame.game.SwitchStop
        def sw_Ceject_active_for_600ms(self,sw):
             self.eject_active('Ceject')
             self.update_jackpot()

        def sw_Leject_active(self, sw):
             if self.jackpot_status == 'superjackpot_lit' and self.game.switches.rampRaise.is_inactive():
                 self.game.base_game_mode.rampmove.move_ramp('down')
             return procgame.game.SwitchStop
        def sw_Leject_active_for_600ms(self,sw):
             if self.multiball_status == 'restart_active':
                self.game.effects.drive_flasher('workshopFlash','off')
                self.multiball_intro()
                self.multiball_status = 'restart_disabled'
                self.cancel_delayed('end_multiball')
                self.game.sound.stop_music()
                self.update_lamps()
             else:
                if self.jackpot_status=='superjackpot_done': #Jackpot ready
                   self.jackpot_status='jackpot_lit'
                   self.game.sound.play(self.game.assets.speech_mb_jackpotIsLit)
                   self.game.base_game_mode.rampmove.move_ramp('up')
                self.eject_active('Leject')
             self.update_jackpot()

        def sw_upperLkicker_active(self, sw):
            self.delay(name='ulkicker', event_type=None, delay=2, handler=self.game.effects.eject_ball, param='upperLkicker')
            return procgame.game.SwitchStop

        def sw_RrampExit_active(self,sw):
            if self.jackpot_status=='superjackpot_lit':
                self.score_superjackpot()
            if self.game.get_player_stats('million_plus'): #million plus is stackable
                self.game.base_game_mode.generalplay.score_millionplus()
            return procgame.game.SwitchStop

        def sw_dropTarget_active(self,sw):
            self.game.score(50000)
            if self.jackpot_status=='jackpot_done': #Superjackpot ready
                self.jackpot_status='superjackpot_lit'
                self.game.sound.play(self.game.assets.speech_mb_superJackpotIsLit)
                self.game.base_game_mode.rampmove.move_ramp('down')
                self.update_lamps()

        def sw_CrampEnter_active(self,sw):
            self.game.score(50000)
            if self.jackpot_status=='jackpot_lit':
                self.score_jackpot()
            return procgame.game.SwitchStop

        def sw_bumperL_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop

        def sw_bumperU_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop

        def sw_bumperR_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop

        def sw_bumperD_active(self,sw):
            self.bumper()
            return procgame.game.SwitchStop

        # make sure ball is plunged before starting multiball
        def sw_shooterLane_open_for_2s(self,sw):
             self.start_multiball()
             #self.game.effects.eject_ball(location='all', ball_save=True)
             #self.display_multiball_layer()
             #self.update_lamps()

        def sw_Lspinner_active(self, sw):
             self.game.score(10000)
             self.game.sound.play(self.game.assets.sfx_bumper)
             return procgame.game.SwitchStop

        # check whether allscoresdouble or end mode when a ball drains
        def sw_outhole_active(self,sw):
            print('number balls in play=', self.game.trough.num_balls_in_play)
            if self.game.trough.num_balls_in_play==3:
                self.game.coils.outhole.pulse(30)
                #self.update_lamps()
                # update jackpot when ball is in trough
                self.delay(name='update_jackpot', event_type=None, delay=1, handler=self.update_jackpot)
            elif self.game.trough.num_balls_in_play==2:
                if self.timelock=='ball_captured':
                   self.cancel_delayed('kickout_Leject')
                   self.cancel_delayed('kickout_Ceject')
                   self.game.effects.eject_ball()
                if self.multiball_status == 'restart_disabled':
                        # end after grace period
                        self.multiball_status='over'
                        self.delay(name='end_multiball', event_type=None, delay=2, handler=self.end_multiball)
                elif self.multiball_status == 'restart_enabled':
                        self.timelock='on'
                        self.display_restart_layer()
                        self.game.effects.drive_flasher('workshopFlash','fast',seconds_on=10)
                        self.delay(name='end_multiball', event_type=None, delay=11, handler=self.end_multiball)
                        self.multiball_status = 'restart_active'
                        self.update_lamps()

        def sw_trough2_active_for_1500ms(self,sw):
            if self.multiball_status!='over':
                if self.game.switches.trough3.is_active():
                   self.multiball_status='over'
                   self.end_multiball()
                else:
                    if self.timelock=='ball_captured':
                        self.cancel_delayed('kickout_Leject')
                        self.cancel_delayed('kickout_Ceject')
                        self.timelock='on'
                        self.game.effects.eject_ball()
                    if self.multiball_status == 'restart_disabled':
                        # end after grace period
                        self.multiball_status='over'
                        self.delay(name='end_multiball', event_type=None, delay=2, handler=self.end_multiball)
                    elif self.multiball_status == 'restart_enabled':
                        self.delay(name='end_multiball', event_type=None, delay=10, handler=self.end_multiball)
                        self.multiball_status = 'restart_active'
                        self.update_lamps()