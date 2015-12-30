import sys
sys.path.append(sys.path[0]+'/../..') # Set the path so we can find procgame.  We are assuming (stupidly?) that the first member is our directory.
import procgame
import pinproc
from effects import *
from assets import *
from extra_ball import *
from info import *
from bonus import *
from general_play import *
from kickback import *
from match import *
from bumpers import *
from ramp_move import *
from lanes1234 import *
from targets_roadkings import *
from crossramp import*
from combos import*
from missions_modes import *
from skillshot import *
from gametips import *
from procgame import *
from threading import Thread
from random import *
from time import strftime
import string
import time
import locale
import math
import copy
import yaml
import random
import logging

##
## 30-07-2013: Software Version 1.5
## 07-09-2013: Software Version 1.66
## 04-10-2013: Software Version 1.7
## 28-10-2013: Software Version 2.0 DPO (Dutch Pinball Open)
## 01-12-2013: Software Version 2.1 
## 16-12-2013: Software version 2.1.2
## 02-04-2013: Software version 2.1.3
## 27-08-2014: Software version 2.1.4
##
logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

#game_locale = config.value_for_key_path('std_locale')
locale.setlocale(locale.LC_ALL,"USA") # used to put commas in the score.

# set overall game path
game_path = config.value_for_key_path('game_path')
print("Using game_path at: %s "%(game_path))
logging.info("Game Path is: "+game_path)

# set linked data path
linked_data_path = config.value_for_key_path('linked_data_path')
print("Using linked_data_path at: %s "%(linked_data_path))
#logging.info("linked_data_path is: "+linked_data_path)

# set configuration paths
machine_config_path = game_path + "config/RoadKings.yaml"
settings_path = game_path +"config/settings.yaml"
game_data_path = game_path +"config/game_data.yaml"
game_data_template_path = game_path +"config/game_data_template.yaml"
settings_template_path = game_path +"config/settings_template.yaml"

# set all paths
fonts_path = game_path + "dmd/fonts/"
shared_sound_path = game_path + "sound/service/"
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
lampshow_path = game_path +"lampshows/"

# set fonts
font_luc12 = dmd.Font(fonts_path+"lucida12.dmd")
font_ber16 = dmd.Font(fonts_path+"berlin16.dmd")
font_hh20 = dmd.Font(fonts_path+"hh20.dmd")
#font_cal13b = dmd.Font(fonts_path+"calibri13b.dmd")
#font_dg18 = dmd.Font(fonts_path+"dg_18aa.dmd")
#font_deut18 = dmd.Font(fonts_path+"deutsch18.dmd")
#font_fl12 = dmd.Font(fonts_path+"fl12.dmd")
font_gow10 = dmd.Font(fonts_path+"gow10ctw.dmd")
font_gow12 = dmd.Font(fonts_path+"gow12ctw.dmd")
font_gow15 = dmd.Font(fonts_path+"gow15.dmd")
#font_gow25 = dmd.Font(fonts_path+"gow25.dmd")
#font_cc5 = dmd.Font(fonts_path+"Font_CC_5px_AZ.dmd")
#font_cc6 = dmd.Font(fonts_path+"Font_CC_6px_az.dmd")
#font_cc7 = dmd.Font(fonts_path+"Font_CC_7px_az.dmd")
#font_cc7B = dmd.Font(fonts_path+"Font_CC_7px_bold_az.dmd")
#font_cc12 = dmd.Font(fonts_path+"Font_CC_12px_az.dmd")
font_tiny7 = dmd.Font(fonts_path+"04B-03-7px.dmd")
font_14x10 = dmd.Font(fonts_path+"Font14x10.dmd")
font_18x12 = dmd.Font(fonts_path+"Font18x12.dmd")
font_07x4 = dmd.Font(fonts_path+"Font07x4.dmd")
font_07x5 = dmd.Font(fonts_path+"Font07x5.dmd")
font_09Bx7 = dmd.Font(fonts_path+"Font09Bx7.dmd")

# set lampshow files for attract mode
lampshow_files = [lampshow_path +"attract/vertikaal.lampshow", \
                  lampshow_path +"attract/horizontaal.lampshow", \
                  lampshow_path +"attract/bigwheel.lampshow", \
                  lampshow_path +"attract/rightleft.lampshow", \
                  lampshow_path +"attract/wiekenlangzaam.lampshow", \
                  lampshow_path +"attract/wiekensnel.lampshow", \
                  lampshow_path +"attract/wisselend.lampshow", ]


