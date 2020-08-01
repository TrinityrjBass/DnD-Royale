#This may be the removed creature class, but I'm going to add it back to DnD.py for now to get things working.


import warnings
import math
from DnDRoyale import DnD

TARGET = 'enemy alive weakest'
N = "<br/>"

class Creature:
    """
    Creature class handles the creatures and their actions and some interactions with the encounter.
    """

    @staticmethod
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
        try:
            import csv
            r = csv.reader(open(path, encoding='utf-8'))
            headers = next(r)
            beastiary = {}
            for line in r:
                beast = {h: line[i] for i, h in enumerate(headers) if line[i]}
                if 'name' in beast:
                    beastiary[beast['name']] = beast
            return beastiary
        except Exception as e:
            warnings.warn('Beastiary error, expected path ' + path + ' error ' + str(e))
            return {}

    beastiary = load_beastiary.__func__('beastiary.csv')
    ability_names = ['str', 'dex', 'con', 'wis', 'int', 'cha']

    def __init__(self, wildcard, **kwargs):  # I removed *args... not sure what they did.
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
        if not kwargs and type(wildcard) is str:
            self._fill_from_beastiary(wildcard)
        elif type(wildcard) is dict:
             self._initialise(**wildcard) # new attempt
            # self._fill_from_dict(wildcard) # OG
            #if not kwargs == {}: # seeing if commenting this out actually messes anything up
            #    print("dictionary passed followed by unpacked dictionary error")
        elif kwargs and type(wildcard) is str:
            if wildcard in self.beastiary:
                self._initialise(base=wildcard, **kwargs)
            else:
                self._initialise(name=wildcard, **kwargs)
        elif type(wildcard) is Creature:
            self._initialise(base=wildcard, **kwargs)
        else:
            warnings.warn("UNKNOWN COMBATTANT:" + str(wildcard))
            print("UNKNOWN COMBATTANT:" + str(wildcard))
            # raise Exception
            print("I will not raise an error. I will raise Cthulhu to punish this user errors")
            self._fill_from_preset("cthulhu")

    def getattacks(self):
        print("loading attack information")
        self.attacks = []
        self.hurtful = 0
        if not 'attack_parameters' in self.settings:
            # Benefit of doubt. Given 'em a dagger . <-- but if you give them a dagger... then they will never use their fist (listed below)
            self.settings['attack_parameters'] = 'punch' # give them fisticuffs!
        if type(self.settings['attack_parameters']) is str:
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
                        self.log += "Weapon matched by str to " + w + N
                        break
                else:
                    raise Exception("Cannot figure out what is: " + self.settings['attack_parameters'] + str(
                        type(self.settings['attack_parameters'])))
        elif type(self.settings['attack_parameters']) is list:
            self.attack_parameters = self.settings['attack_parameters']
            self._attack_parse(self.attack_parameters)
        else:
            raise Exception('Could not determine weapon')

    def getmorale(self):
        if 'cr' in self.settings: 
            self.cr = self.settings['cr']
        elif 'level' in self.settings:
            # TODO check maths on MM.
            if int(self.settings['level']) > 1:
                self.cr = int(self.settings['level']) - 1
            else:
                self.cr = 0.5
        else:
            self.settings['cr'] = 1 # Use 1 as a default value if none is given
            # self.cr = 1
        # Check/set Morale
        #this is where the value is validated or found and assigned max_morale
        # BREAK OUT INTO OWN METHOD
        # could do cr and br assignments in one block. If there is no Cr, there's not going to be a Br
        if 'br' in self.settings:
            self.max_morale = int(self.settings['br'])
            self.current_morale = int(self.settings['br'])
        else : 
            self.settings['max_morale'] = 0
            self.max_morale = 0
            self.current_morale = 0
            
        print("getting Morale value")
        # IF creature is not in Beasiary or if Custom Combatant is given, find proper morale value
        if self.max_morale =='' or int(self.max_morale) == 0:
            morale = 0
            # if morale is 0 or null, then check the CR and figure BR from that (do I need a fallback option?)
            _cr = float(self.settings['cr'])
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
            # self.settings['max_morale'] = morale 
            # self.settings['current_morale'] = morale 
            self.current_morale = morale
            self.max_morale = morale

    def getHp(self):
        print("getting HP value")
        if 'hp' in self.settings.keys():
            self.hp = int(self.settings['hp'])
            self.starting_hp = self.hp
        elif self.settings['level']:
            self.set_level()
        else:
            raise Exception('Cannot make character without hp or hd + level provided')
        
        print("getting ac, initiative, spell ability bonus...")
        # AC
        if not 'ac' in self.settings.keys():
            self.settings['ac'] = 10 + self.ability_bonuses['dex']
        self.ac = int(self.settings['ac'])
        
        # init
        if not 'initiative_bonus' in self.settings:
            self.settings['initiative_bonus'] = self.ability_bonuses['dex']
        self.initiative = DnD.Dice(int(self.settings['initiative_bonus']), 20, role="initiative")
        
        ##spell casting ability_bonuses
        if 'sc_ability' in self.settings:
            self.sc_ab = self.settings['sc_ability'].lower()
        elif 'healing_spells' in self.settings or 'buff_spells' in self.settings:
            self.sc_ab = max('wis', 'int', 'cha',
                             key=lambda ab: self.ability_bonuses[ab])  # Going for highest. seriously?!
            print(
                "Please specify spellcasting ability of " + self.name + " next time, this time " + self.sc_ab + " was used as it was biggest.")
        else:
            self.sc_ab = 'con'  # TODO fix this botch up.
        if not 'healing_bonus' in self.settings:
            self.settings['healing_bonus'] = self.ability_bonuses[self.sc_ab]
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

    def getHd(self):
        self.hd = None
        if 'hd' in self.settings.keys():
            if type(self.settings['hd']) is DnD.Dice:
                self.hd = self.settings['hd']  # we're dealing with a copy of a beastiary obj.
            else:
                self.hd = DnD.Dice(self.ability_bonuses['con'], int(self.settings['hd']), avg=True, role="hd")
        elif 'size' in self.settings.keys():
            size_cat = {"small": 6, "medium": 8, "large": 10, "huge": 12}
            if self.settings['size'] in size_cat.keys():
                self.hd = DnD.Dice(self.ability_bonuses['con'], size_cat[self.settings['size']], avg=True, role="hd")
        elif 'hp' in self.settings and 'level' in self.settings:
            #Guess based on hp and level. It is not that dodgy really as the manual does not use odd dice.
            # hp =approx. 0.5 HD * (level-1) + HD + con * level
            # HD * (0.5* (level-1)+1) = hp - con*level
            # HD = (hp - con*level)/(level+1)
            bestchoice=(int(self.settings['hp'])-int(self.ability_bonuses['con']) * int(self.settings['level']))/((int(self.settings['level'])+1))
            print(int(self.settings['hp']),int(self.ability_bonuses['con']), int(self.settings['level']))
            print("choice HD...",bestchoice)
            #print("diagnosis...",self.ability_bonuses)
            warnings.warn('Unfinished case to guess HD. so Defaulting hit dice to d8 instead') #TODO finish
            self.hd = DnD.Dice(self.ability_bonuses['con'], 8, avg=True, role="hd")
        else:
            #defaulting to d8
            warnings.warn('Insufficient info: defaulting hit dice to d8')
            self.hd = DnD.Dice(self.ability_bonuses['con'], 8, avg=True, role="hd")

    def getAltAttack(self):
        if 'alt_attack' in self.settings and type(self.settings['alt_attack']) is list:
            self.alt_attack = {'name': self.settings['alt_attack'][0],
                               'attack': DnD.Dice(self.settings['alt_attack'][1], 20)}  # CURRENTLY ONLY NETTING IS OPTION!
        else:
            self.alt_attack = {'name': None, 'attack': None}
        # last but not least
        print("Assessing alignment")

    def getAlignment(self):
        if 'alignment' not in self.settings:
            self.settings['alignment'] = "unassigned mercenaries" 
        self.alignment = self.settings['alignment']
        # internal stuff
        self.tally = {'damage': 0, 'hits': 0, 'dead': 0, 'misses': 0, 'battles': 0, 'rounds': 0, 'hp': 0,
                      'healing_spells': 0}
        self.copy_index = 1
        self.condition = 'normal'
        
        self.dodge = 0
        self.concentrating = 0
        self.temp = 0

    def getBuffSpells(self):
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
                 #This method does : 
                 #    checks if there are settings,
                #if there are, call 'clean_settings' (sanify == to make healthy)
                #else use 'commoner' as a base

                # Should look into filling all fields that are given in a custom creature before checking the base creature and filling in the remaining fields
                # But how do you determine a custom creature? I think a custom creature is going to be a dict. but a MM creature will be a string???? 
                # so the check could be if it's a dic or string. if it's string, then fill from MM, if it's a dic, fill given fields, if no base is given, fill from commoner or try to figure it out? <- new functionality
        if settings:
            self.settings = Creature.clean_settings(settings)
        else:
            self._fill_from_preset('commoner')  # or Cthulhu?
            print("EMPTY CREATURE GIVEN. SETTING TO COMMONER")
            return 0

        # Mod of preexisting
        if 'base' in self.settings:
            #Sanify first and make victim
            if type(self.settings['base']) is str:
                victim = Creature(
                    self.settings['base'])  # generate a preset and get its attributes. Seems a bit wasteful.
            elif type(self.settings['base']) is Creature:
                victim = self.settings['base']
            else:
                raise TypeError
            #copy all
            #victim.ability_bonuses #in case the user provided with ability scores, which are overridden by adbility bonues
            base = {x: getattr(victim, x) for x in dir(victim) if getattr(victim, x) and x.find("__") == -1 and x.find("_") != 0 and x != 'beastiary'}
            base['ability_bonuses']={}
            #base.update(**self.settings)
            for (k,v) in self.settings.items():
                if type(v) is dict:
                    base[k].update(v)
                else:
                    base[k] = v
            self.settings = base

        # Name etc.
        self._set('name', 'nameless')
        self._set('level', 0, 'int')
        self._set('xp', None, 'int')
        self.id = 0 # should get overwritten when loaded into combattants list.

        # proficiency. Will be overridden if not hp is provided.
        self._set('proficiency', 1 + round(self.level / 4))  # TODO check maths on PH

        # set abilities
        self._initialise_abilities()
        # self.getHd() #Idon't think that this is used...or needed yet
        self.getHp()
        self.getattacks()
        self.getmorale()
        self.getAltAttack()
        self.getAlignment()
        self.getBuffSpells()

        ##backdoor and overider
        self._set('custom', [])
        for other in self.custom:
            if other == "conc_fx":
                getattr(self, self.settings['conc_fx'])
            else:
                self._set(other)

        self.arena = None
        self.settings = {}

    @staticmethod
    def clean_settings(dirtydex):
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
        #print("debug... ",cleandex['ability_bonuses'])
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
        else:
            setattr(self, item, alt)

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
        for ability in self.settings['abilities']: #a dictionary within a dictionary
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
        if name == "netsharpshooter":
            self._initialise(name="netsharpshooter",
                             alignment="good",
                             hp=18, ac=18, hd = 8,
                             initiative_bonus=2,
                             healing_spells=6, healing_bonus=3, healing_dice=4, sc_ability="cha",
                             attack_parameters=[['rapier', 4, 2, 8]], alt_attack=['net', 4, 0, 0], level=3)
        elif name == "bard":
            self._initialise(name="Bard", alignment="good",
                             hp=18, ac=18,
                             healing_spells=6, healing_bonus=3, healing_dice=4,
                             initiative_bonus=2,
                             attack_parameters=[['rapier', 4, 2, 8]], level=3)

        elif name == "generic_tank":
            self._initialise(name="generic tank", alignment="good",
                             hp=20, ac=17,
                             initiative_bonus=2,
                             attack_parameters=[['great sword', 5, 3, 6, 6]], level=3)

        elif name == "mega_tank":
            self._initialise(name="mega tank", alignment="good",
                             hp=24, ac=17,
                             initiative_bonus=2,
                             attack_parameters=[['great sword', 5, 3, 10]], level=3)

        elif name == "a_b_dragon":
            self._initialise(name="Adult black dragon (minus frightful)", alignment="evil",
                             ac=19, hp=195, initiative_bonus=2,
                             attack_parameters=[['1', 11, 6, 10, 10], ['2', 11, 6, 6, 6], ['2', 11, 4, 6, 6]])

        elif name == "y_b_dragon":
            self._initialise(name="Young black dragon", alignment="evil",
                             ac=18, hp=127,
                             initiative_bonus=2,
                             attack_parameters=[['1', 7, 4, 10, 10, 8], ['2', 7, 4, 6, 6], ['2', 7, 4, 6, 6]])

        elif name == "frost_giant":
            self._initialise(name="Frost Giant", alignment="evil",
                             ac=15, hp=138,
                             attack_parameters=[['club', 9, 6, 12, 12, 12], ['club', 9, 6, 12, 12, 12]])

        elif name == "hill_giant":
            self._initialise(name="Hill Giant", alignment="evil",
                             ac=13, hp=105,
                             attack_parameters=[['club', 8, 5, 8, 8, 8], ['club', 8, 5, 8, 8, 8]])

        elif name == "goblin":
            self._initialise(name="Goblin", alignment="evil",
                             ac=15, hp=7,
                             initiative_bonus=2,
                             attack_parameters=[['sword', 4, 2, 6]])

        elif name == "hero":
            self._initialise(name="hero", alignment="good",
                             ac=16, hp=18,  # bog standard shielded leather-clad level 3.
                             attack_parameters=[['longsword', 4, 2, 8]])

        elif name == "antijoe":
            self._initialise(name="antiJoe", alignment="evil",
                             ac=17, hp=103,  # bog standard leather-clad level 3.
                             attack_parameters=[['shortsword', 2, 2, 6]])

        elif name == "joe":
            self._initialise(name="Joe", alignment="good",
                             ac=17, hp=103,  # bog standard leather-clad level 3.
                             attack_parameters=[['shortsword', 2, 2, 6]])

        elif name == "bob":
            self._initialise(name="Bob", alignment="mad",
                             ac=10, hp=8,
                             attack_parameters=[['club', 2, 0, 4], ['club', 2, 0, 4]])

        elif name == "allo":
            self._initialise(name="Allosaurus", alignment="evil",
                             ac=13, hp=51,
                             attack_parameters=[['claw', 6, 4, 8], ['bite', 6, 4, 10, 10]])

        elif name == "anky":
            self._initialise("Ankylosaurus",
                             ac=15, hp=68, alignment='evil',
                             attack_parameters=[['tail', 7, 4, 6, 6, 6, 6]],
                             log="CR 3 700 XP")

        elif name == "my barbarian":
            self._initialise(name="Barbarian",
                             ac=18, hp=66, alignment="good",
                             attack_parameters=[['greatsword', 4, 1, 6, 6], ['frenzy greatsword', 4, 1, 6, 6]],
                             log="hp is doubled due to resistance", level=3)

        elif name == "my druid":
            self._initialise(name="Twice Brown Bear Druid",
                             hp=86, ac=11, alignment="good",
                             attack_parameters=[['claw', 5, 4, 8], ['bite', 5, 4, 6, 6]],
                             ability_bonuses=[0, 0, 0, 0, 3, 0],
                             sc_ability='wis', buff='cast_barkskin', buff_spells=4,
                             log='The hp is bear x 2 + druid', level=3)

        elif name == "inert":
            self._initialise(name="inert", alignment="bad",
                             ac=10, hp=20,
                             attack_parameters=[['toothpick', 0, 0, 2]])

        elif name == "test":
            self._initialise(name="Test", alignment="good",
                             ac=10, hp=100,
                             attack_parameters=[['club', 2, 0, 4]])

        elif name == "polar":
            self._initialise(name="polar bear", alignment='evil',
                             ac=12, hp=42,
                             attack_parameters=[['bite', 7, 5, 8], ['claw', 7, 5, 6, 6]])

        elif name == "paradox":
            self._initialise(name="Paradox", alignment="evil",
                             ac=10, hp=200,
                             attack_parameters=[['A', 2, 0, 1]])

        elif name == "commoner":
            self._initialise(name="Commoner", alignment="good",
                             ac=10, hp=4,
                             attack_parameters=[['club', 2, 0, 4]])

        elif name == "giant_rat":
            self._initialise(name="Giant Rat", alignment="evil",
                             hp=7, ac=12,
                             initiative_bonus=2,
                             attack_parameters=[['bite', 4, 2, 4]])

        elif name == "twibear":
            self._initialise(name="Twice Brown Bear Druid",
                             hp=86, ac=11, alignment="good",
                             attack_parameters=[['claw', 5, 4, 8], ['bite', 5, 4, 6]], level=3)

        elif name == "barkskin_twibear":
            self._initialise(name="Druid twice as Barkskinned Brown Bear",
                             hp=86, ac=16, alignment="good",
                             attack_parameters=[['claw', 5, 4, 8], ['bite', 5, 4, 6]], level=3)

        elif name == "barkskin_bear":
            self._initialise(name="Barkskinned Brown Bear", alignment="good",
                             hp=34, ac=16,
                             attack_parameters=[['claw', 5, 4, 8], ['bite', 5, 4, 6]], level=4, hd=10)

        elif name == "giant_toad":
            self._initialise(name="Giant Toad", alignment="evil",
                             hp=39, ac=11,
                             attack_parameters=[['lick', 4, 2, 10, 10]])

        elif name == "cthulhu":  # PF stats. who cares. you'll die.
            self._initialise(name="Cthulhu", alignment="beyond",
                             ac=49, hp=774, xp=9830400,
                             initiative_bonus=15,
                             attack_parameters=[['2 claws', 42, 23, 6, 6, 6, 6], ['4 tentacles', 42, 34, 10, 10]],
                             alt_attack=['none', 0],
                             healing_spells=99999, healing_dice=1, healing_bonus=30,
                             ability_bonuses=[56, 21, 45, 31, 36, 34], sc_ability='wis',
                             buff='cast_nothing', buff_spells=0, log=None, hd=8, level=36, proficiency=27,
                             br=99.0)


        else:
            self._initialise(name="Commoner", alignment="evil",
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

        # may need to add Morale here??
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

    def copy(self):
        """
        :return: a copy of the creature. with an altered name.
        """
        self.copy_index += 1
        return Creature(self, name=self.name + ' ' + str(self.copy_index))

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
        for monoattack in attack_parameters:
            att = {'name': monoattack[0]}
            att['damage'] = DnD.Dice(monoattack[2], monoattack[3:], role="damage")
            att['attack'] = DnD.Dice(monoattack[1], 20, role="attack", twinned=att['damage'])
            self.attacks.append(att)
        for x in self.attacks:
            self.hurtful += x['damage'].bonus
            self.hurtful += (sum(x['damage'].dice) + len(
                x['damage'].dice)) / 2  # the average roll of a d6 is not 3 but 3.5

    # Another place where Morale may need to be added
    def __str__(self):
        if self.tally['battles']:
            battles = self.tally['battles']
            return self.name + ": {team=" + self.alignment + "; avg hp=" + str(
                self.tally['hp'] / battles) + " (from " + str(
                self.starting_hp) + "); avg healing spells left=" + str(
                self.tally['healing_spells'] / battles) + " (from " + str(
                self.starting_healing_spells) + "); damage done (per battle average)= " + str(
                self.tally['damage'] / battles) + "; hits/misses (PBA)= " + str(
                self.tally['hits'] / battles) + "/" + str(
                self.tally['misses'] / battles) + "; rounds (PBA)=" + str(
                self.tally['rounds'] / battles) + ";}"
        else:
            return self.name + ": UNTESTED IN BATTLE"

        # Morale may be needed to be factored in here too
    def isalive(self):
        if self.hp > 0: return 1

    def take_damage(self, points, verbose=1):
        self.hp -= points
        if verbose: verbose.append(self.name + self.id + ' took ' + str(points) + ' damage. Now on ' + str(self.hp) + ' hp.')
            
        # Morale Check for bloodied
        if self.hp < self.starting_hp/2: 
            self.current_morale -= 1 # this will cause it to lose morale EVERY TURN while it's bloodied,

        if points > 10 : self.current_morale -= 1 # pseudo critical hit
        if verbose: verbose.append(self.name + self.id + ' is at ' + str(self.current_morale) + ' morale.')

        # if morale gets to be 0 or less, remove from combattants list (run away), else check if concentrating.
        if self.current_morale < 1 : 
            self.hp = 0 #psuedo death (running away)
            if verbose: verbose.append(self.name + self.id + ' lost its desire to fight and ran away from battle')
        else : 
            if self.concentrating:
                dc = points / 2
                if dc < 10: dc = 10
                if DnD.Dice(self.ability_bonuses[self.sc_ab]).roll() < dc:
                    self.conc_fx()
                    if verbose: verbose.append(self.name + ' has lost their concentration')

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
        self.current_morale +=  1
        if verbose: verbose.append(self.name + ' was healed by ' + str(points) + '. Now on ' + str(self.hp) + ' hp.')
        if verbose: verbose.append(self.name + ' got a morale boost from getting healed and is now at ' + str(self.current_morale) + ' morale.')

    def assess_wounded(self, verbose=0):
        targets = self.arena.find('bloodiest allies')
        if len(targets) > 0:
            weakling = targets[0]
            if weakling.starting_hp > (self.healing.dice[0] + self.healing.bonus + weakling.hp):
                if verbose: verbose.append(self.name + " wants to heal " + weakling.name)
                return weakling
            else:
                return 0
        else:
            raise NameError('A dead man wants to heal folk')

    def cast_healing(self, weakling, verbose=0):
        if self.healing_spells > 0:
            weakling.heal(self.healing.roll(), verbose)
            self.healing_spells -= 1

    def multiattack(self, verbose=0, assess=0):
        if assess:
            return 0  # the default
        for i in range(len(self.attacks)):
            try:
                opponent = self.arena.find(TARGET, self)[0]
            except IndexError:
                raise self.arena.Victory()
            if verbose:
                verbose.append(self.name + ' attacks ' + opponent.name + ' with ' + str(self.attacks[i]['name']))
            # This was the hit method. put here for now.
            self.attacks[i]['attack'].advantage = self.check_advantage(opponent)
            if self.attacks[i]['attack'].roll(verbose) >= opponent.ac:
                # self.attacks[i]['damage'].crit = self.attacks[i]['attack'].crit  #Pass the crit if present.
                h = self.attacks[i]['damage'].roll(verbose)
                opponent.take_damage(h, verbose)
                # check to see if the opponent survived the last hit, if not, win
                if opponent.hp < 1 : raise self.arena.Victory()
                self.tally['damage'] += h
                self.tally['hits'] += 1
            else:
                self.tally['misses'] += 1

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
        # heal  -healing word, a bonus action.
        if self.healing_spells > 0:
            weakling = self.assess_wounded(verbose)
            if weakling != 0:
                self.cast_healing(weakling, verbose)
        # Main action!
        economy = len(self.arena.find('allies')) > len(self.arena.find('opponents')) > 0
        # Buff?
        if self.condition == 'netted':
            # NOT-RAW: DC10 strength check or something equally easy for monsters
            if verbose: verbose.append(self.name + " freed himself from a net")
            self.condition = 'normal'
        elif self.buff_spells > 0 and self.concentrating == 0:
            self.conc_fx()
            if verbose: verbose.append(self.name + ' buffs up!')
            # greater action economy: waste opponent's turn.
        elif economy and self is self.arena.find('weakest allies')[0]:
            if verbose: verbose.append(self.name + " is dodging")
            self.dodge = 1
        elif economy and self.alt_attack['name'] == 'net':
            opponent = self.arena.find('fiersomest enemy alive', self)[0]
            if opponent.condition != 'netted':
                self.net(opponent, verbose)
            else:
                self.multiattack(verbose)
        else:

            self.multiattack(verbose)

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