import logging
import sqlalchemy
from datetime import timedelta
from sqlalchemy.orm import mapper
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from xonstat.elo import KREDUCTION, ELOPARMS
from xonstat.util import strip_colors, html_colors, pretty_date

log = logging.getLogger(__name__)

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

# define objects for all tables
class Player(object):
    def nick_html_colors(self):
        if self.nick is None:
            return "Anonymous Player"
        else:
            return html_colors(self.nick)

    def nick_strip_colors(self):
        if self.nick is None:
            return "Anonymous Player"
        else:
            return strip_colors(self.nick)

    def joined_pretty_date(self):
        return pretty_date(self.create_dt)

    def __repr__(self):
        return "<Player(%s, %s)>" % (self.player_id, 
                self.nick.encode('utf-8'))


class GameType(object):
    def __repr__(self):
        return "<GameType(%s, %s, %s)>" % (self.game_type_cd, self.descr, 
                self.active_ind)


class Weapon(object):
    def __repr__(self):
        return "<Weapon(%s, %s, %s)>" % (self.weapon_cd, self.descr, 
                self.active_ind)


class Server(object):
    def __init__(self, name=None, hashkey=None, ip_addr=None):
        self.name = name
        self.hashkey = hashkey
        self.ip_addr = ip_addr

    def __repr__(self):
        return "<Server(%s, %s)>" % (self.server_id, self.name.encode('utf-8'))


class Map(object):
    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return "<Map(%s, %s, %s)>" % (self.map_id, self.name, self.version)


class Game(object):
    def __init__(self, game_id=None, start_dt=None, game_type_cd=None, 
            server_id=None, map_id=None, winner=None):
        self.game_id = game_id
        self.start_dt = start_dt
        self.game_type_cd = game_type_cd
        self.server_id = server_id
        self.map_id = map_id
        self.winner = winner

    def __repr__(self):
        return "<Game(%s, %s, %s, %s)>" % (self.game_id, self.start_dt, 
                self.game_type_cd, self.server_id)

    def fuzzy_date(self):
        return pretty_date(self.start_dt)

    def process_elos(self, session, game_type_cd=None):
        if game_type_cd is None:
            game_type_cd = self.game_type_cd

        scores = {}
        alivetimes = {}
        for (p,s,a) in session.query(PlayerGameStat.player_id, 
                PlayerGameStat.score, PlayerGameStat.alivetime).\
                filter(PlayerGameStat.game_id==self.game_id).\
                filter(PlayerGameStat.alivetime > timedelta(seconds=0)).\
                filter(PlayerGameStat.player_id > 2).\
                all():
                    scores[p] = s
                    alivetimes[p] = a.seconds

        player_ids = scores.keys()

        elos = {}
        for e in session.query(PlayerElo).\
                filter(PlayerElo.player_id.in_(player_ids)).\
                filter(PlayerElo.game_type_cd==game_type_cd).all():
                    elos[e.player_id] = e

        # ensure that all player_ids have an elo record
        for pid in player_ids:
            if pid not in elos.keys():
                elos[pid] = PlayerElo(pid, game_type_cd)

        for pid in player_ids:
            elos[pid].k = KREDUCTION.eval(elos[pid].games, alivetimes[pid], 0)

        elos = self.update_elos(elos, scores, ELOPARMS)

        # add the elos to the session for committing
        for e in elos:
            session.add(elos[e])

        # TODO: duels are also logged as DM for elo purposes

    def update_elos(self, elos, scores, ep):
        eloadjust = {}
        for pid in elos.keys():
            eloadjust[pid] = 0

        # need to turn this into a list to iterate based
        # on numerical index
        elos = list(elos)

        if len(elos) < 2:
            return elos
        for i in xrange(0, len(elos)):
            ei = elos[i]
            for j in xrange(i+1, len(elos)):
                ej = elos[j]
                si = scores[ei.player_id]
                sj = scores[ej.player_id]

                # normalize scores
                ofs = min(0, si, sj)
                si -= ofs
                sj -= ofs
                if si + sj == 0:
                    si, sj = 1, 1 # a draw

                # real score factor
                scorefactor_real = si / float(si + sj)

                # estimated score factor by elo
                elodiff = min(ep.maxlogdistance, max(-ep.maxlogdistance, (ei.elo - ej.elo) * ep.logdistancefactor))
                scorefactor_elo = 1 / (1 + math.exp(-elodiff))

                # how much adjustment is good?
                # scorefactor(elodiff) = 1 / (1 + e^(-elodiff * logdistancefactor))
                # elodiff(scorefactor) = -ln(1/scorefactor - 1) / logdistancefactor
                # elodiff'(scorefactor) = 1 / ((scorefactor) (1 - scorefactor) logdistancefactor)
                # elodiff'(scorefactor) >= 4 / logdistancefactor

                # adjust'(scorefactor) = K1 + K2

                # so we want:
                # K1 + K2 <= 4 / logdistancefactor <= elodiff'(scorefactor)
                # as we then don't overcompensate

                adjustment = scorefactor_real - scorefactor_elo
                eloadjust[ei.player_id] += adjustment
                eloadjust[ei.player_id] -= adjustment
        for e in elos:
            e.elo = max(e.elo + eloadjust[e.player_id] * e.k * ep.global_K / float(len(elos) - 1), ep.floor)
            e.games += 1
        return elos


