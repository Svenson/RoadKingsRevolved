#
# Match sequence
#
# Generate match at end of a game
# called from rk.py
# 
__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"


import procgame
from procgame import *
import random

#all necessary paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"

class Match(game.Mode):

        def __init__(self, game, priority):
            super(Match, self).__init__(game, priority)

            self.match_layer = dmd.TextLayer(128/2, 10, self.game.fonts['num_14x10'], "center", opaque=False)
            self.p1_layer = dmd.TextLayer(0, 0, self.game.fonts['num_09Bx7'], "left", opaque=False)
            self.p2_layer = dmd.TextLayer(20, 0, self.game.fonts['num_09Bx7'], "left", opaque=False)
            self.p3_layer = dmd.TextLayer(108, 0, self.game.fonts['num_09Bx7'], "right", opaque=False)
            self.p4_layer = dmd.TextLayer(128, 0, self.game.fonts['num_09Bx7'], "right", opaque=False)

            self.value_range = 9

        def mode_started(self):
             print("Debug, Match Mode Started")
             self.reset_data()
             self.extract_digits()
             self.play_anim()
             #self.generate_match()
             #self.compare_digits()

        def mode_stopped(self):
             print("Debug, Match Mode Stoped")
             #set the status
             self.game.system_status='game_over'
             print("system status = "+self.game.system_status.upper())
             #add the attact mode
             self.game.modes.add(self.game.attract_mode)

## mode functions

        def reset_data(self):
             #clear data from previous games
             self.display_value = '00'
             self.player_digits = [0,0,0,0]
             self.player_layers = []
             self.match_layer.set_text('')
             self.p1_layer.set_text('')
             self.p2_layer.set_text('')
             self.p3_layer.set_text('')
             self.p4_layer.set_text('')

        def play_anim(self):
            # play animation, at frame 15, generate match and display outcome
            anim = dmd.Animation().load(dmd_path+'bike_across_screen.dmd')
            self.animation_layer = dmd.AnimatedLayer(frames=anim.frames,opaque=False,frame_time=4)
            self.animation_layer.composite_op = "blacksrc"
            self.animation_layer.add_frame_listener(15,self.generate_match)
            #set display layer
            self.layer = dmd.GroupedLayer(128, 32, [self.match_layer,self.p1_layer,self.p2_layer,self.p3_layer,self.p4_layer,self.animation_layer])
            #play sound
            self.game.sound.play(self.game.assets.sfx_horngoby)

        def extract_digits(self):
        #extract and display the last 2 score digits for each player

            self.player_layers=[self.p1_layer,self.p2_layer,self.p3_layer,self.p4_layer]

            for i in range(len(self.game.players)):
                score = self.game.players[i].score
                digit = str(score)[-2:]
                self.player_layers[i].set_text(digit)
                #set var for comparison
                self.player_digits[i]=digit
            print(self.player_digits)

        def generate_match(self):
        #create the match value for comparison

            value = (random.randint(0, self.value_range))*10
            if value==0:
                self.display_value = "0"+str(value)
            else:
                self.display_value = str(value)

            print("Match : "+self.display_value)

            #set text
            self.match_layer.set_text(self.display_value)

            #call compare function
            self.compare_digits()

        def compare_digits(self):
        #compare players last digits with generated match

            for i in range(len(self.game.players)):
                if self.player_digits[i] == self.display_value:
                    self.player_layers[i].set_text(self.player_digits[i], seconds=5, blink_frames=8)
                    self.game.coils.knocker_rampUp.pulse(20)
                    self.game.coils.Llightningbolt.pulse(20)
                    self.game.coils.Rlightningbolt.pulse(20)

            #set clear time
            self.delay(name='clear', event_type=None, delay=3.5, handler=self.clear)

        def clear(self):
            self.layer = None
            self.game.modes.remove(self)
