use std::collections::HashMap;
use std::path::PathBuf;

use actix_web::{web, HttpResponse};
use handlebars::Handlebars;
use serde::{Deserialize, Serialize};

use crate::contents::directory_as_markdown_links;

#[derive(Serialize, Deserialize, Debug)]
pub struct Note {
    pub title: String,
    pub contents: String,
}

pub async fn index(hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    let contents = directory_as_markdown_links(&PathBuf::from("."));
    let html = markdown::to_html(&contents);
    let mut context = HashMap::new();
    context.insert("title", "index");
    context.insert("contents", &html);
    HttpResponse::Ok().body(hb.render("view", &context).unwrap())
}

pub async fn new(hb: web::Data<Handlebars<'_>>) -> HttpResponse {
    let context: HashMap<String, String> = HashMap::new();
    HttpResponse::Ok().body(hb.render("edit", &context).unwrap())
}

pub async fn edit(hb: web::Data<Handlebars<'_>>, title: Option<web::Path<String>>) -> HttpResponse {
    match title {
        None => new(hb).await,
        Some(t) => {
            let p = PathBuf::from(t.to_string());
            let contents = std::fs::read_to_string(p).unwrap();
            let mut context = HashMap::new();
            context.insert("title", t.to_string());
            context.insert("contents", contents.to_string());
            HttpResponse::Ok().body(hb.render("edit", &context).unwrap())
        }
    }
}

pub async fn view(hb: web::Data<Handlebars<'_>>, title: web::Path<String>) -> HttpResponse {
    if title.to_string().is_empty() {
        return edit(hb, None).await;
    }
    let p = PathBuf::from(title.to_string());
    if !p.exists() {
        return edit(hb, Some(title)).await;
    }
    let contents = if p.is_dir() {
        directory_as_markdown_links(&p)
    } else {
        std::fs::read_to_string(p).unwrap()
    };
    let html = markdown::to_html(&contents);
    let mut context = HashMap::new();
    context.insert("title", title.to_string());
    context.insert("contents", html);
    HttpResponse::Ok().body(hb.render("view", &context).unwrap())
}

pub async fn save(hb: web::Data<Handlebars<'_>>, note: web::Form<Note>) -> HttpResponse {
    let filename = if note.title.ends_with(".md") {
        note.title.to_string()
    } else {
        format!("{}.md", &note.title)
    };
    std::fs::write(filename, &note.contents).expect("Couldn't write contents of file.");
    view(hb, web::Path::from(note.title.clone())).await
}
