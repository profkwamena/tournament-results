-- Table definitions for the tournament project.

create table players (
	id serial primary key,
	name text
);

create table match (
	winner integer references players(id),
	loser integer references players(id)
);

create or replace view player_standings as 
	select 
		players.id, 
		players.name, 
		count(match.winner) as wins, 
		(select count(*) from match where players.id = match.winner or players.id = match.loser) as matches
	from 
		players
	left join
		match on
	 		players.id = match.winner
	group by players.id
	order by wins desc;