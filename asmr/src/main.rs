// TODO
// Skip getArtists / levenshtein artist check?
use regex::Regex;

use std::env;
use std::fmt;
use std::fs;
use std::io::{self, Write};

mod command;
mod video;

use self::command::Command;

type Result<T> = ::std::result::Result<T, Box<::std::error::Error>>;

fn urlify<T: ToString + fmt::Display>(url: T) -> Result<String> {
    let url_s = url.to_string();
    let re = Regex::new(r"\?v=(.{11})")?;
    let hash_only = if url_s.len() == 11 {
        url_s
    } else {
        let caps = re.captures(&url_s).expect("No URL match");
        caps.get(1).ok_or("Couldn't capture video hash")?.as_str().to_string()
    };
    Ok(format!("https://www.youtube.com/watch?v={}", hash_only))
}

fn is_match(v: &video::Video, q: impl ToString) -> bool {
    let q_str = q.to_string();
    let matches_title = v.title.to_lowercase().contains(&q_str);
    let matches_artist = v.artist.to_lowercase().contains(&q_str);
    matches_title || matches_artist
}

fn read_choices() -> Result<Vec<usize>> {
    print!("Choose: ");
    io::stdout()
        .flush()
        .expect("read_choices: Couldn't flush stdout");
    let mut response = String::new();
    io::stdin()
        .read_line(&mut response)
        .expect("read_choices: Couldn't read choices");
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
    io::stdout()
        .flush()
        .expect("read_line_with_prompt: Couldn't flush stdout");
    io::stdin()
        .read_line(&mut response)
        .expect("read_line_with_prompt: Couldn't read response");
    Ok(response)
}

fn usage() {
    let msg = "Usage:
    asmr play   [-r] [<query>...]
    asmr delete [<query>...]
    asmr modify [<query>...]
    asmr add    [<query>...]
    asmr view   [<query>...]";
    println!("{}", msg);
}

fn parse_args() -> (Command, String) {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.len() == 0 {
        (Command::Usage, String::new())
    } else {
        let mut queries: Vec<String> = Vec::new();
        let mut is_rand: bool = false;
        for arg in args.iter() {
            if arg == "-r" {
                is_rand = true;
            } else {
                queries.push(arg.to_string());
            }
        }
        let query_lower = queries.join(" ").to_lowercase();
        let cmd = match &args[0].as_str() {
            &"play" => Command::Play(is_rand),
            &"add" => Command::Add,
            &"delete" => Command::Delete,
            &"modify" => Command::Modify,
            &"view" => Command::View,
            _ => Command::Usage,
        };
        (cmd, query_lower)
    }
}

fn display_videos(videos: &[video::Video], mask: &[usize]) {
    println!("{:>5}  {:20}\t{}", "#", "Artist", "Title");
    println!("{}", "-".repeat(60));
    for &idx in mask.iter() {
        println!(
            "{:5}) {:20}\t{}",
            idx, videos[idx].artist, videos[idx].title
        );
    }
}

fn main() -> Result<()> {
    let (cmd, query) = parse_args();
    if cmd == Command::Usage {
        usage();
        return Ok(());
    }
    let videos = video::read_videos_from_file().expect("Couldn't load videos from file");
    let mask: Vec<usize> = videos
        .iter()
        .enumerate()
        .filter(|(_idx, video)| is_match(video, &query))
        .map(|(idx, _video)| idx)
        .collect();

    if !(cmd == Command::Add || cmd == Command::Play(true)) {
        display_videos(&videos, &mask);
    }
    let new_videos = match cmd {
        Command::Play(random) => command::play(&videos, &mask, random)?,
        Command::Delete => command::delete(&videos)?,
        Command::Modify => command::modify(&videos)?,
        Command::Add => command::add(&videos)?,
        _ => videos,
    };
    video::write_videos_to_file(&new_videos)
}
