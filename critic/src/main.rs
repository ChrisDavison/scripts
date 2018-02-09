extern crate argparse;

use std::fs::File;
use std::io::Read;
use argparse::{ArgumentParser, Store};

use badword::badword::{BadWordType, BadWord};
mod badword;


fn main() {
    let mut filename = "".to_owned();
    {
        let mut parser = ArgumentParser::new();
        parser.set_description("Criticise writing.");
        parser.refer(&mut filename).add_option(&["-f", "--filename"],
                                               Store,
                                               "File to check");
        parser.parse_args_or_exit();
    }
    if filename == "" {
        println!("Need to pass filename.  Run with -h flag to see usage.");
        return
    }


    let file_contents = file_to_lines(&filename);
    let passive_words = file_to_lines("words/bw-passive.txt");
    let weasel_words  = file_to_lines("words/bw-weasel.txt");

    for line in file_contents{
        // Pretty nasty...
        // loops over 'passive words' and 'weasel words'
        // for every line in the file
        match words_check(&line, &passive_words, BadWordType::PassiveWord){
            Some(entry) => println!("Passive: {}", entry.desc, entry.source),
            None => print!{""}
        }
        match words_check(&line, &weasel_words, BadWordType::WeaselWord){
            Some(entry) => println!("Weasel: {}",  s.source),
            None => {}
        }
    }
}

fn words_check(line: &str,
               words: &Vec<String>,
               desc: BadWordType)
    -> Option<BadWord>
{
    let mut out: Option<BadWord> = None;
    for word in words{
        if line.contains(word) && !word.is_empty(){
            out = Some(BadWord{source: line.to_owned(), desc: desc});
            break
        }
    }
    out
}

fn file_to_lines<'a>(filename: &'a str) -> Vec<String> {
    let s = file_to_string(filename);
    let v = s.split('\n').map(|s| s.to_owned()).collect();
    v
}

fn file_to_string<'a>(filename: &'a str) -> String {
    let mut s = String::new();
    let mut f = match File::open(filename){
        Ok(f) => f,
        Err(_) => return "".to_owned()
    };
    f.read_to_string(&mut s).ok().expect("Couldn't read to string");
    s
}
