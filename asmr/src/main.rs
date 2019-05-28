// TODO
// Modify
// Add
//
// Skip getArtists / levenshtein artist check?
#[macro_use]
use serde::{Deserialize, Serialize};
use serde_json;
use webbrowser;

use std::env;
use std::fmt;
use std::fs;
use std::io::{self, Write};
use std::path::Path;

type Result<T> = ::std::result::Result<T, Box<::std::error::Error>>;

#[derive(Serialize, Deserialize, Debug,Clone)]
pub struct Video {
    title: String,
    artist: String,
    url: String,
}

impl fmt::Display for Video {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} by {}", self.title, self.artist)
    }
}

fn read_videos() -> Result<Vec<Video>> {
    let fname = env::var("DATADIR")?;
    let fpath = Path::new(&fname).join("asmr.json");
    let data = fs::read_to_string(fpath)?;
    let v: Vec<Video> = serde_json::from_str(&data)?;
    Ok(v)
}

fn urlify(url: &str) -> String {
    match url.starts_with("http") || url.starts_with("www") {
        true => url.to_string(),
        false => format!("https://www.youtube.com/watch?v={}", url)
    }
}

fn is_match(i: usize, v: &Video, q: String) -> Option<usize> {
    let matches_title = v.title.to_lowercase().contains(&q);
    let matches_artist = v.artist.to_lowercase().contains(&q);
    match matches_title || matches_artist {
        true => Some(i),
        _ => None
    }
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    println!("{:?}", args);
    let videos = read_videos().unwrap();
    // let (a, b) = ("ring".to_string(), "bling".to_string());
    // println!("{} {} {}", a, b, levenshtein(&a, &b));
    // webbrowser::open("http://github.com");
    // check_for_similar_artists(&videos);
fn read_choices() -> Vec<usize> {
    print!("Choose: ");
    io::stdout().flush(); // Need to flush to ensure 'choose' gets printed
    let mut response = String::new();
    io::stdin().read_line(&mut response);
    // Now, get rid of newline, and parse integers.
    // Just assume all integers are fine for now
    response
        .trim()
        .split(",")
        .map(|x| x.parse::<usize>().unwrap())
        .collect()
}

mod command {
    use super::*;
    use random::Source;

    pub fn play(v: &[Video], mask: &[usize], random: bool) -> Vec<Video> {
        let mut source = random::default();
        let choices: Vec<usize> = match random {
            true => {
                let rand = source.read::<usize>() % mask.len();
                vec![mask[rand]]
            }
            false => read_choices(),
        };
        for idx in choices {
            println!("{}", v[idx]);
            webbrowser::open(&v[idx].url);
        }
        v.to_vec()
    }

    pub fn add() {
        unimplemented!();
    }

    pub fn modify() {
        unimplemented!();
    }

    pub fn delete(v: &[Video]) -> Vec<Video> {
        let mut choices = read_choices();
        choices.sort();
        choices.reverse();
        println!("{:?}", choices);
        let mut v_new = v.to_vec();
        for idx in choices {
            v_new.remove(idx);
        }
        v_new
    }
}
