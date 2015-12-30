#
# Roadkings Assets
#

__author__="Pieter"
__date__ ="$24 Sept 2013 21:21:21 PM$"

from procgame import *
import random
#import os

# all paths
game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

# Paths
# curr_file_path = os.path.dirname(os.path.abspath( __file__ ))
# self.sounds_path = curr_file_path + "/sounds/"


class Assets():

    def __init__(self, game):
### SCROLLL DOWN FOR OTHER METHODS ###
        self.game = game
        self.selected_tune = 1

        # Loading Assets
        print("Loading Roadkings game assets...")

## Sound + Speech
        # Attract
        self.speech_attract = 'rk_attract'
        self.game.sound.register_sound(self.speech_attract, speech_path+"kk_come_get_some.wav")
        self.game.sound.register_sound(self.speech_attract, speech_path+"extra_ball_hurryup.wav")
        self.game.sound.register_sound(self.speech_attract, speech_path+"el_doitagain.ogg")
        self.game.sound.register_sound(self.speech_attract, speech_path+"kk_taste_my_ball.wav")
        self.sfx_linked = 'linked'
        self.game.sound.register_sound(self.sfx_linked, sound_path+"linked.ogg")
        # Base game mode
        self.sfx_tilt = 'tilt'
        self.game.sound.register_sound(self.sfx_tilt, sound_path+"tilt.ogg")
        self.sfx_shooterLane = 'shooterlane'
        self.game.sound.register_sound(self.sfx_shooterLane, sound_path+"motor_driveaway.aiff")
        self.speech_tiltWarning = 'tilt_warning'
        self.game.sound.register_sound(self.speech_tiltWarning, speech_path+"tilt_warning.ogg")
        self.speech_dnBallSaved = 'dn_ball_saved'
        self.game.sound.register_sound(self.speech_dnBallSaved, speech_path+"dn_ball_saved.wav")
        self.game.sound.register_sound(self.speech_dnBallSaved, speech_path+"dn_timeforreboot.ogg")
        # skillshot
        self.sfx_skillshotMade = 'skillshot_made'
        self.game.sound.register_sound(self.sfx_skillshotMade, speech_path+"great_shot.wav")
        self.game.sound.register_sound(self.sfx_skillshotMade, speech_path+'skillshot.wav')
        self.sfx_superskillMade = 'superskill_made'
        self.game.sound.register_sound(self.sfx_superskillMade, speech_path+'superskillshot.wav')
        self.game.sound.register_sound(self.sfx_superskillMade, speech_path+'superskillshot2.wav')
        self.sfx_skillRev = 'skill_rev'
        self.game.sound.register_sound(self.sfx_skillRev, sound_path+'skill_engine_rev.wav')
        # General play
        self.sfx_slingShot = 'slingshot'
        self.game.sound.register_sound(self.sfx_slingShot, sound_path+"slings.aiff")
        self.sfx_showroom = 'showroom'
        self.game.sound.register_sound(self.sfx_showroom, sound_path+"showroom.aiff")
        self.sfx_spinner = 'spinner'
        self.game.sound.register_sound(self.sfx_spinner, sound_path+"spinner.aiff")
        self.sfx_bark = 'bark'
        self.game.sound.register_sound(self.sfx_bark, sound_path+"bark.aiff")
        self.sfx_jumpApplause = 'jump_applause'
        self.game.sound.register_sound(self.sfx_jumpApplause, sound_path+"jumpramp_applause.ogg")
        self.speech_million = 'million'
        self.game.sound.register_sound(self.speech_million, speech_path+"million.ogg")
        # targets roadkings
        self.sfx_targetHit = 'target_hit'
        self.game.sound.register_sound(self.sfx_targetHit, sound_path+"target_hit.aiff")
        self.sfx_targetLit = 'target_lit'
        self.game.sound.register_sound(self.sfx_targetLit, sound_path+"target_lit.aiff")
        self.sfx_targetsComplete = 'targets_complete'
        self.game.sound.register_sound(self.sfx_targetsComplete, sound_path+"targets_complete.aiff")
        # lanes1234
        self.sfx_laneOn = 'lane_on'
        self.game.sound.register_sound(self.sfx_laneOn, sound_path+"inlanes_on.aiff")
        self.sfx_laneOff = 'lane_off'
        self.game.sound.register_sound(self.sfx_laneOff, sound_path+"inlanes_off.aiff")
        self.sfx_laneComplete = 'lane_complete'
        self.game.sound.register_sound(self.sfx_laneComplete, sound_path+"inlanes_complete.aiff")
        # tunnelTrail
        self.sfx_tunnelHit = 'tunnel_hit'
        self.game.sound.register_sound(self.sfx_tunnelHit, sound_path+"tunnel_hit.aiff")
        # Crossramp(Xramp)
        self.sfx_xramp_shot = 'crossramp_shot'
        self.game.sound.register_sound(self.sfx_xramp_shot, sound_path+"crossramp_shot.aiff")
        self.sfx_hurryupStart = 'hurryup_start'
        self.game.sound.register_sound(self.sfx_hurryupStart, sound_path+"hurryup_start.ogg")
        self.sfx_hurryupScored = 'hurryup_scored'
        self.game.sound.register_sound(self.sfx_hurryupScored, sound_path+"hurryup_scored.ogg")
        self.sfx_hurryupMissed = 'hurryup_missed'
        self.game.sound.register_sound(self.sfx_hurryupMissed, sound_path+"hurryup_missed.ogg")
        self.speech_thatsShooting = 'thats_shooting'
        self.game.sound.register_sound(self.speech_thatsShooting, speech_path+"dh_thats_shootingh.ogg")
        self.game.sound.register_sound(self.speech_thatsShooting, speech_path+"dh_beenpractisingh.ogg")
        # Combos
        self.sfx_combo_made = 'combo_made'
        self.game.sound.register_sound(self.sfx_combo_made, sound_path+"combo1.ogg")
        self.game.sound.register_sound(self.sfx_combo_made, sound_path+"combo2.ogg")
        self.game.sound.register_sound(self.sfx_combo_made, sound_path+"combo3.ogg")
        self.sfx_combos_complete = 'combos_complete'
        self.game.sound.register_sound(self.sfx_combos_complete, sound_path+"combos_complete.ogg")
        # Jumprramp (uses hurryup from Xramp)
        # Mystery
        self.sfx_mystery = 'mystery'
        self.game.sound.register_sound(self.sfx_mystery, sound_path+"electricity.ogg")
        self.sfx_spark = 'spark'
        self.game.sound.register_sound(self.sfx_spark, sound_path+"sparkL.ogg")
        self.game.sound.register_sound(self.sfx_spark, sound_path+"sparkR.ogg")
        # Quick Multiball
        self.sfx_qm_clockTick = 'qm_clock_tick'
        self.game.sound.register_sound(self.sfx_qm_clockTick, sound_path+"qm_clocktick.ogg")
        self.sfx_qm_spinner = 'qm_spinner'
        self.game.sound.register_sound(self.sfx_qm_spinner, sound_path+"qm_spinner.wav")
        # Bumpers
        self.sfx_bumper = 'bumper'
        self.game.sound.register_sound(self.sfx_bumper, sound_path+"bumpers.ogg")
        self.game.sound.register_sound(self.sfx_bumper, sound_path+"bumpers1.ogg")
        self.sfx_bigBumpers = 'bigbumpers'
        self.game.sound.register_sound(self.sfx_bigBumpers, speech_path+"big_men.aiff")
        self.game.sound.register_sound(self.sfx_bigBumpers, speech_path+"bumpers_women1.aiff")
        self.game.sound.register_sound(self.sfx_bigBumpers, sound_path+"super_jets.ogg")
        self.game.sound.register_sound(self.sfx_bigBumpers, speech_path+"big_men1.aiff")
        self.game.sound.register_sound(self.sfx_bigBumpers, speech_path+"bumpers_women2.aiff")
        self.sfx_shootForJets = 'shootforjets'
        self.game.sound.register_sound(self.sfx_shootForJets, speech_path+"shoot_for_jets.wav")
        # Trade miles
        self.sfx_moveMiles = 'move_miles'
        self.game.sound.register_sound(self.sfx_moveMiles, sound_path+"move_miles.ogg")
        self.sfx_moveItem = 'move_item'
        self.game.sound.register_sound(self.sfx_moveItem, sound_path+"move_item.ogg")
        self.sfx_noMiles = 'no_miles'
        self.game.sound.register_sound(self.sfx_noMiles, sound_path+"no_miles.ogg")
        # Kickback
        self.sfx_powerkick = 'powerkick'
        self.game.sound.register_sound(self.sfx_powerkick, sound_path+"powerkick.ogg")
        self.sfx_kickback = 'kickback'
        self.game.sound.register_sound(self.sfx_kickback, sound_path+"super_jets.ogg")
        self.sfx_crash = 'crash'
        self.game.sound.register_sound(self.sfx_crash, sound_path+"outlane_crash.ogg")
        # Mission Modes
        self.sfx_rkmodeStarted = 'rkmode_started'
        self.game.sound.register_sound(self.sfx_rkmodeStarted, sound_path+'rkmode_started1.ogg')
        self.sfx_wizardShutdown = 'wizardshutdown'
        self.game.sound.register_sound(self.sfx_wizardShutdown, sound_path+"Wizard_Atmosfear1.ogg")  #Wizard_Atmosfear, Wizard_boom
        self.sfx_wziardModeReady = 'wziardmodeready'
        self.game.sound.register_sound(self.sfx_wziardModeReady, sound_path+"start_wizard.wav")
        self.sfx_RCstart = 'racestart'
        self.game.sound.register_sound(self.sfx_RCstart, sound_path+"mm_racestart.ogg")
        self.sfx_ERstart = 'letsgoforride'
        self.game.sound.register_sound(self.sfx_ERstart, speech_path+"letsgoforride.ogg")
        self.sfx_KKstart = 'kicksomeking'
        self.game.sound.register_sound(self.sfx_KKstart, speech_path+"kk_its_ass_kicking_time.wav")
        self.sfx_MBstart = 'startyourengine'
        self.game.sound.register_sound(self.sfx_MBstart, speech_path+"startyourengine.wav")
        # Rampmove
        self.sfx_rampChange = 'ramp_change'
        self.game.sound.register_sound(self.sfx_rampChange, sound_path+"rampchange1.aiff")
        self.sfx_selectItem = 'select_item'
        self.game.sound.register_sound(self.sfx_selectItem, sound_path+"select_item.ogg")
        # Extra Ball
        self.sfx_extraBallCollected = 'extra_ball_collected'
        self.game.sound.register_sound(self.sfx_extraBallCollected, sound_path+"extra_ball.wav")
        self.sfx_extraBallLit = 'extra_ball_lit'
        self.game.sound.register_sound(self.sfx_extraBallLit, speech_path+"extra_ball_lit.wav")
        self.sfx_HurryUp = 'hurryup'
        self.game.sound.register_sound(self.sfx_HurryUp, speech_path+"extra_ball_hurryup.wav")
        self.sfx_shootAgain = 'dn_shoot_again'
        self.game.sound.register_sound(self.sfx_shootAgain, speech_path+'dn_lotta_ball.wav')
        # Gametips
        self.sfx_newTip = 'new_tip'
        self.game.sound.register_sound(self.sfx_newTip, sound_path+"rampchange.aiff")
        # Info
        self.sfx_nextItem = 'next_item'
        self.game.sound.register_sound(self.sfx_nextItem, sound_path+"rampchange.aiff")
        # match
        self.sfx_horngoby = 'horngoby'
        self.game.sound.register_sound(self.sfx_horngoby, sound_path+"match_horngoby.ogg")

        # Race Champion
        self.sfx_rc_timeOut = 'rc_time_out'
        self.game.sound.register_sound(self.sfx_rc_timeOut, speech_path+"rc_dontfallbehind.wav")
        self.game.sound.register_sound(self.sfx_rc_timeOut, speech_path+"rc_hurryhurry.wav")
        self.game.sound.register_sound(self.sfx_rc_timeOut, speech_path+"rc_comeonmove.wav")
        self.game.sound.register_sound(self.sfx_rc_timeOut, speech_path+"rc_timesrunningout.wav")
        self.sfx_rc_moveBack = 'rc_move_back'
        self.game.sound.register_sound(self.sfx_rc_moveBack, speech_path+"rc_hehehe.wav")
        self.game.sound.register_sound(self.sfx_rc_moveBack, speech_path+"rc_icandothis.wav")
        self.game.sound.register_sound(self.sfx_rc_moveBack, speech_path+"rc_hmmdammit.wav")
        self.game.sound.register_sound(self.sfx_rc_moveBack, speech_path+"rc_ohno.wav")
        self.sfx_rc_shotMade = 'rc_shot_made'
        self.game.sound.register_sound(self.sfx_rc_shotMade, speech_path+"rc_iamtheman.wav")
        self.game.sound.register_sound(self.sfx_rc_shotMade, speech_path+"rc_steponit.wav")
        self.game.sound.register_sound(self.sfx_rc_shotMade, speech_path+"rc_yes.wav")
        self.sfx_rc_justInTime = 'rc_justintime'
        self.game.sound.register_sound(self.sfx_rc_justInTime, speech_path+"rc_justintime.ogg")
        self.sfx_rc_raceWon = 'rc_racewon'
        self.game.sound.register_sound(self.sfx_rc_raceWon, speech_path+"rc_racewon.ogg")

        # Kickstart King
        self.sfx_kk_jackpotMissed = 'jackpot_missed'
        self.game.sound.register_sound(self.sfx_kk_jackpotMissed, sound_path+"jackpot_missed.ogg")
        self.sfx_kk_Jackpot = 'kk_jackpot'
        self.game.sound.register_sound(self.sfx_kk_Jackpot, speech_path+"kk_hail_to_the_king.wav") # Who's youre king? , Kick ass man! Kick ass!
        self.game.sound.register_sound(self.sfx_kk_Jackpot, speech_path+"kk_I_like_it.wav") # Who's youre king? , Kick ass man! Kick ass!
        self.sfx_kk_jackpotLit = 'kk_jackpot_lit'
        self.game.sound.register_sound(self.sfx_kk_jackpotLit, speech_path+"kk_come_get_some.wav")
        self.game.sound.register_sound(self.sfx_kk_jackpotLit, speech_path+"dn_letsrock.ogg")
        self.game.sound.register_sound(self.sfx_kk_jackpotLit, speech_path+"kk_its_ass_kicking_time.wav")
        self.sfx_kk_gotGuts = 'kk_got_guts'
        self.game.sound.register_sound(self.sfx_kk_gotGuts, speech_path+"kk_you_got_guts.wav")
        self.sfx_kk_kick = 'kick'
        self.game.sound.register_sound(self.sfx_kk_kick, speech_path+"kk_kick.wav")
        self.game.sound.register_sound(self.sfx_kk_kick, speech_path+"kk_uhmpf.wav")
        self.game.sound.register_sound(self.sfx_kk_kick, speech_path+"kk_yeah.wav")
        self.game.sound.register_sound(self.sfx_kk_kick, speech_path+"kk_hmm.wav")
        self.game.sound.register_sound(self.sfx_kk_kick, speech_path+"kk_uhmpf2.wav")

        # MultiBall
        self.speech_mb_jackpotIsLit = 'jackpotislit'
        self.game.sound.register_sound(self.speech_mb_jackpotIsLit, speech_path+"jackpotislit.wav")
        self.speech_mb_superJackpotIsLit = 'superjackpotislit'
        self.game.sound.register_sound(self.speech_mb_superJackpotIsLit, speech_path+"superjackpotislit.wav")
        self.speech_mb_jackpot = 'jackpot'
        self.game.sound.register_sound(self.speech_mb_jackpot, speech_path+"jaackpot.wav")
        self.speech_mb_superJackpot = 'superjackpot'
        self.game.sound.register_sound(self.speech_mb_superJackpot, speech_path+"superjackpot.wav")
        self.speech_mb_lock1 = 'ball1locked'
        self.game.sound.register_sound(self.speech_mb_lock1, speech_path+"mb_ball1captured.wav")
        self.speech_mb_lock2 = 'ball2locked'
        self.game.sound.register_sound(self.speech_mb_lock2, speech_path+"mb_ball2locked.wav")
        self.speech_mb_start = 'startmultiball'
        self.game.sound.register_sound(self.speech_mb_start, sound_path+"startmultiball1.wav")

        # Easy Rider
        self.sfx_siren = 'siren'
        self.game.sound.register_sound(self.sfx_siren, sound_path+"siren1.ogg")
        self.sfx_er_Jackpot = 'er_Jackpot'
        self.game.sound.register_sound(self.sfx_er_Jackpot, sound_path+"easy_rider_jp.ogg")
        self.speech_er_shotMade = 'er_shot_made'
        self.game.sound.register_sound(self.speech_er_shotMade, speech_path+"er_yeahbaby.ogg")
        self.game.sound.register_sound(self.speech_er_shotMade, speech_path+"er_goingeasy.ogg")
        self.game.sound.register_sound(self.speech_er_shotMade, speech_path+"er_justridin.ogg")
        self.game.sound.register_sound(self.speech_er_shotMade, speech_path+"er_meandmybike.ogg")
        self.speech_shootRightRamp = 'shootrightramp'
        self.game.sound.register_sound(self.speech_shootRightRamp, speech_path+"er_shootrightramp.ogg")
        self.speech_er_thatsEasy = 'er_thatseasy'
        self.game.sound.register_sound(self.speech_er_thatsEasy, speech_path+"er_thatseasy.ogg")
        self.speech_er_bornToBeWild = 'er_borntobewild'
        self.game.sound.register_sound(self.speech_er_bornToBeWild, speech_path+"dn_borntobewild.ogg")
        self.speech_er_shootLitShots = 'er_shootlitshots'
        self.game.sound.register_sound(self.speech_er_shootLitShots, speech_path+"er_shootallitshots.ogg")

        # Roadkings
        self.sfx_rk_slam = 'rk_slam'
        self.game.sound.register_sound(self.sfx_rk_slam, sound_path+"rk_slam1.wav")
        self.sfx_rk_slamEnd = 'rk_slam_end'
        self.game.sound.register_sound(self.sfx_rk_slamEnd, sound_path+"rk_slam_end.wav")
        self.sfx_rk_wizardBoom = 'Wizard_boom'
        self.game.sound.register_sound(self.sfx_rk_wizardBoom, sound_path+"Wizard_boom1.ogg")

        print("...")
