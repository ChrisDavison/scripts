// TODO
// Modify
// Add
//
// Skip getArtists / levenshtein artist check?
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
    let videos = read_videos().unwrap();
    let queries: Vec<String> = args.iter().skip(1).map(|x| x.to_owned()).collect();
    let query_lower = queries.join(" ").to_lowercase();
    let mask: Vec<usize> = videos.iter().enumerate()
        .filter_map(|(i, x)| is_match(i, x, query_lower.clone()))
        .collect();
    let cmd: &str = &args[0];
    if cmd != "add" {
        println!("{:>5}  {:20}\t{}", "#", "Artist", "Title");
        println!("{}", "-".repeat(60));
        for &idx in mask.iter() {
            println!("{:5}) {:20}\t{}", idx, videos[idx].artist, videos[idx].title);
        }
    }
    let new_videos = match cmd {
        "play" => command::play(&videos, &mask, false),
        "delete" => command::delete(&videos),
        "modify" => command::modify(&videos),
        "add" => command::add(&videos),
        _ => unimplemented!(),
    };
}

fn read_choices() -> Vec<usize> {
    print!("Choose: ");
    io::stdout().flush().unwrap(); // Need to flush to ensure 'choose' gets printed
    let mut response = String::new();
    io::stdin().read_line(&mut response).unwrap();
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
            webbrowser::open(&v[idx].url).unwrap();
        }
        v.to_vec()
    }

    pub fn add(v: &[Video]) -> Vec<Video> {
        unimplemented!();
    }

    pub fn modify(v: &[Video]) -> Vec<Video> {
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
