use structopt::StructOpt;

#[derive(StructOpt)]
struct Cli {
    /// Lower % heartrate zone
    lower: u8,
    /// Upper % heartrate zone
    upper: u8,
    /// Age, for calculating max HR
    #[structopt(default_value = "30")]
    age: u8,
    /// Resting heartrate, for calculating 'working' heartrate
    #[structopt(default_value = "64")]
    rhr: u8,
}

fn heartrate_bpm_for_percent(age: u8, rhr: u8, pct: u8) -> f64 {
    let whr = (220 - age - rhr) as f64;
    whr * pct as f64 / 100.0 + rhr as f64
}

fn main() {
    let args = Cli::from_args();
    let bpm_lo = heartrate_bpm_for_percent(args.age, args.rhr, args.lower);
    let bpm_hi = heartrate_bpm_for_percent(args.age, args.rhr, args.upper);

    println!(
        "{} to {}% => {} to {}bpm",
        args.lower, args.upper, bpm_lo as u8, bpm_hi as u8
    );
}
