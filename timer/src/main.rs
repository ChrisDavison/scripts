#![feature(duration_zero, duration_consts_2)]
use clap::Clap;
use std::io::{self, Write};

mod timer;

#[derive(Clap, Debug)]
struct Opts {
    message: Vec<String>,
    #[clap(short = 'h', long, default_value = "0")]
    hours: u64,
    #[clap(short = 'm', long, default_value = "50")]
    minutes: u64,
    #[clap(short = 's', long, default_value = "0")]
    seconds: u64,
}

fn main() -> Result<(), std::io::Error> {
    let args = Opts::parse();
    let mut timer = timer::Countdown::new(
        args.hours,
        args.minutes,
        args.seconds,
        if args.message.is_empty() {
            None
        } else {
            Some(args.message.join(" "))
        },
    );
    let reset = format!("\r{}\r", " ".repeat(80));
    let mut stdout = io::stdout();
    while !timer.finished() {
        print!("{}{}", reset, timer);
        stdout.flush()?;
        timer.tick();
    }
    println!("{}DONE.", reset);
    Ok(())
}
