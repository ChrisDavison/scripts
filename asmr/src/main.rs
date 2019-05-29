// TODO
// Skip getArtists / levenshtein artist check?
use regex::Regex;

use std::env;
use std::fmt;
use std::fs;
use std::io::{self, Write};

mod command;
mod video;

type Result<T> = ::std::result::Result<T, Box<::std::error::Error>>;

fn urlify<T: ToString + fmt::Display>(url: T) -> Result<String> {
    let url_s = url.to_string();
    let re = Regex::new(r"\?v=(.{11})")?;
    let hash_only = if url_s.len() == 11 {
        url_s
    } else {
        let caps = re.captures(&url_s).expect("No URL match");
        caps.get(1)
            .expect("No URL capture group")
            .as_str()
            .to_string()
    };
    Ok(format!("https://www.youtube.com/watch?v={}", hash_only))
}

fn is_match(v: &video::Video, q: String) -> bool {
    let matches_title = v.title.to_lowercase().contains(&q);
    let matches_artist = v.artist.to_lowercase().contains(&q);
    matches_title || matches_artist
}

fn read_choices() -> Result<Vec<usize>> {
    print!("Choose: ");
    io::stdout().flush().expect("read_choices: Couldn't flush stdout");
    let mut response = String::new();
    io::stdin().read_line(&mut response).expect("read_choices: Couldn't read choices");
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
    io::stdout().flush().expect("read_line_with_prompt: Couldn't flush stdout");
    io::stdin().read_line(&mut response).expect("read_line_with_prompt: Couldn't read response");
    Ok(response)
}

fn main() -> Result<()> {
    let args: Vec<String> = env::args().skip(1).collect();
    let videos = video::read_videos_from_file().expect("Couldn't load videos from file");
    let queries: Vec<String> = args.iter().skip(1).map(|x| x.to_owned()).collect();
    let query_lower = queries.join(" ").to_lowercase();
    let mask: Vec<usize> = videos
        .iter()
        .enumerate()
        .filter(|(_idx, video)| is_match(video, query_lower.clone()))
        .map(|(i, _video)| idx)
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
    video::write_videos_to_file(&new_videos)
}
