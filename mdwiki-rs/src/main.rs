use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;

use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use handlebars::Handlebars;

fn dir_contents_as_markdown_links(path: &PathBuf) -> String {
    let mut files = String::new();
    let mut dirs = String::new();
    for entry in fs::read_dir(path).unwrap() {
        let entry = entry.unwrap();
        let path = entry.path();
        let link_str = format!(
            "\n- [{}](./view/{})",
            path.file_name().unwrap().to_string_lossy(),
            path.to_string_lossy()
        );
        if path.is_dir() {
            dirs.push_str(link_str.as_ref())
        } else {
            if path.extension().unwrap().to_string_lossy() == "md" {
                files.push_str(link_str.as_ref())
            }
        }
    }

    format!(
        "## directories\n\n{}\n\n---\n\n## files\n\n{}\n",
        dirs, files
    )
}

async fn index(_hb: web::Data<Handlebars<'_>>) -> impl Responder {
    let contents = dir_contents_as_markdown_links(&PathBuf::from("."));
    let html = markdown::to_html(&contents);
    HttpResponse::Ok().body(html)
}

async fn edit(_hb: web::Data<Handlebars<'_>>, title: web::Path<String>) -> impl Responder {
    HttpResponse::Ok().body(format!("Editing not implemented. Title: {}", title))
}

async fn view(hb: web::Data<Handlebars<'_>>, title: web::Path<String>) -> impl Responder {
    let p = PathBuf::from(title.to_string());
    if p.exists() {
        let mut context = HashMap::new();
        if p.is_dir() {
            let contents = dir_contents_as_markdown_links(&p);
            let html = markdown::to_html(&contents);
            context.insert("contents", html);
        } else {
            let contents = std::fs::read_to_string(p).unwrap();
            let html = markdown::to_html(&contents);
            context.insert("contents", html);
        }
        HttpResponse::Ok().body(hb.render("view", &context).unwrap())
    } else {
        HttpResponse::Ok().body(format!("File not found: {}", title))
    }
}

#[actix_rt::main]
async fn main() -> std::io::Result<()> {
    let view_source = include_str!("../templates/view.html");
    let mut handlebars = Handlebars::new();
    handlebars
        .register_template_string("view", view_source)
        .unwrap();
    let handlebars_ref = web::Data::new(handlebars);
    HttpServer::new(move || {
        App::new()
            .app_data(handlebars_ref.clone())
            .route("/", web::get().to(index))
            .route("/view/{title}", web::get().to(view))
            .route("/edit/{title}", web::get().to(edit))
    })
    .bind("127.0.0.1:8088")?
    .run()
    .await
}
