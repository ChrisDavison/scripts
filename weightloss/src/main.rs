use structopt::StructOpt;

#[macro_use]
extern crate simple_error;

type Result<T> = ::std::result::Result<T, Box<dyn::std::error::Error>>;

const START: f64 = 117.0;

#[derive(StructOpt, Debug)]
struct Opts {
    /// Current weight
    value: f64,
    /// Unit of current weight (st|lb|kg)
    unit: String,
}

struct Weight {
    kg: f64
}

impl std::fmt::Display for Weight {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let lb = self.kg * 2.2;
        let st = lb / 14.0;
        write!(
            f,
            "{:.1}kg {:.1}st {:.1}lb (lost {:.1}kg)",
            self.kg,
            st,
            lb,
            START - self.kg,
        )
    }
}

impl Weight {
    fn new(unit: &str, value: f64) -> Result<Weight> {
        let value_kg = match unit {
            "kg" => value,
            "st" => value * 14.0 / 2.2,
            "lb" => value / 2.2,
            _ => bail!(format!("unrecognised unit `{}`", unit)),
        };
        Ok(Weight{kg: value_kg})
    }
}

fn main() -> Result<()> {
    let args = Opts::from_args();
    let w = Weight::new(&args.unit, args.value)?;
    println!("{}", w);
    Ok(())
}
