use shellexpand::tilde;
use rand::random;
use regex::Regex;
use reqwest::blocking::get;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

fn get_request_url() -> Result<String> {
    let token_path = tilde("~/.pinboard").to_string();
    let pinboard_token = std::fs::read_to_string(token_path)?.trim().to_string(); 

	let pinboard_api_url = "https://api.pinboard.in/v1/posts/all?tag=asmr";
    Ok(format!("{}&auth_token={}", pinboard_api_url, pinboard_token))
}

fn get_videos_from_response(response: &str) -> Result<Vec<String>> {
    let re = Regex::new(r#"href="(.+?)"\s"#).expect("Couldn't parse regex".into()); 
    let caps: Vec<String> = re.captures_iter(response).map(|x| x[1].to_string()).collect();
    Ok(caps)
}

fn choose_random_video(videos: &[String]) -> String {
    // let val = random::<usize>() % videos.len();
    videos[random::<usize>() % videos.len()].clone()
}

fn main() {
    let pinboard_url = get_request_url().expect("Failed to read pinboard token");
    let body = get(&pinboard_url).expect("API Request failed").text().expect("API request conversion to text failed");
    let videos = get_videos_from_response(&body).unwrap();
    println!("{}", choose_random_video(&videos));
}
