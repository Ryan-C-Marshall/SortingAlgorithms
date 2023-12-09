import random
import time

import pygame

WIDTH = 1000
HEIGHT = 800
FRAMERATE = 60
BG_COLOUR = (80, 130, 240)
RECT_COLOUR = (150, 90, 140)
RECT_ACTIVATED_COLOUR = (255, 100, 200)
SORTED_COLOUR = (100, 250, 125)
WAIT_TIME = 0.2


class listToSort:
    """
    Creates on object that can be altered by a sorting algorithm and makes visualizing the algorithm easy.
    Call update() whenever you want the display to show the recent changes and wait the specified amount of time
    """

    def __init__(self, values, visualizer, waitTime):
        self.values = values
        self.visualizer = visualizer
        self.waitTime = waitTime

        rectWidth = WIDTH / len(values)
        rectHeightMultiplier = 0.9 * HEIGHT / max(values)
        basicRectHeight = HEIGHT * 0.05
        self.rectangles = [Rectangle(rectWidth, rectHeightMultiplier * value + basicRectHeight)
                           for (i, value) in enumerate(values)]

    def update(self, sleep):
        self.visualizer.update(self)
        if sleep:
            time.sleep(self.waitTime)

    def uncolourAll(self):
        for rect in self.rectangles:
            rect.colour = RECT_COLOUR

    def colour(self, startIndex, endIndex, colour):
        self.uncolourAll()
        for rect in self.rectangles[startIndex:endIndex]:
            rect.colour = colour

    def colourOne(self, index, colour):
        self.rectangles[index].colour = colour

    def move(self, index, newIndex):
        self.values.insert(newIndex, self.values.pop(index))
        self.rectangles.insert(newIndex, self.rectangles.pop(index))

    def at(self, index):
        return self.values[index]


class Rectangle:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colour = RECT_COLOUR


class pygameModule:

    def __init__(self):
        self.running = True
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.update()

    def update(self, array):
        pygame.event.pump()
        self.updateFrame(array)
        pygame.display.update()
        self.clock.tick(FRAMERATE)

    def updateFrame(self, array):
        self.window.fill(BG_COLOUR)
        for i, rect in enumerate(array.rectangles):
            colour = rect.colour
            pygame.draw.rect(self.window, colour, (rect.width * (i + 0.125), HEIGHT - rect.height,
                                                   rect.width * 0.75, rect.height))

        pygame.display.update()


def mergeSort(array, start, end):
    if end - start == 1:
        return

    array.colour(start, end, RECT_ACTIVATED_COLOUR)
    array.update(True)

    midpoint = int(end - (end - start) / 2 + 0.5)

    mergeSort(array, start, midpoint)
    mergeSort(array, midpoint, end)

    # reentered into the larger array, reset the activation
    array.colour(start, end, RECT_ACTIVATED_COLOUR)
    array.update(True)

    merge(array, start, midpoint, end)

    for i in range(start, end):
        array.colourOne(i, SORTED_COLOUR)
        array.update(False)
    array.update(True)


def merge(array, start, midpoint, end):
    numSorted = 0
    jSorted = 0
    i = start
    j = midpoint
    while i < midpoint or j < end:

        if i == midpoint or (j < end and array.at(j) < array.at(i + jSorted)):
            array.move(j, start + numSorted)
            j += 1
            jSorted += 1

            array.update(True)
        else:
            i += 1

        numSorted += 1


# Press the green button in the gutter to run the script.
def main():
    pgModule = pygameModule()
    array = listToSort([random.random() for _ in range(30)], pgModule, WAIT_TIME)

    pgModule.update(array)

    mergeSort(array, 0, len(array.values))
    time.sleep(3)


if __name__ == '__main__':
    main()
