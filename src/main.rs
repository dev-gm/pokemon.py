use std::collections::HashSet;

struct Game {
    maps: HashSet<Map>,
    trainer_types: HashSet<TrainerType>,
    textures: HashSet<Texture>,
}

struct Map {
    size: (usize, usize),
}

struct Sprite<T: SpriteClass> {
    name: String,
    class: T,
    image: SpriteImage,
}

struct Event;

trait SpriteClass {
    fn update(&self, image: &mut SpriteImage, events: &HashSet<Event>);
}

struct PlayerClass(&'static Client);

impl SpriteClass for PlayerClass {
    fn update(&self, image: &mut SpriteImage, events: &HashSet<Event>) {}
}

struct TrainerClass(Trainer);

impl SpriteClass for TrainerClass {
    fn update(&self, image: &mut SpriteImage, events: &HashSet<Event>) {}
}

struct BuildingClass(Vec<Door>);

impl SpriteClass for BuildingClass {
    fn update(&self, image: &mut SpriteImage, events: &HashSet<Event>) {}
}

struct DoorClass(Door);

struct Trainer {
    trainer_type: &'static TrainerType,
    name: String,
    dialog: Vec<String>,
}

struct TrainerType(String);

struct SpriteImage {
    texture: &'static Texture,
    pos: (usize, usize),
    size: (usize, usize),
    rotate: i16, // rotate (mod 360)
}

struct Door {
    orientation: bool, // true = top/bottom, true = right/left
    side: bool, // true = right/top, true = left/bottom
    pos: usize, // if orientation == true, pos = x; if orientation == false, pos = y
    size: usize, // same as above
    destination: &'static Door,
}

struct Client; // purely to communicate with clients, doesn't hold state

struct Texture;

fn main() {
    println!("Hello, world!");
}
