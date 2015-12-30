#
# Ramp move
#
# Game mode that controls movement of the rightramp entrance
#
# Added 24-7-13: control for Trade miles menu, since it is
# activated from same ejecthole as ramp movement.
# In future maybe move all Leject control to general_play game mode for clearity/consistancy
#
__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"


import procgame
from procgame import *
from trade_miles import *

#all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"


class Rampmove(game.Mode):

        def __init__(self, game, priority):
            super(Rampmove, self).__init__(game, priority)

            self.trademiles = Trademiles(self.game, 80) # reference to trademiles

            self.text_layer = dmd.TextLayer(70, 22, self.game.fonts['07x5'], "center", opaque=False)
            self.workshop_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'workshop.dmd').frames[0])
            self.workshop_layer = dmd.GroupedLayer(128, 32, [self.workshop_bgnd, self.text_layer])
            self.workshop_layer.transition = dmd.PushTransition(direction='north')

            self.ramp_up = False
            self.count = 0
            self.trade_miles = False

        def mode_started(self):
            print("Debug, Rampmove Mode Started")
            self.move_ramp('down')
            self.trade_miles = False

        def mode_stopped(self):
            print("Debug, Rampmove Mode Ended")

## lamps and animations

        def update_lamps(self):
            pass

        def play_animation(self):
            script = list()
            script.append({'seconds':2.0, 'layer':self.workshop_layer})
            self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)
            self.delay(name='clear_display', event_type=None, delay=2, handler=self.clear_layer)

        def inform_miles(self):
             anim = dmd.Animation().load(dmd_path+'miles_inform.dmd')
             self.animation_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=True, hold=False, frame_time=20)
             self.layer = self.animation_layer
             self.delay(name='clear_layer', event_type=None, delay=3, handler=self.clear_layer)

        def clear_layer(self):
             self.layer = None

## mode functions

        def check_state(self):
            if self.game.switches.rampRaise.is_active():
                self.ramp_up = False;
                print("Ramp= Down")
            elif self.game.switches.rampRaise.is_inactive():
                self.ramp_up = True;
                print("Ramp= Up")
            self.game.set_player_stats('ramp_state',self.ramp_up)
            # update lamp status's for all modes in case of ramp change
            self.game.effects.update_ramp_lamps()
            return self.ramp_up

        def move_ramp(self,direction='down'):
           #rampup and rampdown procedure:
           #To make sure the rampstate has changed, a repeated call to itself is made to check the change in switch rampRaise
           #The repeated call is cancelled after 3 times to prevent damage or locked coils

           if direction=='down':
                #cancel previous check if direction changes
                self.cancel_delayed('rampupcheck')

                if self.game.switches.rampRaise.is_inactive():
                    #activate ACSelect + coil
                    self.game.coils.ACselect.pulse(50)
                    self.game.coils.midBikeFlash_rampDown.pulse(40)
                    #play sound
                    self.game.sound.play(self.game.assets.sfx_rampChange)
                    #repeat call after delay to check change
                    self.delay(name='rampdowncheck', event_type=None, delay=2, handler=self.move_ramp, param='down')
                    self.count +=1 # raise counter
                    print("Move ramp try: "+str(self.count))

                elif self.game.switches.rampRaise.is_active():
                      self.count =0 # reset counter

           elif direction=='up':
                #cancel previous check if direction changes
                self.cancel_delayed('rampdowncheck')

                if self.game.switches.rampRaise.is_active():
                    #activate ACSelect + coil
                    self.game.coils.ACselect.pulse(100)
                    self.delay(name='rampUp', event_type=None, delay=0.05, handler=self.rampUp) # for delay see: def rampUp(self):
                    #self.game.coils.knocker_rampUp.pulse(50)
                    #play sound
                    self.game.sound.play(self.game.assets.sfx_rampChange)
                    #repeat call after delay to check change
                    self.delay(name='rampupcheck', event_type=None, delay=2, handler=self.move_ramp, param='up')
                    self.count +=1 # raise counter
                    print("Move ramp try: "+str(self.count))

                elif self.game.switches.rampRaise.is_inactive():
                      self.count =0 # reset counter
           else:
                print("rampdirection unclear: "+str(direction))

           # cancel repeated call after 3 times to prevent damage or locked coils
           if self.count == 3:
               self.cancel_delayed('rampupcheck')
               self.cancel_delayed('rampdowncheck')
               print("RAMP ERROR: "+str(direction))
               self.count =0 # reset counter

           # check state after delay
           self.delay(name='check_state', event_type=None, delay=1, handler=self.check_state)

        def rampUp(self):
            #delay added because of timing issue with AC-select solenoid 
            #which activated knocker together with rampup coil.
            self.game.coils.knocker_rampUp.pulse(50)

## switches

        def sw_Leject_active_for_200ms(self, sw):
            self.play_animation()
            self.game.coils.Rlightningbolt.schedule(0x33333333, cycle_seconds=1, now=True)
            if self.game.get_player_stats('miles_collected') > 5:
                if self.game.switches.lane3.time_since_change() < 4 or self.game.switches.CrampRexit.time_since_change() < 4:
                    self.trade_miles = True

        def sw_Leject_active_for_400ms(self, sw):
            if self.game.switches.rampRaise.is_inactive():
                self.text_layer.set_text("RAMP DOWN", blink_frames=10)
                self.move_ramp('down')
            elif self.game.switches.rampRaise.is_active():
                  self.text_layer.set_text("RAMP UP", blink_frames=10)
                  self.move_ramp('up')

            if self.trade_miles:
                self.text_layer.set_text("TRADE MILES", blink_frames=10)

        def sw_Leject_active_for_1s(self, sw):
             if self.trade_miles==True and self.game.get_player_stats('game_feature_running')==False:
                 self.trade_miles = False
                 self.game.effects.drive_flasher('workshopFlash','off')
                 # add trademiles mode
                 self.game.modes.add(self.trademiles)
             else:
                 self.game.effects.eject_ball('Leject')
                 #self.game.coils.Llightningbolt.schedule(0x33333333, cycle_seconds=1, now=True)

        def sw_Rrollunder_active(self,sw):
             # check for minimum miles
             if self.game.get_player_stats('miles_collected') > 5 and self.trade_miles == False and not self.game.get_player_stats('game_feature_running'):
                 self.game.coils.Lgate.schedule(0xffffffff, cycle_seconds=2, now=True)
                 self.game.sound.play(self.game.assets.sfx_selectItem)
                 self.game.coils.rearFlash_upLeftkicker.schedule(schedule=0xaaaaaaaa, cycle_seconds=1, now=True)
                 self.game.effects.drive_flasher('workshopFlash','slow')
                 self.inform_miles()
                 self.trade_miles = True
