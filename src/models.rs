use super::schema::weathers;

#[derive(Queryable, Insertable, AsChangeset, Debug)]
pub struct Weather {
    pub id: i32,
    pub x: i32,
    pub y: i32,
    pub sun: i32,
}