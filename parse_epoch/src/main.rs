use chrono::NaiveDateTime;

fn main() {
    let t = std::env::args().nth(1).unwrap_or(String::new());
    if t.is_empty() {
        eprintln!("usage: parse_epoch <seconds>");
        std::process::exit(1);
    }
    if let Ok(dt) = NaiveDateTime::parse_from_str(&t, "%s") {
        println!("{}", dt.format("%Y-%m-%d %H:%M:%S"));
    }
}
