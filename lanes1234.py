#
# lanes1234 (top rollover & inlanes)
#
# Game mode for 1,2,3,4, lanes
# control for lanechange and bonusmultiplier
# 
__author__="Pieter"
__date__ ="$10 Sep 2012 20:36:37 PM$"

import procgame
from procgame import *

#all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"


class Lanes1234(game.Mode):

        def __init__(self, game, priority):
            super(Lanes1234, self).__init__(game, priority)

            anim = dmd.Animation().load(dmd_path+'lanes_ani.dmd')
            self.bgnd_layer = dmd.AnimatedLayer(frames=anim.frames, opaque=False, repeat=False, hold=True, frame_time=5)
            self.bonus_layer = dmd.TextLayer(98, 4, self.game.fonts['num_09Bx7'], "center", opaque=False)
            self.bonusx_layer = dmd.TextLayer(98, 15, self.game.fonts['num_09Bx7'], "center", opaque=False)

            self.lane_flag = [False,False,False,False]
            self.lamps = ['lane1','lane2','lane3','lane4']
            self.bonusx_flag = [0,0,0,0]
            self.bonusxlamps = ['bonus2x','bonus3x','bonus4x','bonus5x']

            self.bonusx = 1
            self.hold_bonusx = False

            self.lane_on_value = 1000
            self.lane_off_value = -500
            self.reset()

        def reset(self):
            self.numbers_spotted = 0
            self.lane_flag = [False,False,False,False]
            self.clear_lamps()

        def mode_started(self):
            print("Debug, Lanes1234 Mode Started")
            #load player specific data
            self.lane_flag = self.game.get_player_stats('lanes1234_flag')
            self.numbers_spotted = self.game.get_player_stats('lanes1234_numbers_spotted')
            # if hold_bonusx True, get previous bonus
            if self.game.get_player_stats('hold_bonusx'):
                self.bonusx = self.game.get_player_stats('bonus_x')
                # reset hold_bonusx 
                self.game.set_player_stats('hold_bonusx',False)
            else: # else overwrite previous
                self.game.set_player_stats('bonus_x',self.bonusx)
            self.select_bonusxflag()

            #update lamp states
            self.update_lamps()

        def mode_stopped(self):
            #save player specific data
            self.game.set_player_stats('lanes1234_flag',self.lane_flag)
            self.game.set_player_stats('lanes1234_numbers_spotted',self.numbers_spotted)
            #self.game.set_player_stats('bonus_x',self.bonusx)
            print("Debug, Lanes1234 Mode Ended")

## lamps

        def clear_lamps(self):
            for i in range(len(self.lamps)):
                self.game.effects.drive_lamp(self.lamps[i],'off')

        def completed(self):
            for i in range(len(self.lamps)):
                self.game.effects.drive_lamp(self.lamps[i],'superfast')

        def update_lamps(self):
            for i in range(len(self.lamps)):
                if self.lane_flag[i]:
                    self.game.effects.drive_lamp(self.lamps[i],'on')

            if self.game.get_player_stats('hold_bonusx'):
                self.game.effects.drive_lamp('holdBonus','on')
            else:
                self.game.effects.drive_lamp('holdBonus','off')

            self.update_bonusxlamps()

        def update_bonusxlamps(self):
            for i in range(len(self.bonusxlamps)):
                if self.bonusx_flag[i]:
                    self.game.effects.drive_lamp(self.bonusxlamps[i],'on')
                else:
                    self.game.effects.drive_lamp(self.bonusxlamps[i],'off')

        def clear_layer(self):
            self.layer = None

