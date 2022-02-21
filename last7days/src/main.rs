use chrono::{Duration, Local, NaiveDate};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let last_week = Local::now().date() - Duration::days(7);

    if let Some(directory) = std::env::args().nth(1) {
        let directory = format!("{}/**/*.md", shellexpand::tilde(&directory));
        for f in glob::glob(&directory)? {
            if let Ok(fname) = f {
                let stem = fname
                    .file_stem()
                    .expect("Failed to read filename")
                    .to_string_lossy()
                    .to_string();
                if stem.len() < 10 {
                    continue;
                }
                let y = stem[..4].parse()?;
                let m = stem[5..7].parse()?;
                let d = stem[8..10].parse()?;
                let date = NaiveDate::from_ymd(y, m, d);
                if date >= last_week.naive_local() {
                    let contents = std::fs::read_to_string(fname)?;
                    println!("{}", contents);
                    println!("{}", "=".repeat(80));
                }
            }
        }
        Ok(())
    } else {
        eprintln!("usage: last7days <directory>");
        std::process::exit(1);
    }
}
