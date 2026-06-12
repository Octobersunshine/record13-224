from dataclasses import dataclass, field


@dataclass
class TeamStats:
    name: str
    points: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    goals_for: int = 0
    goals_against: int = 0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    @property
    def played(self) -> int:
        return self.wins + self.draws + self.losses


class LeagueService:
    def __init__(self):
        self._teams: dict[str, TeamStats] = {}

    def _get_team(self, name: str) -> TeamStats:
        if name not in self._teams:
            self._teams[name] = TeamStats(name=name)
        return self._teams[name]

    def record_match(self, home: str, away: str, home_goals: int, away_goals: int) -> None:
        if home_goals < 0 or away_goals < 0:
            raise ValueError("Goals cannot be negative")
        if home == away:
            raise ValueError("Home and away teams must be different")

        home_team = self._get_team(home)
        away_team = self._get_team(away)

        home_team.goals_for += home_goals
        home_team.goals_against += away_goals
        away_team.goals_for += away_goals
        away_team.goals_against += home_goals

        if home_goals > away_goals:
            home_team.wins += 1
            home_team.points += 3
            away_team.losses += 1
        elif home_goals < away_goals:
            away_team.wins += 1
            away_team.points += 3
            home_team.losses += 1
        else:
            home_team.draws += 1
            home_team.points += 1
            away_team.draws += 1
            away_team.points += 1

    def get_standings(self) -> list[TeamStats]:
        return sorted(
            self._teams.values(),
            key=lambda t: (t.points, t.goal_difference, t.goals_for, t.name),
            reverse=True,
        )

    def get_team_stats(self, name: str) -> TeamStats | None:
        return self._teams.get(name)

    def reset(self) -> None:
        self._teams.clear()


def print_standings(league: LeagueService) -> None:
    standings = league.get_standings()
    header = f"{'Rank':<5}{'Team':<15}{'P':<4}{'W':<4}{'D':<4}{'L':<4}{'GF':<4}{'GA':<4}{'GD':<5}{'Pts':<4}"
    print(header)
    print("-" * len(header))
    for rank, team in enumerate(standings, 1):
        gd = team.goal_difference
        gd_str = f"+{gd}" if gd > 0 else str(gd)
        print(
            f"{rank:<5}{team.name:<15}{team.played:<4}{team.wins:<4}"
            f"{team.draws:<4}{team.losses:<4}{team.goals_for:<4}"
            f"{team.goals_against:<4}{gd_str:<5}{team.points:<4}"
        )


if __name__ == "__main__":
    league = LeagueService()

    league.record_match("TeamA", "TeamB", 3, 1)
    league.record_match("TeamC", "TeamD", 2, 2)
    league.record_match("TeamA", "TeamC", 1, 0)
    league.record_match("TeamB", "TeamD", 4, 0)
    league.record_match("TeamA", "TeamD", 2, 1)
    league.record_match("TeamB", "TeamC", 1, 3)

    print_standings(league)
