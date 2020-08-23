#![feature(proc_macro_hygiene, decl_macro)]
use std::path::PathBuf;
use std::collections::HashMap;

use markdown;
use rocket::request::{Form, FromForm};
use rocket::response::{Flash, Redirect};
use rocket::{get, post, routes};
use rocket_contrib::templates::Template;


#[derive(FromForm)]
pub struct Post {
    contents: String,
    title: String,
}

#[post("/save", data = "<post>")]
fn save(post: Form<Post>) -> Flash<Redirect> {
    if post.contents.is_empty() {
        Flash::error(Redirect::to("/"), "Cannot be empty.")
    } else {
        Flash::success(
            Redirect::to(format!("/view/{}.md", post.title)),
            "Task added.",
        )
    }
}

#[get("/view/<title>")]
fn view(title: String) -> Template {
    let p = PathBuf::from(&title);
    if p.exists() {
        let contents = std::fs::read_to_string(p).unwrap();
        let html = markdown::to_html(&contents);
        let mut context = HashMap::new();
        context.insert("contents", html);
        Template::render("view", &context)
    } else {
        edit(title)
    }
}

#[get("/edit/<title>")]
fn edit(title: String) -> Template {
    let contents = format!("UNIMPLEMENTED editing {}", title);
    let mut context = HashMap::new();
    context.insert("contents", contents);
    Template::render("view", &context)
}

fn main() {
    rocket::ignite()
        .mount("/", routes![save, edit, view,])
        .attach(Template::fairing())
        .launch();
}
