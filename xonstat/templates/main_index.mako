<%inherit file="base.mako"/>

<%block name="title">
Main Page - ${parent.title()}
</%block>

##### DUEL RANKS #####
<div class="table_block">
<h2>Duel Ranks</h2>
<table class="rank-table">
	<thead>
		<tr>
			<th>#</th>
			<th>Nick</th>
			<th>Elo</th>
		</tr>
	</thead>
	<tbody>
	<% i = 1 %>
	% for (player_id, nick, elo) in duel_ranks:
		<tr>
			<td>${i}</td>
			% if player_id != '-':
			<td><a href="${request.route_url('player_info', id=player_id)}" title="Go to the player info page for this player">${nick}</a></td>
			% else:
			<td>${nick}</td>
			% endif
            % if elo != '-':
			<td>${round(elo, 3)}</td>
            % else:
			<td>${elo}</td>
            % endif
		</tr>
		<% i = i+1 %>
	% endfor
	</tbody>
</table>
<p class="note"><a href="${request.route_url('rank_index', page=1, game_type_cd='duel')}" title="See more duel rankings">More...</a></p>
</div>



##### CTF RANKS #####
<div class="table_block">
<h2>CTF Ranks</h2>
<table class="rank-table">
	<thead>
		<tr>
			<th>#</th>
			<th>Nick</th>
			<th>Elo</th>
		</tr>
	</thead>
	<tbody>
	<% i = 1 %>
	% for (player_id, nick, elo) in ctf_ranks:
		<tr>
			<td>${i}</td>
			% if player_id != '-':
			<td><a href="${request.route_url('player_info', id=player_id)}" title="Go to the player info page for this player">${nick}</a></td>
			% else:
			<td>${nick}</td>
			% endif
            % if elo != '-':
			<td>${round(elo, 3)}</td>
            % else:
			<td>${elo}</td>
            % endif
		</tr>
		<% i = i+1 %>
	% endfor
	</tbody>
</table>
<p class="note"><a href="${request.route_url('rank_index', page=1, game_type_cd='ctf')}" title="See more CTF rankings">More...</a></p>
</div>



##### DM RANKS #####
<div class="table_block">
<h2>DM Ranks</h2>
<table class="rank-table">
	<thead>
		<tr>
			<th>#</th>
			<th>Nick</th>
			<th>Elo</th>
		</tr>
	</thead>
	<tbody>
	<% i = 1 %>
	% for (player_id, nick, elo) in dm_ranks:
		<tr>
			<td>${i}</td>
			% if player_id != '-':
			<td><a href="${request.route_url('player_info', id=player_id)}" title="Go to the player info page for this player">${nick}</a></td>
			% else:
			<td>${nick}</td>
			% endif
            % if elo != '-':
			<td>${round(elo, 3)}</td>
            % else:
			<td>${elo}</td>
            % endif
		</tr>
		<% i = i+1 %>
	% endfor
	</tbody>
</table>
<p class="note"><a href="${request.route_url('rank_index', page=1, game_type_cd='dm')}" title="See more deathmatch rankings">More...</a></p>
</div>



##### TOP PLAYERS #####
<div class="table_block">
<h2>Most Active Players</h2>
<table id="top-players">
	<thead>
		<tr>
			<th>#</th>
			<th>Nick</th>
			<th class="play-time">Play Time</th>
		</tr>
	</thead>
	<tbody>
	<% i = 1 %>
	% for (player_id, nick, alivetime) in top_players:
		<tr>
			<td>${i}</td>
			% if player_id != '-':
			<td><a href="${request.route_url('player_info', id=player_id)}" title="Go to the player info page for this player">${nick|n}</a></td>
			% else:
			<td>${nick}</td>
			% endif
			<td class="play-time">${alivetime}</td>
		</tr>
		<% i = i+1 %>
	% endfor
	</tbody>
</table>
<p class="note">*Most active stats are from the past 7 days</p>
</div>

##### TOP SERVERS #####
<div class="table_block">
<h2>Most Active Servers</h2>
<table id="top-servers">
	<thead>
		<tr>
			<th>#</th>
			<th>Server</th>
			<th>Games</th>
		</tr>
	</thead>
	<tbody>
	<% i = 1 %>
	% for (server_id, name, count) in top_servers:
		<tr>
			<td>${i}</td>
			% if server_id != '-':
			<td><a href="${request.route_url('server_info', id=server_id)}" title="Go to the server info page for ${name}">${name}</a></td>
			% else:
			<td>${name}</td>
			% endif
			<td>${count}</td>
		</tr>
		<% i = i+1 %>
	% endfor
	</tbody>
</table>
</div>

##### TOP MAPS #####
<div class="table_block">
<h2>Most Active Maps</h2>
<table id="top-maps">
	<thead>
		<tr>
			<th>#</th>
			<th>Map</th>
			<th>Games</th>
		</tr>
	</thead>
	<tbody>
	<% i = 1 %>
	% for (map_id, name, count) in top_maps:
		<tr>
			<td>${i}</td>
			% if map_id != '-':
			<td><a href="${request.route_url('map_info', id=map_id)}" title="Go to the map info page for ${name}">${name}</a></td>
			% else:
			<td>${name}</td>
			% endif
			<td>${count}</td>
		</tr>
		<% i = i+1 %>
	% endfor
	</tbody>
</table>
</div>



##### RECENT GAMES #####
<div class="table_block">
<h2>Recent Games</h2>
<table id="recent-games">
	<thead>
		<tr>
			<th>Game #</th>
			<th>Type</th>
			<th>Server</th>
			<th>Map</th>
			<th>Time</th>
			<th>Winner</th>
		</tr>
	</thead>
	<tbody>
	% for (game, server, map, pgstat) in recent_games:
		% if game != '-':
		<tr>
			<td><a href="${request.route_url('game_info', id=game.game_id)}" title="View detailed information about this game">${game.game_id}</a></td>
			<td class="gt_icon"><img title="${game.game_type_cd}" src="/static/images/icons/24x24/${game.game_type_cd}.png" alt="${game.game_type_cd}" /></td>
			<td><a href="${request.route_url('server_info', id=server.server_id)}" title="Go to the detail page for this server">${server.name}</a></td>
			<td><a href="${request.route_url('map_info', id=map.map_id)}" title="Go to the map detail page for this map">${map.name}</a></td>
			<td>${game.start_dt.strftime('%m/%d/%Y %H:%M')}</td>
			<td class=
            % if pgstat.team == 5:
            "blue"
            % elif pgstat.team == 14:
            "red"
            % elif pgstat.team == 13:
            "yellow"
            % endif
            >
            % if pgstat.player_id > 2:
            <a href="${request.route_url('player_info', id=pgstat.player_id)}" title="Go to the player info page for this player">${pgstat.nick_html_colors()|n}</a></td>
            % else:
            ${pgstat.nick_html_colors()|n}</td>
            % endif
		</tr>
		% else:
		<tr>
			<td>-</td>
			<td>-</td>
			<td>-</td>
			<td>-</td>
			<td>-</td>
			<td>-</td>
		</tr>
		% endif
    % endfor
    </tbody>
</table>
</div>


