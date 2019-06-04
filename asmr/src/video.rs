use std::env;
use std::fmt;
use std::path::Path;

use serde::{Deserialize, Serialize};
use serde_json;

use super::*;

type Result<T> = ::std::result::Result<T, Box<::std::error::Error>>;

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Video {
    pub title: String,
    pub artist: String,
    pub url: String,
    pub views: usize,
}

impl fmt::Display for Video {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} by {} (#{})", self.title, self.artist, self.views)
    }
}

/// Read videos from $DATADIR/asmr.json, parsing json into a `Video` struct.
pub fn read_videos_from_file() -> Result<Vec<Video>> {
    let fname = env::var("DATADIR")?;
    let fpath = Path::new(&fname).join("asmr.json");
    let data = fs::read_to_string(fpath)?;
    let v: Vec<Video> = serde_json::from_str(&data)?;
    Ok(v)
}

/// Write all videos, pretty-printed, to $DATADIR/asmr.json,
pub fn write_videos_to_file(v: &[Video]) -> Result<()> {
    let fname = env::var("DATADIR")?;
    let fpath = Path::new(&fname).join("asmr.json");
    let json = serde_json::to_string_pretty(v)?;
    fs::write(fpath, json)?;
    Ok(())
}
