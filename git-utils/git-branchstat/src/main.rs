use std::process::Command;

const VERSION: &'static str = "0.1.0";

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.len() > 0 && args[0] == "version" {
        println!("git-branchstat {}", VERSION);
        std::process::exit(0);
    }
    if !is_git_repo() {
        println!("Not a git repo.");
        std::process::exit(1);
    }
    let outputs = vec![ahead_behind(), modified(), status(), untracked()];
    let mut nonempty = Vec::new();
    for output in outputs {
        if let Some(o) = output {
            nonempty.push(o);
        }
    }
    println!("{}", nonempty.join(", "));
}

fn ahead_behind() -> Option<String> {
    let output = Command::new("git")
        .args(vec![
            "for-each-ref",
            "--format='%(refname:short) %(upstream:track)'",
            "refs/heads",
        ])
        .output()
        .expect("Couldn't get diff status");
    if !output.status.success() {
        panic!("AheadBehind error: {:?}", output.stderr);
    }
    let response = String::from_utf8_lossy(&output.stdout);
    let mut changed = Vec::new();
    for line in response.split("\n") {
        if line.contains("ahead") || line.contains("behind") {
            changed.push(line.trim_matches('\''));
        }
    }
    if changed.is_empty() {
        None
    } else {
        Some(changed.join(", "))
    }
}

fn modified() -> Option<String> {
    let output = Command::new("git")
        .args(vec!["diff", "--shortstat"])
        .output()
        .expect("Couldn't get diff short status");
    if !output.status.success() {
        panic!("Modified error: {:?}", output.stderr);
    }
    let response = String::from_utf8_lossy(&output.stdout).trim().to_string();
    if response.contains(" changed") {
        let num: String = response.trim_start().split(" ").take(1).collect();
        Some(format!("Modified {}", num))
    } else {
        None
    }
}

fn status() -> Option<String> {
    let output = Command::new("git")
        .args(vec!["diff", "--stat", "--cached"])
        .output()
        .expect("Couldn't get diff status");
    if !output.status.success() {
        panic!("Status error: {:?}", output.stderr);
    }
    if output.stdout.len() == 0 {
        None
    } else {
        Some(String::from_utf8(output.stdout).expect("Failed to get diff status output"))
    }
}

fn untracked() -> Option<String> {
    let output = Command::new("git")
        .args(vec!["ls-files", "--others", "--exclude-standard"])
        .output()
        .expect("Couldn't get diff status");
    if !output.status.success() {
        panic!("Untracked error: {:?}", output.stderr);
    }
    if output.stdout.len() == 0 {
        None
    } else {
        let n_items = String::from_utf8_lossy(&output.stdout)
            .trim()
            .split("\n")
            .collect::<Vec<&str>>()
            .len();
        Some(format!("Untracked {}", n_items))
    }
}

fn is_git_repo() -> bool {
    let status = Command::new("git")
        .arg("branch")
        .status()
        .expect("Failed to check if valid git repo");
    match status.code() {
        Some(128) => false,
        _ => true,
    }
}
