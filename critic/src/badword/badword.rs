use std::fmt;

pub enum BadWordType{
    WeaselWord,
    PassiveWord
}

pub struct BadWord {
    pub source: String,
    pub desc: BadWordType
}

impl fmt::Display for BadWordType{
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let str = match *self{
            BadWordType::WeaselWord => "Weasel Word",
            BadWordType::PassiveWord => "Passive Word"
        };
        write!(f, "{}", str)
    }
}

