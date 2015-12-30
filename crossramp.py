#
# Crossramp
#
# Game mode that uses centerramp for shot sequence
# completing nr. of shots awards hurry-up
#
__author__="Pieter"
__date__ ="$18 Sep 2012 20:36:37 PM$"

import procgame
import locale
from procgame import *

# all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"


class Crossramp(game.Mode):

        def __init__(self, game, priority):
            super(Crossramp, self).__init__(game, priority)

            self.title_layer = dmd.TextLayer(128/2, 4, self.game.fonts['num_09Bx7'], "center", opaque=False) #07x5/num_09Bx7
            self.value_layer = dmd.TextLayer(128/2, 16, self.game.fonts['num_14x10'], "center", opaque=False)
            #self.value_layer = dmd.TextLayer(128/2, 12, self.game.fonts['num_09Bx7'], "center", opaque=False) #num_14x10
            #self.number_layer = dmd.TextLayer(128/2, 22, self.game.fonts['07x5'], "center", opaque=False)
            self.hurryup_layer = dmd.TextLayer(128/2, 12, self.game.fonts['num_14x10'], "center", opaque=False)

            self.game.lampctrl.register_show('hurryup_show', lampshow_path+"succes.lampshow")

            self.bonuslamps = ['bonus1k','bonus2k','bonus3k','bonus4k','bonus5k','bonus6k','bonus7k','bonus8k','bonus9k','bonus10k']
            self.hurryuplamps = ['Ctimelock','Clock']

            self.crossramp_base = 100000
            self.crossramp_data = 0
            #self.crossramps_max = 11 # VIA MENU
            self.crossramps_max = self.game.user_settings['Gameplay (Feature)']['Xramps For Hurryup']
            #self.hurryup_base = 10000000 # VIA MENU
            self.hurryup_base = self.game.user_settings['Gameplay (Feature)']['Xramps Hurryup Value']
            self.crossramp_level = 1
            self.counter = 0
            self.ramp_repeat = False
            self.next_ramp = 'right'
            self.hurryup_running = False

        def reset(self):
            pass

        def mode_started(self):
            print("Debug, Crossramp Mode Started")
            #self.update_lamps()
            #load player specific data
            self.crossramp_level = self.game.get_player_stats('crossramp_level')
            self.number_crossramps = self.get_crossramps()
            #print("crossramps=" + str(self.number_crossramps))
            self.set_crossramp_values()

        def mode_stopped(self):
            self.clear_lamps()
            self.clear_layer()
            # save player specific data
            self.game.set_player_stats('crossramp_level',self.crossramp_level)
            print("Debug, Crossramp Mode Ended")

        def mode_tick(self):
            pass

