__author__ = "Trinity"
__copyright__ = ""
__email__ = "trinityrjbass at gmail"
__date__ = '23/03/20'

import random
import math
import warnings
from DnDRoyale import creature


#N="\n"
N = "<br/>"
TARGET = 'enemy alive weakest'
# target='enemy alive weakest', target='enemy alive random', target='enemy alive fiersomest'

"""
This module allows the simulation of a D&D encounter.
It has three main classes:  Dice, Character, Encounter.
It also has a csv file (`beastiary.csv`) containing all 5e SDR monsters.

**Teams.** Multiple creatures of the same alignment will team up to fight creatures of different alignments in a simulation (`Encounter().battle()` for a single iteration or `Encounter().go_to_war()` for multiple).
**Gridless.** The game assumes everyone is in cotact with everyone and not on a grid. The reason being is tactics.
**Tactics.** Tactics are highly problematic both in targetting and actions to take. Players do not play as strategically as they should due to heroism and kill tallies, while the DM might play monsters really dumbly to avoid a TPK.
**Targetting.** The similator is set up as a munchkin combat where everyone targets the weakest opponent (The global variable `TARGET="enemy alive weakest"` makes the `find_weakest_target` method of the `Encounter` be used, but could be changed (unwisely) to a permutation of enemy/ally alive/dead weakest/random/fiercest.
The muchkinishness has a deleterious side-effect when the method deathmatch of the Encounter class is invoked —this allocates each Creature object in the Encounter object in a different team.
**Actions.** Action choice is dictated by turn economy. A character of a team with the greater turn economy will dodge (if it knows itself a target) or throw a net (if it has one), and so forth while a creature on the oppose side will opt for a slugfest.


# Example uses

    >>> import DnD_Battler.py as DnD
    >>> DnD.Creature('aboleth') # get from beastiary
    >>> level1 = DnD.Creature("buff peseant",base='commoner',abilities = {'str': 15,'dex': 14,'con':13,'int':12,'wis':10,'cha': 8}, alignment ="good", attack_parameters='longsword') #a modified creature based off another
    >>> arena = DnD.Encounter(level1, 'badger')  #Encounter accepts both Creature and strings.
    >>> print(arena.go_to_war(1e5) #simulate 10,000 times
    >>> print(arena.battle(verbose = 1)) # simulate one encounter and tell what happens.
    >>> print(DnD.Creature('tarrasque').generate_character_sheet())  #md character sheet.
    >>> print(Encounter("ancient blue dragon").addmob(85).go_to_war(10))  #An ancient blue dragon is nearly a match for 85 commoners (who crit evenutally)...

# Class summary
## Dice
Dice accepts bonus plus an int —8 is a d8— or a list of dice —[6,6] is a 2d6— or nothing —d20.
    roll() distinguishes between a d20 and not. d20 crits have to be passed manually.
## Character
Character has a boatload of attributes. It can be initilised with a dictionary or an unpacked one... or a single name matching a preset.
## Encounter
Encounter includes the following method:
    battle(reset=1) does a single battle (after a reset of values if asked). it calls a few other fuctions such as roll_for_initiative()
    go_to_war(rounds=1000) performs many battles and gives the team results
verbosity (verbose=1) is optional. And will be hopefully be written out of the code.

There is some code messiness resulting from the unclear distinction between Encounter and Creature object, namely
a Creature interacting with another is generally a Creature method, while a Creature searching across the list of Creatures in the Encounter is an Encounter method.

There are one or two approximations that are marked #NOT-RAW. In the Encounter.battle method there are some thought on the action choices.
"""


