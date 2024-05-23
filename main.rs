extern crate sdl2;

use sdl2::event::Event;
use sdl2::image::{self, LoadTexture, InitFlag};
use sdl2::keyboard::Keycode;
use sdl2::rect::{Rect, Point};
use sdl2::render::{Canvas, Texture, TextureCreator};
use sdl2::ttf::Sdl2TtfContext;
use sdl2::video::{Window, WindowContext};
use std::time::Duration;

const SCALE_FACTOR: f64 = 2.3;
const SCALE_PLAYER: f64 = 0.1 * SCALE_FACTOR;
const START_POS_X: f64 = 390.0 * SCALE_FACTOR;
const START_POS_Y: f64 = 433.0 * SCALE_FACTOR;
const FPS: u32 = 144;

struct AbstractCar<'a> {
    img: Texture<'a>,
    max_vel: f64,
    vel: f64,
    rotation_vel: f64,
    angle: f64,
    x: f64,
    y: f64,
    acceleration: f64,
    start_pos: (f64, f64),
}

impl<'a> AbstractCar<'a> {
    fn new(texture: Texture<'a>, max_vel: f64, rotation_vel: f64, start_pos: (f64, f64)) -> Self {
        Self {
            img: texture,
            max_vel,
            vel: 0.0,
            rotation_vel: 0.25 * rotation_vel,
            angle: 0.0,
            x: start_pos.0,
            y: start_pos.1,
            acceleration: 0.1,
            start_pos,
        }
    }

    fn rotate(&mut self, left: bool, right: bool) {
        if left {
            self.angle += self.rotation_vel;
        } else if right {
            self.angle -= self.rotation_vel;
        }
    }

    fn draw(&self, canvas: &mut Canvas<Window>, texture_creator: &TextureCreator<WindowContext>) {
        let center = Point::new(self.x as i32, self.y as i32);
        canvas.copy_ex(&self.img, None, Some(Rect::from_center(center, 50, 50)), self.angle, None, false, false).unwrap();
    }

    fn move_forward(&mut self) {
        self.vel = self.vel.min(self.max_vel) + self.acceleration;
        self.move_car();
    }

    fn move_backward(&mut self) {
        self.vel = self.vel.max(-self.max_vel / 2.0) - self.acceleration;
        self.move_car();
    }

    fn move_car(&mut self) {
        let radians = self.angle.to_radians();
        let vertical = radians.cos() * self.vel;
        let horizontal = radians.sin() * self.vel;

        self.y -= vertical;
        self.x -= horizontal;
    }

    fn collide(&self, mask: &sdl2::surface::Surface) -> Option<Point> {
        // Implement collision detection logic
        None
    }

    fn reset(&mut self) {
        self.x = self.start_pos.0;
        self.y = self.start_pos.1;
        self.angle = 0.0;
        self.vel = 0.0;
    }
}

struct PlayerCar<'a> {
    abstract_car: AbstractCar<'a>,
}

impl<'a> PlayerCar<'a> {
    fn new(texture: Texture<'a>, max_vel: f64, rotation_vel: f64, start_pos: (f64, f64)) -> Self {
        Self {
            abstract_car: AbstractCar::new(texture, max_vel, rotation_vel, start_pos),
        }
    }

    fn reduce_speed(&mut self) {
        self.abstract_car.vel = (self.abstract_car.vel - self.abstract_car.acceleration / 2.0).max(0.0);
        self.abstract_car.move_car();
    }

    fn bounce(&mut self) {
        self.abstract_car.vel = -self.abstract_car.vel * 0.5;
        self.abstract_car.move_car();
    }

    fn draw(&self, canvas: &mut Canvas<Window>, texture_creator: &TextureCreator<WindowContext>) {
        self.abstract_car.draw(canvas, texture_creator);
    }

    fn rotate(&mut self, left: bool, right: bool) {
        self.abstract_car.rotate(left, right);
    }

    fn move_forward(&mut self) {
        self.abstract_car.move_forward();
    }

