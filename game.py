import arcade
import os
import random

# Constants for the game
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Frog Adventures"

TILE_SCALING = 1
PLAYER_JUMP_SPEED = 3
PLAYER_DOUBLE_JUMP_SPEED = 2
GRAVITY = .25

MOVEMENT_SPEED = .6
UPDATES_PER_FRAME = 5

RIGHT_FACING = 0
LEFT_FACING = 1

CHARACTER_SCALING = 1
FOLLOW_DECAY_CONST = 0.3

PLAYER_CLIMB_SPEED = .5


BULLET_SPEED = -1
BULLET_TEXTURE = "rocky_roads/Enemies/bullet.png" 
BULLET_SCALING = 1

QUICKSAND_SPEED_DEBUFF = 0.3

BOUNCE_FORCE = 10
MAX_JUMPS = 2



class GameEnd(arcade.View):
    """
    Menu display for when user completes all three levels, displaying 
    final time and score, while allowing for the option to restart
    or exit the game. 
    """
    def __init__(self, final_score, final_time):
        """
        Initializes the GameEnd view
        Incorporating the final score of the user and the time taken
        to reach the end.
        """
        super().__init__()
        self.final_score = final_score
        self.final_time = f"{final_time:.2f}s"
        
    def on_show_view(self):
        """
        Call when the view is active.
        """
        self.window.background_color = arcade.color.OLD_GOLD
    
    def on_draw(self):
        """
        Drwas the game end screen relevant text.
        """
        self.clear()
        arcade.draw_text("You beat the game! \nCongratulations, ",
                         WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                         arcade.color.BLACK,
                         font_size=40, anchor_x="center")
        
        arcade.draw_text("you are now more financially stable.",
                         WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 45,
                         arcade.color.BLACK,
                         font_size=40, anchor_x="center")
        
        arcade.draw_text(f"You beat the game in {self.final_time},"
                         f"with a score of {self.final_score}!",
                         WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 75,
                         arcade.color.BLACK, font_size = 25,
                         anchor_x="center")
                         
        arcade.draw_text("Press ENTER to quit,"
                        " or CLICK anywhere to restart.",
                         WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 120,
                         arcade.color.BLACK,
                         font_size = 25, anchor_x="center")
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        Handles mouse interactions, identifying location of cursor,
        button pressed and other modifiers, ensuring that the user
        is directed to the GameView() when a mouse button is used..
        """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
        
    def on_key_press(self, key, modifiers):
        """
        Handles keyboard interaction, identifying what key is pressed,
        in this case when the user presses ENTER, it closes the window.
        """
        if key == arcade.key.ENTER:
            arcade.exit()

class MenuView(arcade.View):
    """
        Main menu displayed when the game starts, showcasing the tile.
    """
    def on_show_view(self):
        """
        Sets the background colour of the view. 
        """
        self.window.background_color = arcade.color.COSMIC_LATTE

    def on_draw(self):
        """
        Renders the menu screen and adds text to the view.
        """
        self.clear()
        arcade.draw_text("Welcome to Frog Adventures",
        WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
        arcade.color.BLACK, font_size=50, anchor_x="center")
        
        arcade.draw_text("Click to advance", WINDOW_WIDTH / 2,
        WINDOW_HEIGHT / 2 - 75, arcade.color.GRAY, font_size=25,
        anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handles mouse interactions, identifying location
        and button utilsied. In this case, any mouse button
        will direct user to the instructions menu. """
        instruction_view = InstructionView()
        self.window.show_view(instruction_view)