######################DICE######################
class Dice:
    def __init__(self, bonus=0, dice=20, avg=False, twinned=None, role="ability"):
        """
        Class to handle dice and dice rolls
        :param bonus: int, the bonus added to the attack roll
        :param dice: list of int, the dice size.
        :param avg: boolean flag marking whether the dice always rolls average, like NPCs and PCs on Mechano do for attack rolls.
        :param twinned: a dice. ja. ehrm. this is the other dice. The crits are passed to it. It should be a weak ref or the crits passed more pythonically.
        :param role: string, but actually on a restricted vocabulary: ability, damage, hd or healing. Extras can be added, but they won't trigger some things
        :return: a rollable dice!

        The parameters are set to attributes. Other attributes are:
        * critable: determined from `role` attribute
        * crit: 0 or 1 ... or more if you want to go 3.5 and crit train.
        * advantage: trinary int. -1 is disadvantage, 0 normal, 1 is advantage.
        """
        if twinned:
            self.twinned = twinned
        else:
            self.twinned = None
        ##Can it crit?
        self.role = role
        if self.role == "damage" or self.role == "healing" or self.role == "hd":
            self.critable = 0
        else:
            self.critable = 1

        # stats
        self.bonus = int(bonus)
        if type(dice) is list:
            self.dice = dice
        elif type(dice) is str:
            raise Exception("str is not yet supported as dice type")  # TODO add support of d6 notation
        else:
            self.dice = [dice]
        self.advantage = 0
        self.crit = 0  # multiplier+1. Actually you can't get a crit train anymore.
        self.avg = avg

    def __str__(self):
        """
        This is rather inelegant piece of code and is not overly flexible. If the dice fail to show, they will still work.
        :return: string in dice notation.
        """
        s = ''
        if len(self.dice) == 1:
            s += 'd' + str(self.dice[0]) + '+'
        elif len(self.dice) == 2 and self.dice[0] == self.dice[1]:
            s += '2d' + str(self.dice[0]) + '+'
        elif len(self.dice) == 2 and self.dice[0] != self.dice[1]:
            s += 'd' + str(self.dice[0]) + '+d' + 'd' + str(self.dice[1]) + '+'
        elif len(self.dice) == 3 and self.dice[0] == self.dice[1] == self.dice[1]:
            s += '3d' + str(self.dice[0]) + '+'
        elif len(self.dice) == 3 and self.dice[0] != self.dice[1]:
            s += 'd' + str(self.dice[0]) + '+d' + str(self.dice[1]) + '+d' + str(self.dice[1]) + '+'
        else:
            for x in range(len(self.dice)):
                s += 'd' + str(self.dice[x]) + '+'
        s += str(self.bonus)
        return s

    def multiroll(self, verbose=0):
        """
        A roll that is not a d20. It adds the bonus and rolls (x2 if a crit).
        :param verbose:
        :return:
        """
        result = self.bonus
        for d in self.dice:
            if self.avg:  # NPC rolls
                if self.crit:
                    result += d
                else:
                    result += round(d / 2 + 1)
            else:
                for x in range(0, self.crit + 1): result += random.randint(1, d)
        self.crit = 0
        return result

    def icosaroll(self, verbose=0):
        """
        A roll that is a d20. It rolls advantage and disadvatage and calls `_critcheck`.
        :param verbose:
        :return:
        """
        self.crit = 0
        if self.advantage == 0:
            return self._crit_check(random.randint(1, 20), verbose) + self.bonus
        elif self.advantage == -1:  # AKA disadvatage
            return self._crit_check(sorted([random.randint(1, 20), random.randint(1, 20)])[0], verbose) + self.bonus
        elif self.advantage == 1:
            return self._crit_check(sorted([random.randint(1, 20), random.randint(1, 20)])[1], verbose) + self.bonus

    def _crit_check(self, result, verbose=0):
        """
        Checks if the dice is a crit.
        :param result: dice roll result.
        :param verbose: a debug paramater that I really ought to write out of the code.
        :return: alters the dice roll to -999 if a crit fail or 999 and adds a crit marker to the twinned dice (_i.e._ the attack dice)
        """
        if not self.critable:
            print("DEBUG: A crit check was called on an uncritable roll ", self.role)
            return result
        elif result == 1:
            if verbose: verbose.append("Fumble!")
            return -999  # automatic fail
        elif result == 20:
            if verbose: verbose.append("Critically hit!")
            if self.twinned: self.twinned.crit = 1
            return 999  # automatic hit.
        else:
            return result

    def roll(self, verbose=0):  # THIS ASSUMES NO WEAPON DOES d20 DAMAGE!! Dragonstar and Siege engines don't.
        """
        The roll method, which calls either icosaroll or multiroll.
        :param verbose: debug
        :return: the value rolled (and alters the dice too if need be)
        """
        if not self.dice:
            raise Exception('A non-existant dice has been attempted to be rolled')
        # elif self.dice[0] == 20:
        elif self.critable:  # the problem is crits and adv and only d20 can. Nothing deals d20 damage, but someone might try.
            return self.icosaroll(verbose)
        else:
            return self.multiroll(verbose)


######################CREATURE######################

