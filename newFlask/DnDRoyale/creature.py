#This may be the removed creature class, but I'm going to add it back to DnD.py for now to get things working.

import warnings
import math, os
from DnDRoyale import DnD

TARGET = 'enemy alive weakest'
N = "<br/>"

class Creature:
    """
    Creature class handles the creatures and their actions and some interactions with the encounter.
    """
    #@staticmethod
    def load_beastiary(path):
        """
        `load_beastiary(path)` (formerly just `_beastiary`) is a function while beastiary is the attribute it fills.
        There are a few way of how the creature data comes about. This is to initialise the beastiary, now the standard source of beastiary.
        When the code starts, it tries first to find a `beastiary.csv` file.
        It's a method because it can fail and needs to be rerun in case there is no `beastiary.csv`.
        :param path: the string to the csv file
        :return: the beastiary, a dictionary (keys: creature names) of dictionary (keys: csv headers)
        The headers of the csv are: (some are for analysis, _e.g._ `hp_fudge`)
        * name (becomes the key too)
        * alt
        * alignment
        * type
        * size
        * armour_name
        * stated_ac
        * armor_bonus
        * ac
        * stated_hp
        * hp
        * expected_hp
        * hp_fudge
        * level
        * hd
        * Str
        * Dex
        * Con
        * Int
        * Wis
        * Cha
        * attack_parameters
        * CR
        * xp
        * regen
        * healing_spells
        * healing_dice
        * healing_bonus
        * sc_ability
        * log
        * proficiency
        * initiative_bonus
        * AB_Str   -- as in ability bonus.
        * AB_Dex
        * AB_Con
        * AB_Int
        * AB_Wis
        * AB_Cha
        * max_morale
        * current_morale
        """
        # I like this way better since it yields a dict by default
        # check here https://www.youtube.com/watch?v=efSjcrp87OY
        try:
            import csv
            r = csv.reader(open(path, encoding='utf-8-sig'))

            headers = next(r)
            # print(headers)

            beastiary = {}
            for row in r:
                beast = {h: row[i] for i, h in enumerate(headers) if row[i]}
                if 'name' in beast:
                    beastiary[beast['name']] = beast

            print("beastiary found")
            return beastiary

        except Exception as e:
            warnings.warn('Beastiary error, expected path ' + path + ' error ' + str(e))
            return {}

    beastiary = load_beastiary('DnDRoyale/creatures.csv')
    ability_names = ['str', 'dex', 'con', 'wis', 'int', 'cha']
    debug = True

    def __init__(self, wildcard, **kwargs): 
        """
        Creature object creation. A lot of paramaters make a creature so a lot of assumptions are made (see __init__`).
        :param wildcard: the name of the creature.
          If nothing else is passed it will take it from the beastiary.
          If a dictionary is passed, it will process it like **kwargs,
          If a Creature object is passed it will make a copy
        :param kwargs: a lot of arguments...
        :return: a creature.
        The arguments are many.
        >>> print(Creature(Creature('aboleth'), ac=20).__dict__)
        `{'abilities': None, 'dex': 10, 'con_bonus': 10, 'cr': 17, 'xp': 5900, 'ac': 20, 'starting_healing_spells': 0, 'starting_hp': 135, 'condition': 'normal', 'initiative': <__main__.Dice object at 0x1022542e8>, 'str': 10, 'wis': 10, 'ability_bonuses': {'int': 0, 'cha': 0, 'dex': 0, 'con': 0, 'str': 0, 'wis': 0}, 'custom': [], 'hd': <__main__.Dice object at 0x102242c88>, 'hurtful': 36.0, 'tally': {'rounds': 0, 'hp': 0, 'battles': 0, 'hits': 0, 'damage': 0, 'healing_spells': 0, 'dead': 0, 'misses': 0}, 'hp': 135, 'proficiency': 5, 'cha_bonus': 10, 'able': 1, 'healing_spells': 0, 'copy_index': 1, 'int': 10, 'concentrating': 0, 'wis_bonus': 10, 'con': 10, 'int_bonus': 10, 'sc_ab': 'con', 'str_bonus': 10, 'level': 18, 'settings': {}, 'arena': None, 'dex_bonus': 10, 'log': '', 'cha': 10, 'dodge': 0, 'alt_attack': {'attack': None, 'name': None}, 'alignment': 'lawful evil ', 'attacks': [{'attack': <__main__.Dice object at 0x1022545f8>, 'damage': <__main__.Dice object at 0x1022545c0>, 'name': 'tentacle'}, {'attack': <__main__.Dice object at 0x102254668>, 'damage': <__main__.Dice object at 0x102254630>, 'name': 'tentacle'}, {'attack': <__main__.Dice object at 0x1022546d8>, 'damage': <__main__.Dice object at 0x1022546a0>, 'name': 'tentacle'}], 'attack_parameters': [['tentacle', 9, 5, 6, 6], ['tentacle', 9, 5, 6, 6], ['tentacle', 9, 5, 6, 6]], 'buff_spells': 0, 'temp': 0, 'name': 'aboleth'}`
        """
        self.log = ""
        #if not kwargs and type(wildcard) is str:
        #    print("filling from beastiary - no kwargs")
        #    self._fill_from_beastiary(wildcard)
        if type(wildcard) is dict:
            print("this wildcard is a dict")
            self._initialise(**wildcard)
        #elif kwargs and type(wildcard) is str:
        #    print("kwargs, and also this wildcard is str")
        #    if wildcard in self.beastiary:
        #        print("this wildcard is in the beastiary")
        #        self._initialise(base=wildcard, **kwargs)
        #    else:
        #        self._initialise(name=wildcard, **kwargs)
        #elif type(wildcard) is Creature:
        #    print("this wildcard is a Creature")
        #    self._initialise(base=wildcard, **kwargs)
        else:
            warnings.warn("UNKNOWN COMBATTANT:" + str(wildcard))
            print("UNKNOWN COMBATTANT:" + str(wildcard))
            # raise Exception
            print("I will not raise an error. I will raise Cthulhu to punish this user errors")
            self._fill_from_preset("cthulhu")

    def getattacks(self):
        # get use attacks from user, if none, get from bestiary, if none, figure appropriate attack : fist/claw/slam and params
        print("loading attack information")
        # self.attacks = []
        self.hurtful = 0
        # custom creature that wants default attacks
        if not 'attack_parameters' in self.settings:
            self.settings['attack_parameters'] = self.beastiary['attack_parameters']

        if self.settings['attack_parameters'] == '': # TB
            print("___----==== NO ATTACK PARAMETERS/ATTACK PARAMETER ERROR ====----____")
            try:
                import json
                x = json.loads(self.settings['attack_parameters'].replace("*", "\""))
                x = self.settings['attack_parameters']
                self._attack_parse(x)
                self.attack_parameters = x
            except:
                #These have to be readable by _attack_parse
                weapons = {'club': 4, 'greatclub':8,
                           'dagger': 4, 'shortsword': 6, 'longsword': 8, 'bastardsword': 10, 'greatsword': 12,
                           'rapier': 8, 'scimitar': 6, 'sickle':4,
                           'handaxe':6, 'battleaxe':8, 'waraxe':10,'greataxe':12,
                           'javelin':6, 'spear':6, 'flail':8, 'glaive':10, 'halberd':10, 'lance':12, 'pike':10, 'trident': 6,
                           'war pick':8,
                           'lighthammer':4, 'mace':6, 'warhammer':8,
                           'quaterstaff':6, 'morningstar':8, 'punch':1, 'whip':4} #parsing of strings for dice not implemented yet, so punch is d1 for now.
                # TODO weapons removed as they gave trouble:
                #'maul':[6,6],
                # 'brütal war pick': [8, 8], 
        
                #bastard sword and war axe are no more due to the versatile rule, however they were kept here to keep it simple
                #ranged weapons are missing for now...
                for w in weapons.keys():
                    if self.settings['attack_parameters'].lower().find(w) > -1:
                        # TODO fix the fact that a it gives the finesse option to all.
                        chosen_ab = self.ability_bonuses[max('str', 'dex', key=lambda ab: self.ability_bonuses[ab])]
                        self.attack_parameters = [[w, self.proficiency + chosen_ab, chosen_ab, weapons[w]]]
                        self._attack_parse(self.attack_parameters)
                        self.log += "Weapon matched by " + chosen_ab + " to " + w + N
                        break
                else:
                    raise Exception("Cannot figure out what is: " + self.settings['attack_parameters'] + str(
                    type(self.settings['attack_parameters'])))
        #if not type(self.settings['attack_parameters'][0]) is str: # this is taking a list and making it a string... normal creatures aren't hitting this, but it's messing up Cthulhu
        #    self.settings['attack_parameters'][0] = str(self.settings['attack_parameters'][0])

        self.attack_parameters = self._attack_parse(self.settings['attack_parameters'])
            
        #print("attack is : " + str(self.attacks[0]))

    def getVulnerabilities(self):
        if self.beastiary['vulnerabilities'] != 'none':
            import json
            self.vulnerabilities = json.loads(self.beastiary['vulnerabilities'])

    def getAbilityScores(self):
        for a in self.ability_names: 
            if a in self.settings.keys() and int(self.settings[a]) != 0: # IF custom ability score is provided
                self.abilities[a] = int(self.settings[a])
            else: # ELSE get it from bestiary
                self.abilities[a] = int(self.beastiary[a])
                #will also need to get ability mods
                
    def getAbilityModifiers(self):
        # Ability scores have already been determined. Figure from known
        for mod in self.ability_names: 
            self.ability_bonuses[mod] = int((self.abilities[mod] - 10) // 2)

    def getmorale(self):
        print("getting morale")
        morale = 0
        # TB Need to check this code to make sure everything is correct... also this needs to be made into separate methods
        # TB need to find CR to find the equivalent BR and therefore max_morale amount
        if 'cr' in self.settings: 
            self.cr = self.settings['cr']
        elif 'cr' in self.beastiary: 
            self.cr = self.beastiary['cr']

        #this is where the value is validated or found and assigned max_morale
        # BREAK OUT INTO OWN METHOD
        # could do cr and br assignments in one block. If there is no Cr, there's not going to be a Br
        if 'br' in self.settings:
            self.max_morale = int(self.settings['br'])
            self.current_morale = int(self.settings['br'])
        elif 'br' in self.beastiary:
            self.max_morale = int(self.beastiary['br'])
            self.current_morale = int(self.beastiary['br'])
        else: 
            self.settings['max_morale'] = 0
            self.max_morale = 0
            self.current_morale = 0
            
        print("getting Morale value")
        # IF creature is not in Beasiary or if Custom Combatant is given, find proper morale value
        if self.max_morale =='' or int(self.max_morale) == 0:
            # morale = 0
            # if morale is 0 or null, then check the CR and figure BR from that (do I need a fallback option?)
            _cr = float(self.cr)
            if _cr < 2.0:
                morale = 1
            elif _cr > 1.0 and _cr < 6.0:
                morale = _cr 
            elif _cr > 5.0 and _cr < 10.0: 
                morale = _cr + 1
            elif _cr == 10.0:
                morale = 12
            elif _cr == 11.0:
                morale = 14
            elif _cr == 12.0:
                morale = 15
            elif _cr == 13.0:
                morale = 16
            elif _cr == 14.0:
                morale = 18
            elif _cr == 15.0:
                morale = 20
            elif _cr > 15.0:
                morale = 99 # 99 for testing
        
            # setup max morale and set current morale to max morale (since they start out at max)
        print(self.name + " has " + str(morale) + " morale") 
        self.current_morale = morale
        self.max_morale = morale

    def getTeam(self):
        #recording the different teams... thought they should only be 'Red' and 'Blue'... I think  
        self.team = self.settings['team']

    def getHp(self):
        print("getting HP value")
        if 'hp' in self.settings.keys() and int(self.settings['hp']) != 0 and self.settings['hp'] != '': # IF custom setting
            self.hp = int(self.settings['hp'])
            self.starting_hp = self.hp
        else: # ELSE default values
            self.hp = int(self.beastiary['hp'])
            self.starting_hp = self.hp
        #else:
        #    raise Exception('Cannot make character without hp or hd + level provided')

    def getAc(self):
        print("getting ac, initiative, spell ability bonus...")
        # AC
        if 'ac' in self.settings.keys() and int(self.settings['ac']) != 0: # IF custom setting and default is NOT desired
            self.ac = int(self.settings['ac'])
        else: # ELSE default value
            self.ac = int(self.beastiary['ac'])
        
    def getInitiative(self):
        # init
        if 'initiative_bonus' in self.settings: # IF custom
            self.initiative_bonus = self.ability_bonuses['dex']
        elif self.beastiary['initiative_bonus']: #ELSE Default
            self.initiative_bonus = int(self.beastiary['initiative_bonus'])
        else: #ELSE backup default
           self.initiative_bonus = int(self.beastiary['ab_dex'])
        self.initiative = DnD.Dice(int(self.initiative_bonus), 20, role="initiative")
        
    def getSpellCasting(self):
        ## spell casting ability_bonuses ## should be able to have NO spell ability. 
        ## need to be able to use custom or fall back on bestiary value ... or default custom (option A)
        spells = ''
        if not 'spellCasting' in self.settings: # IF it's default
                spells = "None" # self.beastiary['sc_ability'] # get from Bestiary... but it's going to be ...so We'll just make it "None" for now 
        elif self.settings['spellCasting'] != "None": #IF custom
            casting = self.settings['spellCasting']
            if casting == 'Intelligence': spells = "int"
            elif casting == 'Wisdom' : spells = "wis"
            elif casting == 'Charisma' : spells = "cha"
            else : spells = "None"
        if 'healing_spells' in self.settings:
            self.starting_healing_spells = int(self.settings['healing_spells'])
            self.healing_spells = self.starting_healing_spells
            if not 'healing_dice' in self.settings:
                self.settings['healing_dice'] = 4  # healing word.
            self.healing = DnD.Dice(int(self.settings['healing_bonus']), int(self.settings['healing_dice']),
                                role="healing")  ##Healing dice can't crit or have adv.
        else:
            self.starting_healing_spells = 0
            self.healing_spells = 0

        self.sc_ab = spells

    def getHd(self):
        print("getting hd")
        self.hd = None
        if 'hd' in self.base.keys():
            if type(self.base['hd']) is DnD.Dice:
                self.hd = self.base['hd']  # we're dealing with a copy of a beastiary obj.
            else:
                self.hd = DnD.Dice(self.ability_bonuses['con'], int(self.base['hd']), avg=True, role="hd")
        elif 'size' in self.base.keys():
            size_cat = {"small": 6, "medium": 8, "large": 10, "huge": 12}
            if self.base['size'] in size_cat.keys():
                self.hd = DnD.Dice(self.ability_bonuses['con'], size_cat[self.base['size']], avg=True, role="hd")
        elif 'hp' in self.base and 'level' in self.base:
            #Guess based on hp and level. It is not that dodgy really as the manual does not use odd dice.
            # hp =approx. 0.5 HD * (level-1) + HD + con * level
            # HD * (0.5* (level-1)+1) = hp - con*level
            # HD = (hp - con*level)/(level+1)
            bestchoice=(int(self.base['hp'])-int(self.ability_bonuses['con']) * int(self.base['level']))/((int(self.base['level'])+1))
            print(int(self.base['hp']),int(self.ability_bonuses['con']), int(self.base['level']))
            print("choice HD...",bestchoice)
            #print("diagnosis...",self.ability_bonuses)
            warnings.warn('Unfinished case to guess HD. so Defaulting hit dice to d8 instead') #TODO finish
            self.hd = DnD.Dice(self.ability_bonuses['con'], 8, avg=True, role="hd")
        else:
            #defaulting to d8
            warnings.warn('Insufficient info: defaulting hit dice to d8')
            self.hd = DnD.Dice(self.ability_bonuses['con'], 8, avg=True, role="hd")

    def getAltAttack(self): 
        print("actions")
        # dice(self, bonus=0, dice=20, avg=False, twinned=None, role="ability")
        # this isn't going to work atm...need to get to the damage etc correctly
        if self.beastiary['actions'] != 'none': #IF the creature has actions
            import json
            self.beastiary['actions'].replace('\n', '') #json decoder error possibility
            actions = json.loads(self.beastiary['actions']) # make list of actions into object
            for action in actions: #make relevant dice for random elements in attacks
                print("Action name : " + action['name'])
                dmgMod = 0
                if "damage_modifier" in action:
                     dmgMod = action['damage_modifier']
                if "num_targets" in action:
                    action['num_targets'] = DnD.Dice(math.floor(action['max_targets']/2), dice = math.floor(action['max_targets']/2), role='damage')#role 'damage' makes it non-critable
                if "recharge" in action:
                    action['recharge'] = DnD.Dice(0, dice = action['recharge'], role='damage')
                if "damage" in action:
                    action['damage'] = DnD.Dice(dmgMod, dice = action['damage'], role='damage')
                if "secondary_type" in action:
                    action['secondary_damage'] = DnD.Dice(0, action['secondary_damage'], role='damage')
                if "secondary_save" in action:
                    action['secondary_save'] = DnD.Dice(0, action['secondary_save'], role="save")
                #self.actions = actions
                self.actions.append(action)
        else:
            self.actions = [{'name': None, 'attack': None, 'usable': False}]
       

    def getInternalStuff(self):
        print("internals")
        # internal stuff
        self.tally = {'damage': 0, 'hits': 0, 'dead': 0, 'misses': 0, 'battles': 0, 'rounds': 0, 'hp': 0,
                      'healing_spells': 0}
        self.copy_index = 1
        self.condition = 'normal'
        
        self.dodge = 0
        self.concentrating = 0
        self.temp = 0

    def getBuffSpells(self):
        print("buff spells?")
        self.buff_spells = None
        if 'buff_spells' in self.settings:
            self.buff_spells = int(self.settings['buff_spells'])
            self.conc_fx = getattr(self, self.settings['buff'])
        else:
            self.buff_spells = 0

    def _initialise(self, **settings):
        """`
        Preface.
        Character creation in DnD is rather painful. Here due to missing it is even more complex.
        Also, creature, character and monster are used interchangably here unfortunately, which will be fixed one day.
        The method _set
        This is the order of creation. All attributes are in lowercase regardless of the style on the PHB.
        1. a creature can be based off another, if the `base attribute is set`(str or Creature).
        2. set `name`
        3. set `level` (def 1)
        4. set `xp` (def None)
        5. set `proficiency` (proficiency bonus), 1 + round(self.level / 4) if absent, but will be overidden if hp is not specified as the `set_level` will generate it from HD and level
        6. set ability bonues (`_initialise_abilities` method). To let the user give a base creature and weak a single ability (__e.g.__ `Creature('Commoner',name='mutant commoner', str=20)), the creature has abilities as individual attributes with three letter codes, __e.g.__ `self.str` and as a dictionary (`self.abilities`), while `self.ability_bonuses` has a twin that is the suffix `_bonus` (__e.g.__ `self.str_bonus`).
        7. set `hp`
        8. AC (`self.ac`)
        9. spellcasting (complex, may change in future): `sc_ab` the spellcasting ability as three char str,
        10. `initiative_bonus`
        11. combat stats... attack_parameters=[['rapier', 4, 2, 8]], alt_attack=['net', 4, 0, 0]
        12. set max morale
        13. id. This should be able to be used to single out one combattant of many for the purpose of death/retreat
        name, alignment="good", ac=10, initiative_bonus=None, hp=None, attack_parameters=[['club', 2, 0, 4]],
                 alt_attack=['none', 0],
                 healing_spells=0, healing_dice=4, healing_bonus=None, ability_bonuses=[0, 0, 0, 0, 0, 0], sc_ability='wis',
                 buff='cast_nothing', buff_spells=0, log=None, xp=0, hd=6, level=1, proficiency=2
                 """
        # TB debugging -> getting code path of calls
        print("_initialise")
        # TB settings is ONLY user settings/from app
        self.settings = settings
        # set up for creature ability scores
        self.abilities = {'str': 0, 'dex': 0, 'con': 0, 'int': 0, 'wis': 0, 'cha': 0}
        self.ability_bonuses = {'str': 0, 'dex': 0, 'con': 0, 'int': 0, 'wis': 0, 'cha': 0}
        self.hasAction = True

        #load entry from bestiary -- default values
        if self.settings['base'] == 'cthulhu':
            self.beastiary = self._fill_from_preset('cthulhu')
        else:
            self.beastiary = self.beastiary[self.settings['base']] 
        # TB Need to add check for user input before assigning all default values
        self.vulnerabilities = {} # "type" : severity  0 - immune, .5 - resistant, 1- normal, 2 - vulnerable
        self._set('name', self.beastiary['name'])
        self._set('level', 0, 'int')
        self._set('xp', None, 'int')
        self.id = self.settings['uid'] # value should get overwritten when loaded into combattants list.
        self.actions = [];
        #self.actions = self.beastiary['actions']
        # proficiency. Will be overridden if not hp is provided.
        # self._set('proficiency', 1 + round(self.level / 4))  # TODO check maths on PH
        setattr(self, 'proficiency', int(1 + round(self.level / 4)))
 
        self.getAbilityScores() # new function 
        self.getAbilityModifiers() # new function 
        # self.getHd() #Idon't think that this is used....unless used as a sub for lv, but .base references need to be taken out
        self.getHp()
        self.getAc()
        self.getInitiative()
        self.getSpellCasting()
        self.getattacks()
        self.getVulnerabilities()
        self.getmorale()
        self.getTeam()
        self.getAltAttack()
        self.getInternalStuff()
        self.getBuffSpells()

        print("end of _initialise")
        self.arena = None
        if self.debug == True:
            print(self.log)
        #self.settings = {}

    @staticmethod
    def clean_settings(dirtydex):
        # TB debugging -> getting path of calls
        print("clean_settings")
        """
        Sanify the settings
        :return: a cleaned dictionary
        """
        ability_names=['str', 'dex', 'con', 'wis', 'int', 'cha']
        #lowercase
        lowerdex = {k.lower(): dirtydex[k] for k in dirtydex}

        #sort issue with abilities
        cleandex = {'abilities':{}, 'ability_bonuses': {}}
        ##dicts present
        for grouping in ['abilities','ability_bonuses']:
            if grouping in lowerdex:
                if type(lowerdex[grouping]) is dict:
                    cleandex[grouping] = lowerdex[grouping]
                elif type(lowerdex[grouping]) is list and len(lowerdex[grouping]) == 6:
                    cleandex[grouping] = {ability_names[i]: lowerdex[grouping][i] for i in range(0,6)}
                else:
                    raise TypeError("Cannot parse "+grouping)
        # individual abilities overwrite
        #print("debug... ",cleandex['ability_bonuses'])
        for k in lowerdex:
            if k[0:3] in ability_names:
                cleandex['abilities'][k[0:3]] = int(lowerdex[k])
                if 'ab_'+k not in lowerdex:
                    cleandex['abilities'][k[0:3]] = math.floor(int(lowerdex[k])/2-5)
            elif k in ['ab_str', 'ab_dex', 'ab_con', 'ab_wis', 'ab_int', 'ab_cha']:
                cleandex['ability_bonuses'][k[3:6]] = int(lowerdex[k])
                if k[3:6] not in lowerdex:
                    cleandex['abilities'][k[3:6]] = int(lowerdex[k])*2+10
            elif k in ['abilities','ability_bonuses']:
                pass
            else:
                cleandex[k] = lowerdex[k]
        return cleandex

    def _set(self, item, alt=None, expected_type='string'):
        """
        Method to set the attribute named item based on that in self.settings if present, if not it uses alt value.
        :param item: the name of the self.settings key and attribute of self to set.
        :param alt: default value
        :param expected_type: "string" or "int" for now. Can be easily changed for other types.
        :return: None.
        """
        if item in self.settings:
            if expected_type == 'string':
                setattr(self, item, self.settings[item])
            elif expected_type == 'int':
                setattr(self, item, int(self.settings[item]))
        elif expected_type == 'string':
            #setattr(self, item, alt)
            setattr(self, item, self.beastiary[item])
        else:
            setattr(self, item, int(self.beastiary[item]))

    def _initialise_abilities(self):
        """
        Rewritten so that cleaning module does the cleaning.
        :return: None.
        """
        self.able = 1  # has abilities. if nothing at all is provided it goes to zero. This is for rocks...
        # set blanks
        print("loading ability scores")
        self.ability_bonuses = {n: 0 for n in self.ability_names} #default for no given ability score is 10 (bonus = 0) as per manual.
        self.abilities = {n: 10 for n in self.ability_names}
        for ability in self.settings['abilities']:
            if ability in self.settings['ability_bonuses']:
                if 10+self.settings['ability_bonuses'][ability]*2 != self.settings['abilities'][ability] and 10+self.settings['ability_bonuses'][ability]*2 +1 != self.settings['abilities'][ability]:
                    warnings.warn('Mismatch: both ability score and bonus provided, ' \
                    'but they differ ({0}: 10+{1}*2 vs. {2})'.format(ability,self.settings['ability_bonuses'][ability], self.settings['abilities'][ability]))
            self.abilities[ability] = int(self.settings['abilities'][ability])
            self.ability_bonuses[ability] = math.floor(int(self.settings['abilities'][ability])/2-5)
        print("calculating ability modifiers")
        for ability in self.settings['ability_bonuses']:
            self.ability_bonuses[ability] = self.settings['ability_bonuses'][ability]
            self.abilities[ability] = 10 + 2 * self.ability_bonuses[ability] #I know it means nothing, but I am unsure why this was absent.

    def _fill_from_dict(self, dictionary):
        return self._initialise(**dictionary)

    def _fill_from_beastiary(self, name):
        # Is this being used??
        if name in self.beastiary:
            return self._initialise(**self.beastiary[name])
        else:
            ###For now fallback to preset. In future preset will be removed?
            return self._fill_from_preset(name)

    def _fill_from_preset(self, name):
        """
        Legacy... It might stop working due to code changes.
        :param name: the name of creature.
        :return: the stored creature.
        """
        if name == "cthulhu":  #TB new stats from https://dmdave.com/cthulhu/
            return {"name":"Cthulhu", 
                            "alignment":"beyond", 
                            "base" :"cthulhu",
                            "ac":25, "hp":5000, "xp":465000,
                            "initiative_bonus":15,
                            "attack_parameters":[
                                ["2 claws", 19, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10], 
                                ["tentacle",  19, 10, 10, 10, 10, 10, 10], 
                                ["tentacle",  19, 10, 10, 10, 10, 10, 10],
                                ["tentacle",  19, 10, 10, 10, 10, 10, 10], 
                                ["tentacle",  19, 10, 10, 10, 10, 10, 10]
                                ],
                            "alt_attack":['none', 0],
                            "healing_spells":99999, "healing_dice":20, "healing_bonus":30,
                            "cha": 29, "con": 30, "dex": 12, "int": 30, "str": 30, "wis": 27,
                            "ability_bonuses":{'cha': 9, 'con': 10, 'dex': 1, 'int': 10, 'str': 10, 'wis': 8}, "sc_ability":'int',
                            "buff":'cast_nothing', "buff_spells":0, "log":None, "hd":20, "level":99, "cr":99, "proficiency":19,
                            "br":99.0} #TB DM Dave says that Cthulhu is like fighting 3 CR 30 creatures. Need to do the math on what this translates to.
        
        # TB Original
        #{"name":"Cthulhu", "alignment":"beyond", "base" :"cthulhu",
        #                     "ac":49, "hp":774, "xp":9830400,
        #                     "initiative_bonus":15,
        #                     "attack_parameters":[['2 claws', 42, 23, 6, 6, 6, 6], ['4 tentacles', 42, 34, 10, 10]],
        #                     "alt_attack":['none', 0],
        #                     "healing_spells":99999, "healing_dice":1, "healing_bonus":30,
        #                     "ability_bonuses":[56, 21, 45, 31, 36, 34], "sc_ability":'wis',
        #                     "buff":'cast_nothing', "buff_spells":0, "log":None, "hd":8, "level":36, "proficiency":27,
        #                     "br":99.0}


        else:
             # TB this commoner is causing problems. attack parameters do not get overridden
            self._initialise(name="Default", alignment="evil",
                             ac=10, hp=4,
                             attack_parameters=[['club', 2, 0, 4]])

    def set_level(self, level=None):
        """
        Alter the level of the creature.
        :param level: opt. int, the level. if absent it will set it to the stored level.
        :return: nothing. changes self.
        """
        if not level:
            level = self.level
        old_level = self.level
        if not self.hd:
                warnings.warn('No hit dice specified, setting to d8')
        if not old_level: #zero???
            self.hp = 0
            self.hd.crit = 1  # Not-RAW first level is always max for PCs, but not monsters.
            for x in range(level):
                self.hp += self.hd.roll()
        else:
            for x in range(level-old_level):
                self.hp += self.hd.roll()
        self.level = level
        self.starting_hp = self.hp
        self.proficiency = 1 + round((level) / 4)
        if hasattr(self, 'attacks'):
            for attack in self.attacks:
                attack['attack'].bonus += self.proficiency - 1 + round((old_level) / 4)
                #Changing by delta proficiency as there is no way of knowing what weapon bonuses there may be etc.

    def change_attribute(self,**abilities):
        """
        Setting an ability attribute directly does not result in a recalculation.
        For example:
        >>> slashr = Creature('troll')
        >>> slashr.abilities['cha'] = 16
        This will not change the stats dependent on that ability.
        This method attempts to change the dependent abilities.
        A late addition, so the code does not make use of it.
        :param attributes: key value pair
        :return: None
        """

        for attr in abilities:
            attr = attr[0:3].lower() #just in case
            if attr in self.abilities:
                old_attr=self.abilities[attr]
                self.abilities[attr]=int(abilities[attr])
                delta=math.floor(self.abilities[attr]/2-5)-math.floor(old_attr/2-5)
                old_bonus=self.ability_bonuses[attr]
                self.ability_bonuses[attr] +=delta #it might differ for some reason...
                #con does not change
                if attr == "str":
                    pass
                elif attr == "dex":
                    pass
                elif attr == "con":
                    pass
                elif attr == "int":
                    pass
                elif attr == "wis":
                    pass
                elif attr == "cha":
                    pass
            else:
                raise ValueError('Unrecognised ability')

    def _attack_parse(self, attack_parameters):
        """
        `self.attacks` has a list of attacks. Each attack is a dictionary of `name` string, `attack` Dice and `damage` Dice.
        Dice holds the dice(s) and the bonuses and other properties.
        :param attack_parameters: A not-parsed set of attacks: a list of a list of attack bonus int, damage bonus int and damage dice size int/list
        :return: None (changes self.attacks)
        """
        if type(attack_parameters) is str:
            import json
            attack_parameters = json.loads(attack_parameters)
        self.attacks = []
        if attack_parameters != []:
            for monoattack in attack_parameters:
                #att = {'name': monoattack[0]}
                if "type" not in monoattack : monoattack['type'] = self.damageLookup(monoattack["name"]) #checking for damage type
                monoattack['damage'] = DnD.Dice(monoattack['damage_modifier'], monoattack['damage'], role="damage")
                monoattack['attack'] = DnD.Dice(monoattack['attack'], 20, role="attack", twinned=monoattack['damage'])
                if "secondary_damage" in monoattack:
                    monoattack['secondary_damage'] = DnD.Dice(0, monoattack['secondary_damage'], role="damage") #do any secondary damage types have modifiers? (they have saves sometimes
                self.attacks.append(monoattack)
            for x in self.attacks:
                self.hurtful += x['damage'].bonus
                self.hurtful += (sum(x['damage'].dice) + len(
                    x['damage'].dice)) / 2  # the average roll of a d6 is not 3 but 3.5

    def damageLookup(self, attack):
        #should include variant spellings. ie crossbow and cross bow
        if attack in ['tentacle', 'tentacles', 'hoof', 'hooves', 'tail', 'tails', 'club', 'greatclub', 'slam', 'maul', 'mace', 'light hammer', 'quarterstaff', 'sling', 'flail', 'warhammer' ] : return 'bludgeoning'
        elif attack in ['claw', 'claws', 'hand axe', 'bastard sword', 'sickle', 'battle axe', 'glaive', 'great axe', 'great sword', 'long sword', 'scimitar', 'whip' ] : return 'slashing'
        elif attack in ['dagger', 'bite', 'bites', 'javelin', 'spear', 'crossbow', 'dart', 'short bow', 'lance', 'morningstar', 'pike', 'rapier', 'short sword', 'trident', 'war pick', 'blowgun', 'hand crossbow', 'heavy crossbow', 'longbow'] : return 'piercing'
        else: return 'none'
        
    def __str__(self):
        if self.tally['battles']:
            battles = self.tally['battles']
            return self.name + self.id + ": {team=" + self.team + "; avg hp=" + str(
                self.tally['hp'] / battles) + " (from " + str(
                self.starting_hp) + "); avg healing spells left=" + str(
                self.tally['healing_spells'] / battles) + " (from " + str(
                self.starting_healing_spells) + "); damage done (per battle average)= " + str(
                self.tally['damage'] / battles) + "; hits/misses (PBA)= " + str(
                self.tally['hits'] / battles) + "/" + str(
                self.tally['misses'] / battles) + "; rounds (PBA)=" + str(
                self.tally['rounds'] / battles) + ";}"
        else:
            return self.name + self.id + ": UNTESTED IN BATTLE"

    def isalive(self):
        if self.hp > 0: return 1

    def updateMorale(self, points, verbose=1):
        # Morale Check for bloodied
        if self.hp < self.starting_hp/2: 
            self.current_morale -= 1 # this will cause it to lose morale EVERY TURN while it's bloodied,

        if points >= 10: self.current_morale -= 1 # pseudo critical hit
        if verbose: verbose.append(self.name + self.id + ' is at ' + str(self.current_morale) + ' morale.')

        # if morale gets to be 0 or less, remove from combatants list (run away), else check if concentrating.
        if self.current_morale < 1 and self.hp > 0: 
            if verbose: verbose.append(self.name + self.id + ' lost its desire to fight and ran away from battle')
            self.hp = 0 #psuedo death (running away)

    def take_damage(self, points, verbose=1, type="", magical=False):
        if 'damage' in self.arena.options:
            if type in self.vulnerabilities:
                points = math.floor(points * self.vulnerabilities[type])
        if points < 0: points = 0 #negative damage will heal, we don't want this.
        self.hp -= points
        if verbose: 
            #verbose.append(self.name + str(self.id) + ' took ' + str(points) + ' damage. Now on ' + str(self.hp) + ' hp.') # This Verbose.append causes an error somehow
            print(self.name + str(self.id) + ' took ' + str(points) + ' of ' + type + ' damage. Now on ' + str(self.hp) + ' hp.')
        if "morale" in self.arena.options:
            self.updateMorale(points, verbose)

        if self.hp <= 0: '{} {} dies'.format(self.name, str(self.id))
        # can be new method
        if self.concentrating:
            dc = points / 2
            if dc < 10: dc = 10
            if DnD.Dice(self.ability_bonuses[self.sc_ab]).roll() < dc:
                self.conc_fx()
                if verbose: verbose.append(self.name + str(self.id) + ' has lost their concentration')

    def ready(self):
        self.dodge = 0
        # there should be a few more.
        # conditions.

    def reset(self, hard = False):
        """
        Resets the creature back to health (a long rest). a hard reset resets its scores
        :param hard: bool, false keeps tallies
        :return: None
        """
        self.hp = self.starting_hp
        self.current_morale = self.max_morale
        for x in self.actions:
            if 'recharge' in x:
                x['usable'] = True
        if self.concentrating:
            self.conc_fx() #TODO this looks fishy
        self.healing_spells = self.starting_healing_spells
        if hard:
            self.tally={'damage': 0,'hp': 0, 'hits': 0,'misses': 0,'rounds': 0,'healing_spells': 0,'battles': 0,'dead':0}

    def check_advantage(self, opponent):
        adv = 0
        if opponent.dodge:
            adv += -1
        if (opponent.condition == 'netted') or (opponent.condition == 'restrained'):
            adv += 1
        # Per coding it is impossible that a netted creature attempts an attack.
        if (self.condition == 'netted') or (self.condition == 'restrained'):
            adv += -1
        return adv

    def net(self, opponent, verbose=0):
        self.alt_attack['attack'].advantage = self.check_advantage(opponent)
        if self.alt_attack['attack'].roll(verbose) >= opponent.ac:
            opponent.condition = 'netted'
            self.tally['hits'] += 1
            if verbose: verbose.append(self.name + " netted " + opponent.name)
        else:
            self.tally['misses'] += 1

    def cast_barkskin(self):
        if self.concentrating == 0:
            self.temp = self.ac
            self.ac = 16
            self.concentrating = 1
        elif self.concentrating == 1:
            self.ac = self.temp
            self.concentrating = 0

    def cast_nothing(self, state='activate'):  # Something isn't quite right if this is invoked.
        pass

    def heal(self, points, verbose=1):
        self.hp += points
        if verbose: verbose.append(self.name + self.id + ' was healed by ' + str(points) + '. Now on ' + str(self.hp) + ' hp.')

        if 'morale' in self.arena.options:
            self.current_morale +=  1
            if verbose: verbose.append(self.name + self.id + ' got a morale boost from getting healed and is now at ' + str(self.current_morale) + ' morale.')

    def assess_wounded(self, verbose=0):
        targets = self.arena.find('bloodiest allies')
        if len(targets) > 0:
            weakling = targets[0]
            if weakling.starting_hp > (self.healing.dice[0] + self.healing.bonus + weakling.hp):
                if verbose: verbose.append(self.name + self.id + " wants to heal " + weakling.name + weakling.id)
                return weakling
            else:
                return 0
        else:
            raise NameError('A dead man wants to heal folk')

    def cast_healing(self, weakling, verbose=0):
        if self.healing_spells > 0:
            weakling.heal(self.healing.roll(), verbose)
            # self.healing_spells -= 1

    def multiattack(self, verbose=1, assess=0):
        if assess:
            return 0  # the default
        for i in range(len(self.attacks)):
            try:
                opponent = self.arena.find(TARGET, self)[0]
            except IndexError:
                raise self.arena.Victory()
            s = '{} {} attacks {} {} with {}{}'.format(self.name, self.id, opponent.name, opponent.id, self.attacks[i]['name'], str(i))
            if verbose:
                verbose.append(self.name + self.id + ' attacks ' + opponent.name + ' with ' + str(self.attacks[i]['name']))
            print(s)
            # This was the hit method. put here for now.
            self.attacks[i]['attack'].advantage = self.check_advantage(opponent)
            attackRoll = self.attacks[i]['attack'].roll(verbose)
            if attackRoll == 999 and 'morale' in self.arena.options:
                opponent.current_morale-=1
                print("CRITICAL HIT! " + opponent.name + " loses some morale")
            if attackRoll >= opponent.ac:
                # self.attacks[i]['damage'].crit = self.attacks[i]['attack'].crit  #Pass the crit if present.
                h = self.attacks[i]['damage'].roll(verbose)
                if self.attacks[i]['damage_modifier']:
                   h += self.attacks[i]['damage_modifier'] 
                print("damage done is " + str(h))
                opponent.take_damage(h, verbose, type = self.attacks[i]['type'], magical = "isMagical" in self.attacks[i] )
                if 'secondary_type' in self.attacks[i]:
                    opponent.take_damage(self.attacks[i]['secondary_damage'].roll(), verbose, type = self.attacks[i]['secondary_type'], magical = self.attacks[i]["isMagical"] )
                self.tally['damage'] += h
                self.tally['hits'] += 1
                # check to see if the opponent survived the last hit, if not, win
                if opponent.hp < 1:
                    print(opponent.name + " " + str(opponent.id) + " dies")
            else:
                self.tally['misses'] += 1
                print('and misses')

    # TODO
    def check_action(self, action, verbose):
        return getattr(self, action)(assess=1)

    # TODO
    def do_action(self, action, verbose):
        # do it.
        pass

    # TODO
    def TBA_act(self, verbose=0):
        if not self.arena.find('alive enemy'):
            raise DnD.Encounter.Victory()
        x = {'nothing': 'cast_nothing'}
        choice = [self.check_action(x) for x in self.actions]
        best = sorted(choice.keys(), key=choice.get)[0]
        self.do_action(best)

    def act(self, verbose=0):
        if not self.arena.find('alive enemy'):
            raise DnD.Encounter.Victory()
        # BONUS ACTION
        # heal  -healing word, a bonus action. #TB nobody has healing except the big guy and custom combatants
        if self.healing_spells > 0:
            weakling = self.assess_wounded(verbose)
            if weakling != 0:
                self.cast_healing(weakling, verbose)
        # Main action!
        economy = len(self.arena.find('allies')) > len(self.arena.find('opponents')) > 0
        ## Buff?
        if 'restrained' in self.condition:
            # try to get out of being restrained
            if verbose:
                verbose.append(self.name + self.id + " freed himself from a net")
                self.condition = 'normal'
        elif self.buff_spells > 0 and self.concentrating == 0:
            self.conc_fx()
            if verbose: verbose.append(self.name + self.id + ' buffs up!')
            # greater action economy: waste opponent's turn.
        elif economy and self is self.arena.find('weakest allies')[0]:# If it is the weakest, then dodge??
            if verbose:
                verbose.append(self.name + self.id + " is dodging")
            print(self.name + " " + self.id + " is dodging")
            self.dodge = 1
        # special abilities
        # bloodied
        elif self.hp <= self.starting_hp / 2 or economy == True:
            if self.actions[0]['name'] != None:
                for action in self.actions:# Try to recharge ability
                    if 'recharge' in action and action['usable'] == False:
                        if action['recharge'].roll() >= action['recharge_threshold']:
                            action['usable'] = True
                            print(action['name'] + " is recharged!")
                        else:
                            print(action['name'] + " is not recharged")
                    #if 'healing' in self.actions[0]['role'] and self.actions[0]['usable']:
                    if action['role'] == 'damage' and action['usable'] == True:
                        if self.hasAction == False: break #don't allow actions if it's not available
                        print("we're going to use " + action['name'])
                        self.checkDamageAction(action)
                if self.hasAction:
                    self.multiattack(verbose)
                    self.hasAction == False
                self.hasAction = True #the reset for next round. Each action check method will have to mark the action when one is executed.
            else : 
                self.multiattack(verbose)
        elif len(self.arena.find('allies')) < len(self.arena.find('opponents')):
            if economy and 'role' in self.actions:
                #if it has special abilities, use them.
                determineAction(self.actions)
            else:
                self.multiattack(verbose)
        else:
            self.multiattack(verbose)

    def determineAction(self, actions): #deprecating
        for action in actions:
            if action['role'] == 'healing':
                # TODO healing actions first
                print("TODO")
            elif action['role'] == 'damage':
                # TODO damage
                print("TODO")
            elif action['role'] == 'support':
                # TODO support
                print("TODO")
            else:
                self.multiattack(verbose)

    def checkHealingAction(self, action):
        if action['role'] == 'healing':
            # TODO healing/support actions first?
            self.arena.find('weakest allies')[0]
            # and heal them
            print("TODO")

    def checkDamageAction(self, action):
        if action['name'] == 'breath weapon': # we may not need this if statement
            targets = []
            num_targets = action['num_targets'].roll()
            total_enemies = len(self.arena.find('alive enemy'))
            # get enemy/ies, check save, roll damage, check immunity/vulnerable, apply damage, roll for ability recharge
            if num_targets > total_enemies: num_targets = total_enemies
            for x in range (num_targets):
                targets.append(self.arena.find(TARGET, self)[x]) #select a group of enemies
            # loop through targets and check saves
            damage = 0
            for target in targets: # check save (ability_bonus + D20
                if DnD.Dice(target.ability_bonuses['dex'], 20, role="save").roll() <= action['dc']:
                    # roll damage
                    damage = action['damage'].roll()
                    print("Watch out for full damage!")
                    print(str(damage) + " points of damage!")
                else:
                    # roll save damage
                    print("taking 1/2 damage")
                    damage = math.floor(action['damage'].roll()/2) # TB testing to see if I can handle saves this way
                #apply damage to target
                target.take_damage(damage, type = action['type'])
                action['usable'] = False
        elif action['name'] == 'multiattack':
            # get target
            # to hit
            # damage
            # or can I use existing functions?
            print("checkDamageAction else block")
                
    def checkSupportAction():
        if action['role'] == 'support':
            # TODO support
            print("TODO")

    def toFile(s):
        """
        utility function to help with manipulating/rewriting mass data.
        I still need to add headers manually when using this function
        """
        fileName = "newfile.csv" #something relevant to the current use.
        f = open("DnDRoyale/" + fileName, "a")
        f.write(s)
        f.close()

    # I dont' think I'll ever use this function
    def generate_character_sheet(self):
        """
        An markdown character sheet.
        :return: a string
        """
        def writeline(field,value,secvalue=None):
            #returns _field_: value (secvalue)
            #secvalues is if has a secondary value to be added in brachets
            if not secvalue:
                return '_'+str(field).replace("_"," ")+'_: '+str(value)+'  \n'
            else:
                return '_'+str(field).replace("_"," ")+'_: '+str(value)+' ('+str(secvalue)+')  \n'
        sheet = '# '+self.name.upper()+'\n'
        sheet +=  writeline('Name',self.name)
        sheet +=  writeline('Alignment',self.alignment)
        if self.cr:
            level = self.cr
            lname = 'CR'
        else:
            level = self.level
            lname = 'Level'
        if self.hd:
            sheet +=  writeline(lname+' (hit dice)',level,self.hd)
        else:
            sheet +=  writeline(lname,level)
        if self.xp:
            sheet += writeline('XP',self.xp)
        sheet += '## Abilities\n'
        for ab in self.ability_names:
            sheet +=  writeline(ab,self.abilities[ab],self.ability_bonuses[ab])
        sheet += '## Combat\n'
        sheet +=  writeline('Hit points (hp total)',self.hp,self.starting_hp)
        sheet +=  writeline('Condition',self.condition)
        sheet +=  writeline('Initiative',self.initiative)
        sheet +=  writeline('Proficiency',self.proficiency)
        sheet +=  writeline('Armour class',self.ac)
        sheet += '### Attacks\n'
        sheet +=  writeline('Potential average damage per turn',self.hurtful)
        for d in self.attacks:
                sheet += "* "+ writeline(d['name'],d['attack'],d['damage'])
        sheet += '### Raw data\n'
        sheet+=str(self.__dict__).replace('<br/>','\n')
        return sheet