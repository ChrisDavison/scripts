#![allow(dead_code, unused_variables)]
use std::collections::HashMap;
use std::path::PathBuf;

use glob::glob;
use lazy_static::lazy_static;
use regex::Regex;
use structopt::StructOpt;

type Result<T> = std::result::Result<T, Box<dyn ::std::error::Error>>;

/// Backlinks works on links between markdown files.
/// A 'backlink' is a link from file B to file A.
/// A 'forward' link is a link from file A to file B.
/// An 'orphan' is a file that is not linked to from elsewhere.
#[derive(StructOpt, Debug)]
#[structopt(name = "backlinks")]
struct Opt {
    /// Files
    files: Vec<PathBuf>,

    /// List files without any backlinks
    #[structopt(short, long)]
    orphan: bool,

    /// Count links to each file
    #[structopt(short, long)]
    count: bool,

    /// Show links FROM each file
    #[structopt(short, long)]
    forward: bool,
}

fn main() -> Result<()> {
    let args = Opt::from_args();
    let files = if args.files.is_empty() {
        get_md_files_in_curdir()?
    } else {
        args.files
    };
    if args.orphan {
        print_orphaned_links(files.as_ref())?;
    } else if args.forward {
        print_forward_links(&files, args.count)?;
    } else {
        print_back_links(&files, args.count)?;
    }
    println!("---");
    Ok(())
}

/// Glob for markdown files under the current working directory
fn get_md_files_in_curdir() -> Result<Vec<PathBuf>> {
    Ok(glob("*.md")?
        .filter(|x| x.is_ok())
        .map(|x| x.expect("Already tested each glob is ok"))
        .collect())
}

/// Read all links to other files inside a given file
fn links_in_file(filename: &PathBuf) -> Result<Vec<String>> {
    lazy_static! {
        static ref RE: Regex = Regex::new(r#"\((?:\./)*([a-zA-Z0-9\-_]*?\.md)\)"#)
            .expect("Error compiling link regex");
    }
    let mut links: Vec<String> = Vec::new();
    let contents = std::fs::read_to_string(filename)?;
    for cap in RE.captures_iter(&contents) {
        links.push(cap[1].into())
    }
    Ok(links)
}

/// Get list of files which point to each file
fn get_backlinks() -> Result<HashMap<String, Vec<String>>> {
    let mut backlinks: HashMap<String, Vec<String>> = HashMap::new();
    for fname in get_md_files_in_curdir()? {
        let fn_str = fname.to_string_lossy().to_string();
        let links = links_in_file(&fname)?;
        for link in links {
            let entry = backlinks.entry(link).or_insert(Vec::new());
            (*entry).push(fn_str.clone());
        }
    }
    Ok(backlinks)
}

/// Print all files that are never linked to
fn print_orphaned_links(files: &[PathBuf]) -> Result<()> {
    let backlinks = get_backlinks()?;
    for filename in files {
        let fn_str = filename.to_string_lossy().to_string();
        if !backlinks.contains_key(&fn_str) {
            println!("{}", fn_str);
        }
    }
    Ok(())
}

/// Display what other files each file links to 
fn print_forward_links(files: &[PathBuf], count: bool) -> Result<()> {
    let backlinks = get_backlinks()?;
    for file in files {
        let fn_str = file.to_string_lossy().to_string();
        let links = links_in_file(&file)?;
        if links.is_empty() {
            continue;
        }
        if count {
            println!("{} {}", links.len(), fn_str);
        } else {
            println!("{}", fn_str);
            for link in links {
                println!(" > {}", link);
            }
        }
    }
    Ok(())
}

/// Display what other files link to each given filename
fn print_back_links(files: &[PathBuf], count: bool) -> Result<()> {
    let backlinks = get_backlinks()?;
    for file in files {
        let fn_str = file.to_string_lossy().to_string();
        let links = backlinks.get(&fn_str);
        if let Some(links) = backlinks.get(&fn_str) {
            if count {
                println!("{} {}", links.len(), fn_str);
            } else {
                println!("{}", fn_str);
                for link in links {
                    println!(" ^ {}", link);
                }
            }
        }
    }
    Ok(())
}
