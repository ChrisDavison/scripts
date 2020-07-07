use rand::random;
use regex::Regex;
use reqwest::blocking::get;
use shellexpand::tilde;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

fn get_request_url() -> Result<String> {
    let token_path = tilde("~/.pinboard").to_string();
    let pinboard_token =
        std::fs::read_to_string(token_path).map_err(|e| format!("Pinboard token: {}", e))?;

    Ok(format!(
        "https://api.pinboard.in/v1/posts/all?tag=asmr&auth_token={}",
        pinboard_token.trim()
    ))
}

fn get_videos_from_response(response: &str) -> Result<Vec<String>> {
    let re = Regex::new(r#"href="(.+?)"\s"#).map_err(|_| "Failed to parse regex")?;
    let caps: Vec<String> = re
        .captures_iter(response)
        .map(|x| x[1].to_string())
        .collect();
    Ok(caps)
}

fn choose_random_video(videos: &[String]) -> String {
    videos[random::<usize>() % videos.len()].clone()
}

fn main() {
    let video = get_request_url()
        .and_then(|url| get(&url).map_err(|_| "Couldn't GET".into()))
        .and_then(|response| response.text().map_err(|_| "Couldn't read response".into()))
        .and_then(|body| get_videos_from_response(&body).into())
        .map(|videos| choose_random_video(&videos));
    match video {
        Ok(video) => println!("{}", video),
        Err(e) => println!("{}", e),
    };
}
