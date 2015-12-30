#
# Gametips mode
#
# Display gametips during the game
#

__author__="Pieter"
__date__ ="$05 aug 2013 21:21:21 PM$"

from procgame import *
from random import *
import random

# all paths
game_path = config.value_for_key_path('game_path')
speech_path = game_path +"speech/"
sound_path = game_path +"sound/"
music_path = game_path +"music/"
dmd_path = game_path +"dmd/"
lampshow_path = game_path +"lampshows/"

class Gametips(game.Mode):

        def __init__(self, game, priority):
             super(Gametips, self).__init__(game, priority)

             self.tips_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'basic_layer.dmd').frames[0])
             self.tipnr_layer = dmd.TextLayer(128/2, 3, self.game.fonts['num_09Bx7'], "center", opaque=False)
             self.line1_layer = dmd.TextLayer(128/2, 14, self.game.fonts['tiny7'], "center", opaque=False)
             self.line2_layer = dmd.TextLayer(128/2, 22, self.game.fonts['tiny7'], "center", opaque=False) #07x5

             self.tip_items = list()
             self.index = 0
             self.index_max = 1
             self.tip_on = True
             self.autotip_on = False
             self.create_tip_items()

        def mode_started(self):
             pass

        def mode_stopped(self):
             pass

## lamps & animations

        def animate_layer(self):
             script = list()
             script.append({'seconds':4.0, 'layer':self.tips_layer})
             self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)

        def clear_layer(self):
             self.layer = None

