use random::Source;
use std::collections::HashSet;
use std::io::Write;
use webbrowser;

use super::video::Video;
use super::{read_choices, read_line_with_prompt, urlify};

use itertools::Itertools;
use strsim::levenshtein;

type Result<T> = ::std::result::Result<T, Box<::std::error::Error>>;

/// An enum to control the command given by command line.
#[derive(PartialEq)]
pub enum Command {
    Play(bool),
    Add,
    Delete,
    Modify,
    View,
    Usage,
    Artists,
    Popular,
}

/// Run a levenshtein distance check between a newly entered artist name and
/// all artists in the video list.  If a similar (but _not_ exact) artist
/// is found, prompt the user to choose one of the existing artists, or keep
/// their newly entered value.
pub fn check_for_similar_artist(artist: &str, videos: &[Video]) -> Result<String> {
    let artist_and_distance: HashSet<(String, usize)> = videos
        .iter()
        .map(|v| (v.artist.clone(), levenshtein(artist, &v.artist)))
        .filter(|(_v, d)| *d < 3)
        .collect();
    let similar_artists: HashSet<String> = artist_and_distance
        .iter()
        .map(|(v, _d)| v.to_owned())
        .collect();
    let exact_artists: HashSet<String> = artist_and_distance
        .iter()
        .filter(|(_v, d)| *d == 0)
        .map(|(v, _d)| v.to_owned())
        .collect();
    if !exact_artists.is_empty() {
        Ok(artist.to_string())
    } else if similar_artists.is_empty() {
        Ok(artist.to_string())
    } else {
        println!("Found similar artists:");
        let artists: Vec<String> = similar_artists.iter().map(|x| x.to_owned()).collect();
        for (i, artist) in artists.iter().enumerate() {
            println!("{}) {}", i, artist);
        }
        print!("Choose index, or -1 to keep '{}': ", artist);
        let mut response = String::new();
        std::io::stdout().flush()?;
        std::io::stdin().read_line(&mut response)?;
        let idx: i64 = response.trim().parse()?;
        if idx < 0 || idx > (artists.len() as i64) {
            Ok(artist.to_string())
        } else {
            Ok(artists[idx as usize].clone())
        }
    }
}

/// Display the current value of a variable, and prompt for a new value (with a message).
/// If the user does not enter a new value, return the current value.
fn current_or_new(current: &String, pre_prompt: &String) -> Result<String> {
    let new = read_line_with_prompt(format!("{} ({}): ", pre_prompt, current))?;
    match new == "\n" {
        true => Ok(current.clone()),
        false => Ok(new),
    }
}

/// Prompt the user for their choice of video(s) to play, or a random video
/// if the random flag is given.
///
/// The video list will be filtered (using `mask`) based on the query passed
/// as a command line argument.
///
/// The same list of videos are returned, with the view count increased, for
/// updating the video file.
pub fn play(v: &[Video], mask: &[usize], random: bool) -> Result<Vec<Video>> {
    let mut source = random::default();
    let choices = if mask.len() == 1 {
        println!("\nOnly 1 match");
        mask.to_vec()
    } else {
        match random {
            true => {
                let rand = source.read::<usize>() % mask.len();
                vec![mask[rand]]
            }
            false => read_choices()?,
        }
    };
    let mut v_new: Vec<Video> = v.to_vec();
    for idx in choices {
        println!("{}", v[idx]);
        webbrowser::open(&v[idx].url)?;
        v_new[idx].views += 1;
    }
    Ok(v_new)
}

/// Prompt the user for information of a video to add, with a 'similarity'
/// check done on the artist (with prompt to use similar, or keep entered).
/// Video list with new video appended is returned, to allow writing
/// updates to file.
pub fn add(v: &[Video]) -> Result<Vec<Video>> {
    let mut v_new = v.to_vec();
    let artist = check_for_similar_artist(&read_line_with_prompt("Artist")?, v)?;
    let title = read_line_with_prompt("Title")?;
    let url = urlify(read_line_with_prompt("URL")?)?;
    let views = 0;
    v_new.push(Video {
        title,
        artist,
        url,
        views,
    });
    Ok(v_new)
}

/// Prompt the user for which video(s) to modify, and then run a series
/// of prompts to either keep the current value or enter a new value
/// for each field.
pub fn modify(v: &[Video]) -> Result<Vec<Video>> {
    let mut v_new: Vec<Video> = v.to_vec();
    let choices = read_choices()?;
    println!("Update info, or ENTER to keep current");
    for idx in choices {
        let current = v[idx].clone();
        v_new[idx].artist = current_or_new(&current.artist, &"Artist".to_string())?;
        v_new[idx].title = current_or_new(&current.title, &"Title".to_string())?;
        v_new[idx].url = urlify(current_or_new(&current.url, &"URL".to_string())?)?;
        let viewstr = format!("{}", current.views);
        v_new[idx].views = current_or_new(&viewstr, &"VIEWS".to_string())?.parse()?;
    }
    Ok(v_new.to_vec())
}

/// Prompt the user for which video(s) to delete, returning the vector
/// with those videos removed, to allow updating the file.
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

/// Print all artists, grouped under their leading character.
pub fn artists(v: &[Video]) -> Vec<Video> {
    let artists: HashSet<String> = v.iter().map(|x| x.artist.to_string()).collect();
    let mut artists_s: Vec<String> = artists.iter().map(|x| x.to_string()).collect();
    artists_s.sort();
    for (key, mut group) in &artists_s.iter().group_by(|x| x.chars().nth(0).unwrap()) {
        let artist_string = group.join("   ");
        println!("{})\t{}", key, artist_string);
    }
    v.to_vec()
}

/// Show the top 10 videos by view count.
pub fn popular(v: &[Video]) -> Vec<Video> {
    let mut v_new = v.to_vec();
    v_new.sort_by(|a, b| b.views.cmp(&a.views));
    for artist in v_new.iter().take(10) {
        println!("{}", artist);
    }
    v.to_vec()
}
