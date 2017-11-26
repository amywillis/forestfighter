#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import time
import sys
import pygame
from robot import AmyBot, CamJamBot
from joystick import Joystick
from argparse import ArgumentParser
import logging


LOGGER = logging.getLogger(__name__)


def main(amybot=True, camjambot=False):
    joystick = Joystick()
    if amybot:
        bot = AmyBot()
    else:
        bot = CamJamBot()
    # Re-direct our output to standard error, we need to ignore standard out to hide some nasty print statements from pygame
    sys.stdout = sys.stderr

    interval = 0.0

    # Power settings
    voltageIn = 6.0                        # Total battery voltage to the PicoBorg Reverse
    voltageOut = 5.0 #* 0.95                # Maximum motor voltage, we limit it to 95% to allow the RPi to get uninterrupted power

    # Setup the power limits
    if voltageOut > voltageIn:
        maxPower = 1.0
    else:
        maxPower = voltageOut / float(voltageIn)

    # Setup pygame and wait for the joystick to become available

    try:
        LOGGER.info('Press CTRL+C to quit')
        running = True
        # Loop indefinitely
        while running:
            # Get the latest events from the system
            hadEvent = False
            events = pygame.event.get()
            # Handle each event individually
            for event in events:
                if event.type == pygame.QUIT:
                    # User exit
                    running = False
                    break
                elif event.type == pygame.JOYBUTTONDOWN:
                    # A button on the joystick just got pushed down
                    hadEvent = True
                elif event.type == pygame.JOYAXISMOTION:
                    # A joystick has been moved
                    hadEvent = True
                if hadEvent:
                    # Read axis positions (-1 to +1) + determine how much to move by
                    left_drive, right_drive = joystick.get_reading()
                    bot.move(left_drive, right_drive)
            time.sleep(interval)

    except KeyboardInterrupt:
        # CTRL+C exit, disable all drives
        #LeftMotor.speed(0)
        #RightMotor.speed(0)
        LOGGER.debug('Motors off')


if __name__ == '__main__':
    parser = ArgumentParser()
    # either amybot or camjambot can be passed in, but not both.
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--amybot", help="Use the kit amy has (whatever Jim provided)")
    group.add_argument("--camjambot", help="Use the camjam edubot kit")
    args = parser.parse_args()

    main(args.amybot, args.camjambot)