class Attract(game.Mode):
    """docstring for AttractMode"""
    def __init__(self, game):
        super(Attract, self).__init__(game, 1)
        self.player_layers = []
        self.attracttime = 50
        #Disable flippers
        self.game.coils.flipperEnable.disable()

    def mode_started(self):

                # run feature lamp patterns
                self.change_lampshow()

                # run attract sounds
                if self.game.user_settings['Gameplay (Feature)']['Attract Mode Sounds'] == 'Yes':
                    self.delay(name='attract_sounds', event_type=None, delay=20, handler=self.play_attractsounds)

                #check for stuck balls
                self.delay(name='stuck_balls', event_type=None, delay=2, handler=self.game.effects.release_stuck_balls)

                print("Trough is full:" +str(self.game.trough.is_full()))

                #create dmd attract screens
                self.superpinball_logo = dmd.AnimatedLayer(frames=dmd.Animation().load(game_path+'dmd/splogo_new.dmd').frames,frame_time=8,hold=True) #splog.dmd
                self.superpinball_logo.transition = dmd.CrossFadeTransition(width=128,height=32)

                self.presents = dmd.TextLayer(128/2, 10, font_09Bx7, "center", opaque=False).set_text("PRESENTS")
                self.presents.transition = dmd.CrossFadeTransition(width=128,height=32)

                self.version = dmd.TextLayer(128, 26, font_tiny7, "right", opaque=False).set_text("v2.1.4") #font_07x4, font_tiny7
                self.rk_logo = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(game_path+'dmd/RKR_Logo.dmd').frames[0]) #RKR_Logo , road_kingsll
                self.roadkings_logo_v = dmd.GroupedLayer(128, 32, [self.rk_logo, self.version])
                self.roadkings_logo_v.transition = dmd.ExpandTransition(direction='vertical')
                self.roadkings_logo = dmd.GroupedLayer(128, 32, [self.rk_logo])
                self.roadkings_logo.transition = dmd.PushTransition(direction='west')

                self.williams_logo = dmd.AnimatedLayer(frames=dmd.Animation().load(game_path+'dmd/williams_animated.dmd').frames,frame_time=1,hold=True)

                self.proc_logo = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load(game_path+'dmd/splash.dmd').frames[0])
                self.proc_logo.transition = dmd.ExpandTransition(direction='vertical')

                self.game_tips = self.game.gametips.get_tip()

                self.press_start = dmd.TextLayer(128/2, 18, font_09Bx7, "center", opaque=False).set_text("PRESS START", seconds=None, blink_frames=1)
                self.free_play = dmd.TextLayer(128/2, 6, font_09Bx7, "center", opaque=False).set_text("FREE PLAY")
                self.coins_layer = dmd.GroupedLayer(128, 32, [self.free_play, self.press_start])
                self.coins_layer.transition = dmd.PushTransition(direction='north')

                #create last scores screens
                self.p1_layer = dmd.TextLayer(0, 0, self.game.fonts['num_09Bx7'], "left", opaque=False)
                self.p2_layer = dmd.TextLayer(128, 0, self.game.fonts['num_09Bx7'], "right", opaque=False)
                self.p3_layer = dmd.TextLayer(0, 24, self.game.fonts['num_09Bx7'], "left", opaque=False)
                self.p4_layer = dmd.TextLayer(128, 24, self.game.fonts['num_09Bx7'], "right", opaque=False)
                self.last_scores_layer = dmd.GroupedLayer(128, 32, [self.p1_layer,self.p2_layer,self.p3_layer,self.p4_layer])
                self.last_scores_layer.transition = dmd.CrossFadeTransition(width=128,height=32)

                self.game_over_layer = dmd.TextLayer(128/2, 10, font_09Bx7, "center", opaque=True).set_text("GAME OVER")
                self.game_over_layer.transition = dmd.CrossFadeTransition(width=128,height=32)

                self.scores_layer = dmd.TextLayer(128/2, 11, font_09Bx7, "center", opaque=True).set_text("HIGH SCORES")
                self.scores_layer.transition = dmd.PushTransition(direction='west')

                gen = dmd.MarkupFrameGenerator()
                gen.font_plain = font_tiny7 #font_luc12
                gen.font_bold = font_09Bx7 #font_ber16  font_hh20
                credits_frame = gen.frame_for_markup("""

#CREDITS#

#Rules & concept:#
[Steven van der Staaij]
[Pieter van Leijen]

#Initial design:#
[Steven van der Staaij]

#Lead programming:#
[Pieter van Leijen]

#Dots & Animations:#
[Pieter van Leijen]
[Steven van der Staaij]

#Music & SFX:#
[Pieter van Leijen]

#Special thanks to#
[Jean-Paul de W.]
[Richard B.]
[Mark S.]

#Thanks for the help:#
[Gerry Stellenberg]
[Adam Preble]
[Members Pinballcontrollers forum]


""")

                self.credits_layer = dmd.PanningLayer(width=128, height=32, frame=credits_frame, origin=(0,0), translate=(0,1), bounce=False)

                #run attract dmd screens
                self.attract_display()
                self.change_gametip()

    def sw_outhole_active(self, sw):
            self.game.coils.outhole.pulse(30)
            return True

    def change_lampshow(self):
            shuffle(self.game.lampshow_keys)
            self.game.lampctrl.play_show(self.game.lampshow_keys[0], repeat=True)
            self.delay(name='attract_lampshow', event_type=None, delay=10, handler=self.change_lampshow)

    def attract_display(self):
            script = list()

            script.append({'seconds':1.0, 'layer':self.proc_logo})
            script.append({'seconds':5.0, 'layer':self.superpinball_logo})
            script.append({'seconds':3.0, 'layer':self.presents})
            script.append({'seconds':5.0, 'layer':self.roadkings_logo_v})
            script.append({'seconds':6.0, 'layer':self.game_tips})
            script.append({'seconds':6.0, 'layer':self.williams_logo})
            script.append({'seconds':3.0, 'layer':self.coins_layer})
            script.append({'seconds':6.0, 'layer':self.game_tips})
            script.append({'seconds':3.0, 'layer':self.scores_layer})
            for frame in highscore.generate_highscore_frames(self.game.highscore_categories):
                new_layer = dmd.FrameLayer(frame=frame)
                new_layer.transition = dmd.PushTransition(direction='west')
                script.append({'seconds':2.0, 'layer':new_layer})
            script.append({'seconds':5.0, 'layer':self.roadkings_logo})
            script.append({'seconds':23.0, 'layer':self.credits_layer})

            #add in the game over screen
            go_index=4
            go_time=3
            if self.game.system_status=='game_over':
                go_index=0
                go_time=3

                #add in the player scores after a game is played
                self.player_layers=[self.p1_layer,self.p2_layer,self.p3_layer,self.p4_layer]
                for i in range(len(self.game.players)):
                     score = self.game.players[i].score
                     self.player_layers[i].set_text(locale.format("%d", score, True))

                ls_index=0
                ls_time=10
                self.game.system_status='attract'
                print("system status = "+self.game.system_status.upper())

                script.insert(ls_index,{'seconds':ls_time, 'layer':self.last_scores_layer})

            script.insert(go_index,{'seconds':go_time, 'layer':self.game_over_layer})

            self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)

    def mode_stopped(self):
        self.game.lampctrl.stop_show()

    def mode_tick(self):
        pass

    # Enter service mode when the enter button is pushed.
    def sw_enter_active(self, sw):
        # cancel lights & sounds
        self.cancel_delayed('attract_lampshow')
        self.cancel_delayed('attract_sounds')
        self.game.lampctrl.stop_show()
        for lamp in self.game.lamps:
            lamp.disable()
        self.game.modes.add(self.game.service_mode)
        return True

    def sw_exit_active(self, sw):
        return True

    # Outside of the service mode, up/down control audio volume.
    def sw_down_active(self, sw):
        volume = self.game.sound.volume_down()
        self.game.set_status("Volume Down : " + str(volume))
        return True

    def sw_up_active(self, sw):
        volume = self.game.sound.volume_up()
        self.game.set_status("Volume Up : " + str(volume))
        return True

    # Start button starts a game if the trough is full.
    # Otherwise it initiates a ball search.
    def sw_startButton_active(self, sw):
        #check for change game data
        if self.game.switches.exit.is_active():
            self.game.sound.play(self.game.assets.sfx_linked)
            self.game.change_game_data()
        #reload game data for linked games, to make sure latest highscores are used
        if self.game.linked_game == True:
            self.game.load_game_data(game_data_path, linked_data_path)

        if self.game.trough.is_full:
            # Remove attract mode from mode queue - Necessary?
            self.game.modes.remove(self)
            # Initialize game
            self.game.start_game()
            # Add the first player
            self.game.add_player()
            # Start the ball.  This includes ejecting a ball from the trough.
            self.game.start_ball()
            # Check if ball is served in shooterlane after delay. (To solve a 'once-in-a-while' error)
            self.game.base_game_mode.generalplay.check_ball_in_shooter_delay()
            #SYS11: enable the flippers
            self.game.coils.flipperEnable.enable()
        else:
            self.game.set_status("Ball Search!")
            self.game.effects.ball_search()
        return True

    def play_attractsounds(self):
         # call itself and add X sec. so time between voice calls gets bigger everytime
         self.game.sound.play_voice(self.game.assets.speech_attract)
         self.delay(name='attract_sounds', event_type=None, delay=self.attracttime, handler=self.play_attractsounds)
         self.attracttime += 20

    def change_gametip(self):
         self.game_tips = self.game.gametips.get_tip()
         self.delay(name='change_gametip', event_type=None, delay=32, handler=self.change_gametip)

