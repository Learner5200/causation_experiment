def causation(condition, window):

    # === IMPORTS ===
    import pygame

    # === CONSTANTS ===

    # Variables from the main program
    condition = condition
    window = window # 'window' variable is used to allow variables to be overwritten in scope of functions

    # General Shape Parameters
    BALL_SIZE = 80
    TARGET_SIZE = 50
    KEY_SIZE = 20
    GOAL_SIZE = 120

    MAIN_BACKGROUND_COLOUR = (255, 255, 255)
    BALL_COLOUR = (0, 0, 255)
    TARGET_COLOUR = (255, 0, 0)
    TRIANGLE_COLOUR = (255, 255, 0)
    KEY_COLOUR = (0, 255, 0)
    LOCK_COLOUR = (0, 0, 0)
    GOAL_COLOUR = (255, 0, 255)

    # Text
    WIN_MESSAGE = 'Congratulations!\nRound {0} complete. Press SPACE to continue.'
    FONT_COLOUR = (255, 0, 0)

    # Buttons
    BUTTON_SIZE = 40

    BUTTONS_BACKGROUND_COLOUR = (230, 230, 230)
    PLAY_COLOUR = (0, 200, 0)
    PLAY_BACKGROUND_DEFAULT = (230, 230, 230)
    PLAY_BACKGROUND_CLICKED = (200, 200, 200)
    RESET_COLOUR = (60, 60, 60)
    RESET_BACKGROUND_DEFAULT = (255, 165, 0)
    RESET_BACKGROUND_CLICKED = (180, 115, 0)

    # Cursor
    DEFAULT_CURSOR = pygame.cursors.arrow
    DRAG_CURSOR = pygame.cursors.broken_x # Cursor when hovering over draggable objects


    # Physics
    REPEL_MAGNITUDE = 1 # Strength of ball repulsion force
    REPEL_RANGE = 300 # Effective range of ball repulsion force
    GOAL_RANGE = GOAL_SIZE / 2 # Required closeness to goal

    TICK_DURATION = 25 # Length of each frame
    ticksPerSecond = 1000 / TICK_DURATION

    # This dictionary defines the number of rounds, and the shapes of each type present in each round, defined by their
    # parameter values (see class definitions).
    SHAPES = {

        1: {
            'Balls': [
            ],

            'Targets': [
                (600, 500, TARGET_SIZE, TARGET_SIZE, 0, 0, -10, 0, True, True)
            ],

            'Keys': [
            ],

            'Locks': [
            ],

            'Goals': [
                (100, 100, GOAL_SIZE, GOAL_SIZE, False)
            ]
        },

        2: {
            'Balls': [
                (250, 350, BALL_SIZE, BALL_SIZE, True)
            ],

            'Targets': [
                (400, 500, TARGET_SIZE, TARGET_SIZE, 0, 0, 0, 0, False, True)
            ],

            'Keys': [
            ],

            'Locks': [
            ],

            'Goals': [
                (800, 100, GOAL_SIZE, GOAL_SIZE, False)
            ]
        },

        3: {
            'Balls': [
                (500, 200, BALL_SIZE, BALL_SIZE, True)
            ],

            'Targets': [
                (600, 200, TARGET_SIZE, TARGET_SIZE, 0, 0, 0, 0, True, False)
            ],

            'Keys': [
                (600, 400, KEY_SIZE, KEY_SIZE, 0, 0, 0, 0, True)
            ],

            'Locks': [
                (1000, 550, KEY_SIZE, GOAL_SIZE, False)
            ],

            'Goals': [
                (100, 600, GOAL_SIZE, GOAL_SIZE, False)
            ]
        },

        4: {
            'Balls': [
                (500, 200, BALL_SIZE, BALL_SIZE, True),
                (900, 600, BALL_SIZE, BALL_SIZE, False)
            ],

            'Targets': [
                (300, 200, TARGET_SIZE, TARGET_SIZE, 0, 0, 0, 0, True, False)
            ],

            'Keys': [
                (600, 400, KEY_SIZE, KEY_SIZE, 0, 0, 0, 0, True)
            ],

            'Locks': [
                (500, 550, KEY_SIZE, GOAL_SIZE, False)
            ],

            'Goals': [
                (900, 100, GOAL_SIZE, GOAL_SIZE, False)
            ]
        },

        5: {
            'Balls': [
                (750, 610, BALL_SIZE, BALL_SIZE, False),
                (300, 160, BALL_SIZE, BALL_SIZE, False)
            ],

            'Targets': [
                (520, 625, TARGET_SIZE, TARGET_SIZE, 0, 0, 0, 0, False, False)
            ],

            'Keys': [
                (460, 190, KEY_SIZE, KEY_SIZE, 0, 0, 0, 0, False)
            ],

            'Locks': [
                (700, 140, KEY_SIZE, GOAL_SIZE, False)
            ],

            'Goals': [
                (300, 590, GOAL_SIZE, GOAL_SIZE, False)
            ]
        }

    }

    # This dictionary defines the instruction message (if any) to be presented prior to each round.
    INSTRUCTIONS = {
        1: 'You will now play a puzzle game where your aim is to put a yellow triangle into a purple goal. To achieve this you can move certain objects. To find out which objects are moveable, put your mouse cursor over them. If the object can be moved, the cursor will change to a cross.\n\nAfter you position the various objects, click play (or press ‘p’ on the keyboard) to see whether your triangle will reach the box. If you fail to get the triangle into the box, you may click reset (or press ‘r’ on the keyboard) to reload the scene and try again. You have as many attempts as you need.\n\nPress SPACE when ready to get started.',
        2: '',
        3: 'Well done! From the next stage, your goal will be to put a red square into the purple goal. However, the purple box still only accepts yellow triangles. So you need to find a way to transform the square into a triangle before it reaches the goal.\n\nPress SPACE when ready to continue.',
        4: '',
        5: 'On the following screen, please click play (or press ‘p’ on the keyboard) and carefully observe what happens to the objects. You will not be able to control the objects. \n\nPress SPACE when ready to continue.'
    }

    # === FUNCTIONS ===

    def listOfLines(text, maxCharacters):
        # Turns text into slices of a given maximum length (sliced at each linebreak, and otherwise at the first space
        # before this maximum length), and returns a list of these slices; this is necessary because Pygame can only
        # render text one line at a time
        lines = []
        startPoint = 0
        search = True
        while search == True:
            if '\n' in text[startPoint:startPoint+maxCharacters]:
                nextPoint = text.find('\n', startPoint, startPoint + maxCharacters)
                lines.append(text[startPoint:nextPoint])
                startPoint = nextPoint + 1
            elif startPoint <= len(text) - maxCharacters - 1:
                nextPoint = text.rfind(' ', 0, startPoint + maxCharacters)
                lines.append(text[startPoint:nextPoint])
                startPoint = nextPoint + 1
            else:
                nextPoint = len(text)
                lines.append(text[startPoint:nextPoint])
                search = False
        return lines

    def createTextSurface(text, maxCharacters):
        # Renders each line in a list of lines to a surface and blits each surface to the screen, starting partway
        # down and spaced appropriately, centred horizontally.
        lineList = listOfLines(text, maxCharacters)
        font = pygame.font.SysFont(None, 30)
        numberOfLines = 0
        for line in lineList:
            numberOfLines += 1
            currentLine = font.render(line, True, FONT_COLOUR)
            currentXPosition = (SCREEN_WIDTH - currentLine.get_width()) / 2 # centres the line
            currentYPosition = ((SCREEN_HEIGHT * 0.2) + (currentLine.get_height() * numberOfLines))
            currentPosition = (currentXPosition, currentYPosition)
            screen.blit(currentLine, currentPosition)

    def Instructions():
        # Presents the relevant screen of instructions, if any, prior to each round
        while window.showInstructions == True:
            screen.fill(MAIN_BACKGROUND_COLOUR)
            createTextSurface(INSTRUCTIONS[window.currentRound], 90)

            # Moves on from the instruction screen upon pressing SPACE
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    window.showInstructions = False
            pygame.display.update()

    def initialiseRound(round):
        # Sets up a new round, creating shapes from the parameters in the dictionary above.
        window.roundComplete = False
        window.begin = False
        if round == len(SHAPES):
            pygame.time.set_timer(triangleEvent, 0)  # Cancels triangle timer if user resets final round
            window.triangleTimerCount = 0 # Allows timer to be called again if user resets final round
        # These lists keep track of the shapes within each category, and are populated as the objects are
        # constructed from the relevant class
        window.shapes = []
        window.balls = []
        window.targets = []
        window.keys = []
        window.goals = []
        window.locks = []

        for item in SHAPES[round]['Balls']:
            ball(*item) # The '*' ensures that the parameters are taken from the tuples in the dictionary
        for item in SHAPES[round]['Targets']:
            target(*item)
        for item in SHAPES[round]['Keys']:
            key(*item)
        for item in SHAPES[round]['Locks']:
            lock(*item)
        for item in SHAPES[round]['Goals']:
            goal(*item)

    def playPause():
        # Toggles the state of the round from playing (objects exert forces etc.) to paused and vice versa
        window.begin = 1 - window.begin

    def next():
        # Moves to next round by incrementing the round counter, displaying instructions if specified, and initialising

        # Prevents attempted setup of rounds not specified in the dictionary
        if window.currentRound >= len(SHAPES):
            window.is_running = False

        else:
            window.currentRound += 1
            if INSTRUCTIONS[window.currentRound] != '':
                window.showInstructions = True
            initialiseRound(window.currentRound)

    def cursorChange():
        # Changes the cursor when the mouse hovers over a draggable object.
        mousePosition = pygame.mouse.get_pos()
        overlappingDraggables = [shape for shape in window.shapes if
                                 (shape.drag == True and shape.collidepoint(mousePosition))]
        if overlappingDraggables == []:
            pygame.mouse.set_cursor(*DEFAULT_CURSOR)
        else:
            pygame.mouse.set_cursor(*DRAG_CURSOR)


    # === CLASSES ===

    class ball(pygame.Rect):
        # Balls exert a force in all directions on targets and keys
        def __init__(self, left, top, width, height, drag):
            super().__init__(left, top, width, height)
            self.drag = drag # Boolean, determines whether item can be dragged
            window.shapes.append(self)
            window.balls.append(self)

        def repel(self, magnitude, range):
            # Exerts a force on targets and keys within range every tick, increasing with their distance from the ball
            for shape in (window.targets + window.keys):
                xDistance = float(shape.centerx - self.centerx)
                yDistance = float(shape.centery - self.centery)
                if abs(xDistance) < range and abs(yDistance) < range:
                    shape.velocityX += (magnitude * xDistance)
                    shape.velocityY += (magnitude * yDistance)

    class moveableRect(pygame.Rect):
        # moveableRect objects have velocity and acceleration, and update their position each tick according to these
        def __init__(self, left, top, width, height, startingVelocityX, startingVelocityY, startingAccelerationX,
                     startingAccelerationY, drag):
            super().__init__(left, top, width, height)
            self.velocityX = startingVelocityX
            self.velocityY = startingVelocityY
            self.accelerationX = startingAccelerationX
            self.accelerationY = startingAccelerationY
            self.drag = drag
            window.shapes.append(self)

        def naturalMove(self):
            # Updates position according to velocity, and velocity according to acceleration, each tick
            self.velocityX += self.accelerationX
            self.x += self.velocityX / ticksPerSecond # Ensures that velocity values are per-second increases
            self.velocityY += self.accelerationY
            self.y += self.velocityY / ticksPerSecond

        def wallBounce(self):
            # Optional, unused method: causes moveableRects to bounce off of the walls of the screen
            if self.left < 0 or self.right > SCREEN_WIDTH:
                self.accelerationX = 0 - (self.accelerationX)
                self.velocityX = 0 - (self.velocityX)
            if self.top < 0 or self.bottom > SCREEN_HEIGHT:
                self.accelerationY = 0 - (self.accelerationY)
                self.velocityY = 0 - (self.velocityY)

    class target(moveableRect):
        # Targets can become triangles: the aim is to get them into the goal
        def __init__(self, left, top, width, height, startingVelocityX, startingVelocityY, startingAccelerationX,
                     startingAccelerationY, drag, triangle):
            super().__init__(left, top, width, height, startingVelocityX, startingVelocityY, startingAccelerationX,
                             startingAccelerationY, drag)
            self.triangle = triangle # Boolean, determines whether item is triangle or square
            window.targets.append(self)

    class key(moveableRect):
        # Keys cannot become triangles: the aim is to fire them into the lock
        def __init__(self, left, top, width, height, startingVelocityX, startingVelocityY, startingAccelerationX,
                     startingAccelerationY, drag):
            super().__init__(left, top, width, height, startingVelocityX, startingVelocityY, startingAccelerationX,
                             startingAccelerationY, drag)
            window.keys.append(self)

    class lock(pygame.Rect):
        # Locks cause targets to become triangles when hit by a key
        def __init__(self, left, top, width, height, drag):
            super().__init__(left, top, width, height)
            self.drag = drag
            window.shapes.append(self)
            window.locks.append(self)

        def unlock(self):
            # 'Sticks' keys to it by stopping their motion, and changes all targets to triangles
            for shape in window.keys:
                if self.colliderect(shape):
                    shape.velocityX = 0
                    shape.velocityY = 0
                    shape.accelerationX = 0
                    shape.accelerationY = 0
                    if window.currentRound < len(SHAPES):
                        for shape in window.targets:
                            shape.triangle = True
                    else:
                        window.roundComplete = True #Completes final round, where this is the final event

    class goal(pygame.Rect):
        # Goals repel non-triangle targets, and attract triangle targets, completing the round.
        def __init__(self, left, top, width, height, drag):
            super().__init__(left, top, width, height)
            self.drag = drag
            window.shapes.append(self)
            window.goals.append(self)

        def bounce(self):
            # Causes non-triangle targets to bounce off
            for shape in window.targets:
                if shape.triangle == False and self.colliderect(shape):
                    if shape.left < self.right or shape.right > self.left:
                        shape.accelerationX = 0 - (shape.accelerationX)
                        shape.velocityX = 0 - (shape.velocityX)
                    if shape.top < self.bottom or shape.bottom > self.top:
                        shape.accelerationY = 0 - (shape.accelerationY)
                        shape.velocityY = 0 - (shape.velocityY)

        def attract(self, range):
            # Causes triangles within range to enter and stay at the centre of the goal, and the round to complete
            for shape in window.targets:
                xDistance = shape.centerx - self.centerx
                yDistance = shape.centery - self.centery
                if abs(xDistance) < range and abs(yDistance) < range and shape.triangle == True:
                    shape.velocityX = 0
                    shape.velocityY = 0
                    shape.accelerationX = 0
                    shape.accelerationY = 0
                    shape.centerx = self.centerx
                    shape.centery = self.centery
                    window.roundComplete = True

        def violateCausalLaws(self):
            # Allows target to enter the goal without turning into a triangle
            for shape in window.targets:
                if self.colliderect(shape):
                    shape.velocityX = 0
                    shape.velocityY = 0
                    shape.accelerationX = 0
                    shape.accelerationY = 0
                    shape.centerx = self.centerx
                    shape.centery = self.centery
                    if window.triangleTimerCount == 0:
                        pygame.time.set_timer(triangleEvent, 150) # Timer to transform target before key hits lock
                        window.triangleTimerCount += 1

    # === SETUP ===

    pygame.init()

    # Sets width and height of screen according to parameters of the desktop
    desktop = pygame.display.Info()
    SCREEN_WIDTH = desktop.current_w
    SCREEN_HEIGHT = desktop.current_h
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


    # Creates a surface for play and reset buttons
    buttonSurfaceWidth = SCREEN_WIDTH
    buttonSurfaceHeight = int(SCREEN_HEIGHT / 10)
    buttonSurface = pygame.Surface((buttonSurfaceWidth, buttonSurfaceHeight))
    buttonSurfaceRect = buttonSurface.get_rect()
    buttonSurface.fill(BUTTONS_BACKGROUND_COLOUR)

    #Creates play and reset buttons to the left and right of the surface's centre,
    playButton = pygame.Rect((buttonSurfaceRect.centerx - BUTTON_SIZE * 2),
                             (buttonSurfaceRect.centery - BUTTON_SIZE / 2), BUTTON_SIZE, BUTTON_SIZE)
    resetButton = pygame.Rect((buttonSurfaceRect.centerx + BUTTON_SIZE), (buttonSurfaceRect.centery - BUTTON_SIZE / 2),
                              BUTTON_SIZE * 2, BUTTON_SIZE)

    # Sets background colour for buttons to default values; these will change on mouse-over
    playBackground = PLAY_BACKGROUND_DEFAULT
    resetBackground = RESET_BACKGROUND_DEFAULT

    # Determines starting round according to condition; those in the control condition see only the final round
    if condition == 'experimental':
        window.currentRound = 1
    elif condition == 'control':
        window.currentRound = len(SHAPES)

    selected = None # By default, no shape is selected
    window.showInstructions = True # Instructions are shown for the first round

    triangleEvent = pygame.USEREVENT+1 # Creates a user event; will be used to turn target into triangle in final round
    window.triangleTimerCount = 0 # Needed to ensure the timer for the above event is set only once in the main loop
    # (otherwise, timers longer than the tick duration will never trigger their events, as each new timer will push the
    # event into the future

    initialiseRound(window.currentRound)
    clock = pygame.time.Clock() # Sets up the clock whose ticks determine the framerate
    window.is_running = True


    # === MAIN LOOP ===

    while window.is_running:

        Instructions()
        cursorChange()

        # Checks for events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                window.is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window.is_running = False
                    # Allows users to pause and reset the round with buttons
                if event.key == pygame.K_p:
                    playPause()
                if event.key == pygame.K_r:
                    initialiseRound(window.currentRound)

                # Allows users to move past the instructions by pressing space.
                if event.key == pygame.K_SPACE and window.roundComplete == True:
                    next()
                if event.key == pygame.K_RIGHT:  # Allows tester to skip through the rounds; disable before experiment
                    next()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Selects shapes clicked on and adds an offset to track position relative to mouse
                    for shape in window.shapes:
                        if shape.drag == True and shape.collidepoint(event.pos):
                            selected = shape
                            window.selectedOffsetX = shape.x - event.pos[0]
                            window.selectedOffsetY = shape.y - event.pos[1]

                    # Enables playing/pausing and resetting by clicking buttons, with change to colour on click
                    if playButton.collidepoint(event.pos):
                        playBackground = PLAY_BACKGROUND_CLICKED
                        playPause()
                    if resetButton.collidepoint(event.pos):
                        resetBackground = RESET_BACKGROUND_CLICKED
                        initialiseRound(window.currentRound)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    selected = None

                # Returns button colour to default after releasing click
                if playBackground == PLAY_BACKGROUND_CLICKED:
                    playBackground = PLAY_BACKGROUND_DEFAULT
                if resetBackground == RESET_BACKGROUND_CLICKED:
                    resetBackground = RESET_BACKGROUND_DEFAULT

            elif event.type == pygame.MOUSEMOTION:
                if selected is not None:
                    # Moves selected object with mouse
                    selected.x = event.pos[0] + window.selectedOffsetX
                    selected.y = event.pos[1] + window.selectedOffsetY

            elif event.type == triangleEvent:
                for shape in window.targets:
                    shape.triangle = True

        if window.begin == True:
            # Boolean determines whether shapes exert forces on one another or not (i.e. 'play' vs 'pause' states)
            for shape in window.goals:
                if window.currentRound == len(SHAPES):
                    shape.violateCausalLaws() # In the fifth round, the causal laws are violated!
                else:
                    shape.attract(GOAL_RANGE)
                    shape.bounce()
            for shape in window.locks:
                shape.unlock()
            for shape in window.balls:
                shape.repel(REPEL_MAGNITUDE, REPEL_RANGE)
            for shape in (window.targets + window.keys):
                shape.naturalMove()

        # Draws to screen
        screen.fill(MAIN_BACKGROUND_COLOUR)

        pygame.draw.rect(buttonSurface, playBackground, playButton)
        pygame.draw.polygon(buttonSurface, PLAY_COLOUR, ( # Draws 'play' symbol onto play button
            playButton.topleft,
            playButton.bottomleft,
            playButton.midright
        ))
        pygame.draw.rect(buttonSurface, resetBackground, resetButton)

        # Creates button text to blit onto button location
        resetFont = pygame.font.SysFont(None, 30)
        resetText = resetFont.render('RESET', True, RESET_COLOUR)
        resetX = resetButton.centerx - resetText.get_width() / 2
        resetY = resetButton.centery - resetText.get_height() / 2
        buttonSurface.blit(resetText, (resetX, resetY))

        screen.blit(buttonSurface, (0, 0)) # Blits surface with all the buttons on it to the main surface

        # Draws all shapes that have been created in the round in their current positions
        for shape in window.goals:
            pygame.draw.rect(screen, GOAL_COLOUR, shape)
        for shape in window.locks:
            pygame.draw.rect(screen, LOCK_COLOUR, shape)
        for shape in window.targets:
            if shape.triangle == True: #Draws a triangle instead of a red square
                pygame.draw.polygon(screen, TRIANGLE_COLOUR, (
                    shape.bottomleft,
                    shape.midtop,
                    shape.bottomright
                ))
            else:
                pygame.draw.rect(screen, TARGET_COLOUR, shape)
        for shape in window.keys:
            pygame.draw.rect(screen, KEY_COLOUR, shape)
        for shape in window.balls:
            pygame.draw.circle(screen, BALL_COLOUR, shape.center, int(shape.width / 2))

        # Presents a congratulations message when the round is complete
        if window.roundComplete == True:
            createTextSurface(WIN_MESSAGE.format(window.currentRound), 90)

        pygame.display.update()
        clock.tick(TICK_DURATION)

    # === END OF MAIN LOOP ===

    pygame.quit()
