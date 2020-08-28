use actix_web::{web, App, HttpServer};
use handlebars::Handlebars;

mod contents;
mod routes;

#[actix_rt::main]
async fn main() -> std::io::Result<()> {
    let view_source = include_str!("../templates/view.html");
    let edit_source = include_str!("../templates/edit.html");
    let mut hb = Handlebars::new();
    hb.register_template_string("view", view_source).unwrap();
    hb.register_template_string("edit", edit_source).unwrap();

    let handlebars_ref = web::Data::new(hb);
    HttpServer::new(move || {
        App::new()
            .app_data(handlebars_ref.clone())
            .route("/", web::get().to(routes::index))
            .route("/view/{title}", web::get().to(routes::view))
            .route("/new", web::get().to(routes::new))
            .route("/edit/{title}", web::get().to(routes::edit))
            .route("/save", web::post().to(routes::save))
    })
    .bind("127.0.0.1:8089")?
    .run()
    .await
}
