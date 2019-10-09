
#[macro_use]
// ORM
extern crate diesel;

// Environment variables
extern crate dotenv;

// Rand
extern crate rand;

pub mod schema;
pub mod models;

use diesel::prelude::*;
use dotenv::dotenv;
use std::env;
use rand::Rng;
use std::{thread, time};

use self::models::{Weather};

fn establish_connection() -> PgConnection {
    dotenv().ok();

    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    PgConnection::establish(&database_url).expect(&format!("Error connecting to {}", database_url))
}

fn create_weather(weather: Weather, connection: &PgConnection) -> Weather {
    use schema::weathers;

    diesel::insert_into(weathers::table)
        .values(&weather)
        .get_result(connection)
        .expect("Error saving new weather")
}

fn update_weather(weathers: Weather, connection: &PgConnection) -> Weather {
    use schema::weathers;
    diesel::update(weathers::table.find(weathers.id))
        .set(&weathers)
        .get_result(connection)
        .expect(&format!("Unable to find weather {}", weathers.id))
}

fn main() {
    // use the-tensox-etl::schema::weathers::dsl::*;

    let connection = establish_connection();
    /*
    create_weather(Weather {
        id: 0,
        x: 1,
        y: 1,
        sun: 3
    }, &connection);
    println!("ok {:?}", schema::weathers::table.find(0).get_result::<Weather>(&connection));
    */
    random_sun(&connection)




    // println!("ok {:?}", schema::weathers::table.find(3).get_result::<Weather>(&connection));
}

fn random_sun(connection: &PgConnection) {
    // Randomly generated sun
    let mut rng = rand::thread_rng();
    
    loop {
        let x = rng.gen_range(0, 100);
        let y = rng.gen_range(0, 100);
        let sun = rng.gen_range(0, 10);
        println!("Updating weather: x: {}, y: {}, sun: {}", x, y, sun);
        update_weather(Weather {
            id: 1,
            x: x,
            y: y,
            sun: sun
        }, &connection);
        let ten_millis = time::Duration::from_millis(100);
        thread::sleep(ten_millis);
    }
}