## mode functions

        def create_tip_items(self):
             self.tip_items.append({'line1':'Enjoy','line2':'playing ROADKINGS'})
             self.tip_items.append({'line1':'Play every mode', 'line2':'to become King of the Road'})
             self.tip_items.append({'line1':'Relight kickback','line2':'with ROAD targets'})
             self.tip_items.append({'line1':'KINGS targets', 'line2':'raises spinner value'})
             self.tip_items.append({'line1':'Complete lanes 1234', 'line2':'for bonus X'})
             self.tip_items.append({'line1':'Load mystery', 'line2':'with spinner turns'})
             self.tip_items.append({'line1':'Start mystery', 'line2':'in the showroom'})
             self.tip_items.append({'line1':'Hold a flipper while', 'line2':'shooting the droptarget...'})
             self.tip_items.append({'line1':'Spell ROADKINGS 3 times', 'line2':'for extra ball'})
             self.tip_items.append({'line1':'Play all missions and modes', 'line2':'for wizard mode'})
             self.tip_items.append({'line1':'There are 5 bumper', 'line2':'levels to explore'})
             self.tip_items.append({'line1':'Jetbumpers count', 'line2':'to next level award'})
             self.tip_items.append({'line1':'Xramp is in the middle', 'line2':'Jumpramp on the right'})
             self.tip_items.append({'line1':'Complete Xramp for', 'line2':'hurry up score'})
             self.tip_items.append({'line1':'Complete Jumpramp for', 'line2':'hurry up score'})
             self.tip_items.append({'line1':'Xramp starts', 'line2':'combo possibility'})
             self.tip_items.append({'line1':'Xramp + spinner', 'line2':'makes left combo'})
             self.tip_items.append({'line1':'Xramp + Jumpramp', 'line2':'makes Jump combo'})
             self.tip_items.append({'line1':'Xramp + under ramp', 'line2':'makes right combo'})
             self.tip_items.append({'line1':'Collect miles', 'line2':'to trade for awards'})
             self.tip_items.append({'line1':'Shoot the workshop', 'line2':'to move the ramp'})
             self.tip_items.append({'line1':'Trade miles for awards', 'line2':'in the workshop'})
             self.tip_items.append({'line1':'Shoot the showroom', 'line2':'to start mystery'})
             self.tip_items.append({'line1':'Miles and Jumpramps', 'line2':'add to bonus'})
             self.tip_items.append({'line1':'Bumperlevel 1', 'line2':'Regular hits'})
             self.tip_items.append({'line1':'Bumperlevel 2', 'line2':'Quick M-ball, shoot spinner'})
             self.tip_items.append({'line1':'Bumperlevel 3', 'line2':'Bigbumpers, hits worth 100k'})
             self.tip_items.append({'line1':'Bumperlevel 4', 'line2':'Bumpers count for miles'})
             self.tip_items.append({'line1':'Bumperlevel 5', 'line2':'Tunneltrail mode'})
             self.tip_items.append({'line1':'Shoot the spinner', 'line2':'during Quick multiball'})
             self.tip_items.append({'line1':'Shoot under the ramp', 'line2':'during Tunneltrial'})
             self.tip_items.append({'line1':'To start a mode', 'line2':'shoot the jumpramp'})
             self.tip_items.append({'line1':'To activate Trade miles', 'line2':'shoot under the ramp'})
             self.tip_items.append({'line1':'Right inlane activates', 'line2':'Trade miles in workshop'})
             self.tip_items.append({'line1':'Complete mode', 'line2':'to improve Wizardmode'})
             self.tip_items.append({'line1':'To complete a mode', 'line2':'score a jackpot or win race'})
             self.tip_items.append({'line1':'Complete Race Champion for', 'line2':'double scoring in wizardmode'})
             self.tip_items.append({'line1':'Complete Kickstart King for', 'line2':'double JP-time in wizardmode'})
             self.tip_items.append({'line1':'Complete Multiball for', 'line2':'ext. ballsave in wizardmode'})
             self.tip_items.append({'line1':'Complete Easy Rider for', 'line2':'unlim. kickback in wizardmode'})
             self.tip_items.append({'line1':'For ball search', 'line2':'Hold both flip.buttons 10 sec.'})

             # print complete list of items with values
             #for x in self.tip_items:
             #    print x["line1"], x["line2"]

             # determine max lenght of list
             self.index_max = len(self.tip_items) - 1
             print("nr. of tips: "+str(self.index_max))

        def get_info(self,tipnr):
             self.tipnr_layer.set_text('GAME TIP '+str(tipnr), blink_frames=None)
             self.line1_layer.set_text(self.tip_items[tipnr]['line1'])
             self.line2_layer.set_text(self.tip_items[tipnr]['line2'])
             self.tips_layer = dmd.GroupedLayer(128, 32, [self.tips_bgnd,self.tipnr_layer,self.line1_layer,self.line2_layer])

        def display_tip(self, tipnr=None):
             if self.tip_on and not self.game.get_player_stats('game_feature_running'):
                 self.game.sound.play(self.game.assets.sfx_newTip)
                 if tipnr==None or tipnr > self.index_max:
                      tipnr = random.randrange(0, len(self.tip_items),1)
                 print("tipnr: "+str(tipnr))
                 self.get_info(tipnr)
                 self.tips_layer.transition = dmd.PushTransition(direction='south')
                 self.animate_layer()
                 if self.autotip_on == False: # Don't clear while in auto progress
                     self.delay(name='clear_layer', event_type=None, delay=4.0, handler=self.clear_layer)

        def progress_tip(self):
             self.cancel_delayed('delayed_progress')
             if self.index == self.index_max:
                 self.index = 0
             else:
                 self.index += 1
             self.display_tip(self.index)
             self.delay(name='delayed_progress', event_type=None, delay=4.0, handler=self.progress_tip)

        def start_gametips(self):
             self.autotip_on = True
             self.progress_tip()

        def exit(self):
             self.cancel_delayed('delayed_progress')
             self.autotip_on = False
             self.clear_layer()

        def get_tip(self, tipnr=None):
             if tipnr==None or tipnr > self.index_max:
                  tipnr = random.randrange(0, len(self.tip_items),1)
             #print("tipnr: "+str(tipnr))
             self.get_info(tipnr)
             return self.tips_layer

## switches

        def sw_flipperLwL_active(self,sw):
             if self.autotip_on:
                 if self.game.switches.flipperLwR.is_active():
                     self.progress_tip()

        def sw_flipperLwR_inactive(self,sw):
             if self.autotip_on:
                 if self.game.switches.flipperLwL.is_inactive():
                     self.exit()
