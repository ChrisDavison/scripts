#![allow(dead_code, unused_variables)]

const L_IN_UK_GAL: f64 = 4.54609;
const KM_IN_MI: f64 = 1.60934;

#[derive(Debug, Clone, PartialEq)]
enum Fuel {
    Mpg(f64),
    KmPerL(f64),
    LPer100Km(f64),
}

#[derive(Debug, Clone, PartialEq)]
enum Range {
    Miles(f64),
    Kilometres(f64),
}

impl Range {
    fn miles(&self) -> Range {
        match self {
            Range::Miles(_) => self.clone(),
            Range::Kilometres(val) => Range::Miles(val / 1.6),
        }
    }
    fn kilometres(&self) -> Range {
        match self {
            Range::Miles(val) => Range::Kilometres(val * 1.6),
            Range::Kilometres(val) => self.clone(),
        }
    }
}

impl std::fmt::Display for Range {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Range::Miles(val) => write!(f, "{:.2} mi", val),
            Range::Kilometres(val) => write!(f, "{:.2} km", val),
        }
    }
}

impl Fuel {
    fn kmperl(&self) -> Fuel {
        match self {
            Fuel::Mpg(val) => Fuel::KmPerL(val / L_IN_UK_GAL * KM_IN_MI),
            Fuel::KmPerL(val) => self.clone(),
            Fuel::LPer100Km(val) => Fuel::KmPerL(100.0 / val),
        }
    }

    fn lper100km(&self) -> Fuel {
        match self {
            Fuel::Mpg(mpg) => Fuel::LPer100Km(1.0 / (mpg * KM_IN_MI / L_IN_UK_GAL / 100.0)),
            Fuel::KmPerL(val) => Fuel::LPer100Km(100.0 * val),
            Fuel::LPer100Km(val) => self.clone(),
        }
    }

    fn mpg(&self) -> Fuel {
        match self {
            Fuel::Mpg(val) => self.clone(),
            Fuel::KmPerL(val) => Fuel::Mpg(val * L_IN_UK_GAL / KM_IN_MI),
            Fuel::LPer100Km(val) => self.kmperl().mpg(),
        }
    }

    fn range(&self, tank_capacity_l: f64) -> Range {
        match self {
            Fuel::Mpg(val) => Range::Miles(val * tank_capacity_l / L_IN_UK_GAL),
            Fuel::KmPerL(val) => Range::Kilometres(val * tank_capacity_l),
            Fuel::LPer100Km(val) => self.kmperl().range(tank_capacity_l),
        }
    }
}

impl std::fmt::Display for Fuel {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Fuel::Mpg(val) => write!(f, "{:.2} mpg", val),
            Fuel::KmPerL(val) => write!(f, "{:.2} km/l", val),
            Fuel::LPer100Km(val) => write!(f, "{:.2} l/100km", val),
        }
    }
}

fn parse_args() -> Result<Fuel, Box<dyn std::error::Error>> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    if args.is_empty() {
        std::process::exit(1);
    }
    match args[1].to_lowercase().as_str() {
        "mpg" | "m/g" => Ok(Fuel::Mpg(args[0].parse()?)),
        "kmperl" | "km/l" => Ok(Fuel::Mpg(args[0].parse()?)),
        "l/100km" | "l_per_100km" => Ok(Fuel::Mpg(args[0].parse()?)),
        _ => std::process::exit(2),
    }
}

fn main() {
    if let Ok(fuel) = parse_args() {
        println!("Economy {} ({})", fuel.mpg(), fuel.kmperl());
        println!("Consumption {}", fuel.lper100km());
        let tank = 10.0;

        println!("\nFor {} l tank...", tank);
        println!("\t{}", fuel.range(tank));
        println!("\t{}", fuel.range(tank).kilometres());
    }
}
