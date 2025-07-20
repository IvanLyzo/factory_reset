# Factory Reset
Note that this README file is still in development, so anything written here may or may not be removed or changed at any point. Any references to time-sensitive information (i.e. "current", "latest", etc.) are likely incorrect and will need to be modified. Feel free to read, but keep this in mind.

---

## Problems & Extensions

The current version of the game, as it is presented, was done as a final assignment for a highschool course in one week (June 16th - June 23rd). As such, time crunch was a big factor in the decisions made, both with the code and assets—all of which are hand-made. Due to this limiting factor, corners had to be cut from an already simplified version of the inital idea. I may or may not decide to continue development for personal reasons, but as of right, the code in this repository is what was submitted and evaluated. The following will be a compilation of known issues or inadequacies with the game that could not be fixed with the time allowed.

### Collisions
You may or may not notice that the collisions for all sprites are pygame Rect objects. Furthermore, all of these Rects are sized at init, and their size not modified further on. Sprites, on the other hand, are not all perfect squares or rects—in fact most aren't—and are also modified after init in the form of animations or alternate sprite images being loaded for turning and such. This leads to a drift between the collision Rect and the sprite visual, meaning that sometimes you may get treated unfairly. For example, the player's Rect is a perfect square of TILESIZE (16, constant), but the graphics are not only not square, but are also animated and switch depending on the direction the player is going in. This can lead to bullets colliding logically (based on Rect) but not visually. An obvious solution would be to tie the collision to the sprite, however I did not have time to implement this.