    fn move_backward(&mut self) {
        self.abstract_car.move_backward();
    }

    fn move_car(&mut self) {
        self.abstract_car.move_car();
    }

    fn collide(&self, mask: &sdl2::surface::Surface) -> Option<Point> {
        self.abstract_car.collide(mask)
    }
}

fn draw(
    canvas: &mut Canvas<Window>,
    images: &[(Texture, Point)],
    player_car: &PlayerCar,
    ttf_context: &Sdl2TtfContext,
) {
    canvas.clear();
    for (img, pos) in images.iter() {
        canvas.copy(&img, None, Some(Rect::new(pos.x, pos.y, 800, 600))).unwrap();
    }

    // Draw FPS counter (for simplicity, it shows a fixed value)
    let font = ttf_context.load_font("assets/comicsans.ttf", 44).unwrap();
    let surface = font.render("FPS: 144").blended(sdl2::pixels::Color::RGBA(255, 255, 255, 255)).unwrap();
    let texture = canvas.texture_creator().create_texture_from_surface(&surface).unwrap();
    canvas.copy(&texture, None, Some(Rect::new(10, 10, 200, 50))).unwrap();

    player_car.draw(canvas, &canvas.texture_creator());

    canvas.present();
}

fn move_player(player_car: &mut PlayerCar, keys: &sdl2::keyboard::KeyboardState) {
    let mut moved = false;

    if keys.is_scancode_pressed(sdl2::keyboard::Scancode::A) {
        player_car.rotate(true, false);
    }
    if keys.is_scancode_pressed(sdl2::keyboard::Scancode::D) {
        player_car.rotate(false, true);
    }
    if keys.is_scancode_pressed(sdl2::keyboard::Scancode::W) {
        moved = true;
        player_car.move_forward();
    }
    if keys.is_scancode_pressed(sdl2::keyboard::Scancode::S) {
        moved = true;
        player_car.move_backward();
    }

    if !moved {
        player_car.reduce_speed();
    }
}

fn main() -> Result<(), String> {
    let sdl_context = sdl2::init()?;
    let video_subsystem = sdl_context.video()?;
    let ttf_context = sdl2::ttf::init().map_err(|e| e.to_string())?;
    let _image_context = image::init(InitFlag::PNG | InitFlag::JPG)?;

    let window = video_subsystem
        .window("SuperTuxKart", (800.0 * SCALE_FACTOR) as u32, (600.0 * SCALE_FACTOR) as u32)
        .position_centered()
        .build()
        .map_err(|e| e.to_string())?;

    let mut canvas = window.into_canvas().build().map_err(|e| e.to_string())?;
    let texture_creator = canvas.texture_creator();

    let track = texture_creator.load_texture("imgs/rennstrecke.jpg")?;
    let track_border = texture_creator.load_texture("imgs/rennstrecke_mask_s.xcf")?;
    let finish_border = texture_creator.load_texture("imgs/finish-line.png")?;
    let racer1_texture = texture_creator.load_texture("imgs/tuxi.xcf")?;
    let racer2_texture = texture_creator.load_texture("imgs/yoshi.xcf")?;

    let images = vec![(track, Point::new(0, 0))];
    let mut player_car = PlayerCar::new(racer1_texture, 3.0, 4.0, (START_POS_X, START_POS_Y));

    let mut event_pump = sdl_context.event_pump()?;
    let mut clock = sdl2::timer::Timer::new()?;

    while let Some(event) = event_pump.poll_iter().find(|event| match event {
        Event::Quit { .. } => true,
        _ => false,
    }) {
        // Game loop setup
        draw(&mut canvas, &images, &player_car, &ttf_context);
        clock.tick(FPS);

        // Player control
        move_player(&mut player_car, &event_pump.keyboard_state());

        // Check collisions
        if let Some(_) = player_car.collide(&track_border) {
            player_car.bounce();
        }

        // Handle player 2 control here if needed

        canvas.present();
    }

    Ok(())
}

