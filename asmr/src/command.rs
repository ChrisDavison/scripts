use random::Source;
use webbrowser;

use super::video::Video;
use super::{read_choices, read_line_with_prompt, urlify};

type Result<T> = ::std::result::Result<T, Box<::std::error::Error>>;

#[derive(PartialEq)]
pub enum Command {
    Play(bool),
    Add,
    Delete,
    Modify,
    View,
    Usage,
}

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
