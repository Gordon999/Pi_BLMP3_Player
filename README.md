# Pi_BLMP3_Player

This version will also display with 20 leds which track is playing.

10 button switches for letters A to J, 10 button switches for numbers 1 to 10. 3 buttons required for STOP, SHUFFLE and SHUTDOWN.

A coin slot switch also connects between gpio and gnd. (can be disabled in the code)

Select a song (upto 100), stored in home/pi/Music, by choosing a LETTER and then a NUMBER, eg A3.

Can be operated in Continuous Play Mode. Press Button B for 5 seconds to operate. It will play tracks until STOP pressed for 5 seconds. In Continuous Play Mode: - A will play previous track, C will play next track, D will skip 10 tracks back, E will skip 10 tracks forward.

Continuous Play Mode can play more than 100 songs. It can shuffle the songs, settable in the code.

To just use Continuous Play Mode you could just fit buttons A,B,C,D,E, STOP and SHUTDOWN.

## Schematic

![Schematic](Schematic01.jpg)
![Schematic](Schematic02.jpg)

## Showing Playing Track B5
![Prototype](prototype001.jpg)