## Music
        self.music_mainTheme1 = 'main_theme1'
        self.game.sound.register_music(self.music_mainTheme1, music_path+"rk_mainTheme_ZZT.ogg")
        self.music_shooterLane_loop1 = 'shooterlane_loop1'
        self.game.sound.register_music(self.music_shooterLane_loop1, music_path+"shooterlaneLoop_ZZT.wav")
        self.music_mainTheme2 = 'main_theme2'
        self.game.sound.register_music(self.music_mainTheme2, music_path+"rk_mainTheme_LZ.ogg")
        self.music_shooterLane_loop2 = 'shooterlane_loop2'
        self.game.sound.register_music(self.music_shooterLane_loop2, music_path+"shooterlaneLoop_LZ.wav")
        self.music_mainTheme3 = 'main_theme3'
        self.game.sound.register_music(self.music_mainTheme3, music_path+"rk_mainTheme_RH.ogg")
        self.music_shooterLane_loop3 = 'shooterlane_loop3'
        self.game.sound.register_music(self.music_shooterLane_loop3, music_path+"shooterlaneLoop_RH.wav")

        self.music_hurryupTheme = 'hurryup_theme'
        self.game.sound.register_music(self.music_hurryupTheme, music_path+"crossramp_hurryup.ogg")
        self.music_hurryupjumpRamp = 'hurryup_jumpRamp'
        self.game.sound.register_music(self.music_hurryupjumpRamp, music_path+"polly_hurryup.ogg")
        self.music_bonusTune = 'bonus_tune'
        self.game.sound.register_music(self.music_bonusTune, music_path+"gaspump_bonus.aiff")
        self.music_quickMultiball = 'quick_multiball'
        self.game.sound.register_music(self.music_quickMultiball, music_path+"rock_spinner.ogg")
        self.music_qm_clockTickAlarm = 'qm_clock_tickalarm'
        self.game.sound.register_music(self.music_qm_clockTickAlarm, sound_path+"qm_clocktick_alarm.wav")
        self.music_tmBackground = 'tm_background'
        self.game.sound.register_music(self.music_tmBackground, music_path+"workshop.ogg")

        self.music_RCmode00 = 'racechampion_theme00'
        self.game.sound.register_music(self.music_RCmode00, music_path+"mode_racechampion00.ogg")
        self.music_RCmode60 = 'racechampion_theme60'
        self.game.sound.register_music(self.music_RCmode60, music_path+"mode_racechampion60.ogg")
        self.music_RCmode70 = 'racechampion_theme70'
        self.game.sound.register_music(self.music_RCmode70, music_path+"mode_racechampion70.ogg")
        self.music_RCmode80 = 'racechampion_theme80'
        self.game.sound.register_music(self.music_RCmode80, music_path+"mode_racechampion80.ogg")
        self.music_RCmode90 = 'racechampion_theme90'
        self.game.sound.register_music(self.music_RCmode90, music_path+"mode_racechampion90.ogg")
        self.music_RCmode100 = 'racechampion_theme100'
        self.game.sound.register_music(self.music_RCmode100, music_path+"mode_racechampion100.ogg")

        self.music_KKmode = 'kickstartking_theme'
        self.game.sound.register_music(self.music_KKmode, music_path+"kickstartking.ogg")
        self.sfx_KKintro = 'kickstartking_intro'
        self.game.sound.register_sound(self.sfx_KKintro, music_path+"kk_intro.wav")

        self.music_MBmode = 'multiball_theme'
        self.game.sound.register_music(self.music_MBmode, music_path+"bumperbastard.ogg")

        self.music_ERmode = 'easyrider_theme'
        self.game.sound.register_music(self.music_ERmode, music_path+"EasyRider_pusher_small.wav") #EasyRider_pusher / EasyRider_theme

        self.music_RKmode = 'roadkings_theme'
        self.game.sound.register_music(self.music_RKmode, music_path+"WizardMode.ogg")

        print("...Done loading Roadkings game assets!")


## Music control methods

    def rk_play_music(self, tune='main_theme'):
             #always fade_out previous music
             self.game.sound.fadeout_music(time_ms=100)
             #start selected tune
             if tune == 'stop':
                 self.game.sound.stop_music()
             elif tune == 'main_theme':
                 if self.selected_tune == 1:
                     self.game.sound.play_music(self.music_mainTheme1, loops=-1)
                 elif self.selected_tune == 2:
                     self.game.sound.play_music(self.music_mainTheme2, loops=-1)
                 elif self.selected_tune == 3:
                     self.game.sound.play_music(self.music_mainTheme3, loops=-1)
             elif tune == 'shooterLane_loop':
                 if self.selected_tune == 1:
                     self.game.sound.play_music(self.music_shooterLane_loop1, loops=-1)
                 if self.selected_tune == 2:
                     self.game.sound.play_music(self.music_shooterLane_loop2, loops=-1)
                 if self.selected_tune == 3:
                     self.game.sound.play_music(self.music_shooterLane_loop3, loops=-1)

    def select_tune(self, tune=0):
             if tune == 0:
                 self.selected_tune = random.randint(1,3) # select from 3 tunes
             else:
                 self.selected_tune = tune
             print("Selected tune: "+str(self.selected_tune))
