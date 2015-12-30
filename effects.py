#
# Effects
#
# Basic mode for general effects and control of game items (lamps, coils, etc.)
# Loaded in startup, so also operational in Attract mode
#
__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"


import procgame
from procgame import *

#game_path = config.value_for_key_path('game_path')
#dmd_path = game_path +"dmd/"

class Effects(game.Mode):

        def __init__(self, game):
            super(Effects, self).__init__(game, 4)

# Lamp effects

        def drive_lamp_schedule(self, lamp_name, schedule=0x0f0f0f0f, cycle_seconds=0, now=True):
            self.game.lamps[lamp_name].schedule(schedule=schedule, cycle_seconds=cycle_seconds, now=now)

        def drive_lamp(self, lamp_name, style='on',time=2):
            if style == 'slow':
               self.game.lamps[lamp_name].schedule(schedule=0x00ff00ff, cycle_seconds=0, now=True)
            elif style == 'medium':
              self.game.lamps[lamp_name].schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
            elif style == 'fast':
                self.game.lamps[lamp_name].schedule(schedule=0x55555555, cycle_seconds=0, now=True)
            elif style == 'superfast':
                self.game.lamps[lamp_name].schedule(schedule=0x99999999, cycle_seconds=0, now=True)
            elif style == 'on':
                self.game.lamps[lamp_name].enable()
            elif style == 'off':
                self.game.lamps[lamp_name].disable()
                # also cancel any pending delays
                self.cancel_delayed(lamp_name+'_medium')
                self.cancel_delayed(lamp_name+'_fast')
                self.cancel_delayed(lamp_name+'_superfast')
            elif style == 'smarton':
                self.game.lamps[lamp_name].schedule(schedule=0xaaaaaaaa, cycle_seconds=0, now=True)
                self.delay(name=lamp_name+'_on', event_type=None, delay=0.6, handler=self.game.lamps[lamp_name].enable)
            elif style == 'smartoff':
                self.game.lamps[lamp_name].schedule(schedule=0xaaaaaaaa, cycle_seconds=0, now=True)
                self.delay(name=lamp_name+'_off', event_type=None, delay=0.6, handler=self.game.lamps[lamp_name].disable)
            elif style == 'timeout':
                self.game.lamps[lamp_name].schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)
                if time>10:
                    self.delay(name=lamp_name+'_medium', event_type=None, delay=time-10, handler=self.drive_medium, param=lamp_name)
                if time>5:
                    self.delay(name=lamp_name+'_fast', event_type=None, delay=time-5, handler=self.drive_fast, param=lamp_name)
                if time>1:
                    self.delay(name=lamp_name+'_superfast', event_type=None, delay=time-1, handler=self.drive_super_fast, param=lamp_name)
                self.delay(name=lamp_name+'_off', event_type=None, delay=time, handler=self.game.lamps[lamp_name].disable)

        def drive_super_fast(self, lamp_name):
             self.game.lamps[lamp_name].schedule(schedule=0x99999999, cycle_seconds=0, now=True)

        def drive_fast(self, lamp_name):
             self.game.lamps[lamp_name].schedule(schedule=0x55555555, cycle_seconds=0, now=True)

        def drive_medium(self, lamp_name):
             self.game.lamps[lamp_name].schedule(schedule=0x0f0f0f0f, cycle_seconds=0, now=True)

        def clear_all_lamps(self):
             for lamp in self.game.lamps:
                 lamp.disable()

        def update_ramp_lamps(self):
            # called from ramp_move to update lamps after change in rampstatus
            # add call to lamp update function for specific mode
            self.game.base_game_mode.missions_modes.update_ramp_lamps()
            self.game.base_game_mode.generalplay.update_ramp_lamps()

# Flashers + GI effects

        def drive_flasher(self, flasher_name, style='off',seconds_on=0):
            if style == 'slow':
               self.game.coils[flasher_name].schedule(schedule=0x0000FFFF, cycle_seconds=seconds_on, now=True)
            elif style == 'medium':
              self.game.coils[flasher_name].schedule(schedule=0x00FF00FF, cycle_seconds=seconds_on, now=True)
            elif style == 'fast':
                self.game.coils[flasher_name].schedule(schedule=0x0F0F0F0F, cycle_seconds=seconds_on, now=True)
            elif style == 'off':
                self.game.coils[flasher_name].disable()

        def all_flashers_off(self):
             self.game.coils.workshopFlash.disable()
             self.game.coils.showroomFlash.disable()
             self.game.coils.Llightningbolt.disable()
             self.game.coils.Rlightningbolt.disable()

        def gi_on(self):
             self.game.coils.GIrelay.disable()

        def gi_off(self):
             self.game.coils.GIrelay.enable()

        def gi_blinking(self, schedule=0x0f0f0f0f, cycle_seconds=1, now=True):
             self.game.coils.GIrelay.schedule(schedule=schedule, cycle_seconds=cycle_seconds, now=now)