class PlayerGameStat(object):
    def __init__(self, player_game_stat_id=None, create_dt=None):
        self.player_game_stat_id = player_game_stat_id
        self.create_dt = create_dt

    def __repr__(self):
        return "<PlayerGameStat(%s, %s, %s)>" \
        % (self.player_id, self.game_id, self.create_dt)

    def nick_stripped(self):
        if self.nick is None:
            return "Anonymous Player"
        else:
            return strip_colors(self.nick)

    def nick_html_colors(self):
        if self.nick is None:
            return "Anonymous Player"
        else:
            return html_colors(self.nick)

    def team_html_color(self):
        # blue
        if self.team == 5:
            return "red"
        # red
        if self.team == 14:
            return "blue"
        if self.team == 13:
            return "yellow"
        if self.team == 10:
            return "pink"


class Achievement(object):
    def __repr__(self):
        return "<Achievement(%s, %s, %s)>" % (self.achievement_cd, self.descr,
                self.limit)


class PlayerAchievement(object):
    def __repr__(self):
        return "<PlayerAchievement(%s, %s)>" % (self.player_id, self.achievement_cd)


class PlayerWeaponStat(object):
    def __repr__(self):
        return "<PlayerWeaponStat(%s, %s, %s)>" % (self.player_weapon_stats_id,
                self.player_id, self.game_id)


class Hashkey(object):
    def __init__(self, player_id=None, hashkey=None):
        self.player_id = player_id
        self.hashkey = hashkey

    def __repr__(self):
        return "<Hashkey(%s, %s)>" % (self.player_id, self.hashkey)


class PlayerNick(object):
    def __repr__(self):
        return "<PlayerNick(%s, %s)>" % (self.player_id, self.stripped_nick)


class PlayerElo(object):
    def __init__(self, player_id=None, game_type_cd=None):
        self.player_id = player_id
        self.game_type_cd = game_type_cd
        self.elo = 0
        self.k = 0.0
        self.score = 0

    def __repr__(self):
        return "<PlayerElo(%s, %s, %s)>" % (self.player_id, self.game_type_cd,
                self.elo)


def initialize_db(engine=None):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    MetaData = sqlalchemy.MetaData(bind=engine, reflect=True)

    # assign all those tables to an object
    achievements_table = MetaData.tables['achievements']
    cd_achievement_table = MetaData.tables['cd_achievement']
    cd_game_type_table = MetaData.tables['cd_game_type']
    cd_weapon_table = MetaData.tables['cd_weapon']
    db_version_table = MetaData.tables['db_version']
    games_table = MetaData.tables['games']
    hashkeys_table = MetaData.tables['hashkeys']
    maps_table = MetaData.tables['maps']
    player_game_stats_table = MetaData.tables['player_game_stats']
    players_table = MetaData.tables['players']
    player_weapon_stats_table = MetaData.tables['player_weapon_stats']
    servers_table = MetaData.tables['servers']
    player_nicks_table = MetaData.tables['player_nicks']
    player_elos_table = MetaData.tables['player_elos']

    # now map the tables and the objects together
    mapper(PlayerAchievement, achievements_table)
    mapper(Achievement, cd_achievement_table)
    mapper(GameType, cd_game_type_table)
    mapper(Weapon, cd_weapon_table)
    mapper(Game, games_table)
    mapper(Hashkey, hashkeys_table)
    mapper(Map, maps_table)
    mapper(PlayerGameStat, player_game_stats_table)
    mapper(Player, players_table)
    mapper(PlayerWeaponStat, player_weapon_stats_table)
    mapper(Server, servers_table)
    mapper(PlayerNick, player_nicks_table)
    mapper(PlayerElo, player_elos_table)