class BaseGameMode(game.Mode):
    """docstring for BaseGameMode"""
    def __init__(self, game):
            super(BaseGameMode, self).__init__(game, 5)
            self.tilt_layer = dmd.TextLayer(128/2, 7, font_18x12, "center", opaque=True).set_text("TILT")
            self.multiply_layer = dmd.TextLayer(128/2, 26, font_07x5, "center", opaque=False)
            self.time1_layer = dmd.TextLayer(0, 0, self.game.fonts['num_09Bx7'], "left", opaque=False)
            self.time2_layer = dmd.TextLayer(128, 0, self.game.fonts['num_09Bx7'], "right", opaque=False)
            self.layer = None # Presently used for tilt layer
            self.ball_starting = True

            self.ball_saved = False
            self.ball_save_time = self.game.user_settings['Gameplay (Feature)']['Ballsave Timer']
            self.instant_info_on = False

    def mode_started(self):
        #debug
        print("Basic Game Mode Started, Ball "+str(self.game.ball))
        #set player status
        self.game.set_player_stats('status','general')

        #Disable any previously active lamp
        for lamp in self.game.lamps:
            lamp.disable()

        # Enable the flippers
        self.game.coils.flipperEnable.enable()

        # Each time this mode is added to game Q, set this flag true.
        self.ball_starting = True

        # Reset tilt warnings and status
        self.times_warned = 0;
        self.tilt_status = 0

        #reset playfield multiplier values
        self.game.set_pf_multiplier(value=1, time=0)

        #setup game modes
        self.add_game_modes(self);

        #Update lamp status's for all modes
        self.game.update_lamps()

        # GI on
        self.game.effects.gi_on()

        #Random select main tune
        self.game.assets.select_tune()

        # Put the ball into play and start tracking it.
        self.game.trough.launch_balls(1, self.ball_launch_callback)

        #Not SYS11: Enable ball search in case a ball gets stuck during gameplay.
        #self.game.ball_search.enable()

        # In case a higher priority mode doesn't install it's own ball_drained handler.
        self.game.trough.drain_callback = self.ball_drained_callback

        #ball save callback - exp
        self.game.ball_save.callback = self.ball_save_callback

    def add_game_modes(self,ball_in_play):

            #lower priority game modes
            self.generalplay = Generalplay(self.game, 20)
            self.bumpers = Bumpers(self.game, 22)
            self.rampmove = Rampmove(self.game, 24)
            self.lanes1234 = Lanes1234(self.game, 26)
            self.targets_roadkings = TargetsRoadkings(self.game, 28)

            #medium priority game modes

            self.combo = Combo(self.game, 44)

            #higher priority game modes
            self.crossramp = Crossramp(self.game, 62)
            self.missions_modes = MissionsModes(self.game, 64)
            self.skillshot = Skillshot(self.game, 66)
            self.skillshot.callback = self.skillshot_callback
            self.kickback = Kickback(self.game, 68)
            self.info = Info(self.game, 70)
            self.info.callback = self.info_callback

            #start modes
            self.game.modes.add(self.generalplay)
            self.game.modes.add(self.bumpers)
            self.game.modes.add(self.rampmove)
            #self.game.modes.add(self.lanes1234) added after skillshot in skillshot_callback
            self.game.modes.add(self.targets_roadkings)
            self.game.modes.add(self.crossramp)
            self.game.modes.add(self.combo)
            self.game.modes.add(self.kickback)
            self.game.modes.add(self.skillshot)
            self.game.modes.add(self.missions_modes)

    def ball_save_callback(self):
            anim = dmd.Animation().load(game_path+"dmd/ball_saved.dmd")
            self.layer = dmd.AnimatedLayer(frames=anim.frames,hold=False)
            self.game.sound.play_voice(self.game.assets.speech_dnBallSaved)
            print("Ball saved")
            self.delay(name='clear_display', event_type=None, delay=2, handler=self.clear)
            self.ball_saved = True

    def clear(self):
            self.layer=None

    def ball_launch_callback(self):
            #print("Debug - Ball Starting var is:"+str(self.ball_starting))
            if self.ball_starting:
                self.game.ball_save.start_lamp()

    def mode_tick(self):
            if self.game.switches.startButton.is_active(1) and self.game.switches.flipperLwL.is_active(1) and self.game.switches.flipperLwR.is_active():
                print("reset button code entered")
                self.game.sound.stop_music()
                self.game.end_run_loop()

                while len(self.game.dmd.frame_handlers) > 0:
                    del self.game.dmd.frame_handlers[0]

                del self.game.proc

    def mode_stopped(self):
            print("Basic Game Mode Ended, Ball "+str(self.game.ball))

            # Ensure flippers are disabled
            self.game.coils.flipperEnable.disable()

            # Deactivate the ball search logic so it won't search due to no switches being hit.
            #self.game.ball_search.disable()

            self.game.modes.remove(self.bumpers)
            self.game.modes.remove(self.generalplay)
            self.game.modes.remove(self.rampmove)
            self.game.modes.remove(self.lanes1234)
            self.game.modes.remove(self.targets_roadkings)
            self.game.modes.remove(self.crossramp)
            self.game.modes.remove(self.combo)
            self.game.modes.remove(self.kickback)
            #self.game.modes.remove(self.skillshot) # already removed in skillshot_callback
            self.game.modes.remove(self.missions_modes)

    def ball_drained_callback(self):
        if self.game.trough.num_balls_in_play == 0:
            # End the ball
            self.finish_ball()

    def finish_ball(self):
        # music fadeout
        self.game.sound.fadeout_music()
        self.game.effects.all_flashers_off()

        # Cancel playfield multiplier if it was running
        self.cancel_delayed('countdown_multiplier')

        # Turn off tilt display (if it was on) now that the ball has drained.
        if self.tilt_status and self.layer == self.tilt_layer:
            self.layer = None

        # Create the bonus mode so bonus can be calculated.
        self.bonus = Bonus(self.game, 98)
        self.game.modes.add(self.bonus)

        # Only compute bonus if it wasn't tilted away.
        if not self.tilt_status:
            # all lamps + gi off
            self.game.effects.gi_off()
            for lamp in self.game.lamps:
                lamp.disable()
            self.bonus.calculate(self.end_ball)
        else:
            self.end_ball()

    def end_ball(self):
        #remove bonus mode
        self.game.modes.remove(self.bonus)

        # Tell the game object it can process the end of ball
        # (to end player's turn or shoot again)
        self.game.end_ball()

    ## Instant Info & Gametips ##
    def start_instant_info(self):
        self.instant_info_on = True
        self.game.modes.add(self.info)

    def info_callback(self):
        self.game.modes.remove(self.info)
        self.instant_info_on = False

    def sw_flipperLwL_active_for_6s(self,sw):
        if not self.game.get_player_stats('game_feature_running') and not self.instant_info_on:
            self.start_instant_info()

    def sw_flipperLwR_active_for_7s(self,sw):
        if not self.game.get_player_stats('game_feature_running') and not self.instant_info_on:
            #self.start_instant_info()
            self.game.gametips.start_gametips()
    ## End Instant Info & Gametips ##

    def sw_startButton_active(self, sw):
        if self.game.ball == 1 and len(self.game.players)<self.game.max_players:
            p = self.game.add_player()
            self.game.set_status(p.name + " added")

    def sw_flipperLwR_active_for_10s(self, sw):
        if self.game.switches.flipperLwL.is_active():
            self.game.set_status("Ball Search!")
            self.game.effects.ball_search()

    def sw_startButton_active_for_5s(self, sw):
        if self.game.ball > 1 and self.game.user_settings['Machine (Standard)']['Game Restart']:
            self.game.set_status("Reset!")

            # Need to build a mechanism to reset AND restart the game.  If one ball
            # is already in play, the game can restart without plunging another ball.
            # It would skip the skill shot too (if one exists).

            # Currently just reset the game. This forces the ball(s) to drain and
            # the game goes to AttractMode. This makes it painfully slow to restart,
            # but it's better than nothing.
            self.game.reset()
            return True

    def sw_shooterLane_open_for_1s(self,sw):
        if self.ball_starting:
            self.ball_starting = False
            #ball_save_time = 10 VIA MENU
            self.game.ball_save.start(num_balls_to_save=1, time=self.ball_save_time, grace_time=2, now=True, allow_multiple_saves=False)

    def sw_shooterLane_active(self, sw):
        if self.ball_starting:
            self.game.assets.rk_play_music('shooterLane_loop')

    def sw_shooterLane_open_for_200ms(self,sw):
        if self.ball_starting:
           self.game.assets.rk_play_music('main_theme')
           self.game.lampctrl.play_show('rev_show', False, self.game.update_lamps)
           self.game.coils.bikesFlash_dropTarget.schedule(schedule=0x0f0f0f0f, cycle_seconds=1, now=True)

    # superskillshot preview
    def sw_flipperLwL_active_for_500ms(self, sw):
            if self.ball_starting and self.game.switches.shooterLane.is_active():
                self.skillshot.activate_superskill()

    # end superskillshot preview
    def sw_flipperLwL_inactive(self, sw):
            if self.ball_starting and self.game.switches.shooterLane.is_active():
                self.skillshot.deactivate_superskill()

    # end skillshot mode and add lanes1234 to modeqeue
    def skillshot_callback(self):
        self.game.modes.remove(self.skillshot)
        self.game.modes.add(self.lanes1234)

    # Allow service mode to be entered during a game.
    def sw_enter_active(self, sw):
        self.game.lampctrl.stop_show()
        for lamp in self.game.lamps:
            lamp.disable()
        self.game.modes.add(self.game.service_mode)
        return True

    def sw_tilt_active(self, sw):
        if self.times_warned == self.game.user_settings['Machine (Standard)']['Tilt Warnings']:
            self.tilt()
        else:
            self.times_warned += 1
            #play sound
            self.game.sound.play_voice(self.game.assets.speech_tiltWarning)
            #add a display layer and add a delayed removal of it.
            self.game.set_status("Tilt Warning " + str(self.times_warned) + "!")

    def tilt(self):
        # Process tilt.
        # First check to make sure tilt hasn't already been processed once.
        # No need to do this stuff again if for some reason tilt already occurred.
        if self.tilt_status == 0:

            #play sound
            self.game.sound.play(self.game.assets.sfx_tilt)
            self.game.sound.stop_music()

            # Display the tilt graphic
            self.layer = self.tilt_layer

            # Cancel playfield multiplier if it was running
            self.cancel_delayed('countdown_multiplier')

            # Disable flippers so the ball will drain.
            self.game.coils.flipperEnable.disable()

            # Make sure ball won't be saved when it drains.
            self.game.ball_save.disable()
            #self.game.modes.remove(self.ball_save)

            # Make sure the ball search won't run while ball is draining.
            #NOT SYS11: self.game.ball_search.disable()

            # Ensure all lamps are off.
            for lamp in self.game.lamps:
                lamp.disable()

            # Kick balls out of places it could be stuck.
            self.game.effects.release_stuck_balls()

            self.tilt_status = 1

    ## Playfield multiplier ##
    def display_pf_multiplier(self, value=1, time=0):
         # Display multiplier
         self.multiplier = value
         self.multiplier_time = time
         if self.multiplier > 1:
             self.multiply_layer.set_text("        Playfield X"+str(self.multiplier)+"        ",seconds=10, blink_frames=None)
             self.layer = self.multiply_layer
             if self.multiplier_time > 0:
                 self.countdown_pf_multiplier()
         else:
             self.layer = None

    def countdown_pf_multiplier(self):
         self.multiply_layer.set_text("    Playfield X"+str(self.multiplier)+"      "+str(self.multiplier_time),blink_frames=None)
         self.layer = self.multiply_layer
         self.multiplier_time-=1
         self.delay(name='countdown_multiplier', event_type=None, delay=1, handler=self.countdown_pf_multiplier)
         if self.multiplier_time < 0:
             self.cancel_delayed('countdown_multiplier')
             self.layer = None
             self.game.set_pf_multiplier()

    def pause_pf_multiplier(self, set=True):
         if self.multiplier_time > 0:
             if set:
                 self.cancel_delayed('countdown_multiplier')
                 #self.layer = None
                 print("Playfield multiplier PAUSED")
             else:
                 self.countdown_pf_multiplier()
                 print("Playfield multiplier RESUMED")
    ## End Playfield multiplier ##

