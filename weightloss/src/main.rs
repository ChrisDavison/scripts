use structopt::StructOpt;

#[macro_use]
extern crate simple_error;

type Result<T> = ::std::result::Result<T, Box<dyn::std::error::Error>>;

const START: f64 = 115.0;

#[derive(StructOpt, Debug)]
struct Opts {
    /// Unit of current weight (st|lb|kg)
    unit: String,
    /// Current weight
    value: f64,
}

struct Weight {
    value_kg: f64,
    value_st: f64,
    value_lb: f64,
}

impl std::fmt::Display for Weight {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{:.2}kg {:.2}st {:.2}lb (lost {:.2}kg)",
            self.value_kg,
            self.value_st,
            self.value_lb,
            START - self.value_kg,
        )
    }
}

impl Weight {
    fn new(unit: &str, value: f64) -> Result<Weight> {
        let unit = unit.to_string();
        let value_kg = match unit.as_ref() {
            "kg" => value,
            "st" => value * 14.0 / 2.2,
            "lb" => value / 2.2,
            _ => bail!(format!("unrecognised unit `{}`", unit)),
        };
        Ok(Weight {
            value_kg: value_kg,
            value_lb: value_kg * 2.2,
            value_st: value_kg * 2.2 / 14.0,
        })
    }
}

fn main() -> Result<()> {
    let args = Opts::from_args();
    let w = Weight::new(&args.unit, args.value)?;
    println!("{}", w);
    Ok(())
}