## lamps & animations

        def update_lamps(self):
             # turn detour lamp on
             self.game.effects.drive_lamp('detourWL','medium')

        def clear_lamps(self):
             for i in range(len(self.bonuslamps)):
                 self.game.effects.drive_lamp(self.bonuslamps[i],'off')
             self.game.effects.drive_lamp('detourWL','off')
             if self.game.switches.dropTarget.is_active():
                 self.game.effects.drive_lamp('spotLetter','off')

        def light_hurryup_lamps(self):
             self.game.effects.drive_lamp('detourWL','smarton')
             for i in range(len(self.hurryuplamps)):
                 self.game.effects.drive_lamp(self.hurryuplamps[i],'fast')
             self.game.effects.drive_flasher('showroomFlash','fast')

        def clear_hurryup_lamps(self):
             for i in range(len(self.hurryuplamps)):
                 self.game.effects.drive_lamp(self.hurryuplamps[i],'off')
             self.game.effects.drive_flasher('showroomFlash','off')

        def light_crossramps(self):
             for i in range(self.number_crossramps):
                 self.game.effects.drive_lamp(self.bonuslamps[i],'medium')

        def bonuslamps_arrow(self, seconds=1):
             self.game.lamps.detourWL.schedule(schedule=0x55555555, cycle_seconds=3, now=True)
             self.game.lamps.bonus1k.schedule(schedule=0b00001111111111110000111111111111, cycle_seconds=seconds, now=True)
             self.game.lamps.bonus2k.schedule(schedule=0b00011111111111100001111111111110, cycle_seconds=seconds, now=True)
             self.game.lamps.bonus3k.schedule(schedule=0b00111111111111000011111111111100, cycle_seconds=seconds, now=True)
             self.game.lamps.bonus4k.schedule(schedule=0b01111111111110000111111111111000, cycle_seconds=seconds, now=True)
             self.game.lamps.bonus5k.schedule(schedule=0b11111111111100001111111111110000, cycle_seconds=seconds, now=True)
             self.game.lamps.bonus6k.schedule(schedule=0b11111111111000001111111111100000, cycle_seconds=seconds, now=True)
             self.game.lamps.bonus7k.schedule(schedule=0b11111111110000001111111111000000, cycle_seconds=seconds, now=True)
             self.game.lamps.bonus8k.schedule(schedule=0b11111111100000001111111110000000, cycle_seconds=seconds, now=True)
             self.game.lamps.bonus9k.schedule(schedule=0b11111111000000001111111100000000, cycle_seconds=seconds, now=True)
             self.game.lamps.bonus10k.schedule(schedule=0b11111110000000001111111000000000, cycle_seconds=seconds, now=True)

        def crossramp_animation(self):
            if self.next_ramp == 'right':
                anim = dmd.Animation().load(dmd_path+'crossramp_right.dmd')
                self.title_layer.set_text('CROSSRAMP RIGHT')
            else:
                anim = dmd.Animation().load(dmd_path+'crossramp_left.dmd')
                self.title_layer.set_text('CROSSRAMP LEFT')

            self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=False, frame_time=4)
            self.animation_layer.add_frame_listener(-1, self.clear_layer)
            self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.title_layer, self.value_layer])

        def hurryup_animation(self):
             anim = dmd.Animation().load(dmd_path+'crossramp_hurryup.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=7)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.hurryup_layer])

        def inform_player(self):
             anim = dmd.Animation().load(dmd_path+'crossramp_inform.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=20)
             self.layer = self.animation_layer

        def hurryup_scored_ani(self):
             anim = dmd.Animation().load(dmd_path+'crossramp_hurryup_scored.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=10)
             self.layer = dmd.GroupedLayer(128, 32, [self.animation_layer, self.hurryup_layer])

        def clear_layer(self):
             self.layer = None

## mode functions

        def get_crossramps(self):
             self.crossramp_data = self.game.get_player_stats('crossramps_made')
             #extract last digit (0-9) for completion till 10
             nr_crossramps = int(str(self.crossramp_data)[-1:])
             return nr_crossramps

        def raise_crossramps(self,number=1):
             #external call; raise number of crossramps with parameter.
             #Only if below maximum - number to prevent overflow (e.g.):
             # 5 < (10 - 2) = valid, raise to 7
             # 7 < (10 - 3) = not valid, don't raise
             if self.number_crossramps < (self.crossramps_max - number):
                 self.number_crossramps += number
                 self.game.add_player_stats('crossramps_made',number)

        def set_crossramp_values(self, value=100000):
             # check for raise ramp value, else use standard value
             # Used for external call (trademiles.py) to raise value
             if value > 100000:
                 self.crossramp_value = value
             else:
                 self.crossramp_value = self.crossramp_base*self.crossramp_level
             self.hurryup_value = self.hurryup_base*self.crossramp_level

        def check_crossramps_made(self):
             if self.number_crossramps < self.crossramps_max:
                 # add 1 crossramp
                 self.number_crossramps += 1
                 # save player specific data
                 self.game.add_player_stats('crossramps_made',1)

             if self.number_crossramps == self.crossramps_max:
                 self.number_crossramps = 0
                 # update missions
                 self.game.base_game_mode.missions_modes.update_missions(4)
                 # start hurry up
                 self.prepare_hurryup()

        def check_repeating_ramp(self):
             # if repeating shot, raise counter, else just count 1
             if self.ramp_repeat == True:
                 self.counter += 1
                 self.game.sound.play(self.game.assets.speech_thatsShooting)
                 # cancel previous delay if shot is repeated
                 self.cancel_delayed('clear_repeat')
             else:
                 self.counter = 1
             # set repeat=True and clear after 5 seconds
             self.ramp_repeat = True
             self.delay(name='clear_repeat', event_type=None, delay=4, handler=self.clear_repeat)

        def clear_repeat(self):
             self.ramp_repeat = False
             self.update_lamps()
             self.game.base_game_mode.missions_modes.update_mission_lamps()

        def prepare_hurryup(self):
             print ("prepare hurryup!")
             #stop music, play sound
             self.game.sound.fadeout_music(time_ms=250)
             self.game.sound.play(self.game.assets.sfx_hurryupStart)
             #play lampshow
             self.game.effects.gi_blinking(schedule=33003300, cycle_seconds=2)
             #play animation
             self.inform_player()
             # raise droptarget
             self.game.effects.raise_droptarget()
             #light lamps
             self.light_hurryup_lamps()
             # set hurryup status True
             self.hurryup_running = True
             # start after (delay) seconds, or if ball leaves ramp (see switches)
             self.delay(name='start_hurryup', event_type=None, delay=4, handler=self.start_hurryup)

        def start_hurryup(self):
             print ("start hurryup!")
             self.cancel_delayed('start_hurryup')
             #play music
             self.game.sound.play_music(self.game.assets.music_hurryupTheme, loops=0)
             #play animation
             self.hurryup_animation()
             #start countdown
             self.hurryup_countdown()

        def hurryup_countdown(self):
             # repeat call to itself to countdown hurryup value
             if self.hurryup_value > 500000:
                 self.hurryup_value -= (40230*self.crossramp_level)
                 self.delay(name='hurryup_countdown', event_type=None, delay=0.04, handler=self.hurryup_countdown)
                 self.hurryup_layer.set_text(locale.format("%d", self.hurryup_value, True))
             else:
                 self.game.sound.play(self.game.assets.sfx_hurryupMissed)
                 self.clear_hurryup()

        def score_hurryup(self):
             print ("score hurryup!")
             self.hurryup_running = False
             #stop hurryup music and play sound
             self.game.sound.stop_music()
             self.game.sound.play(self.game.assets.sfx_hurryupScored)
             #cancel hurryup countdown
             self.cancel_delayed('hurryup_countdown')
             #play lampshow
             self.game.lampctrl.play_show('hurryup_show', False, 'None')
             #play animation
             self.hurryup_scored_ani()
             #add score
             self.game.score(self.hurryup_value)
             # raise level
             self.crossramp_level += 1
             # eject ball after delay
             self.delay(name='eject_ball', event_type=None, delay=2.5, handler=self.game.effects.eject_ball)
             # clear hurryup after delay
             self.delay(name='clear_hurryup', event_type=None, delay=3, handler=self.clear_hurryup)

        def score_droptarget(self):
             print ("score droptarget!")
             self.hurryup_running = False
             #stop hurryup music and play sound
             self.game.sound.stop_music()
             self.game.sound.play(self.game.assets.sfx_hurryupMissed)
             #cancel hurryup countdown
             self.cancel_delayed('hurryup_countdown')
             #play animation
             self.hurryup_layer.set_text(locale.format("%d", 1000000, True))
             self.hurryup_scored_ani()
             #add score
             self.game.score(1000000)
             # clear hurryup after delay
             self.delay(name='clear_hurryup', event_type=None, delay=2, handler=self.clear_hurryup)
	     
        def clear_hurryup(self):
             print ("clear hurryup!")
             self.hurryup_running = False
             # stop hurryup music
             self.game.sound.stop_music()
             # calculate new  values
             self.set_crossramp_values()
             # cancel delays in case its running
             self.cancel_delayed('start_hurryup')
             self.cancel_delayed('hurryup_countdown')
             # restart main theme music
             self.game.assets.rk_play_music()
             self.game.effects.eject_ball('Ceject')
             # clear items
             self.clear_layer()
             self.clear_hurryup_lamps()
             # restore missionlamps
             self.game.base_game_mode.missions_modes.update_mission_lamps()

## switches

        def sw_CrampEnter_active_for_10ms(self,sw):
             # sounds&dots crossramps not during hurryup
             if self.hurryup_running == False:
                 # check for number of crossramps
                 self.check_crossramps_made()
                 # check for repeating shot
                 self.check_repeating_ramp()
                 # calculate score
                 display_score = self.counter*self.crossramp_value
                 self.game.score(display_score)
                 ### sounds&dots crossramps not during hurryup
                 ###if self.hurryup_running == False:
                 # play sound
                 self.game.sound.play(self.game.assets.sfx_xramp_shot)
                 # lamp effect
                 self.clear_lamps()
                 self.game.effects.drive_lamp('detourWL','smarton')
                 self.game.coils.bikesFlash_dropTarget.schedule(0x0F0F0F0F, cycle_seconds=1, now=True)
                 # light number of shots made
                 self.light_crossramps()
                 # play animation
                 self.value_layer.set_text(locale.format("%d", display_score, True), seconds=2, blink_frames=2)
                 #self.number_layer.set_text('crossramps: '+str(self.number_crossramps))
                 self.crossramp_animation()

        def sw_CrampRexit_active(self,sw):
             self.bonuslamps_arrow(2)
             self.next_ramp = 'left'
             if self.hurryup_running == True:
                  self.start_hurryup()

        def sw_lane4_active(self,sw):
             if self.game.switches.CrampEnter.time_since_change() < 3:
                 self.bonuslamps_arrow(2)
                 self.next_ramp = 'right'
                 if self.hurryup_running == True:
                     self.start_hurryup()

        def sw_Ceject_active(self, sw):
             if self.hurryup_running == True:
                 self.score_hurryup()
                 #self.game.sound.play(self.game.assets.sfx_hurryupMissed)
                 #self.clear_hurryup()
                 return procgame.game.SwitchStop

        def sw_dropTarget_active(self,sw):
             if self.hurryup_running == True:
                 self.score_droptarget()
                 #self.game.sound.play(self.game.assets.sfx_hurryupMissed)
                 #self.clear_hurryup()
                 #self.score_hurryup()
                 return procgame.game.SwitchStop

        def sw_outhole_active(self,sw):
             if self.hurryup_running == True:
                 self.clear_hurryup()
