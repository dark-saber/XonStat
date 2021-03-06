<%def name="nav(active='leaderboard', login_logout=False)">
    <div class="navbar navbar-inverse navbar-top">
      <div class="navbar-inner">
        <div class="container">
          <a class="navbar-toggle collapsed" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </a>
          <a class="navbar-brand" href="${request.route_url('main_index')}">
           <img src="/static/css/img/menu_icon.png" style="-webkit-filter: drop-shadow(0px 5px 5px grey);"/>
           QLStats
          </a>
          <nav class="nav-main nav-collapse in collapse" role="navigation" style="height: auto;">
            <ul class="nav">
              <li 
                % if active=="leaderboard":
                class="active"
                % endif
                ><a href="${request.route_url('main_index')}" title="Leaderboard">Leaderboard</a></li>
              <li 
                % if active=="players":
                class="active"
                % endif
                ><a href="${request.route_url('player_index')}" title="Player Index">Players</a></li>
              <li 
                % if active=="games":
                class="active"
                % endif
                ><a href="${request.route_url('game_index')}" title="Game Index">Games</a></li>
              <li 
                % if active=="servers":
                class="active"
                % endif
                ><a href="${request.route_url('server_index')}" title="Server Index">Servers</a></li>
              <li 
                % if active=="maps":
                class="active"
                % endif
                ><a href="${request.route_url('map_index')}" title="Map Index">Maps</a></li>
            </ul>

            ##### Login/logout button goes here only if needed #####
            % if login_logout:
            <ul class="nav pull-left">
              <li>${request.persona_button}</li>
            </ul>
            % endif

            <form class="navbar-form pull-left" action="${request.route_url('search')}" method="get">
              <input type="hidden" name="fs" />
              <input type="search" class="input-small search" placeholder="search" name="sval"/>
              <select class="search" name="stype">
                <option>players</option>
                <option>servers</option>
                <option>maps</option>
              </select>
            [<a href="${request.route_url('search')}" title="Advanced search">+</a>]
            </form>
          </nav>

        </div>
      </div>
    </div>
</%def>
