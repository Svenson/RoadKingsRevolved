#
# Instant Info
#
# Gives info about game items and progress
# Mode is started (from rk.py) if flipper button pressed for > 6 sec. (not during multiball)
#
__author__="Pieter"
__date__ ="$29 Okt 2012 20:36:37 PM$"


import procgame
from procgame import *

#all paths
game_path = config.value_for_key_path('game_path')
dmd_path = game_path +"dmd/"


class Info(game.Mode):

    def __init__(self, game, priority):
        super(Info, self).__init__(game, priority)

        self.info_bgnd = dmd.FrameLayer(opaque=False, frame=dmd.Animation().load(dmd_path+'bgnd_info.dmd').frames[0]) #statusreport_bgnd3
        self.item_layer = dmd.TextLayer(128/2, 4, self.game.fonts['num_09Bx7'], "center")
        self.value_layer = dmd.TextLayer(128/2, 15, self.game.fonts['num_14x10'], "center")
        self.info_layer = dmd.GroupedLayer(128, 32, [self.info_bgnd,self.item_layer,self.value_layer])
        self.info_layer.transition = dmd.PushTransition(direction='west')

        self.game_items = ['bonus_x','miles_collected','crossramps_made','ramps_made','spinner_value','combo_flag','roadkings_complete']

        self.info_items = list() # e.g.({"name":bonus x,"value":2})
        self.index = 0

    def mode_started(self):
        print("Debug, Info Mode Started")
        #self.inform_player()
        self.create_info_items()
        self.update_display()

    def mode_stopped(self):
        print("Debug, Info Mode Stopped")

## Sounds & Animations

    def inform_player(self):
        self.game.sound.play(self.game.assets.sfx_nextItem)
        self.title_layer = dmd.TextLayer(128/2, 12, self.game.fonts['num_09Bx7'], "center").set_text("STATUS REPORT")
        self.inform_layer = dmd.GroupedLayer(128, 32, [self.info_bgnd,self.title_layer])
        self.inform_layer.transition = dmd.PushTransition(direction='west')
        script = list()
        script.append({'seconds':2.0, 'layer':self.inform_layer})
        self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)
        self.delay(name='update_display', event_type=None, delay=2, handler=self.update_display)

    def animate_layer(self):
        script = list()
        script.append({'seconds':6.0, 'layer':self.info_layer})
        self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)

    def clear_layer(self):
        self.layer = None

## mode functions

    def create_info_items(self):

         # create general game data
         nrball = str(self.game.ball)
         xball = str(self.game.current_player().extra_balls)
         ballspg = str(self.game.balls_per_game)
         #self.info_items.append({'name':'STATUS', 'value':'REPORT'})
         self.info_items.append({'name':'BALL IN PLAY','value':nrball})
         self.info_items.append({'name':'EXTRA BALLS','value':xball})
         self.info_items.append({'name':'BALLS PER GAME','value':ballspg})

         # create game specific game data
         for i in range(len(self.game_items)):
               game_item = self.game_items[i]
               # convert text to uppercase without underscore
               game_item = game_item.replace("_", " ").upper()
               item_value = str(self.game.get_player_stats(self.game_items[i]))
               # append data to list
               self.info_items.append({'name':game_item,'value':item_value})

         # create highscore data : ONLY WITH DEVELOP INSTALL AND _init_.py
         for hs_text in highscore.generate_highscore_text(self.game.highscore_categories):
               self.info_items.append(hs_text)

         # print complete list of items with values
         for x in self.info_items:
             print x["name"], x["value"]

         # determine max lenght of list
         self.index_max = len(self.info_items) - 1

    def exit(self):
        self.cancel_delayed('delayed_progression')
        self.clear_layer()
        self.callback()

    def get_info(self,i):
        self.item_layer.set_text(self.info_items[i]['name'])
        self.value_layer.set_text(self.info_items[i]['value'])

    def progress(self, direction):
        self.cancel_delayed('update_display')
        self.cancel_delayed('delayed_progression')
        if direction:
            if self.index == self.index_max:
                self.index = 0
            else:
                self.index += 1
        else:
            if self.index == 0:
                self.index = self.index_max
            else:
                self.index -= 1

        self.update_display()

    def update_display(self):
        self.game.sound.play(self.game.assets.sfx_nextItem)
        self.get_info(self.index)
        self.animate_layer()
        self.delay(name='delayed_progression', event_type=None, delay=4.0, handler=self.progress, param=True)

## switches

    def sw_flipperLwL_active(self,sw):
        if self.game.switches.flipperLwR.is_active():
            #self.progress(False) # Move left
            self.progress(True) # Move Right

    def sw_flipperLwR_active(self,sw):
        if self.game.switches.flipperLwL.is_active():
            self.progress(True) # Move Right

    def sw_flipperLwL_inactive(self,sw):
        if self.game.switches.flipperLwR.is_inactive():
            self.exit()

    def sw_flipperLwR_inactive(self,sw):
        if self.game.switches.flipperLwL.is_inactive():
            self.exit()
