// TODO
// Skip getArtists / levenshtein artist check?
use serde::{Deserialize, Serialize};
use serde_json;
use regex::Regex;
use webbrowser;

use std::env;
use std::fmt;
use std::fs;
use std::io::{self, Write};
use std::path::Path;

type Result<T> = ::std::result::Result<T, Box<::std::error::Error>>;

#[derive(Serialize, Deserialize, Debug, Clone)]
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

fn write_videos(v: &[Video]) -> Result<()> {
    let fname = env::var("DATADIR")?;
    let fpath = Path::new(&fname).join("asmr.json");
    let j = serde_json::to_string_pretty(v)?;
    fs::write(fpath, j)?;
    Ok(())
}

fn urlify<T: ToString + fmt::Display>(url: T) -> Result<String> {
    let url_s = url.to_string();
    let re = Regex::new(r"\?v=(.{11})")?;
    let hash_only = if url_s.len() == 11 {
        url_s
    } else {
        let caps = re.captures(&url_s).expect("No URL match");
        caps.get(1).expect("No URL capture group").as_str().to_string()
    };
    Ok(format!("https://www.youtube.com/watch?v={}", hash_only))
}

fn is_match(i: usize, v: &Video, q: String) -> Option<usize> {
    let matches_title = v.title.to_lowercase().contains(&q);
    let matches_artist = v.artist.to_lowercase().contains(&q);
    match matches_title || matches_artist {
        true => Some(i),
        _ => None,
    }
}

fn read_choices() -> Result<Vec<usize>> {
    print!("Choose: ");
    io::stdout().flush()?; // Need to flush to ensure 'choose' gets printed
    let mut response = String::new();
    io::stdin().read_line(&mut response)?;
    // Now, get rid of newline, and parse integers.
    // Just assume all integers are fine for now
    Ok(response
        .trim()
        .split(",")
        .filter_map(|x| x.parse::<usize>().ok())
        .collect())
}

pub fn read_line_with_prompt<T: ToString + fmt::Display>(prompt: T) -> Result<String> {
    let mut response = String::new();
    println!("{}", prompt);
    io::stdout().flush()?;
    io::stdin().read_line(&mut response)?;
    Ok(response)
}

fn main() -> Result<()> {
    let args: Vec<String> = env::args().skip(1).collect();
    let videos = read_videos()?;
    let queries: Vec<String> = args.iter().skip(1).map(|x| x.to_owned()).collect();
    let query_lower = queries.join(" ").to_lowercase();
    let mask: Vec<usize> = videos
        .iter()
        .enumerate()
        .filter_map(|(i, x)| is_match(i, x, query_lower.clone()))
        .collect();
    let cmd: &str = &args[0];
    if cmd != "add" {
        println!("{:>5}  {:20}\t{}", "#", "Artist", "Title");
        println!("{}", "-".repeat(60));
        for &idx in mask.iter() {
            println!(
                "{:5}) {:20}\t{}",
                idx, videos[idx].artist, videos[idx].title
            );
        }
    }
    let new_videos = match cmd {
        "play" => command::play(&videos, &mask, false)?,
        "delete" => command::delete(&videos)?,
        "modify" => command::modify(&videos)?,
        "add" => command::add(&videos)?,
        _ => videos,
    };
    write_videos(&new_videos)
}

mod command {
    use super::*;
    use random::Source;

    fn current_or_new(current: &String, pre_prompt: &String) -> Result<String> {
        let new = read_line_with_prompt(format!("{} ({}): ", pre_prompt, current))?;
        match new == "\n" {
            true => Ok(current.clone()),
            false => Ok(new),
        }
    }

    pub fn play(v: &[Video], mask: &[usize], random: bool) -> Result<Vec<Video>> {
        let mut source = random::default();
        let choices: Vec<usize> = match random {
            true => {
                let rand = source.read::<usize>() % mask.len();
                vec![mask[rand]]
            }
            false => read_choices()?,
        };
        for idx in choices {
            println!("{}", v[idx]);
            webbrowser::open(&v[idx].url)?;
        }
        Ok(v.to_vec())
    }

    pub fn add(v: &[Video]) -> Result<Vec<Video>> {
        let mut v_new = v.to_vec();
        let artist = read_line_with_prompt("Artist")?;
        let title = read_line_with_prompt("Title")?;
        let url = urlify(read_line_with_prompt("URL")?)?;
        v_new.push(Video { title, artist, url });
        Ok(v_new)
    }

    pub fn modify(v: &[Video]) -> Result<Vec<Video>> {
        let mut v_new: Vec<Video> = v.to_vec();
        let choices = read_choices()?;
        println!("Update info, or ENTER to keep current");
        for idx in choices {
            let current = v[idx].clone();
            v_new[idx].artist = current_or_new(&current.artist, &"Artist".to_string())?;
            v_new[idx].title = current_or_new(&current.title, &"Title".to_string())?;
            v_new[idx].url = urlify(current_or_new(&current.url, &"URL".to_string())?)?;
        }
        Ok(v_new.to_vec())
    }

    pub fn delete(v: &[Video]) -> Result<Vec<Video>> {
        let mut choices = read_choices()?;
        choices.sort();
        choices.reverse();
        println!("{:?}", choices);
        let mut v_new = v.to_vec();
        for idx in choices {
            v_new.remove(idx);
        }
        Ok(v_new)
    }
}