## mode functions

        def spell_1234(self):
            if self.numbers_spotted ==4:

                #Increase bonus x
                self.game.add_player_stats('bonus_x',1)
                self.bonusx = self.game.get_player_stats('bonus_x')
                #print("bonus x "+str(self.bonusx))
                self.select_bonusxflag()

                #set text layers
                #OLDself.bonus_layer.set_text("BONUS X"+str(self.bonusx),seconds=2)
                self.bonus_layer.set_text("BONUS",seconds=2)
                self.bonusx_layer.set_text("X"+str(self.bonusx),seconds=2)
                #set display layer
                self.layer = dmd.GroupedLayer(128, 32, [self.bgnd_layer, self.bonus_layer, self.bonusx_layer])
                #set layer clear time
                self.delay(name='clear_layer', event_type=None, delay=2, handler=self.clear_layer)

                if self.bonusx >=15:
                    self.delay(name='bonus_text', event_type=None, delay=2, handler=self.extra_ball_lit)

                #flash all lamps when completed then reset after delay
                self.completed()
                self.delay(name='reset_lanes', event_type=None, delay=1.5, handler=self.reset)

        def select_bonusxflag(self):
             if self.bonusx == 1:
                 self.bonusx_flag = [0,0,0,0]
             elif self.bonusx == 2:
                 self.bonusx_flag = [1,0,0,0]
             elif self.bonusx == 3:
                 self.bonusx_flag = [0,1,0,0]
             elif self.bonusx == 4:
                 self.bonusx_flag = [0,0,1,0]
             elif self.bonusx == 5:
                 self.bonusx_flag = [0,0,0,1]
             elif self.bonusx == 6:
                 self.bonusx_flag = [1,0,1,0]
             elif self.bonusx == 7:
                 self.bonusx_flag = [0,1,1,0]
             elif self.bonusx == 8:
                 self.bonusx_flag = [0,1,0,1]
             elif self.bonusx == 9:
                 self.bonusx_flag = [0,0,1,1]
             elif self.bonusx == 10:
                 self.bonusx_flag = [1,1,0,1]
             elif self.bonusx == 11:
                 self.bonusx_flag = [1,0,1,1]
             elif self.bonusx == 12:
                 self.bonusx_flag = [0,1,1,1]
             elif self.bonusx == 13:
                 self.bonusx_flag = [0,1,1,1]
             elif self.bonusx >= 14:
                 self.bonusx_flag = [1,1,1,1]
             # update bonusxlamps
             self.update_bonusxlamps()

        def extra_ball_lit(self):
            self.game.extra_ball.lit('Rextraball')

        def lanes(self,id):
            if self.lane_flag[id] == False:
                #If lane was off, turn it on
                self.lane_flag[id]=True;
                self.numbers_spotted +=1
                #update player stats
                self.game.set_player_stats('lanes1234_flag',self.lane_flag)
                #print("lane lamp on: %s "%(self.lamps[id]))
                self.game.score(self.lane_on_value)

                #play sounds
                if self.numbers_spotted ==4:
                    self.game.sound.play(self.game.assets.sfx_laneComplete)
                else:
                    self.game.sound.play(self.game.assets.sfx_laneOn)
                    self.game.effects.drive_lamp(self.lamps[id],'on')

            else:
                #play sounds
                self.game.sound.play(self.game.assets.sfx_laneOff)

                #If lane was on, turn it off.
                #Maybe not suitable for novice players to unlit lane?
                self.game.score(self.lane_off_value)
                self.lane_flag[id]=False;
                self.numbers_spotted -=1
                self.game.effects.drive_lamp(self.lamps[id],'off')
                #update player stats
                self.game.set_player_stats('lanes1234_flag',self.lane_flag)
                #print("lane lamp off: %s "%(self.lamps[id]))

            self.spell_1234()
            #print(self.lane_flag)
            #print(self.numbers_spotted)


        def lane_change(self,direction):
            list = ['lane1','lane2','lane3','lane4']
            flag_orig = self.lane_flag
            flag_new = [False,False,False,False]
            carry = False
            j=0

            if direction=='left':
                start = 0
                end = len(list)
                inc =1
            elif direction=='right':
                start = len(list)-1
                end = -1
                inc =-1

            for i in range(start,end,inc):
                if flag_orig[i]:

                    if direction=='left':
                        j=i-1
                        if j<0:
                            j=3
                            carry = True
                    elif direction=='right':
                        j=i+1
                        if j>3:
                            j=0
                            carry = True

                    flag_new[i] = False
                    flag_new[j]= True

                    self.game.effects.drive_lamp(list[i],'off')
                    self.game.effects.drive_lamp(list[j],'on')

            #update the carry index if required
            if carry and direction=='left':
                flag_new[3]= True
                self.game.effects.drive_lamp(list[3],'on')
            elif carry and direction=='right':
                flag_new[0]= True
                self.game.effects.drive_lamp(list[0],'on')

            self.lane_flag=flag_new
            #print(self.lane_flag)

## switches

        def sw_lane1_active(self, sw):
            self.lanes(0)

        def sw_lane2_active(self, sw):
            self.lanes(1)

        def sw_lane3_active(self, sw):
            self.lanes(2)

        def sw_CrampRexit_active(self, sw):
            self.lanes(2)

        def sw_lane4_active(self, sw):
            self.lanes(3)


        def sw_flipperLwL_active(self, sw):
            self.lane_change('left')

        def sw_flipperLwR_active(self, sw):
            self.lane_change('right')