class InstructionView(arcade.View):
    """Menu used to deliver the instructions of the game to the user"""
    def on_show_view(self):
        """Sets background colour of the view."""
        self.window.background_color = arcade.color.GO_GREEN

    def on_draw(self):
        """Renders the view, placing the text."""
        self.clear()
        arcade.draw_text("You are a Frog, collect as" 
                         " many diamonds and coins in the",
                         WINDOW_WIDTH / 2, 
                         WINDOW_HEIGHT / 2,
                         arcade.color.BLACK, font_size=25, anchor_x="center")
        
        arcade.draw_text("shortest amount time\n" 
                         " to be most succesful in the future.",
                         WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2-45,
                         arcade.color.BLACK, font_size=25, anchor_x="center")
                         
        arcade.draw_text("A/D to move left and right,"
        "Space/W to jump, and double tap jump to double jump.",
        WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
                         
        arcade.draw_text("Click to advance", WINDOW_WIDTH / 2,
        WINDOW_HEIGHT / 2 - 175, arcade.color.GRAY, font_size=20,
        anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handles mouse interaction, directing user to the GameView
        when any mouse button is used."""
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameOverView(arcade.View):
    """Menu displayed when user loses all their lives."""
    def __init__(self, final_score, final_time):
        """Initialise the final score and final time at the time of
        the user losing all their lives, storing in variables."""
        super().__init__()
        self.final_score = final_score
        self.final_time = f"{final_time:.2f}s"

    def on_show_view(self):
        """Setting the background colour for the view."""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Rendering the view, placing and adding styling
        to the text."""
        self.clear()
        arcade.draw_text("Game Over", WINDOW_WIDTH / 2,
                         WINDOW_HEIGHT / 2 + 100, arcade.color.RED, 60,
                         anchor_x="center")
        
        arcade.draw_text(f"Final Score and Time: {self.final_score}pts"
                         f"and {self.final_time}.",
                         WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 25,
                         arcade.color.RED, 60, anchor_x="center")
        
        arcade.draw_text(f"Click to restart, or ENTER to quit.",
                         WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 150,
                         arcade.color.RED, 60, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """Handling keyboard interactions, identifying that when
        ENTER is pressed, the window closes."""
        if key == arcade.key.ENTER:
            arcade.exit()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Handling mouse interactions, ensuring that when a mouse
        button is clicekd GameView() is called, starting the game."""
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class PlayerCharacter(arcade.Sprite):
    """Player character sprite with animations"""
    def __init__(self, idle_texture_pairs,
                 walk_texture_pairs, jump_texture_pairs):
        """Initialize the plaer character
        and the textures for their movement"""
        self.character_face_direction = RIGHT_FACING
        self.cur_texture = 0

        self.idle_texture_pairs = idle_texture_pairs
        self.walk_textures = walk_texture_pairs
        self.jump_texture_pairs = jump_texture_pairs

        super().__init__(self.idle_texture_pairs[0], scale=CHARACTER_SCALING)
        
        # Limits and measures for the double jump function.
        self.jump_count = 0
        self.max_jumps = MAX_JUMPS

    def update_animation(self, delta_time: float = 1 / 60):
        """Update the players animations and textures based on
        current state and time."""
        # Redirecting characters direction based on movement.
        if self.change_x < 0:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0:
            self.character_face_direction = RIGHT_FACING
        
        if self.change_y > 0:
            self.cur_texture += 1
            if self.cur_texture >= (len(self.jump_texture_pairs)
                                    * UPDATES_PER_FRAME):
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.jump_texture_pairs[frame][direction]
            return

        
        if self.change_x == 0:
            self.cur_texture += 1
            if self.cur_texture >= (len(self.idle_texture_pairs)
                                    * UPDATES_PER_FRAME):
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction
            self.texture = self.idle_texture_pairs[frame][direction]
            return

        self.cur_texture += 1
        if self.cur_texture >= 8 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        direction = self.character_face_direction
        self.texture = self.walk_textures[frame][direction]


class Bullet(arcade.Sprite):
    """ Integrating bullet sprite fired by Cannon layer."""
    def __init__(self, filename, scale):
        """Initialize bullet sprite
        using arguments for the file location and tile scaling of the
        sprite."""
        super().__init__(filename, scale)
        self.should_be_removed = False

    def update(self, delta_time: float = 1/60): 
        """Update bullet position and identify location during
        time intervals. Identifying locatiob helps with configuring
        of the bullet sprite should be removed as it is passed map 
        borders."""
        super().update()
        # Identifying the bullets location and confirming its removal.
        if (self.right < 0 or self.left > WINDOW_WIDTH or
            self.bottom < 0 or self.top > WINDOW_HEIGHT):
            self.should_be_removed = True


class GameView(arcade.View):
    """Main game view, where the gameplay occurs and graphics 
    are displayed."""
    def __init__(self):
        """Initialize the game view."""
        super().__init__()

        # Initializing modules for use within the game.
        self.tile_map = None
        self.scene = None
        self.camera = None
        self.gui_camera = None
        self.player_sprite_list = None
        self.physics_engine = None

        self.player = None

        self.lives = 5
        self.font_size = 20
        self.font_color = arcade.color.WHITE

        self.score = 0
        self.level = 1
        self.time_taken = 0

        self.view_bottom = 0
        self.view_left = 0
        # Double jump check
        self.was_on_ground = False
        
        # Character resource path
        character = "frog_man/frog_man"
        # Updating sprite sheet animations
        # According to character movement
        self.idle_texture_pairs = []
        for i in range(8):
            texture = arcade.load_texture(f"{character}_idle{i}.png")
            self.idle_texture_pairs.append((texture,
                                            texture.flip_left_right()))

        self.walk_texture_pairs = []
        for i in range(8):
            texture = arcade.load_texture(f"{character}_walk{i}.png")
            self.walk_texture_pairs.append((texture,
                                            texture.flip_left_right()))

        self.jump_texture_pairs = []
        for i in range(2):
            texture = arcade.load_texture(f"{character}_jump{i}.png")
            self.jump_texture_pairs.append((texture,
                                            texture.flip_left_right()))
        # SpriteList storing and managing all active bullets in
        # the game.
        self.bullet_list = arcade.SpriteList()
        # Dictionary to keep track of firing cooldowns.
        self.cannon_fire_timers = {}
        # Flag indicating if user is on quicksand to enable debuff
        # Temp variable for modifying player speed in quicksand
        self.is_on_quicksand = False
        self.current_movement_speed =  MOVEMENT_SPEED
        
    

    def setup(self):
        """Set up game levels with platforms,
        enemies and collectibles."""
        # Enabling spatial hash to detect collisions frequently.
        layer_options = {
            "Platform": {
                "use_spatial_hash": True
            },
            "Coins": {
                "use_spatial_hash": True
            },
            "Danger": {
                "use_spatial_hash": True
            },
            "Diamond": {
                "use_spatial_hash": True
            },
            "x_moving_platform": {
                "use_spatial_hash": True
            },
            "y_moving_platform": {
                "use_spatial_hash": True
            },
            "moving_danger": {
                "use_spatial_hash": True
            },
            "Bounce": {
                "use_spatial_hash": True
            },
            "Quicksand": {
                "use_spatial_hash": True
            },
            "CrabEnemy": {
                "use_spatial_hash": True
            }
            
        }

        map_path = os.path.join(os.path.dirname(__file__),
                                f"level{self.level}.tmx")
        
        if not os.path.exists(map_path):
            raise FileNotFoundError(f"Level{self.level} map file missing.")

        self.tile_map = arcade.load_tilemap(
            map_path,
            scaling=TILE_SCALING,
            layer_options=layer_options,
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Camera settings to adjust scrolling follow view,
        # And detect map boundaries
        zoom_level = 3
        self.camera = arcade.Camera2D()
        self.camera.zoom = zoom_level

        map_width_pixels = self.tile_map.width * self.tile_map.tile_width
        map_height_pixels = self.tile_map.height * self.tile_map.tile_height

        half_screen_width = (self.window.width / 2) / zoom_level
        half_screen_height = (self.window.height / 2) / zoom_level

        self.camera_bounds = arcade.LRBT(
            left=half_screen_width,
            right=map_width_pixels - half_screen_width,
            bottom=half_screen_height,
            top=map_height_pixels - half_screen_height
        )

        # Managing player sprites and animations.
        self.player_sprite_list = arcade.SpriteList()

        self.player = PlayerCharacter(
            self.idle_texture_pairs,
            self.walk_texture_pairs,
            self.jump_texture_pairs,
        )
        # Spawn settings and priorities, dictating player spawn
        # Location and preferences.
        self.player.center_x = 60
        self.player.center_y = 160
        self.spawn_x = self.player.center_x
        self.spawn_y = self.player.center_y
        self.player_sprite_list.append(self.player)
        self.scene.add_sprite("Player", self.player)
        self.scene.add_sprite_list_before("Foreground", "Player")

        # Managing active sprites in map for specific layers.
        self.moving_danger_list = arcade.SpriteList()
        self.cannon_list = arcade.SpriteList()
        self.bounce_list = arcade.SpriteList()
        self.crab_enemy_list = arcade.SpriteList()
        
        # Appending tiles if in map to list.
        if "Bounce" in self.scene:
            self.bounce_list = self.scene["Bounce"]

        if "Cannon" in self.scene:
            self.cannon_list = self.scene["Cannon"]

        if "moving_danger" in self.scene:
            self.moving_danger_list = self.scene["moving_danger"]
            
        if "CrabEnemy" in self.scene:
            self.crab_enemy_list = self.scene["CrabEnemy"]
            
        # Bool for ladder climbing identification
        self.jump_key_pressed = False
        
        self.ladder_list = (self.scene["Ladder"] if "Ladder" 
                            in self.scene else arcade.SpriteList())
        # Boundary limits for moving platforms and enemies
        if "x_moving_platform" in self.scene:
            for platform in self.scene["x_moving_platform"]:
                platform.boundary_left = platform.center_x
                platform.boundary_right = platform.center_x + 260

        if "y_moving_platform" in self.scene:
            for platform in self.scene["y_moving_platform"]:
                platform.boundary_top = platform.center_y + 400
                platform.boundary_bottom = platform.center_y

        if "moving_danger" in self.scene:
            for platform in self.scene["moving_danger"]:
                platform.boundary_top = platform.center_y + 155
                platform.boundary_bottom = platform.center_y

        if "UpMovingPlatforms" in self.scene:
            for platform in self.scene["UpMovingPlatforms"]:
                platform.boundary_top = platform.center_y + 400
                platform.boundary_bottom = platform.center_y

        if "DownMovingPlatforms" in self.scene:
            for platform in self.scene["DownMovingPlatforms"]:
                platform.boundary_top = platform.center_y
                platform.boundary_bottom = platform.center_y - 400
                
        if "CrabEnemy" in self.scene: 
            for enemy in self.scene["CrabEnemy"]:
                enemy.boundary_left = enemy.center_x
                enemy.boundary_right = enemy.center_x + 250

        # Integrating physics engine for collisions between
        # These object layers.
        all_platforms = arcade.SpriteList()
        if "x_moving_platform" in self.scene:
            all_platforms.extend(self.scene["x_moving_platform"])
        if "y_moving_platform" in self.scene:
            all_platforms.extend(self.scene["y_moving_platform"])
        if "moving_danger" in self.scene:
            all_platforms.extend(self.scene["moving_danger"])
        if "UpMovingPlatforms" in self.scene:
            all_platforms.extend(self.scene["UpMovingPlatforms"])
        if "DownMovingPlatforms" in self.scene:
            all_platforms.extend(self.scene["DownMovingPlatforms"])
        if "CrabEnemy" in self.scene:
            all_platforms.extend(self.scene["CrabEnemy"])
            

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, walls=self.scene["Platform"],
            platforms=all_platforms,
            gravity_constant=GRAVITY
        )

        self.gui_camera = arcade.Camera2D()
        self.camera.zoom = 3

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        
        # Initialize each cannon within the map with a 
        # Random firing delay between 1-50 seconds
        if "Cannon" in self.scene:
            for cannon in self.scene["Cannon"]:
                self.cannon_fire_timers[cannon] = random.uniform(1, 50)

    def on_draw(self):
        """
        Display player life, score and time stats in GameView
        """
        # Setup statements to clear screen and setup camera.
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.bullet_list.draw() 
        self.gui_camera.use()

        arcade.draw_text(
            f"Lives Remaining: {self.lives}",
            10, WINDOW_HEIGHT - 30,
            font_size=self.font_size,
            color=self.font_color
        )

        arcade.draw_text(
            f"Score: {self.score}",
            10, WINDOW_HEIGHT - 60,
            font_size=self.font_size,
            color=self.font_color
        )

        arcade.draw_text(
            f"Time Taken: {self.time_taken}",
            10, WINDOW_HEIGHT - 90,
            font_size=self.font_size,
            color=self.font_color
        )
        

    def center_camera_to_player(self):
        """Center the camera to player movement using
        smooth movements"""
        
        # Aligning camera position with user position and 
        # Camera delay for adjustment.
        self.camera.position = arcade.math.smerp_2d(
            self.camera.position,
            self.player.position,
            self.window.delta_time,
            FOLLOW_DECAY_CONST,
        )
        # Camera boundaries to prevent straying
        self.camera.view_data.position = arcade.camera.grips.constrain_xy(
            self.camera.view_data, self.camera_bounds
        )

    def on_resize(self, width: int, height: int):
        """Handles window resize events, ensuring that window
        remains in appropriate viewing"""
        super().on_resize(width, height)
        self.camera.match_window
        self.gui_camera.match_window(position=True)

    def on_update(self, delta_time):
        """Main game loop updates."""
        self.update_sprites(delta_time)
        self.handle_collisions(delta_time)
        self.check_game_state(delta_time)
        
        # Vertical map boundaries
        map_height = self.tile_map.height * self.tile_map.tile_height
        self.player.top = min(self.player.top, map_height)
        self.player.bottom = max(self.player.bottom, 0)
        
        if self.player.bottom < 0:
            self.player_dies
            
        
        
        
        self.physics_engine.update()
        self.scene.update(delta_time)
        
    def update_sprites(self, delta_time):
        """Handles the updating of sprite animations and positioning"""
        # Sprite animation updates
        self.player_sprite_list.update()
        self.player.update_animation(delta_time)
        self.scene["Coins"].update_animation(delta_time)
        self.scene["Diamond"].update_animation(delta_time)
        self.moving_danger_list.update_animation(delta_time)
        self.cannon_list.update_animation(delta_time)
        self.scene["Danger"].update_animation(delta_time)
        self.crab_enemy_list.update_animation(delta_time)
        

        
    def handle_collisions(self,delta_time): 
        """Handles all collision checks for both hazards
          and platforms"""
        if "Danger" in self.scene:
            danger_hit_list = (arcade.check_for_collision_with_list
                               (self.player, self.scene["Danger"]))
            if danger_hit_list:
                self.player_dies()

        if "moving_danger" in self.scene:
            moving_danger_hit_list = (arcade.check_for_collision_with_list
                                      (self.player,
                                       self.scene["moving_danger"]))
            if moving_danger_hit_list:
                self.player_dies()
                
        if "CrabEnemy" in self.scene:
            crab_enemy_hit_list = (arcade.check_for_collision_with_list
                                   (self.player, self.scene["CrabEnemy"]))
            if crab_enemy_hit_list:
                self.player_dies()
                
        if "Bounce" in self.scene:
            bounce_hit_list = (arcade.check_for_collision_with_list
                               (self.player, self.scene["Bounce"]))
            if bounce_hit_list:
                self.player.change_y = min(BOUNCE_FORCE, 15)
                self.player.jump_count = 1
        
        # Store quicksand collisions        
        quicksand_hit_list = []
        # Identify collisions
        if "Quicksand" in self.scene:
            quicksand_hit_list = (arcade.check_for_collision_with_list
                                  (self.player, self.scene["Quicksand"]))
        # Collision detected, activate quicksand state flag, and apply
        # Debuff respectively
        if quicksand_hit_list:
            if not self.is_on_quicksand:
                self.is_on_quicksand = True
                self.current_movement_speed = (MOVEMENT_SPEED 
                                               * QUICKSAND_SPEED_DEBUFF)
                
            # Ensure debuff remains as player X-movement changes.    
            if self.player.change_x != 0:
                self.player.change_x = (self.player.change_x  / 
                                        abs(self.player.change_x)
                                        * self.current_movement_speed)
        # Player identified not on quicksand, deactive flag, and 
        # Return original movement speed.
        else:
            if self.is_on_quicksand:
                self.is_on_quicksand = False
                self.current_movement_speed = MOVEMENT_SPEED
                
                # Reset movement speed when player X-movement changes
                if self.player.change_x != 0:
                    self.player.change_x = (self.player.change_x /
                                            abs(self.player.change_x) *
                                            self.current_movement_speed)
        
        # Collision detection between bullet sprite and player,
        # Calling player_dies function to handle death, 
        # And removing the bullet.
        bullet_hit_list = (arcade.check_for_collision_with_list
                           (self.player, self.bullet_list))
        for bullet in bullet_hit_list:
            bullet.remove_from_sprite_lists()
            self.player_dies()

        # Handle sprite collison with collectables
        # And level progressors, add score for collectables.
        coin_hit_list = (arcade.check_for_collision_with_list
                         (self.player, self.scene["Coins"]))

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1

        diamond_hit_list = (arcade.check_for_collision_with_list
                            (self.player, self.scene["Diamond"]))

        for diamond in diamond_hit_list:
            diamond.remove_from_sprite_lists()
            self.score += 5
        # Reinitiating setup values when progression to new level
        if "Chest" in self.scene:
            chest_hit_list = (arcade.check_for_collision_with_list
                              (self.player, self.scene["Chest"]))
            if chest_hit_list:
                self.level += 1
                self.setup()
        # Displaying end menu when user completes the entire game
        # By colliding with the final chest sprite.
        if "Final" in self.scene:
            final_chest_hit_list = (arcade.check_for_collision_with_list
                                    (self.player, self.scene["Final"]))
            if final_chest_hit_list:
                game_end = GameEnd(self.score, self.time_taken)
                self.window.show_view(game_end)
                # Identifying ladder interaction
                # for upwards climb motion
                
        is_on_ladder = arcade.check_for_collision_with_list(self.player,
                                                            self.ladder_list)
        # Redifing movement to accustom for ladder mechanics
        # Allowing user to climb upwards.
        if is_on_ladder:
            self.player.change_y = 0

            if self.jump_key_pressed:
                self.player.change_y = PLAYER_CLIMB_SPEED
                
    def check_game_state(self, delta_time):
        """Maintains other game features, updating additional features
        such as time score, camera, map boundaries, sprite removal,
        cannon firing cooldown, and double jump cooldown."""
        # Time Score
        self.time_taken += delta_time

        # Recall camera function to consistently follow user.
        self.center_camera_to_player()
        
         

        # Set map boundaries constantly ensuring user doesnt walk off
        map_left = 0
        map_right = self.tile_map.width * self.tile_map.tile_width

        if self.player.left < map_left:
            self.player.left = map_left
        elif self.player.right > map_right:
            self.player.right = map_right
            
        self.bullet_list.update(delta_time) 

        # Removing bullet sprites that have been identified to leave
        # Map boundaries
        for bullet in self.bullet_list:
            if bullet.should_be_removed:
                bullet.remove_from_sprite_lists()
            if self.level == 3:
                bullet.remove_fromt_sprite_lists()


        # Handling cannon cooldown by identifying delay using frame
        # Time, then checking if its ready to fire (cooldown expired)
        # Before reseting the cooldown with a random delay
        # Generating unpredictable firing patterns
        if "Cannon" in self.scene:
            for cannon in self.scene["Cannon"]:
                self.cannon_fire_timers[cannon] -= delta_time
                if self.cannon_fire_timers[cannon] <= 0:
                    self.fire_bullet_from_cannon(cannon)
                    self.cannon_fire_timers[cannon] = random.uniform(1, 10) 
        # Double jump checker            
        is_on_ground = self.physics_engine.can_jump()
        
        if is_on_ground and not self.was_on_ground:
            self.player.jump_count = 0
        
        self.was_on_ground = is_on_ground
        

    def player_dies(self):
        """ Handles player deaths by removing lives and resetting
        spawn point, as well as directing user to GameOverView, 
        when lives run out."""
        self.lives -= 1
        
        if self.lives < 0:
            self.lives = 0
            game_over_view = GameOverView(self.score, self.time_taken)
            self.window.show_view(game_over_view)
        
        if self.lives > 0:
            self.player.center_x = self.spawn_x
            self.player.center_y = self.spawn_y
            self.player.change_y = 0
            
        else:
            game_over_view = GameOverView(self.score, self.time_taken)
            self.window.show_view(game_over_view)

    def fire_bullet_from_cannon(self, cannon):
        """Determing bullet preferences, such as speed, scaling
        and adding bullets to the scene."""
        bullet = Bullet(BULLET_TEXTURE, BULLET_SCALING)
        bullet.center_x = cannon.center_x
        bullet.center_y = cannon.center_y
        bullet.change_x = BULLET_SPEED
        self.bullet_list.append(bullet)


    def on_key_press(self, key, modifiers):
        """Handles player mvovement keys, applying speed to
        jumps and horizontal motion. """
        is_on_ladder  = (arcade.check_for_collision_with_list
        (self.player,
        self.ladder_list))
        
        if key in (arcade.key.W, arcade.key.SPACE):
            if is_on_ladder:
                self.jump_key_pressed = True
                self.player.change_y = PLAYER_CLIMB_SPEED
            else:
                if self.physics_engine.can_jump():
                    """ Identifying player ability to double jump
                    ensuring cooldown is off."""
                    self.player.change_y = PLAYER_JUMP_SPEED
                    self.player.jump_count += 1
            # Applying additional jump
                elif self.player.jump_count < self.player.max_jumps:
                    self.player.change_y = PLAYER_DOUBLE_JUMP_SPEED
                    self.player.jump_count += 1
            
                
                
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.change_x = -self.current_movement_speed
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = self.current_movement_speed
        elif key in (arcade.key.ESCAPE, arcade.key.Q):
            arcade.close_window()
        # Upwards climb for ladder interaction
        

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT,
                   arcade.key.A, arcade.key.D):
            self.player.change_x = 0
        # Disable motion and default to gravity when
        # User stops climbing on ladder.
        if key == arcade.key.W or key == arcade.key.SPACE:
            self.jump_key_pressed = False
        is_on_ladder = arcade.check_for_collision_with_list(self.player,
                                                            self.ladder_list)
        if is_on_ladder:
            self.player.change_y = 0


def main():
    """Main function handling the start of the game
    calling necessary functions to display and run the game."""
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()