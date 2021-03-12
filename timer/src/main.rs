#![feature(duration_zero)]
use clap::Clap;
use std::io::{self, Write};
use std::time::Duration;

#[derive(Clap, Debug)]
struct Opts {
    message: Vec<String>,
    #[clap(short = 'h', long, default_value = "0")]
    hours: i64,
    #[clap(short = 'm', long, default_value = "50")]
    minutes: i64,
    #[clap(short = 's', long, default_value = "0")]
    seconds: i64,
}

fn duration_as_hms(d: std::time::Duration) -> String {
    let mut total = d.as_secs();
    let hours = (total / 3600) as u64;
    total -= hours * 3600;
    let minutes = (total / 60) as u64;
    total -= minutes * 60;
    format!("{:02}:{:02}:{:02}", hours, minutes, total)
}

fn main() -> Result<(), std::io::Error> {
    let args = Opts::parse();
    let hours_as_seconds = args.hours * 60 * 60;
    let minutes_as_seconds = args.minutes * 60;
    let seconds = args.seconds;
    let total_seconds = hours_as_seconds + minutes_as_seconds + seconds;
    let mut d = Duration::new(total_seconds as u64, 0);
    let second = Duration::new(1, 0);
    let reset = format!("\r{}\r", " ".repeat(80));
    let mut stdout = io::stdout();
    if !args.message.is_empty() {
        println!("{}", args.message.join(" "));
    }
    while !d.is_zero() {
        print!("{}{}", reset, duration_as_hms(d));
        stdout.flush()?;
        d -= second;
        std::thread::sleep(second);
    }
    println!("DONE.");
    println!();
    Ok(())
}
