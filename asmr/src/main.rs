// TODO
// Skip getArtists / levenshtein artist check?
use regex::Regex;

use std::env;
use std::fmt;
use std::fs;
use std::io::{self, Write};

pub mod command;
pub mod video;

use self::command::Command;

type Result<T> = ::std::result::Result<T, Box<::std::error::Error>>;

/// Extract the video hash from a given url, returning the tidy, launchable url.
fn urlify<T: ToString + fmt::Display>(url: T) -> Result<String> {
    let url_s = url.to_string();
    let re = Regex::new(r"\?v=(.{11})")?;
    let hash_only = if url_s.len() == 11 {
        url_s
    } else {
        let caps = re.captures(&url_s).expect("No URL match");
        caps.get(1)
            .ok_or("Couldn't capture video hash")?
            .as_str()
            .to_string()
    };
    Ok(format!("https://www.youtube.com/watch?v={}", hash_only))
}

/// Check if query matches video title or artist (case insensitive)
fn is_match(v: &video::Video, q: impl ToString) -> bool {
    let q_str = q.to_string();
    let matches_title = v.title.to_lowercase().contains(&q_str);
    let matches_artist = v.artist.to_lowercase().contains(&q_str);
    matches_title || matches_artist
}

/// Get a list of numeric choices from the user, splitting on any
/// non-numeric value (so spaces, commas, tabs etc can all be used).
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
    // As I'm splitting on non-numeric, it should only be numeric remaining
    // and thus we just trust that they are parseable
    Ok(response
        .trim()
        .split(|x: char| !x.is_numeric())
        .filter_map(|x| x.parse::<usize>().ok())
        .collect())
}

/// Display a message to the user and then return the resulting string (trimmed).
/// Handles flushing to ensure that the response is displayed on the same
/// line as the prompt.
pub fn read_line_with_prompt<T>(prompt: T) -> Result<String>
where
    T: ToString + fmt::Display,
{
    let mut response = String::new();
    print!("{}: ", prompt);
    io::stdout()
        .flush()
        .expect("read_line_with_prompt: Couldn't flush stdout");
    io::stdin()
        .read_line(&mut response)
        .expect("read_line_with_prompt: Couldn't read response");
    Ok(response.trim().to_string())
}

/// Print a short usage message.
fn usage() {
    let msg = "Usage:
    asmr play    [-r] [<query>...]
    asmr delete  [<query>...]
    asmr modify  [<query>...]
    asmr view    [<query>...]
    asmr add
    asmr artists
    asmr popular";
    println!("{}", msg);
}

/// Parse all command line arguments, returning the command enum and the query.
/// This is a bit hacky and would probably benefit from something like clap
/// or docopt.
fn parse_args() -> (Command, String) {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.len() == 0 {
        (Command::Usage, String::new())
    } else {
        let mut queries: Vec<String> = Vec::new();
        let mut is_rand: bool = false;
        for arg in args.iter().skip(1) {
            if arg == "-r" {
                is_rand = true;
            } else {
                queries.push(arg.to_string());
            }
        }
        let query_lower = queries.join(" ").to_lowercase();
        let arg0 = &args[0].as_str();
        let cmd = match (arg0.len(), arg0) {
            (0, _) => Command::View,
            (_, &"play") => Command::Play(is_rand),
            (_, &"add") => Command::Add,
            (_, &"delete") => Command::Delete,
            (_, &"modify") => Command::Modify,
            (_, &"view") => Command::View,
            (_, &"artists") => Command::Artists,
            (_, &"popular") => Command::Popular,
            _ => Command::Usage,
        };
        (cmd, query_lower)
    }
}

/// Display the index, artist, and title of each video.
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
    let new_videos = match cmd {
        Command::Play(random) => {
            if !random {
                display_videos(&videos, &mask);
            }
            command::play(&videos, &mask, random)?
        }
        Command::Delete => {
            display_videos(&videos, &mask);
            command::delete(&videos)?
        }
        Command::Modify => {
            display_videos(&videos, &mask);
            command::modify(&videos)?
        }
        Command::Add => command::add(&videos)?,
        Command::Usage => videos,
        Command::View => {
            display_videos(&videos, &mask);
            videos
        }
        Command::Artists => command::artists(&videos),
        Command::Popular => command::popular(&videos),
    };
    video::write_videos_to_file(&new_videos)
}
