use structopt::StructOpt;

#[derive(StructOpt)]
struct Cli {
    /// Lower % heartrate zone
    lower: u8,
    /// Upper % heartrate zone
    upper: u8,
    /// Age, for calculating max HR
    #[structopt(default_value="30")]
    age: u8,
    /// Resting heartrate, for calculating 'working' heartrate
    #[structopt(default_value="64")]
    rhr: u8,
}

fn main() {
    let args = Cli::from_args();
    let whr = (220 - args.age - args.rhr) as f64;
    let bpm_low = whr * args.lower as f64 / 100.0 + args.rhr as f64;
    let bpm_high = whr * args.upper as f64 / 100.0 + args.rhr as f64;
    
    println!("Working Heartrate: {}bpm", whr);
    println!("    {} to {}%", args.lower, args.upper);
    println!("    {} to {}bpm", bpm_low as u8, bpm_high as u8);
}
