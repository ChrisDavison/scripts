use std::time::Duration;

const SECOND: std::time::Duration = Duration::new(1, 0);

pub struct Timer {
    duration: Duration,
    message: Option<String>,
}
pub type Countdown = Timer;

impl Timer {
    pub fn new(hours: u64, minutes: u64, seconds: u64, message: Option<String>) -> Timer {
        Timer {
            duration: Duration::new(hours * 360 + minutes * 60 + seconds, 0),
            message: message,
        }
    }

    pub fn tick(&mut self) {
        std::thread::sleep(SECOND);
        self.duration -= SECOND;
    }

    pub fn finished(&self) -> bool {
        self.duration.is_zero()
    }
}

impl std::fmt::Display for Timer {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        let mut total = self.duration.as_secs();
        let h = (total / 3600) as u64;
        total -= h * 3600;
        let m = (total / 60) as u64;
        total -= m * 60;
        let s = total;
        let msg = match &self.message {
            Some(m) => format!(" - {}", m),
            None => "".into(),
        };
        write!(f, "{:02}:{:02}:{:02}{}", h, m, s, msg)
    }
}
