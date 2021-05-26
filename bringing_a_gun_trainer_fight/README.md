# Bringing a Gun to a Trainer Fight

## Readme
```
Bringing a Gun to a Trainer Fight
=================================

Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny trainers! Fortunately, you grabbed a beam weapon from an abandoned storeroom while you were running through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the bunny trainers: its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits either you or the bunny trainer, it will stop immediately (albeit painfully). 

Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

For example, if you and the elite trainer were positioned in a room with dimensions [3, 2], your_position [1, 1], trainer_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the elite trainer (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite trainer with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the elite trainer with a total shot distance of sqrt(5).
```

## Hints
* mirrored rooms/angles
* trainer radius is 0

## Analysis and Explanation
At first I thought this was impossible because there could be an infinite number of possible solutions. Take the case where you're at `(1,1)` and the trainer is at `(2,1)`.
If you shoot at `(9999, 1)` then you'll still hit the trainer because that's an angle of ~0.005 degrees. I was stumped for a little bit, so I did some googling (googleing?)
and found a blog post. I skimmed and saw two words: "mirror" and "angle" and closed the page. If you're looking for hints, I've listed them above so you don't have to see
any more of my analysis if you want to figure it out on your own. Turns out that we have to assume that the trainer we're trying to shoot is infinitely skinny, that's the
only way we can get a precise number of answers.

So what do I mean by mirrored? Let's look at an even more basic example: a room 5 wide by 2 tall, we are at `(1,1)` and the trainer/guard is at `(3,1)`.
If we shoot at the angle 0° then we'll hit him for sure. But if you shoot up and at an angle your shot will bounce off the wall and still hit him, so how
do we figure out exactly where to fire at on the wall to shoot the guard? Imagine for a moment a mirrored copy of the main room sitting directly above it.
This puts you at `(1, -1)` and the guard at `(3,-1)`. The angle from your **original** position to the **imaginary** guard is a 45° angle.
Go ahead, do the math. I'll wait. Now if you imagine how that shot will bounce in the real room, it'll bounce off the wall at a 45° angle, and then hit
the real guard, yay! So firing at `(3,-1)` is a valid option. In addition the distance from your **real** position to the **fake** guard's position
is the same distance as the bouncing ray, so there's no extra math to deal with.

Now that we have a basic example out of the way, let's talk details. For this to work you have to properly mirror the rooms, either on the X axis, Y axis,
or both. For example the mirrored room copy at `(2,2)` (in room coordinates) is an exact duplicate of the original room, while the room at `(1,1)` is
mirrored on both the X and Y axes. Also note that you only need to locations of your mirrored self and the mirrored guard, you don't need any mirrored room
dimensions or things like that. Finally, make sure you're not shooting *through* yourself to shoot at the guard, sorting by distance may help
with this.

