from cmu_graphics import *
import random

'''
Creative Elements:

Firstly, I have changed the colors of the app, added a moon, and added windows to the buildings.
Additionally, every time a blot hits a building, an explosion is seen. I implemented this in redrawAll and 
changed the size of the explosion using onStep. Finally, when the blot hits the opponent, a smaller explosion appears 
and the screen displays a "Game Over" message. One other thing that I changed from the original game
is changing "Current Player: 1" to "Current Player: Pink" (the same applies to the blue dot / player). The stars which
appear to be twinkling in the background are added using a for loop and the random feature in order to randomize
their location each time cmu graphics calls redrawAll.

'''

def onAppStart(app):
    app.step = 0
    app.width = 1000
    app.height = 600
    app.buildingCount = 10
    app.playerRadius = 15
    app.holeRadius = 50
    startNewGame(app)

def startNewGame(app):
    app.gameOver = False
    app.buildingHeights = [random.randrange(50, 300) for _ in range(app.buildingCount)]
    colors = ['lightSalmon', 'lightBlue', 'thistle', 'lightPink']
    app.buildingColors = [random.choice(colors) for _ in range(app.buildingCount)]
    #place new players
    buildingWidth = app.width / app.buildingCount
    cx0 = buildingWidth / 2
    cy0 = app.height - app.buildingHeights[0] - app.playerRadius
    cx1 = app.width - buildingWidth / 2
    cy1 = app.height - app.buildingHeights[-1] - app.playerRadius
    app.players = [ (cx0, cy0, 'plum'), (cx1, cy1, 'deepSkyBlue')]
    app.currentPlayer = 0
    app.showBlot = False
    app.showExplosion = False
    app.holes = []
    app.explosionRadius = 10

    
def getBuildingBounds(app, i):
    height = app.buildingHeights[i]
    width = app.width / app.buildingCount
    left = i*width
    top = app.height - height
    return left, top, width, height

def redrawAll(app):


    drawRect(0, 0, app.width, app.height, fill ='mediumSlateBlue')
    drawCircle(app.width / 8, app.height / 8, 45, fill = 'lightCyan')
    for i in range(20):
        randomStarX = random.randint(0, app.width)
        randomStarY = random.randint(0, app.height)
        drawStar(randomStarX, randomStarY, 10, 4, fill = random.choice(['goldenrod', 'lightYellow', 'yellow']))
    # draw buildings
    for i in range(app.buildingCount):
        color = app.buildingColors[i]
        left, top, width, height = getBuildingBounds(app, i)
        drawRect(left, top, width, height, fill = color, border = 'black', borderWidth = 2)  
        numWindows = height // 15
        for i in range(numWindows):
            for j in range(4):
                drawRect(left + (width / 6)*(j+1), top + (height / numWindows)*(i+1), 5, 5, fill = 'gold', border = 'blue', borderWidth = 0.5)
    #draw holes
    for cx, cy in app.holes:
        drawCircle(cx, cy, app.holeRadius, fill = 'mediumSlateBlue')
        explosionCx, explosionCy = cx, cy
    #showing an explosion when hitting a building
    if app.showExplosion:
        drawStar(explosionCx, explosionCy, app.explosionRadius, 15, fill = 'orange' if app.explosionRadius % 2 == 0 else 'red')
    # draw players
    for player in range(len(app.players)):
        cx, cy, color = app.players[player]
        drawCircle(cx, cy, app.playerRadius, fill = color)
    # draw player's turn
    drawLabel(f'BlotShooter!', app.width / 2, 20, size=20, bold = True, fill = 'white')
    if app.currentPlayer == 0:
        currPlayer = 'Pink'
    else:
        currPlayer = 'Blue'
    if not app.gameOver:
        drawLabel(f'Current Player: {currPlayer}', app.width / 2, 50, size=20, fill = 'white')
    #draw blot
    if app.showBlot:
        drawCircle(app.blotCx, app.blotCy, app.playerRadius, fill = app.blotColor)
        
    if app.gameOver:
        drawLabel('Game Over', app.width / 2, app.height / 4, size = 30, bold = True, fill = 'white')
        drawLabel('Press n for new game', app.width / 2, app.height / 4 + 20, fill = 'white')
        #drawing small explosion on losing character
        cx, cy, color = app.players[1 - app.currentPlayer] 
        drawStar(cx, cy, 20, 12, fill = 'red')
        drawStar(cx, cy, 15, 12, fill = 'orange')
        drawStar(cx, cy, 10, 12, fill = 'yellow')


def onStep(app):
    app.step += 1
    if app.showExplosion:
        app.explosionRadius += 5
    if app.explosionRadius == app.holeRadius:
        app.explosionRadius = 10
        app.showExplosion = False
    if app.showBlot and not app.gameOver:
        app.blotCx += app.dx
        app.blotCy += app.dy
        app.dy += 0.3
        #check if dots intersect
        cx, cy, color = app.players[1 - app.currentPlayer] 
        blotR = app.playerRadius
        if distance(app.blotCx, app.blotCy, cx, cy) <= app.playerRadius + blotR: 
            app.gameOver = True 
        if ((app.blotCx < 0) or (app.blotCx > app.width) or (app.blotCy > app.height)):
            app.showBlot = False
            app.currentPlayer = 1 - app.currentPlayer
        else:
            #check if hit building
            for i in range(app.buildingCount):
                left, top, width, height = getBuildingBounds(app, i)
                if ((left <= app.blotCx <= left + width) and (top <= app.blotCy <= top + height) and not (inHole(app))):
                    #we just hit a building
                    app.showBlot = False
                    app.showExplosion = True
                    app.holes.append((app.blotCx, app.blotCy))
                    app.currentPlayer = 1 - app.currentPlayer
 
def inHole(app):
    for hole in range(len(app.holes)):
        cx, cy = app.holes[hole]
        if distance(app.blotCx, app.blotCy, cx, cy) <= app.holeRadius:
            return True
    return False
 
def distance(x0, y0, x1, y1):
    return ((x0 - x1)**2 + (y0 - y1)**2)**0.5

def onMousePress(app, mouseX, mouseY):
    if not app.gameOver:
        if app.showBlot:
            app.showExplosion = False
            return
        app.blotCx, app.blotCy, app.blotColor = app.players[app.currentPlayer]
        dx = (mouseX - app.blotCx) / 20 
        dy = (mouseY - app.blotCy) / 20
        app.dx, app.dy = dx, dy 
        app.showBlot = True


def onKeyPress(app, key):
    if key == 'n':
        startNewGame(app)
    
    
    
def main():
    runApp()
main()
