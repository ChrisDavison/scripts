use csv::Reader;
use std::env;
use std::fs::File;

use serde::Deserialize;

#[derive(Debug)]
struct Config {
    salary: f64,
    bank: f64,
    costs: Vec<Cost>,
}

#[derive(Debug, Deserialize)]
struct Cost {
    name: String,
    value: f64,
    category: String,
    one_off: bool,
}

fn read_config(filepath: &str, costs: Vec<Cost>) -> Config {
    let config = std::fs::read_to_string(&filepath).expect("Couldn't read config");
    let mut salary = 0.0;
    let mut bank = 0.0;

    for line in config.lines() {
        let parts: Vec<&str> = line.split(",").collect();
        let name = parts[0];
        let value: f64 = parts[1].parse().unwrap();
        match name {
            "monthly" => salary = value,
            "bank" => bank = value,
            _ => continue,
        }
    }

    Config {
        salary,
        bank,
        costs,
    }
}

fn read_costs(filepath: &str) -> Vec<Cost> {
    let costfile = File::open(filepath).expect(&format!("Couldn't open {}", filepath));
    let mut costfile_rdr = Reader::from_reader(&costfile);
    let mut costs = Vec::new();
    for result in costfile_rdr.deserialize() {
        let cost: Cost = result.expect("Couldn't get csv record");
        costs.push(cost);
    }
    costs
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();

    if args.len() < 2 {
        eprintln!("usage: budget CONFIG COSTS [-v]");
        return;
    }

    let costs = read_costs(&args[1]);
    let config = read_config(&args[0], costs);
    let verbose = args.len() > 2 && &args[2] == "-v";

    let monthly_costs: Vec<&Cost> = config
        .costs
        .iter()
        .filter(|x| x.category == "monthly")
        .collect();
    let monthly_sum: f64 = monthly_costs.iter().map(|x| x.value).sum();
    let delta = config.salary - monthly_sum;
    println!("£{} savings", config.bank);

    println!(
        "MONTHLY\n\tIN: £{}\n\tOUT: £{}\n\tDELTA: £{}",
        config.salary, monthly_sum, delta,
    );

    let cost_of_oneoffs: f64 = config
        .costs
        .iter()
        .filter(|x| x.one_off)
        .map(|x| x.value)
        .sum();
    println!("One-off payments: £{}", cost_of_oneoffs);
    println!(
        "Savings after payments: £{}",
        config.bank - cost_of_oneoffs
    );
    println!(
        "Expected savings (1yr): £{}",
        (config.bank - cost_of_oneoffs) + (12.0 * delta)
    );

    if verbose {
        println!("\nMonthly payments");
        for cost in config.costs {
            if cost.category == "monthly" {
                println!("{:10} {}", cost.value, cost.name);
            }
        }
    }
}
