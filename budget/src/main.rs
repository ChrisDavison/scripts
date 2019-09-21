use csv::Reader;
use std::env;
use std::fs::File;

type Result<T> = std::result::Result<T, Box<dyn::std::error::Error>>;

#[derive(Debug)]
struct Config {
    salary: f64,
    bank: f64,
    monthly: Vec<Cost>,
    one_off: Vec<Cost>,
}

use cost::Cost;

fn display_sorted_costs(costs: Vec<Cost>) {
    let mut costs = costs;
    costs.sort();
    costs.reverse();
    for cost in costs {
        println!("{:10} {}", cost.value, cost.name)
    }
}

fn parse_config(fn_config: &str, fn_costs: &str) -> Result<Config> {
    let config = std::fs::read_to_string(&fn_config)?;
    let mut salary = 0.0;
    let mut bank = 0.0;

    for line in config.lines() {
        let parts: Vec<&str> = line.split(",").collect();
        let name = parts[0];
        let value: f64 = parts[1].parse()?;
        match name {
            "wage" => salary = value,
            "bank" => bank = value,
            _ => continue,
        }
    }

    let costfile = File::open(fn_costs).expect(&format!("Couldn't open {}", fn_costs));
    let mut costfile_rdr = Reader::from_reader(&costfile);
    let mut costs = Vec::new();
    for result in costfile_rdr.deserialize() {
        let cost: Cost = result?;
        costs.push(cost);
    }

    let one_off: Vec<Cost> = costs.iter().filter(|x| x.one_off).cloned().collect();
    let monthly: Vec<Cost> = costs
        .iter()
        .filter(|x| !x.one_off && x.category == "monthly")
        .cloned()
        .collect();

    Ok(Config {
        salary,
        bank,
        monthly,
        one_off,
    })
}

fn show_budget(fn_config: &str, fn_costs: &str, verbose: bool) -> Result<()> {
    let config = parse_config(fn_config, fn_costs)?;

    println!("{:10} £{}", "Savings", config.bank);
    println!("{:10} £{}", "Wage", config.salary);

    let one_off_sum: f64 = config.one_off.iter().map(|x| x.value).sum();
    println!("{:10} £{}", "One-offs", one_off_sum);
    if verbose {
        display_sorted_costs(config.one_off);
    }

    let monthly_sum: f64 = config.monthly.iter().map(|x| x.value).sum();
    println!("{:10} £{}", "Monthly", monthly_sum);
    if verbose {
        display_sorted_costs(config.monthly);
    }

    let delta = config.salary - monthly_sum;
    let bank_after_spend: i64 = (config.bank - one_off_sum) as i64;
    println!("\nSavings after one-offs: £{}", bank_after_spend);
    println!(
        "Expected savings (1yr): £{}",
        bank_after_spend + (12.0 * delta) as i64
    );
    Ok(())
}

fn main() {
    let (fn_config, fn_costs) = match (env::var("BUDGET_CONFIG"), env::var("BUDGET_COSTS")) {
        (Ok(a), Ok(b)) => (a, b),
        (_, _) => {
            let args: Vec<String> = env::args().skip(1).collect();

            if args.len() < 2 {
                eprintln!("usage: budget CONFIG COSTS [-v]");
                return;
            }
            (String::from(&args[0]), String::from(&args[1]))
        }
    };
    let verbose = env::args()
        .filter(|x| x == "-v")
        .collect::<Vec<String>>()
        .len()
        > 0;
    match show_budget(&fn_config, &fn_costs, verbose) {
        Ok(_) => {}
        Err(e) => eprintln!("{}", e),
    };
}

mod cost {
    use serde::Deserialize;
    use std::cmp::Ordering;

    const EPSILON: f64 = 0.0001;

    #[derive(Debug, Deserialize, Clone)]
    pub struct Cost {
        pub value: f64,
        pub name: String,
        pub category: String,
        pub one_off: bool,
    }

    impl PartialOrd for Cost {
        fn partial_cmp(&self, other: &Cost) -> Option<Ordering> {
            Some(self.cmp(other))
        }
    }

    impl Ord for Cost {
        fn cmp(&self, other: &Cost) -> Ordering {
            let diff = self.value - other.value;
            if diff > EPSILON {
                Ordering::Greater
            } else if diff < -EPSILON {
                Ordering::Less
            } else {
                Ordering::Greater
            }
        }
    }

    impl PartialEq for Cost {
        fn eq(&self, other: &Cost) -> bool {
            (self.value - other.value).abs() < 0.0001
        }
    }

    impl Eq for Cost {}

}
