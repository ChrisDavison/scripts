use std::env;
use structopt::StructOpt;

#[macro_use]
extern crate simple_error;

#[derive(StructOpt, Debug)]
#[structopt(name = "repoutil", version = "0.3.0")]
struct Opts {
    /// Command (one of fetch|stat)
    command: String,
}

type Result<T> = ::std::result::Result<T, Box<dyn::std::error::Error>>;

fn main() -> Result<()> {
    let args = Opts::from_args();
    let repos = get_repos()?;
    let cmd = match args.command.as_ref() {
        "fetch" => fetch,
        "stat" => stat,
        _ => bail!(format!("unrecognised command `{}`", args.command)),
    };

    for repo in repos {
        let out: String = cmd(repo.clone());
        if !out.is_empty() {
            println!("{}\n{}", repo.display(), out);
        }
    }
    Ok(())
}

fn fetch(p: std::path::PathBuf) -> String {
    let out = std::process::Command::new("git")
        .current_dir(p.clone())
        .args(&["fetch", "--all"])
        .output()
        .expect(format!("couldn't fetch {:?}", p).as_str());
    std::str::from_utf8(&out.stdout)
        .expect("couldn't convert stdout")
        .to_string()
}

fn stat(p: std::path::PathBuf) -> String {
    let out = std::process::Command::new("git")
        .current_dir(p.clone())
        .args(&["status", "-s", "-b"])
        .output()
        .expect(format!("couldn't stat {:?}", p).as_str());
    std::str::from_utf8(&out.stdout)
        .expect("couldn't convert stdout")
        .to_string()
}

fn is_git_repo(mut p: std::path::PathBuf) -> bool {
    p.push(".git");
    p.exists()
}

fn get_repos() -> Result<Vec<::std::path::PathBuf>> {
    let codedir = env::var("CODEDIR")?;
    let repos: Vec<_> = std::fs::read_dir(codedir)?
        .filter(|d| d.is_ok())
        .filter(|d| {
            let entry = d.as_ref().unwrap().path();
            entry.is_dir() && is_git_repo(entry)
        })
        .map(|d| d.unwrap().path())
        .collect();
    Ok(repos)
}