class Game(game.BasicGame):
    """docstring for Game"""
    def __init__(self, machine_type):
        super(Game, self).__init__(machine_type)
        self.sound = procgame.sound.SoundController(self)
        self.lampctrl = procgame.lamps.LampController(self)
        self.settings = {}
        self.flipper_flashers_high_score_activated=False
        self.multiplier = 1
        self.linked_game = False

    def save_settings(self):
        super(Game, self).save_settings(settings_path)

    def save_game_data(self, path=game_data_path):
        super(Game, self).save_game_data(path)

    def change_game_data(self):
        # load game data for linked or regular games, depending on state of self.linked_game
        if self.linked_game == False:
            #load highscore data for linked games, use game_data as template
            self.linked_game = True
            self.load_game_data(game_data_path, linked_data_path)
            self.set_status("Highscores linked")
        else:
            #load game data for regular games
            self.linked_game = False
            self.load_game_data(game_data_template_path, game_data_path)
            self.set_status("Highscores unlinked")

    def create_player(self, name):
        return rkPlayer(name)

    def setup(self):
        """docstring for setup"""
        self.load_config(self.yamlpath)
        #diagnostic led blinks till software is stopped
        self.coils.diagnosticLed.schedule(schedule=0xff00ff00)

        self.load_settings(settings_template_path, settings_path)
        self.sound.music_volume_offset = self.user_settings['Sound']['Music volume offset']
        self.sound.set_volume(self.user_settings['Sound']['Initial volume'])

        # load regular game data or linked game data, depending on setting
        if self.user_settings['Gameplay (Feature)']['Linked Data'] == 'Yes':
            self.load_game_data(game_data_path, linked_data_path)
            self.linked_game = True
            self.set_status("Highscores linked")
        else:
            self.load_game_data(game_data_template_path, game_data_path)

        #define system status var
        self.system_status='power_up'
        print("system status = "+self.system_status.upper())

        #print "Stats:"
        #print self.game_data
        #print "Settings:"
        #print self.settings

        #print("Initial switch states:")
        #for sw in self.switches:
        #    print("  %s:\t%s" % (sw.name, sw.state_str()))

        self.balls_per_game = self.user_settings['Machine (Standard)']['Balls Per Game']
        self.score_display.set_left_players_justify(self.user_settings['Display']['Left side score justify'])

        # Note - Game specific item:
        # The last parameter should be the name of the game's ball save lamp
        self.ball_save = procgame.modes.BallSave(self, self.lamps.cruiseAgain, 'shooterLane')

        trough_switchnames = []
        # Note - Game specific item:
        # This range should include the number of trough switches for
        # the specific game being run.  In range(1,x), x = last number + 1.
        for i in range(1,4):
            trough_switchnames.append('trough' + str(i))
        early_save_switchnames = ['outlaneR']

        # Note - Game specific item:
        # Here, trough6 is used for the 'eject_switchname'.  This must
        # be the switch of the next ball to be ejected.  Some games
        # number the trough switches in the opposite order; so trough1
        # might be the proper switchname to user here.
        self.trough = procgame.modes.Trough(self,trough_switchnames,'trough3','trough', early_save_switchnames, 'shooterLane', self.drain_callback)

        # Link ball_save to trough
        self.trough.ball_save_callback = self.ball_save.launch_callback
        self.trough.num_balls_to_save = self.ball_save.get_num_balls_to_save
        self.ball_save.trough_enable_ball_save = self.trough.enable_ball_save

        # Setup and instantiate service mode
        self.sound.register_sound('service_enter', shared_sound_path+"sfx-menu-enter.wav")
        self.sound.register_sound('service_exit', shared_sound_path+"sfx-menu-exit.wav")
        self.sound.register_sound('service_next', shared_sound_path+"sfx-menu-up.wav")
        self.sound.register_sound('service_previous', shared_sound_path+"sfx-menu-down.wav")
        self.sound.register_sound('service_switch_edge', shared_sound_path+"sfx-menu-switch-edge.wav")
        self.sound.register_sound('service_save', shared_sound_path+"sfx-menu-save.wav")
        self.sound.register_sound('service_cancel', shared_sound_path+"sfx-menu-cancel.wav")
        self.service_mode = procgame.service.ServiceMode(self,100,font_tiny7,[])

        # Highscore sound
        self.sound.register_sound('high_score_vc', speech_path+'hs_champion.ogg')
        self.sound.register_music('high_score_theme', music_path+"Highscore.ogg")

        # Setup fonts
        self.fonts = {}
        self.fonts['tiny7'] = font_tiny7
        self.fonts['18x12'] = font_18x12
        self.fonts['07x5'] = font_07x5
        self.fonts['num_14x10'] = font_14x10
        self.fonts['num_07x4'] = font_07x4
        self.fonts['num_09Bx7'] = font_09Bx7
        # Custom fonts
        self.fonts['font_gow10'] = font_gow10
        self.fonts['font_gow12'] = font_gow12
        self.fonts['font_gow15'] = font_gow15

        # Register lampshow files for attract
        self.lampshow_keys = []
        key_ctr = 0
        for file in lampshow_files:
            key = 'attract_lamps_' + str(key_ctr)
            self.lampshow_keys.append(key)
            self.lampctrl.register_show(key, file)
            key_ctr += 1

        # Setup High Scores
        self.highscore_categories = []

        # Classic High Scores
        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'ClassicHighScoreData'
        self.highscore_categories.append(cat)

        # Miles High Scores
        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'MilesHighClub'
        cat.titles = ['Miles High Club']
        cat.score_for_player = lambda player: player.player_stats['miles_collected']
        cat.score_suffix_singular = ' mile'
        cat.score_suffix_plural = ' miles'
        self.highscore_categories.append(cat)

        # Multiball High Scores
        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'MultiBallChampion'
        cat.titles = ['MultiBall Champion']
        cat.score_for_player = lambda player: player.player_stats['multiball_total']
        cat.score_suffix_singular = ' '
        cat.score_suffix_plural = ' '
        self.highscore_categories.append(cat)

        # Kickstart King High Scores
        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'KickstartKing'
        cat.titles = ['Kickstart King']
        cat.score_for_player = lambda player: player.player_stats['kicks_made']
        cat.score_suffix_singular = ' kick'
        cat.score_suffix_plural = ' kicks'
        self.highscore_categories.append(cat)

        # King of the Road High Scores
        cat = highscore.HighScoreCategory()
        cat.game_data_key = 'KingOfTheRoad'
        cat.titles = ['King of the Road']
        cat.score_for_player = lambda player: player.player_stats['roadkings_score']
        cat.score_suffix_singular = ' '
        cat.score_suffix_plural = ' '
        self.highscore_categories.append(cat)

        for category in self.highscore_categories:
            category.load_from_game(self)

        #Maximum Players
        self.max_players = 4;

        #add basic modes
        #------------------
        #assets mode
        self.assets = Assets(self) #2
        #attract mode
        self.attract_mode = Attract(self) #1
        #basic game control mode
        self.base_game_mode = BaseGameMode(self) #5
        #game tips mode
        self.gametips = Gametips(self,3)
        #effects mode
        self.effects = Effects(self) #4
        #extra ball mode
        self.extra_ball = Extra_Ball(self) #90
        #match mode
        self.match = Match(self,10)
        #------------------

        # Instead of resetting everything here as well as when a user initiated reset occurs,
        # do everything in self.reset() and call it now and during a user initiated reset.
        self.reset()

    def set_player_stats(self,id,value):
        p = self.current_player()
        p.player_stats[id]=value

    def get_player_stats(self,id):
        p = self.current_player()
        return p.player_stats[id]

    def add_player_stats(self,id,value):
        p = self.current_player()
        p.player_stats[id]+=value

    def subtract_player_stats(self,id,value):
        p = self.current_player()
        p.player_stats[id]-=value

    def reset(self):
        # Reset the entire game framework
        super(Game, self).reset()

        # Add the basic modes to the mode queue
        self.modes.add(self.attract_mode)
        #Not SYS11: self.modes.add(self.ball_search)
        self.modes.add(self.ball_save)
        self.modes.add(self.trough)
        self.modes.add(self.extra_ball)
        self.modes.add(self.effects)
        self.modes.add(self.gametips)

    # Empty callback just incase a ball drains into the trough before another
    # drain_callback can be installed by a gameplay mode.
    def drain_callback(self):
        pass

    def start_game(self):
        super(Game, self).start_game()
        self.game_data['Audits']['Games Started'] += 1
        self.system_status='game_started'
        print("system status = "+self.system_status.upper())

    def shoot_again(self):
        self.extra_ball.shoot_again()
        #self.ball_starting()

    def ball_starting(self):
        super(Game, self).ball_starting()
        self.modes.add(self.base_game_mode)

    def ball_ended(self):
        self.modes.remove(self.base_game_mode)
        super(Game, self).ball_ended()
        # Handle stats for ball here
        self.save_ball_stats()

    def game_ended(self):
        super(Game, self).game_ended()

        self.modes.remove(self.base_game_mode)
        #self.modes.add(self.match)  # after highscore_entry_finished()

        # handle game stats here
        self.save_game_stats()

        # High Score Stuff
        seq_manager = highscore.EntrySequenceManager(game=self, priority=2)
        seq_manager.finished_handler = self.highscore_entry_finished
        seq_manager.logic = highscore.CategoryLogic(game=self, categories=self.highscore_categories)
        seq_manager.ready_handler = self.highscore_entry_ready_to_prompt
        self.modes.add(seq_manager)

    def highscore_entry_ready_to_prompt(self, mode, prompt):
        self.sound.play_voice('high_score_vc')
        self.sound.play_music('high_score_theme', loops=-1)
        self.effects.flippers(True)
        banner_mode = game.Mode(game=self, priority=8)
        markup = dmd.MarkupFrameGenerator()
        markup.font_plain = dmd.font_named('04B-03-7px.dmd')
        markup.font_bold = dmd.font_named('04B-03-7px.dmd')
        text = '\n[GREAT SCORE!!]\n#%s#\n' % (prompt.left.upper()) # we know that the left is the player name
        frame = markup.frame_for_markup(markup=text, y_offset=0)
        banner_mode.layer = dmd.ScriptedLayer(width=128, height=32, script=[{'seconds':4.0, 'layer':dmd.FrameLayer(frame=frame)}])
        banner_mode.layer.on_complete = lambda: self.highscore_banner_complete(banner_mode=banner_mode, highscore_entry_mode=mode)
        self.modes.add(banner_mode)

        self.lampctrl.stop_show()
        for lamp in self.lamps:
            lamp.disable()
        self.effects.gi_off()
        self.flipper_flashers_high_score = FlipperFlasherHighscore(self)
        self.modes.add(self.flipper_flashers_high_score)
        self.flipper_flashers_high_score_activated=True

    def highscore_banner_complete(self, banner_mode, highscore_entry_mode):
        self.modes.remove(banner_mode)
        highscore_entry_mode.prompt()
        self.effects.gi_on()

    def highscore_entry_finished(self, mode):
        if self.flipper_flashers_high_score_activated==True:
            self.modes.remove(self.flipper_flashers_high_score)
            self.flipper_flashers_high_score_activated=False

        self.sound.fadeout_music(time_ms = 2000)
        self.modes.remove(mode)
        self.effects.flippers(False)

        #self.modes.add(self.attract_mode) # called in match.py
        self.modes.add(self.match)

        # Handle game stats here
        print("## save game data: ")
        if self.linked_game:
            self.save_game_data(linked_data_path)
            print("## linked game ##")
        else:
            self.save_game_data()
            print("## regular game ##")

    def save_ball_stats(self):
        self.game_data['Audits']['Avg Ball Time'] = self.calc_time_average_string(self.game_data['Audits']['Balls Played'], self.game_data['Audits']['Avg Ball Time'], self.ball_time)
        self.game_data['Audits']['Balls Played'] += 1

    def save_game_stats(self):
        for i in range(0,len(self.players)):
            game_time = self.get_game_time(i)
            self.game_data['Audits']['Avg Game Time'] = self.calc_time_average_string( self.game_data['Audits']['Games Played'], self.game_data['Audits']['Avg Game Time'], game_time)
            self.game_data['Audits']['Games Played'] += 1

        for i in range(0,len(self.players)):
            self.game_data['Audits']['Avg Score'] = self.calc_number_average(self.game_data['Audits']['Games Played'], self.game_data['Audits']['Avg Score'], self.players[i].score)

    def calc_time_average_string(self, prev_total, prev_x, new_value):
          prev_time_list = prev_x.split(':')
          prev_time = (int(prev_time_list[0]) * 60) + int(prev_time_list[1])
          avg_game_time = int((int(prev_total) * int(prev_time)) + int(new_value)) / (int(prev_total) + 1)
          avg_game_time_min = avg_game_time/60
          avg_game_time_sec = str(avg_game_time%60)
          if len(avg_game_time_sec) == 1:
                  avg_game_time_sec = '0' + avg_game_time_sec
          return_str = str(avg_game_time_min) + ':' + avg_game_time_sec
          print("Avg time: "+str(return_str))
          return return_str

    def calc_number_average(self, prev_total, prev_x, new_value):
          avg_game_time = int((prev_total * prev_x) + new_value) / (prev_total + 1)
          return int(avg_game_time)

    def set_status(self, text):
        self.dmd.set_message(text, 3)
        print(text)

    def extra_ball_count(self):
        p = self.current_player()
        p.extra_balls += 1

    def set_pf_multiplier(self, value=1, time=0):
         self.multiplier = value
         print("set multiplier: ", self.multiplier)
         self.base_game_mode.display_pf_multiplier(value=self.multiplier, time=time)

    def score(self, points):
         """add points to the current player, using multiplier"""
         #self.base_game_mode.cancel_delayed('display_tip')
         p = self.current_player()
         p.score += (points*self.multiplier)
         #self.base_game_mode.delay(name='display_tip', event_type=None, delay=10, handler=self.gametips.display_tip)


