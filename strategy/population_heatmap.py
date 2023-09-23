from game.game_state import GameState

class PopulationHeatmap():

    def __init__(self, game_state_: GameState):
        self.game_state = game_state_
        self.heatmap = [list(0 for _ in range(10)) for _ in range(10)]

    def calcHeatmap(self):
        for c in self.game_state.characters.values():
            if c.is_zombie:
                x_grid = c.position.x // 10
                y_grid = c.position.y // 10
                self.heatmap[y_grid][x_grid] -= 1
            else:
                x_grid = c.position.x // 10
                y_grid = c.position.y // 10
                self.heatmap[y_grid][x_grid] += 1

    def hottest(self):
        hottest_value = -100
        hottest_x = 0
        hottest_y = 0   
        for i in range(10):
            for k in range(10):
                if self.heatmap[i][k]:
                    if (self.heatmap[i][k] > hottest_value):
                        hottest_value = self.heatmap[i][k]
                        hottest_y = i
                        hottest_x = k
        return hottest_y, hottest_x

    def coolest(self):
        coolest_value = -100
        coolest_x = 0
        coolest_y = 0
        for i in range(10):
            for k in range(10):
                if self.heatmap[i][k]:
                    if (self.heatmap[i][k] < coolest_value):
                        coolest_value = self.heatmap[i][k]
                        coolest_y = i
                        coolest_x = k
        return coolest_y, coolest_x
