import random


class perlinNoise():

    def __init__(self, height=32, width=32, bit_depth=255, smoothing=32):
        self.height = height
        self.width = width
        self.bit_depth = bit_depth
        self.smooth = smoothing

    def randomize(self):

        self.seed = [[random.randint(0, self.bit_depth)/self.bit_depth for y in range(self.height)] for x in range(self.width)]

    def noise2D(self, x, y):

        return self.seed[x][y]

    def smoothNoise2D(self, bit_depth=255, smoothing_passes=15, upper_value_limit=1):

        values = self.seed

        for _ in range(smoothing_passes):
            values = [
                [((values[x][y] + values[x + 1][y] + values[x][y + 1] + values[x - 1][y] + values[x][y - 1]) / 5) for y
                 in range(len(values[x]) - 1)] for x in range(len(values) - 1)]

        return values