class FlipperFlasherHighscore(game.Mode):
    """docstring for FlipperFlasherHighscore"""
    def __init__(self, game):
        super(FlipperFlasherHighscore, self).__init__(game, 10)
        self.game.sound.register_sound('hs_stamp', sound_path+"stamp.ogg")
    def mode_stopped(self):
        self.game.effects.gi_on()
    # Flashers when entering initials
    def sw_flipperLwL_active(self, sw):
        self.game.coils.Llightningbolt.pulse(20)
    def sw_flipperLwR_active(self, sw):
        self.game.coils.Rlightningbolt.pulse(20)
    def sw_startButton_active(self, sw):
        self.game.effects.gi_off()
        self.game.coils.rearFlash_upLeftkicker.schedule(schedule=0xaaaaaaaa, cycle_seconds=1, now=True)
        self.game.coils.midBikeFlash_rampDown.schedule(schedule=0xf0f0f0f0, cycle_seconds=1, now=True)
        self.game.coils.bikesFlash_dropTarget.schedule(schedule=0xaaaaaaaa, cycle_seconds=1, now=True)
        self.game.sound.play('hs_stamp')


class rkPlayer(game.Player):
    """docstring for rkPlayer"""
    def __init__(self, name):
                super(rkPlayer, self).__init__(name)

                # create player stats
                self.player_stats = {}

                # set player stats defaults
                self.player_stats['status']=''

                # game items
                self.player_stats['bonus_x']= 1
                self.player_stats['hold_bonusx']= False
                self.player_stats['skillshots']= 0
                self.player_stats['miles_collected']= 1   # bonus count,  # Highsore: Miles High Club
                self.player_stats['bumper_level']= 1
                self.player_stats['spinner_value']= 1000
                self.player_stats['spinner_turns'] = 0
                self.player_stats['crossramps_made']= 0
                self.player_stats['crossramp_level']= 1
                self.player_stats['kicks_made']= 0        # Highsore: Kickstart King
                self.player_stats['ramps_made']= 0        # bonus count
                self.player_stats['jumpramps_count']= 0
                #self.player_stats['combo_flag']= [False,False,False]
                self.player_stats['combo_flag']= [0,0,0]
                self.player_stats['mystery_award']=0
                self.player_stats['road_targets']= [False,False,False,False]
                self.player_stats['kings_targets']= [False,False,False,False,False]
                self.player_stats['roadkings_complete']= 0
                self.player_stats['roadkings_xball']= 0
                self.player_stats['lanes1234_flag']= [False,False,False,False]
                self.player_stats['lanes1234_numbers_spotted']= 0

                # control stats
                self.player_stats['ramp_state']= False
                self.player_stats['kickback']= 'normal'
                self.player_stats['million_plus']= False
                self.player_stats['millionplus_value']= 1
                self.player_stats['extraball_on']= False
                self.player_stats['current_mode_num']= 0
                self.player_stats['mode_enabled']= False
                self.player_stats['game_feature_running']= False
                self.player_stats['mode_status_tracking']= [0,0,0,0]
                #self.player_stats['mode_status_tracking']= [1,1,1,1] # TEST
                self.player_stats['modes_completed']= [False,False,False,False] #[racechampion,kickstartking,multiball,easyrider]
                #self.player_stats['modes_completed']= [True,True,True,True] # TEST [racechampion,kickstartking,multiball,easyrider]
                self.player_stats['mission_status_tracking']= [0,0,0,0,0,0,0,0,0,0]
                #self.player_stats['mission_status_tracking']= [0,1,1,1,1,1,1,1,1,1] # TEST

                # Main Modes score stats
                self.player_stats['racechampion_total']= 0
                self.player_stats['kickstartking_total']= 0
                self.player_stats['multiball_total']= 0     # Highsore: Multiball Champion
                self.player_stats['easyrider_total']= 0
                self.player_stats['roadkings_score']= 0     # Highscore: King of the Road

def main():

    config = yaml.load(open(machine_config_path, 'r'))
    print("Using config at: %s "%(machine_config_path))
    machine_type = config['PRGame']['machineType']
    config = 0
    game = None
    try:
        game = Game(machine_type)
        game.yamlpath = machine_config_path
        game.setup()
        game.run_loop()

    finally:
        del game


if __name__ == '__main__': main()
