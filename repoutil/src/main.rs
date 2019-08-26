use std::thread;

#[macro_use]
extern crate simple_error;

type Result<T> = ::std::result::Result<T, Box<dyn::std::error::Error>>;

fn main() -> Result<()> {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.is_empty() {
        bail!("repoutil (stat|fetch)");
    }
    let repos = git::get_repos()?;
    let cmd = match args[0].as_ref() {
        "fetch" => git::fetch,
        "stat" => git::stat,
        _ => bail!(format!("unrecognised command `{}`", args[0])),
    };

    let mut handles = Vec::new();
    for repo in repos {
        // Spawn a thread for each repo
        // and run the chosen command.
        // The handle must 'move' to take ownership of `cmd`
        let handle = thread::spawn(move || {
            let out: String = cmd(repo.clone());
            if !out.is_empty() {
                println!("{}\n{}", repo.display(), out);
            }
        });
        handles.push(handle);
    }
    for h in handles {
        h.join().unwrap();
    }
    Ok(())
}

mod git {
    use super::Result;
    use std::env;

    pub fn is_git_repo(mut p: std::path::PathBuf) -> bool {
        p.push(".git");
        p.exists()
    }

    fn command_output(dir: std::path::PathBuf, args: &[&str], err_msg: Option<String>) -> String {
        let err_msg = match err_msg {
            Some(d) => d,
            None => format!("couldn't run command `git {:?}`", args),
        };
        let out = std::process::Command::new("git")
            .current_dir(dir)
            .args(args)
            .output()
            .expect(&err_msg);
        std::str::from_utf8(&out.stdout)
            .expect("couldn't convert stdout")
            .to_string()
    }

    pub fn fetch(p: std::path::PathBuf) -> String {
        let err_msg = Some(format!("couldn't fetch {:?}", p));
        command_output(p, &["fetch", "--all"], err_msg)
    }

    pub fn stat(p: std::path::PathBuf) -> String {
        let err_msg = Some(format!("couldn't stat {:?}", p));
        command_output(p, &["status", "-s", "-b"], err_msg)
    }

    pub fn get_repos() -> Result<Vec<::std::path::PathBuf>> {
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
}