######################ARENA######################
class Encounter:
    """
    In a dimentionless model, move action and the main actions dash, disengage, hide, shove back/aside, tumble and overrun are meaningless.
    weapon attack —default
    two-weapon attack —
        Good when the opponent has low AC (<12) if 2nd attack is without proficiency.
        Stacks with bonuses such as sneak attack or poisoned weapons —neither are in the model.
        Due to the 1 action for donning/doffing a shield, switch to two handed is valid for unshielded folk only.
        Best keep two weapon fighting as a prebuild not a combat switch.
    AoE spell attack — Layout…
    targetted spell attack —produce flame is a cantrip so could be written up as a weapon. The bigger ones. Spell slots need to be re-written.
    spell buff —Barkskin is a druidic imperative. Haste? Too much complication.
    spell debuff —Bane…
    dodge —targetted and turn economy
    help —high AC target (>18), turn economy, beefcake ally
    ready —teamwork preplanning. No way.
    grapple/climb —very situational. grapple/shove combo or barring somatic.
    disarm —disarm… grey rules about whether picking it up or kicking it away is an interact/move/bonus/main action.
        netting is a better option albeit a build.
    called shot —not an official rule. Turn economy.
    """

    class Victory(Exception):
        """
        The way the encounter ends is a victory error is raised to stop the creatures from acting further.
        """
        pass

    def __init__(self, *lineup):
        '''
        creates the variables necessary to run the encounter and then instantiates each combatant
        '''
        self.KILL=False #needed for code.
        self.tally = {'rounds': 0, 'battles': 0, 'perfect': None, 'close': None, 'victories': None}
        self.active = None
        self.num_combattants = 0
        self.name = 'Encounter'
        self.masterlog = []
        self.note = ''
        self.combattants = []
        self.sides = ''
        
        for chap in lineup:
            if type(chap) is dict:
                # TODO cope with dictionary input from custom combattant 
                print("Custom Combattant detected, attempting to add to combattant list")
                newChap = creature.Creature(chap)
                self.append(newChap)
            elif type(chap) is str: 
                self.append(chap)            
            else:
                print("pls don't summon the big guy here")
                continue #pls dont' randomly add Cthulhu

        self.blank()

    def blank(self, hard=True):
        ''' resets the teams '''
        # This is where The teams are set
        self.sides = set([dude.alignment for dude in self])
        self.tally['battles'] = 0
        self.tally['rounds'] = 0
        self.tally['perfect'] = {side: 0 for side in self.sides}
        self.tally['close'] = {side: 0 for side in self.sides}
        self.tally['victories'] = {side: 0 for side in self.sides}
        self.reset(hard)


    def append(self, newbie):
        ''' add a creature to the list of combatants '''
        #print("appending " + newbie + str(len(self.combattants))) #debugging
        if not type(newbie) is creature.Creature:
            newbie = creature.Creature(newbie) 
        newbie.id = str(len(self.combattants)) #this should be in the beginning of the method
        self.combattants.append(newbie)
        newbie.arena = self
        self.blank()

    def extend(self, iterable):
        for x in iterable:
            self.append(x)
        return self
    # ===== DEPRECATION CHECK =====
    #def addmob(self, n):
    #    """
    #    Adds _n_ commoners to the battle
    #    :param n: number of commoners
    #    :return: self
    #    """
    #    for x in range(int(n)):
    #        self.append("commoner")
    #    return self

    def __str__(self):
        ''' formats the battle results and data to be displayed on the web page''' 
        string = "=" * 50 + ' ' + self.name + " " + "=" * 50 + N
        string += self.predict()
        string += "-" * 110 + N
        string += "Battles: " + str(self.tally['battles']) + "; Sum of rounds: " + str(
            self.tally['rounds']) + "; " + self.note + N
        for s in self.sides:
            string += "> Team " + str(s) + " = winning battles: " + str(
                self.tally['victories'][s]) + "; perfect battles: " + str(
                self.tally['perfect'][s]) + "; close-call battles: " + str(self.tally['close'][s]) + ";\n"
        string += "-" * 49 + " Combattants  " + "-" * 48 + N
        for fighter in self.combattants: string += str(fighter) + N
        return string

    def json(self):
        import json
        jsdic = {"prediction": self.predict(),
                 "battles": self.tally['battles'],
                 "rounds": self.tally['rounds'],
                 "notes": self.note,
                 "team_names": list(self.sides),
                 "team_victories": [self.tally['victories'][x] for x in list(self.sides)],
                 "team_perfects": [self.tally['perfect'][x] for x in list(self.sides)],
                 "team_close": [self.tally['close'][x] for x in list(self.sides)],
                 "combattant_names": [x.name for x in self.combattants],
                 "combattant_alignments": [x.alignment for x in self.combattants],
                 "combattant_damage_avg": [x.tally['damage'] / self.tally['battles'] for x in self.combattants],
                 "combattant_hit_avg": [x.tally['hits'] / self.tally['battles'] for x in self.combattants],
                 "combattant_miss_avg": [x.tally['misses'] / self.tally['battles'] for x in self.combattants],
                 "combattant_rounds": [x.tally['rounds'] / self.tally['rounds'] for x in self.combattants],
                 "sample_encounter": N.join(self.masterlog)
                 }
        return json.dumps(jsdic)

    def __len__(self):
        return len(self.combattants)

    def __add__(self, other): 
        if type(other) is str:
            self.append(creature.Creature(other))
        elif type(other) is creature.Creature:
            self.append(other)
        elif type(other) is Encounter:
            self.extend(other.combattants)
        else:
            raise TypeError('Unsupported type '+str(type(other)))

    def __iter__(self):
        ''' instantiate custom creature'''
        return iter(self.combattants)

    def __getitem__(self, item):
        for character in self:
            if character.name == item:
                return character
        raise Exception('Nobody by this name')

    def reset(self, hard=False):
        for schmuck in self.combattants:
            schmuck.reset(hard)
        return self

    def remove(self,moriturus):
        """
        Removes a creature and resets and rechecks
        :param moriturus: The creature name to be dropped
        :return: self
        """
        if type(moriturus) is str:
            for chap in self.combattants:
                if chap.name == moriturus: # this should be changed to chap.id
                    self.combattants.remove(chap)
                    break
            else:
                raise ValueError(moriturus+' not found in Encounter among '+"; ".join([chap.name for chap in self.combattants]))
        elif type(moriturus) is creature.Creature:
            self.combattants.remove(moriturus)
        self.blank()

        
    def set_deathmatch(self):
        """ setting colors for functionality that isn't used in this app"""
        colours = 'red blue green orange yellow lime cyan violet ultraviolet pink brown black white octarine teal magenta blue-green fuchsia purple cream grey'.split(
            ' ')
        for schmuck in self:
            schmuck.alignment = colours.pop(0) + " team"
        return self

    def roll_for_initiative(self, verbose=0):
        self.combattants = sorted(self.combattants, key=lambda fighter: fighter.initiative.roll())
        if verbose:
            verbose.append("Turn order:")
            verbose.append(str([x.name for x in self]))

    def predict(self):
        def safediv(a, b, default=0):
            try:
                return a / b
            except:
                return default

        def not_us(side):
            (a, b) = list(self.sides)
            if a == side:
                return b
            else:
                return a

        if len(self.sides) != 2:
            # print('Calculations unavailable for more than 2 teams')
            return "Prediction unavailable for more than 2 teams"
        t_ac = {x: [] for x in self.sides}
        for character in self:
            t_ac[character.alignment].append(character.ac)
        ac = {x: sum(t_ac[x]) / len(t_ac[x]) for x in t_ac.keys()}
        damage = {x: 0 for x in self.sides}
        hp = {x: 0 for x in self.sides}
        for character in self:
            for move in character.attacks:
                move['damage'].avg = True
                damage[character.alignment] += safediv((20 + move['attack'].bonus - ac[not_us(character.alignment)]),
                                                       20 * move['damage'].roll())
                move['damage'].avg = False
                hp[character.alignment] += character.starting_hp
        (a, b) = list(self.sides)
        rate = {a: safediv(hp[a], damage[b], 0.0), b: safediv(hp[b], damage[a], 0.0)}
        return ('Rough a priori predictions:' + N +
                '> ' + str(a) + '= expected rounds to survive: ' + str(
            round(rate[a], 2)) + '; crudely normalised: ' + str(
            round(safediv(rate[a], (rate[a] + rate[b]) * 100))) + '%' + N +
                '> ' + str(b) + '= expected rounds to survive: ' + str(
            round(rate[b], 2)) + '; crudely normalised: ' + str(
            round(safediv(rate[b], (rate[a] + rate[b]) * 100))) + '%' + N)

    def battle(self, reset=1, verbose=1):
        """iterates through combattants in a single fight"""
        if verbose: self.masterlog.append('==NEW BATTLE==')
        self.tally['battles'] += 1
        if reset: self.reset()
        for schmuck in self: schmuck.tally['battles'] += 1
        # WTF is "schmuck"? in this context...
        self.roll_for_initiative(self.masterlog)
        while True:
            try:
                if verbose: self.masterlog.append('**NEW ROUND**')
                self.tally['rounds'] += 1
                for character in self:
                    character.ready()
                    if character.isalive():
                        self.active = character
                        character.tally['rounds'] += 1
                        character.act(self.masterlog)
                    else:
                        character.tally['dead'] += 1
            except Encounter.Victory:
                break
        # closing up maths
        side = self.active.alignment
        team = self.find('allies')
        self.tally['victories'][side] += 1
        perfect = 1
        close = 0
        for x in team:
            if x.hp < x.starting_hp:
                perfect = 0
            if x.hp < 0:
                close = 1
        if not perfect:
            self.tally['perfect'][side] += perfect
        self.tally['close'][side] += close
        for character in self:
            character.tally['hp'] += character.hp
            character.tally['healing_spells'] += character.healing_spells
        if verbose: self.masterlog.append(str(self))
        # return self or side?
        return self

    def go_to_war(self, rounds=1000):
        """run number of encounters equal to the number of rounds parameter"""
        for i in range(rounds):
            print(i,self.KILL)
            self.battle(1, 0)
            if self.KILL==True:
                break
        x = {y: self.tally['victories'][y] for y in self.sides}
        se = {}
        for i in list(x):
            x[i] /= rounds
            try:
                se[i] = math.sqrt(x[i] * (1 - x[i]) / rounds)
            except Exception:
                se[i] = "NA"
        self.reset()
        for i in list(x):
            try:
                self.note += str(i) + ': ' + str(round(float(x[i]), 2)) + ' ± ' + str(round(float(se[i]), 2)) + '; '
            except:
                self.note += str(i) + ': ' + str(x[i]) + ' ± ' + str(se[i]) + '; '
        return self

    def find(self, what, searcher=None, team=None):

        def _enemies(folk):
            return [query for query in folk if (query.alignment != team)]

        def _allies(folk):
            return [query for query in folk if (query.alignment == team)]

        def _alive(folk):
            return [query for query in folk if (query.hp > 0)]

        def _normal(folk):
            return [joe for joe in folk if joe.condition == 'normal']

        def _random(folk):
            random.shuffle(folk)
            return folk

        def _weakest(folk):
            return sorted(folk, key=lambda query: query.hp)

        def _bloodiest(folk):
            return sorted(folk, key=lambda query: query.hp - query.starting_hp)

        def _fiersomest(folk):
            return sorted(folk, key=lambda query: query.hurtful, reverse=True)

        def _opponents(folk):
            return _alive(_enemies(folk))

        searcher = searcher or self.active
        team = team or searcher.alignment
        folk = self.combattants
        agenda = list(what.split())
        opt = {
            'enemies': _enemies,
            'enemy': _enemies,
            'opponents': _opponents,
            'allies': _allies,
            'ally': _allies,
            'normal': _normal,
            'alive': _alive,
            'fiersomest': _fiersomest,
            'weakest': _weakest,
            'random': _random,
            'bloodiest': _bloodiest
        }
        for cmd in list(agenda):  # copy it.
            if folk == None:
                folk = []
            for o in opt:
                if (cmd == o):
                    folk = opt[o](folk)
                    agenda.remove(cmd)
        if agenda:
            raise Exception(str(cmd) + ' field not found')
        return folk


########### Junk methods #####

def tarrasquicide():
    print('Test module...of sorts: 128 commoners can kill a tarrasque')
    print('how many commoners are needed to kill a tarasque')
    ted = creature.Creature("tarrasque")
    print(ted)
    wwe = Encounter(ted, "commoner", "commoner").battle(1, 1)

    print(wwe.masterlog)
    max = 1
    while not wwe.tally['victories']['good']:
        max *= 2
        x = ["commoner" for x in range(int(max))]
        wwe.extend(x).battle(1, 0)
        wwe.tally['victories']['good']
        print(str(int(max)) + " commoners: " + str(wwe.tally['victories']['good']))
        print(ted.hp)

def creature_check(who= 'commoner'):
    """
    Dev test area. Prints the abilities of a given creature from the beastiary to see if all is okay.
    :param who: name
    :return: None
    """
    print('Ability bonus...')
    print('Beastiary: ',{x: Creature.beastiary[who][x] for x in 'AB_Str AB_Int AB_Con AB_Cha AB_Dex AB_Wis'.split()})
    print('Instance: ',Creature(who).ability_bonuses)
    print('Mod: ',Creature(who,str=999).ability_bonuses)


if __name__ == "__main__":
    pass
    #TODO I was updating the change_ability method of creature
