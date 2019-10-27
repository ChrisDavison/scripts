use std::process::{Command,exit};

fn main() {
    let output = Command::new("acpi").output().expect("couldn't run acpi");
    let battery_string: String = String::from_utf8_lossy(&output.stdout).into();
    if battery_string.contains("Full") {
        println!("B FULL");
        exit(1);
    }
    let arrow = match battery_string.contains("Charging") {
        true => "↑",
        false => "↓",
    };
    let remaining: &str = battery_string.split(", ").nth(2).expect("couldn't split acpi output");
    let time: String = remaining.split(" ").take(1).collect::<String>()[..5].into();
	println!("B{} {}", arrow, time);
}