# AC-Select coils

        def raise_droptarget(self):
             if self.check_droptarget() == False:
                 self.game.coils.ACselect.pulse(60)
                 self.game.coils.bikesFlash_dropTarget.pulse(60)
                 self.drive_lamp('spotLetter','on')

        def check_droptarget(self):
            if self.game.switches.dropTarget.is_active():
                self.droptarget_up = False;
                self.drive_lamp('spotLetter','off')
                print("Droptarget= Down")
            elif self.game.switches.dropTarget.is_inactive():
                self.droptarget_up = True;
                self.drive_lamp('spotLetter','on')
                print("Droptarget= Up")
            return self.droptarget_up

# Ball control

        def flippers(self, flip_on=True):
             if flip_on:
                self.game.coils.flipperEnable.enable()
             else:
                self.game.coils.flipperEnable.disable()

        def release_stuck_balls(self):
             #left eject
             if self.game.switches.Leject.is_active():
                 self.game.coils.Leject.pulse(20)

             #center eject
             if self.game.switches.Ceject.is_active():
                 self.game.coils.Ceject.pulse(20)

             #upper left kicker
             if self.game.switches.upperLkicker.is_active():
                 self.game.coils.ACselect.pulse(35)
                 self.game.coils.rearFlash_upLeftkicker.pulse(30)

             #outhole
             if self.game.switches.outhole.is_active():
                 self.game.coils.outhole.pulse(30)

        def eject_ball(self, location='all', ball_save=False):
             #left eject
             if location == 'all' or location == 'Leject':
                if self.game.switches.Leject.is_active():
                    self.game.coils.workshopFlash.schedule(schedule=0x33333333, cycle_seconds=1, now=True)
                    self.delay(name='search_leject', event_type=None, delay=0.8, handler=self.search_leject)
                    #self.game.coils.Leject.pulse(30)

             #center eject
             if location == 'all' or location == 'Ceject':
                if self.game.switches.Ceject.is_active():
                    self.game.coils.showroomFlash.schedule(schedule=0x33333333, cycle_seconds=1, now=True)
                    self.delay(name='search_ceject', event_type=None, delay=0.8, handler=self.search_ceject)
                    #self.game.coils.Ceject.pulse(30)
                    if ball_save:
                        self.game.ball_save.start(num_balls_to_save=1, time=2, now=True, allow_multiple_saves=False)
                        #self.game.ball_save.add(add_time=2, allow_multiple_saves=False)

             #upper left kicker
             if location == 'all' or location == 'upperLkicker':
                if self.game.switches.upperLkicker.is_active():
                    self.game.coils.ACselect.pulse(35)
                    self.game.coils.rearFlash_upLeftkicker.pulse(30)

        def ball_search(self):
             self.delay(name='search_leject', event_type=None, delay=0.4, handler=self.search_leject)
             self.delay(name='search_ceject', event_type=None, delay=0.8, handler=self.search_ceject)
             self.delay(name='search_upleftkicker', event_type=None, delay=1.2, handler=self.search_upleftkicker)
             self.delay(name='search_rampup', event_type=None, delay=1.6, handler=self.search_rampup)
             self.delay(name='search_outhole', event_type=None, delay=2.0, handler=self.search_outhole)

        def search_leject(self):
             self.game.coils.Leject.pulse(20)

        def search_ceject(self):
             self.game.coils.Ceject.pulse(15)

        def search_upleftkicker(self):
             self.game.coils.ACselect.pulse(40)
             self.game.coils.rearFlash_upLeftkicker.pulse(30)

        def search_rampup(self):
             self.game.coils.ACselect.pulse(60)
             self.game.coils.knocker_rampUp.pulse(50)

        def search_outhole(self):
             self.game.coils.outhole.pulse(40)

