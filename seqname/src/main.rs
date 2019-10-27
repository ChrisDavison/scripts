use std::path::PathBuf;
use structopt::StructOpt;

#[derive(Debug, StructOpt)]
#[structopt(name = "seqname", about = "rename files sequentially")]
struct Opt {
    /// Text to insert before number
    #[structopt(short, long)]
    prefix: Option<String>,

    /// Text to insert after number
    #[structopt(short, long)]
    suffix: Option<String>,

    /// Show files moved/renamed
    #[structopt(short, long)]
    verbose: bool,

    /// Directories with files to rename
    dirs: Vec<PathBuf>,
}

struct Renamer {
    prefix: String,
    suffix: String,
    verbose: bool,
}

impl Renamer {
    fn new(prefix: Option<String>, suffix: Option<String>, verbose: bool) -> Renamer {
        let prefix = match prefix {
            Some(p) => format!("{}--", p),
            None => "".into(),
        };
        let suffix = match suffix {
            Some(s) => format!("--{}", s),
            None => "".into(),
        };
        Renamer {
            prefix,
            suffix,
            verbose,
        }
    }

    fn rename(&self, dir: &PathBuf) -> Result<(), Box<dyn std::error::Error>> {
        let valid_paths = dir
            .read_dir()?
            .filter_map(|x| x.ok())
            .filter(|x| x.path().is_file());
        for (i, path) in valid_paths.enumerate() {
            let mut new = path.path().clone();
            let ext = match path.path().extension() {
                Some(e) => format!(".{}", e.to_string_lossy()),
                None => "".into()
            };
            new.set_file_name(format!("{}{:04}{}{}", self.prefix, i, self.suffix, ext));
            if self.verbose {
                println!("{:?} ->\n\t{:?}", path.path(), new);
            }
            std::fs::rename(path.path(), new)?;
        }
        Ok(())
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let opt = Opt::from_args();
    let renamer = Renamer::new(opt.prefix, opt.suffix, opt.verbose);
    for dir in opt.dirs {
        match renamer.rename(&dir) {
            Ok(_) => continue,
            Err(e) => eprintln!("Failed in dir {:?}: {}", dir.display(), e)
        };
    }
    Ok(())
}
